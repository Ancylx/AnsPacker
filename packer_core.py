# packer_core.py
import subprocess
import sys
import os
import platform
import threading
from pathlib import Path
import importlib.util
import importlib
import traceback

class PackerCore:
    """打包核心逻辑"""
    
    def __init__(self):
        self.process = None
        self.is_running = False
        self.thread = None
    
    def ensure_pyinstaller(self, log_callback):
        """
        确保PyInstaller已安装，如果没有则自动安装
        所有消息都会输出到GUI日志中
        """
        def check_pyinstaller_installed():
            """检查PyInstaller是否已安装"""
            try:
                # 方法1：检查模块是否可以导入
                spec = importlib.util.find_spec("PyInstaller")
                if spec is not None:
                    return True
                
                # 方法2：尝试执行pyinstaller命令
                result = subprocess.run(
                    [sys.executable, "-m", "PyInstaller", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                return result.returncode == 0
            except:
                return False
        
        # 检查是否已安装
        log_callback.log("正在检查PyInstaller安装状态...", "info")
        
        if check_pyinstaller_installed():
            log_callback.log("✓ PyInstaller已安装", "success")
            return True
        
        # 未安装，开始自动安装
        log_callback.log("✗ PyInstaller未安装", "warning")
        log_callback.log("正在尝试自动安装PyInstaller...", "info")
        log_callback.log("注意：这需要网络连接和pip配置正确", "info")
        
        try:
            # 尝试使用pip安装PyInstaller
            install_cmd = [sys.executable, "-m", "pip", "install", "pyinstaller"]
            
            log_callback.log(f"执行命令: {' '.join(install_cmd)}", "info")
            
            # 运行pip安装命令
            install_process = subprocess.Popen(
                install_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                encoding='utf-8',
                errors='backslashreplace'
            )
            
            # 实时显示安装日志
            log_callback.log("="*50, "info")
            log_callback.log("开始安装PyInstaller...", "info")
            log_callback.log("="*50, "info")
            
            for line in install_process.stdout:
                if line.strip():
                    log_callback.log(f"[PIP] {line.strip()}", "info")
            
            # 等待安装完成
            return_code = install_process.wait()
            
            if return_code == 0:
                log_callback.log("="*50, "success")
                log_callback.log("✓ PyInstaller安装成功！", "success")
                log_callback.log("="*50, "success")
                
                # 验证安装
                if check_pyinstaller_installed():
                    log_callback.log("✓ 安装验证通过", "success")
                    return True
                else:
                    log_callback.log("✗ 安装验证失败，可能未正确安装", "error")
                    return False
            else:
                log_callback.log("="*50, "error")
                log_callback.log(f"✗ PyInstaller安装失败！返回码: {return_code}", "error")
                log_callback.log("="*50, "error")
                return False
                
        except FileNotFoundError as e:
            log_callback.log("="*50, "error")
            log_callback.log("✗ 执行失败：未找到Python或pip命令", "error")
            log_callback.log(f"详细信息: {str(e)}", "error")
            log_callback.log("请确保Python已正确安装并添加到系统PATH", "warning")
            log_callback.log("="*50, "error")
            return False
            
        except subprocess.TimeoutExpired as e:
            log_callback.log("="*50, "error")
            log_callback.log("✗ 执行超时：网络连接太慢或卡住", "error")
            log_callback.log(f"详细信息: {str(e)}", "error")
            log_callback.log("建议: 1. 检查网络连接 2. 使用国内镜像源", "warning")
            log_callback.log("="*50, "error")
            return False
            
        except subprocess.CalledProcessError as e:
            log_callback.log("="*50, "error")
            log_callback.log("✗ 安装过程出错", "error")
            log_callback.log(f"返回码: {e.returncode}", "error")
            if e.output:
                log_callback.log(f"错误输出: {e.output}", "error")
            log_callback.log("="*50, "error")
            return False
            
        except Exception as e:
            log_callback.log("="*50, "error")
            log_callback.log("✗ 安装PyInstaller时发生未知错误", "error")
            log_callback.log(f"错误类型: {type(e).__name__}", "error")
            log_callback.log(f"错误信息: {str(e)}", "error")
            log_callback.log("详细堆栈:", "error")
            
            # 输出详细堆栈信息到日志
            for line in traceback.format_exc().split('\n'):
                if line.strip():
                    log_callback.log(f"  {line}", "error")
            
            log_callback.log("="*50, "error")
            log_callback.log("常见原因:", "warning")
            log_callback.log("1. 网络连接问题", "warning")
            log_callback.log("2. pip配置错误", "warning")
            log_callback.log("3. 权限不足（请以管理员身份运行）", "warning")
            log_callback.log("4. 防火墙或代理阻止访问", "warning")
            log_callback.log("5. Python环境损坏", "warning")
            log_callback.log("="*50, "error")
            return False
    
    def build_command(self, config):
        """构建PyInstaller命令"""
        cmd = [sys.executable, "-m", "PyInstaller"]
        
        # 基本参数
        if config['onefile']:
            cmd.append("--onefile")
        
        if config['noconsole']:
            cmd.append("--noconsole")
        
        if config['debug']:
            cmd.append("--debug=all")
        
        if config['clean']:
            cmd.append("--clean")
        
        # 程序名称
        if config['name']:
            cmd.extend(["--name", config['name']])
        
        # 图标文件
        if config['icon_file']:
            cmd.extend(["--icon", config['icon_file']])
        
        # 资源文件
        for resource in config['resources']:
            resource_path = Path(resource)
            if platform.system() == "Windows":
                # Windows格式: src;dest
                cmd.extend(["--add-data", f"{resource_path};."])
            else:
                # Linux/macOS格式: src:dest
                cmd.extend(["--add-data", f"{resource_path}:."])
        
        # 额外参数
        if config['extra_params']:
            cmd.extend(config['extra_params'].split())
        
        # 输出目录
        if config['output_dir']:
            cmd.extend(["--distpath", str(Path(config['output_dir']) / "dist")])
            cmd.extend(["--workpath", str(Path(config['output_dir']) / "build")])
            cmd.extend(["--specpath", config['output_dir']])
        
        # 主程序文件
        cmd.append(config['main_file'])
        
        return cmd
    
    def pack(self, config, log_callback):
        """执行打包"""
        if self.is_running:
            log_callback.log("已有打包任务正在进行！", "warning")
            return
        
        # 确保PyInstaller已安装
        if not self.ensure_pyinstaller(log_callback):
            log_callback.log("无法继续打包，请先手动安装PyInstaller", "error")
            self.is_running = False
            return
        
        self.is_running = True
        
        # 在新线程中执行打包，避免阻塞GUI
        self.thread = threading.Thread(
            target=self._run_pack_process,
            args=(config, log_callback),
            daemon=True
        )
        self.thread.start()
    
    def _run_pack_process(self, config, log_callback):
        """运行打包进程"""
        try:
            cmd = self.build_command(config)
            log_callback.log("="*50, "info")
            log_callback.log("开始构建PyInstaller命令...", "info")
            cmd_display = ' '.join(cmd)
            log_callback.log(f"命令: {cmd_display}", "info")
            log_callback.log("="*50, "info")
            
            # 启动进程
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                encoding='utf-8',
                errors='backslashreplace'
            )
            
            # 实时读取输出
            for line in self.process.stdout:
                if line:
                    self._process_log_line(line.strip(), log_callback)
            
            # 等待进程结束
            return_code = self.process.wait()
            
            if return_code == 0:
                log_callback.log("="*50, "success")
                log_callback.log("打包成功完成！", "success")
                log_callback.log(f"输出目录: {config.get('output_dir', 'dist')}", "success")
                log_callback.log("="*50, "success")
            else:
                log_callback.log("="*50, "error")
                log_callback.log(f"打包失败！返回码: {return_code}", "error")
                log_callback.log("="*50, "error")
        
        except FileNotFoundError:
            log_callback.log("错误: 未找到PyInstaller或Python！请检查安装", "error")
        except Exception as e:
            log_callback.log(f"异常错误: {str(e)}", "error")
            log_callback.log(f"错误类型: {type(e).__name__}", "error")
        finally:
            self.is_running = False
            self.process = None
    
    def _process_log_line(self, line, log_callback):
        """处理日志行，根据内容设置级别"""
        lower_line = line.lower()
        
        if "error" in lower_line or "failed" in lower_line or "traceback" in lower_line:
            log_callback.log(line, "error")
        elif "warning" in lower_line or "warn" in lower_line:
            log_callback.log(line, "warning")
        elif "success" in lower_line or "complete" in lower_line or "finished" in lower_line:
            log_callback.log(line, "success")
        elif "info" in lower_line or "processing" in lower_line or "analyzing" in lower_line:
            log_callback.log(line, "info")
        else:
            log_callback.log(line)
    
    def stop(self):
        """停止打包进程"""
        if self.process and self.is_running:
            try:
                self.process.terminate()
                self.process.kill()
                self.is_running = False
                return True
            except Exception as e:
                print(f"停止进程失败: {e}")
                return False
        return False
    
    def is_process_running(self):
        """检查进程是否正在运行"""
        return self.is_running and self.process is not None