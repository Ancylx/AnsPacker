# main.py
import tkinter as tk
from gui import AnsPackerGUI
from packer_core import PackerCore

class ApplicationController:
    """主控制器，协调GUI和核心逻辑"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.packer = PackerCore()
        self.gui = AnsPackerGUI(self.root, self)
        
    def run(self):
        """启动应用"""
        self.root.mainloop()
    
    def start_packaging(self, config):
        """开始打包流程"""
        try:
            self.gui.log_area.clear()
            self.packer.pack(config, self.gui.log_area)
        except Exception as e:
            self.gui.show_error(f"打包启动失败: {str(e)}")
    def stop_packaging(self):
        """停止打包"""
        self.packer.stop()

if __name__ == "__main__":
    app = ApplicationController()
    app.run()
    