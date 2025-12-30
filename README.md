<div align="center">
  <img src="resources\icons\AnsPack.ico" alt="AnsPacker" width="200"/>
  <h1>AnsPacker</h1>
  <p>
    <a href="https://github.com/Ancylx/AnsPacker/releases"><img src="https://img.shields.io/github/v/release/Ancylx/AnsPacker" alt="Release"></a>
  </p>
</div>
<img src="Screenshot\AnsPacker-v1.0.0.png" alt="AnsPacker"/>

## ✨ 核心特性

- 📊 **实时日志追踪** - 打包过程实时显示详细日志，错误信息高亮提示，问题排查一目了然
- 📁 **智能资源管理** - 批量添加图片、配置文件等非代码资源，自动处理 `--add-data` 参数
- ⚡ **参数预设系统** - 内置常用参数模板，一键添加高级选项，无需记忆复杂命令
- 🎨 **现代化界面** - 基于 Tkinter 的简约主题，配色干净、交互流畅
- 📦 **零依赖分发** - 一键生成独立可执行文件，目标用户无需安装 Python 环境

## 🚀 快速开始

### 环境要求

- Python 3.7+
- Windows/Linux/macOS
- pip 包管理器

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/Ancylx/AnsPacker.git
cd AnsPacker

# 安装 PyInstaller
pip install -r requirements.txt
```

### 运行程序

```bash
python main.py
```

## 🎯 完整使用教程

### 1. 基础配置

1. **选择主程序**：点击"浏览"选择你的 `main.py` 入口文件
2. **配置输出目录**：指定打包后的文件存放位置（建议使用空目录）
3. **添加资源文件**：点击"添加"批量导入图片、配置文件等非代码资源

### 2. 高级选项

- **单文件模式**：生成一个独立的 `.exe` 文件，便于分发
- **隐藏控制台**：GUI 程序必选，运行时不会弹出黑窗口
- **清理临时文件**：打包完成后自动清理 build 目录，节省空间
- **参数预设**：从下拉菜单快速添加 `--version-file`、`--uac-admin` 等高级参数

### 3. 执行打包

点击"开始打包"后，实时日志会显示 PyInstaller 的完整输出过程。打包成功后，在输出目录的 `dist` 文件夹中找到生成的可执行文件。

### 4. 分发应用

将生成的 `.exe` 文件（及相关资源，如果有）发送给最终用户。用户**无需安装 Python**，直接双击运行即可。

## 📁 项目结构

```
AnsPacker/
├── main.py                 # 程序入口与控制器
├── gui.py                  # GUI 界面与事件处理
├── packer_core.py          # 打包核心逻辑与 PyInstaller 调用
├── requirements.txt        # 依赖列表（PyInstaller）
├── README.md              # 项目说明文档
├── LICENSE                # MIT 开源协议
└── resources/
    └── icons/
        └── AnsPack.ico    # 程序图标（32x32 ICO 格式）
```

## 🔧 技术栈与实现细节

- **GUI 框架**：Tkinter + ttk，采用 `clam` 主题引擎深度定制
- **打包引擎**：PyInstaller（通过 `subprocess` 实时读取输出流）
- **编码处理**：UTF-8 编码 + `backslashreplace` 错误处理，完美支持中文路径
- **并发处理**：多线程执行打包任务，避免界面冻结
- **错误处理**：完整的异常捕获与日志分析，智能判断 PyInstaller 安装状态
- **资源嵌入**：智能处理 `--add-data` 参数，自动适配 Windows/Linux/macOS 路径格式

## 🛠️ 开发与贡献

### 本地开发环境搭建

```bash
# 克隆仓库
git clone https://github.com/Ancylx/AnsPacker.git
cd AnsPacker

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装开发依赖
pip install -r requirements.txt
```

### 待办事项

- [ ] 随系统切换中/英文
- [ ] 随系统切换深/浅色主题
- [ ] 更多 PyInstaller 参数预设模板
- [ ] 打包配置预设+一键导入/导出功能

## 📄 开源协议

本项目采用 **MIT 协议** 开源，您可以自由使用、修改和分发。详情请参见 [LICENSE](LICENSE) 文件。

---

### ⭐ Star 支持

如果AnsPacker对您有帮助，不妨点点 Star 支持！
