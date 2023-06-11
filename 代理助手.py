import winreg
import ctypes
import tkinter as tk
import ctypes
import sys

def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        # 如果已经以管理员权限运行，则直接执行脚本
        run_script()
    else:
        # 以管理员权限重新运行脚本
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

def run_script():
    # 创建主窗口
    window = tk.Tk()
    window.title("代理设置")
    window.geometry("300x200")

    # 使窗口始终在最前面显示
    window.wm_attributes('-topmost', 1)

    # 定义代理服务器地址和端口的默认值
    default_ip = "127.0.0.1"
    default_port = "8080"

    def set_proxy():
        # 获取输入框中的代理服务器地址和端口
        proxy_ip = ip_entry.get()
        proxy_port = port_entry.get()

        # 校验输入框的值
        if not proxy_ip or not proxy_port:
            status_label.config(text="请输入有效的代理服务器地址和端口")
            return

        try:
            # 打开Internet设置的注册表键
            internet_settings = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                               r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                                               0, winreg.KEY_WRITE)

            # 设置代理服务器地址和端口
            proxy_address = f"{proxy_ip}:{proxy_port}"
            winreg.SetValueEx(internet_settings, "ProxyServer", 0, winreg.REG_SZ, proxy_address)

            # 启用代理
            winreg.SetValueEx(internet_settings, "ProxyEnable", 0, winreg.REG_DWORD, 1)

            # 刷新系统代理设置
            internet_option_refresh = ctypes.windll.Wininet.InternetSetOptionW
            internet_option_refresh(0, 37, 0, 0)

            status_label.config(text="代理已设置为：" + proxy_address)

        except Exception as e:
            status_label.config(text="设置代理时发生错误：" + str(e))

    def reset_proxy():
        try:
            # 打开Internet设置的注册表键
            internet_settings = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                               r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                                               0, winreg.KEY_WRITE)

            # 禁用代理
            winreg.SetValueEx(internet_settings, "ProxyEnable", 0, winreg.REG_DWORD, 0)

            # 刷新系统代理设置
            internet_option_refresh = ctypes.windll.Wininet.InternetSetOptionW
            internet_option_refresh(0, 37, 0, 0)

            status_label.config(text="已恢复不走代理")

        except Exception as e:
            status_label.config(text="恢复代理时发生错误：" + str(e))

    # 创建输入框和标签
    ip_label = tk.Label(window, text="代理IP地址:")
    ip_label.pack()
    ip_entry = tk.Entry(window)
    ip_entry.insert(tk.END, default_ip)
    ip_entry.pack()

    port_label = tk.Label(window, text="代理端口:")
    port_label.pack()
    port_entry = tk.Entry(window)
    port_entry.insert(tk.END, default_port)
    port_entry.pack()

    # 创建按钮
    set_button = tk.Button(window, text="设置代理", command=set_proxy)
    set_button.pack()

    reset_button = tk.Button(window, text="取消代理", command=reset_proxy)
    reset_button.pack()

    # 创建状态标签
    status_label = tk.Label(window, text="")
    status_label.pack()

    # 运行主循环
    window.mainloop()

run_as_admin()
