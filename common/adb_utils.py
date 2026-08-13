import os
import time
from config import config

class AdbUtils:
    """
    封装常用的 ADB 命令，用于规避 Appium 原生 click 导致的 UiAutomation 崩溃问题。
    默认使用 config.py 中配置的 DEVICE_NAME。
    """
    
    @staticmethod
    def tap(x, y, device=config.DEVICE_NAME):
        """坐标点击"""
        os.system(f"adb -s {device} shell input tap {x} {y}")

    @staticmethod
    def input_text(text, device=config.DEVICE_NAME):
        """输入文本"""
        os.system(f"adb -s {device} shell input text {text}")

    @staticmethod
    def keyevent(keycode, device=config.DEVICE_NAME):
        """发送按键事件 (如: 4 为返回键, 66 为回车键)"""
        os.system(f"adb -s {device} shell input keyevent {keycode}")

    # --- Android 系统三大金刚键封装 ---

    @staticmethod
    def press_back(device=config.DEVICE_NAME):
        """按下返回键 (Back)"""
        print("🔙 模拟按下物理/虚拟返回键")
        # 某些真机/系统下 keyevent 4 可能失效，这里改为基于截图计算的绝对坐标点击
        # os.system(f"adb -s {device} shell input keyevent 4")
        AdbUtils.tap(206, 1561, device)

    @staticmethod
    def press_home(device=config.DEVICE_NAME):
        """按下主页键 (Home)，回到手机桌面"""
        print("🏠 模拟按下物理/虚拟主页键")
        # os.system(f"adb -s {device} shell input keyevent 3")
        AdbUtils.tap(360, 1561, device)

    @staticmethod
    def press_recent_apps(device=config.DEVICE_NAME):
        """按下多任务键 (Recent Apps)，呼出后台应用列表"""
        print("🗂️ 模拟按下物理/虚拟多任务键")
        # os.system(f"adb -s {device} shell input keyevent 187")
        AdbUtils.tap(513, 1561, device)

    @staticmethod
    def screencap(save_path, device=config.DEVICE_NAME):
        """截取屏幕并保存到本地电脑"""
        os.system(f"adb -s {device} shell screencap -p /data/local/tmp/sc.png")
        os.system(f"adb -s {device} pull /data/local/tmp/sc.png {save_path}")
