# gui.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import webbrowser

# 主题配置
THEME_COLOR = "#b6da3e"
THEME_DARK = "#8aa62f"
THEME_LIGHT = "#d4f069"
BG_COLOR = "#f5f5f5"
PLACEHOLDER_COLOR = "#cacaca"  # 提示文字颜色

# PyInstaller预设参数
PARAMETER_PRESETS = {
    "--version-file <FILE>": "添加版本信息文件",
    "--manifest <FILE or XML>": "添加manifest文件",
    "--uac-admin": "请求管理员权限",
    "--hidden-import <MODULE>": "手动指定隐式导入的模块",
    "--exclude-module <MODULE>": "排除指定模块",
    "--add-binary <SRC;DEST>": "添加二进制文件",
    "--splash <IMAGE>": "添加启动画面",
    "--debug all": "详细调试模式",
    "--strip": "去除符号信息（减小体积）",
    "--noupx": "禁用UPX压缩",
    "--runtime-tmpdir <PATH>": "指定运行时临时目录"
}

class PlaceholderEntry(ttk.Entry):
    """带占位符提示的输入框"""
    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(parent, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = PLACEHOLDER_COLOR
        self.default_fg = self.cget('foreground')
        
        self._is_showing_placeholder = False
        self._show_placeholder()
        
        # 绑定事件
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
    
    def _show_placeholder(self):
        """显示占位符"""
        if not self.get() and self.placeholder:
            self.configure(foreground=self.placeholder_color)
            self.insert(0, self.placeholder)
            self._is_showing_placeholder = True
    
    def _hide_placeholder(self):
        """隐藏占位符"""
        if self._is_showing_placeholder:
            self.configure(foreground=self.default_fg)
            self.delete(0, 'end')
            self._is_showing_placeholder = False
    
    def _on_focus_in(self, event):
        """获得焦点时隐藏占位符"""
        if self._is_showing_placeholder:
            self._hide_placeholder()
    
    def _on_focus_out(self, event):
        """失去焦点时显示占位符"""
        if not self.get():
            self._show_placeholder()
    
    def get_real_value(self):
        """获取真实值（不包括占位符）"""
        if self._is_showing_placeholder:
            return ""
        return self.get()

class LogTextArea(scrolledtext.ScrolledText):
    """日志显示区域"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.tag_configure("error", foreground="red")
        self.tag_configure("success", foreground="green")
        self.tag_configure("info", foreground="blue")
        self.tag_configure("warning", foreground="orange")
        self.config(state='disabled')
    
    def log(self, message, level="info"):
        """添加日志"""
        self.config(state='normal')
        self.insert('end', f"{message}\n", level)
        self.see('end')
        self.config(state='disabled')
        self.update()
    
    def clear(self):
        """清空日志"""
        self.config(state='normal')
        self.delete(1.0, 'end')
        self.config(state='disabled')

class AnsPackerGUI:
    """主窗口GUI"""
    
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_window()
        self.create_widgets()
        self.setup_layout()
        self.create_styles()
    
    def setup_window(self):
        """窗口初始化设置"""
        self.root.title("AnsPacker-v1.0.0")
        self.root.geometry("1200x800")
        self.root.minsize(985, 675)
        
        # 设置窗口图标
        try:
            self.root.iconbitmap("resources\icons\AnsPack.ico")
        except:
            pass
    
    def create_styles(self):
        """创建自定义样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 按钮样式
        style.configure(
            'Custom.TButton',
            background=THEME_COLOR,
            foreground='black',
            padding=8,
            font=('Microsoft YaHei', 10)
        )
        style.map('Custom.TButton',
            background=[('active', THEME_DARK), ('pressed', THEME_DARK)]
        )
        
        # 标签样式
        style.configure(
            'Custom.TLabel',
            background=BG_COLOR,
            font=('Microsoft YaHei', 10)
        )
        
        # 框架样式
        style.configure(
            'Custom.TFrame',
            background=BG_COLOR
        )
        
        # 复选框样式
        style.configure(
            'Custom.TCheckbutton',
            background=BG_COLOR,
            font=('Microsoft YaHei', 10)
        )
        
        # 下拉列表样式
        style.configure(
            'Custom.TCombobox',
            background=BG_COLOR,
            font=('Microsoft YaHei', 10)
        )
    
    def create_widgets(self):
        """创建所有控件"""
        # 主框架
        main_frame = ttk.Frame(self.root, style='Custom.TFrame')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)

        # 内容区域
        content_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        content_frame.pack(fill='both', expand=True)
        
        # 左侧配置区域
        left_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # 文件选择区域
        self.create_file_selection(left_frame)
        
        # 参数配置区域
        self.create_parameter_section(left_frame)
        
        # 右侧日志区域
        self.create_log_section(content_frame)
        
        # 控制按钮区域
        self.create_control_buttons(main_frame)
        
    def create_file_selection(self, parent):
        """文件选择区域"""
        file_frame = ttk.LabelFrame(
            parent,
            text="文件选择",
            padding=10,
            style='Custom.TFrame'
        )
        file_frame.pack(fill='x', pady=(0, 15))
        
        # 主文件选择
        ttk.Label(
            file_frame,
            text="主程序文件:",
            style='Custom.TLabel'
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        self.main_file_entry = PlaceholderEntry(
            file_frame,
            placeholder="请选择主程序文件 (*.py)",
            width=40
        )
        self.main_file_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
        
        ttk.Button(
            file_frame,
            text="浏览...",
            command=self.select_main_file,
            style='Custom.TButton'
        ).grid(row=0, column=2, pady=5)
        
        # 输出目录选择
        ttk.Label(
            file_frame,
            text="输出目录:",
            style='Custom.TLabel'
        ).grid(row=1, column=0, sticky='w', pady=5)
        
        self.output_entry = PlaceholderEntry(
            file_frame,
            placeholder="请选择输出目录",
            width=40
        )
        self.output_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=5)
        
        ttk.Button(
            file_frame,
            text="浏览...",
            command=self.select_output_dir,
            style='Custom.TButton'
        ).grid(row=1, column=2, pady=5)
        
        # 资源文件选择
        ttk.Label(
            file_frame,
            text="额外资源:",
            style='Custom.TLabel'
        ).grid(row=2, column=0, sticky='w', pady=5)
        
        self.resource_list = tk.Listbox(file_frame, height=3, width=38)
        self.resource_list.grid(row=2, column=1, sticky='ew', pady=5, padx=5)
        
        resource_btn_frame = ttk.Frame(file_frame, style='Custom.TFrame')
        resource_btn_frame.grid(row=2, column=2, sticky='ns')
        
        ttk.Button(
            resource_btn_frame,
            text="添加",
            command=self.add_resource,
            style='Custom.TButton',
            width=8
        ).pack(fill='x', pady=2)
        
        ttk.Button(
            resource_btn_frame,
            text="删除",
            command=self.remove_resource,
            style='Custom.TButton',
            width=8
        ).pack(fill='x', pady=2)
        
        # 图标文件选择
        ttk.Label(
            file_frame,
            text="图标文件(.ico):",
            style='Custom.TLabel'
        ).grid(row=3, column=0, sticky='w', pady=5)
        
        self.icon_entry = PlaceholderEntry(
            file_frame,
            placeholder="请选择图标文件 (可选)",
            width=40
        )
        self.icon_entry.grid(row=3, column=1, sticky='ew', pady=5, padx=5)
        
        ttk.Button(
            file_frame,
            text="浏览...",
            command=self.select_icon,
            style='Custom.TButton'
        ).grid(row=3, column=2, pady=5)
        
        # 配置列权重
        file_frame.columnconfigure(1, weight=1)
    
    def create_parameter_section(self, parent):
        """参数配置区域"""
        param_frame = ttk.LabelFrame(
            parent,
            text="PyInstaller参数配置",
            padding=10,
            style='Custom.TFrame'
        )
        param_frame.pack(fill='x', pady=(0, 15))
        
        # 复选框参数
        checkbox_frame = ttk.Frame(param_frame, style='Custom.TFrame')
        checkbox_frame.pack(fill='x', pady=5)
        
        self.onefile_var = tk.BooleanVar(value=True)
        self.noconsole_var = tk.BooleanVar(value=True)
        self.debug_var = tk.BooleanVar(value=False)
        self.clean_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(
            checkbox_frame,
            text="单文件模式 --onefile",
            variable=self.onefile_var,
            style='Custom.TCheckbutton'
        ).pack(side='left', padx=10)
        
        ttk.Checkbutton(
            checkbox_frame,
            text="隐藏控制台 --noconsole",
            variable=self.noconsole_var,
            style='Custom.TCheckbutton'
        ).pack(side='left', padx=10)
        
        ttk.Checkbutton(
            checkbox_frame,
            text="调试模式 --debug",
            variable=self.debug_var,
            style='Custom.TCheckbutton'
        ).pack(side='left', padx=10)
        
        ttk.Checkbutton(
            checkbox_frame,
            text="清理临时文件 --clean",
            variable=self.clean_var,
            style='Custom.TCheckbutton'
        ).pack(side='left', padx=10)
        
        # 高级参数
        advanced_frame = ttk.Frame(param_frame, style='Custom.TFrame')
        advanced_frame.pack(fill='x', pady=10)
        
        # 打包名称
        ttk.Label(
            advanced_frame,
            text="程序名称:",
            style='Custom.TLabel'
        ).grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        self.name_entry = PlaceholderEntry(
            advanced_frame,
            placeholder="程序名称 (可选)",
            width=25
        )
        self.name_entry.grid(row=0, column=1, sticky='w')
        
        # 额外参数
        ttk.Label(
            advanced_frame,
            text="额外参数:",
            style='Custom.TLabel'
        ).grid(row=1, column=0, sticky='w', pady=10, padx=(0, 10))
        
        self.extra_params_entry = PlaceholderEntry(
            advanced_frame,
            placeholder="额外命令行参数 (可选)",
            width=40
        )
        self.extra_params_entry.grid(row=1, column=1, sticky='ew', pady=10)
        
        # 参数预设下拉列表
        ttk.Label(
            advanced_frame,
            text="参数预设:",
            style='Custom.TLabel'
        ).grid(row=2, column=0, sticky='w', padx=(0, 10))
        
        self.param_preset_combobox = ttk.Combobox(
            advanced_frame,
            values=list(PARAMETER_PRESETS.keys()),
            state='readonly',
            width=38,
            font=('Microsoft YaHei', 10)
        )
        self.param_preset_combobox.grid(row=2, column=1, sticky='ew', pady=(0, 10))
        self.param_preset_combobox.set("选择常用参数...")
        
        # 绑定选择事件
        self.param_preset_combobox.bind("<<ComboboxSelected>>", self.on_preset_selected)
        
        # 提示标签
        self.preset_desc_label = ttk.Label(
            advanced_frame,
            text="",
            style='Custom.TLabel',
            foreground=THEME_DARK,
            font=('Microsoft YaHei', 9, 'italic')
        )
        self.preset_desc_label.grid(row=3, column=1, sticky='w', pady=(0, 10))
        
        advanced_frame.columnconfigure(1, weight=1)
    
    def create_log_section(self, parent):
        """日志显示区域"""
        log_frame = ttk.LabelFrame(
            parent,
            text="实时日志",
            padding=10,
            style='Custom.TFrame'
        )
        log_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self.log_area = LogTextArea(
            log_frame,
            height=20,
            width=45,
            font=('Consolas', 9)
        )
        self.log_area.pack(fill='both', expand=True)
        
        # 日志控制按钮
        log_btn_frame = ttk.Frame(log_frame, style='Custom.TFrame')
        log_btn_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(
            log_btn_frame,
            text="清空日志",
            command=self.log_area.clear,
            style='Custom.TButton'
        ).pack(side='left')
        
        self.log_level_var = tk.StringVar(value="INFO")
        log_level_menu = ttk.OptionMenu(
            log_btn_frame,
            self.log_level_var,
            "INFO",
            "DEBUG", "INFO", "WARNING", "ERROR"
        )
        log_level_menu.pack(side='right')
        
        ttk.Label(
            log_btn_frame,
            text="日志级别:",
            style='Custom.TLabel'
        ).pack(side='right', padx=5)
    
    def create_control_buttons(self, parent):
        """控制按钮"""
        btn_frame = ttk.Frame(parent, style='Custom.TFrame')
        btn_frame.pack(fill='x', pady=(15, 0))
        
        ttk.Button(
            btn_frame,
            text="开始打包",
            command=self.on_start_pack,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="停止打包",
            command=self.on_stop_pack,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="清空配置",
            command=self.clear_config,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="关于",
            command=self.show_about,
            style='Custom.TButton'
        ).pack(side='right', padx=5)
    
    def setup_layout(self):
        """布局设置"""
        # 主窗口背景
        self.root.config(bg=BG_COLOR)
    
    # 预设参数选择事件
    def on_preset_selected(self, event):
        """参数预设选择事件"""
        selected = self.param_preset_combobox.get()
        
        if selected in PARAMETER_PRESETS:
            # 添加参数到输入框
            current_value = self.extra_params_entry.get_real_value()
            
            # 如果输入框已有内容，添加空格分隔
            if current_value:
                new_value = f"{current_value} {selected}"
            else:
                new_value = selected
            
            self.extra_params_entry._hide_placeholder()
            self.extra_params_entry.delete(0, 'end')
            self.extra_params_entry.insert(0, new_value)
            
            # 显示参数说明
            self.preset_desc_label.config(text=f"说明: {PARAMETER_PRESETS[selected]}")
    
    # 事件处理方法
    def select_main_file(self):
        """选择主程序文件"""
        filename = filedialog.askopenfilename(
            title="选择主程序文件",
            filetypes=[
                ("Python文件", "*.py"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.main_file_entry._hide_placeholder()
            self.main_file_entry.delete(0, 'end')
            self.main_file_entry.insert(0, filename)
    
    def select_icon(self):
        """选择图标文件"""
        filename = filedialog.askopenfilename(
            title="选择图标文件",
            filetypes=[
                ("图标文件", "*.ico"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.icon_entry._hide_placeholder()
            self.icon_entry.delete(0, 'end')
            self.icon_entry.insert(0, filename)
    
    def select_output_dir(self):
        """选择输出目录"""
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_entry._hide_placeholder()
            self.output_entry.delete(0, 'end')
            self.output_entry.insert(0, directory)
    
    def add_resource(self):
        """添加资源文件"""
        files = filedialog.askopenfilenames(
            title="选择资源文件",
            filetypes=[
                ("所有文件", "*.*")
            ]
        )
        for file in files:
            self.resource_list.insert('end', file)
    
    def remove_resource(self):
        """删除选中的资源文件"""
        selection = self.resource_list.curselection()
        if selection:
            self.resource_list.delete(selection)
    
    def on_start_pack(self):
        """开始打包按钮点击事件"""
        # 收集配置
        config = self.gather_config()
        
        # 验证配置
        if not self.validate_config(config):
            return
        
        self.controller.start_packaging(config)
    
    def on_stop_pack(self):
        """停止打包按钮点击事件"""
        self.controller.stop_packaging()
    
    def clear_config(self):
        """清空配置"""
        if messagebox.askyesno("确认", "确定要清空所有配置吗？"):
            # 重置所有输入框
            self.main_file_entry.delete(0, 'end')
            self.main_file_entry._show_placeholder()
            
            self.icon_entry.delete(0, 'end')
            self.icon_entry._show_placeholder()
            
            self.resource_list.delete(0, 'end')
            
            self.output_entry.delete(0, 'end')
            self.output_entry._show_placeholder()
            
            self.name_entry.delete(0, 'end')
            self.name_entry._show_placeholder()
            
            self.extra_params_entry.delete(0, 'end')
            self.extra_params_entry._show_placeholder()
            
            # 重置复选框
            self.onefile_var.set(True)
            self.noconsole_var.set(True)
            self.debug_var.set(False)
            self.clean_var.set(True)
            
            # 重置预设选择
            self.param_preset_combobox.set("选择常用参数...")
            self.preset_desc_label.config(text="")
            
            # 清空日志
            self.log_area.clear()
    
    def show_about(self):
        """打开项目GitHub页面"""
        webbrowser.open("https://github.com/Ancylx/AnsPacker")
    
    def gather_config(self):
        """收集所有配置信息"""
        resources = list(self.resource_list.get(0, 'end'))
        
        return {
            'main_file': self.main_file_entry.get_real_value(),
            'icon_file': self.icon_entry.get_real_value(),
            'resources': resources,
            'output_dir': self.output_entry.get_real_value(),
            'name': self.name_entry.get_real_value(),
            'onefile': self.onefile_var.get(),
            'noconsole': self.noconsole_var.get(),
            'debug': self.debug_var.get(),
            'clean': self.clean_var.get(),
            'extra_params': self.extra_params_entry.get_real_value()
        }
    
    def validate_config(self, config):
        """验证配置有效性"""
        if not config['main_file']:
            self.show_error("请选择主程序文件！")
            return False
        
        if not os.path.isfile(config['main_file']):
            self.show_error(f"主程序文件不存在：{config['main_file']}")
            return False
        
        if config['icon_file'] and not os.path.isfile(config['icon_file']):
            self.show_error(f"图标文件不存在：{config['icon_file']}")
            return False
        
        for resource in config['resources']:
            if not os.path.exists(resource):
                self.show_error(f"资源文件不存在：{resource}")
                return False
        
        if config['output_dir'] and not os.path.isdir(config['output_dir']):
            self.show_error(f"输出目录不存在：{config['output_dir']}")
            return False
        
        return True
    
    def show_error(self, message):
        """显示错误信息"""
        messagebox.showerror("错误", message)
    
    def show_success(self, message):
        """显示成功信息"""
        messagebox.showinfo("成功", message)
    
    def show_warning(self, message):
        """显示警告信息"""
        messagebox.showwarning("警告", message)