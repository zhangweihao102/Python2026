import unittest
import time
import os
from datetime import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import config


class AppiumDemoTest(unittest.TestCase):
    
    def setUp(self):
        """
        初始化 Appium WebDriver 并启动 App
        """
        print("🔄 正在连接 Appium Server 并启动 App...")
        
        # 配置 Appium 连接参数 (Desired Capabilities)
        options = UiAutomator2Options()
        # 设备信息
        options.platform_name = config.PLATFORM_NAME
        # 设备名称，可通过 adb devices 获取
        options.device_name = config.DEVICE_NAME 
        
        # 目标 App 信息
        # 被测 App 的包名
        options.app_package = config.APP_PACKAGE
        # 被测 App 的启动 Activity
        options.app_activity = config.APP_ACTIVITY
        
        # 其他配置
        options.no_reset = config.NO_RESET # 不要重置 App 数据
        options.automation_name = config.AUTOMATION_NAME # 使用 UiAutomator2 引擎
        
        # 防止 Appium 在初始化时强制重启 App（如果需要每次都从头跑，可以把这两行注释掉）
        # options.set_capability("appium:dontStopAppOnReset", True)
        # options.set_capability("appium:forceAppLaunch", False)
        
        # 规避系统安全键盘弹起导致 UiAutomator 进程被杀 (SecurityException)
        # options.set_capability("unicodeKeyboard", True)
        # options.set_capability("resetKeyboard", True)
        # 禁用软键盘弹起，避免动画影响
        options.set_capability("appium:disableWindowAnimation", True)
        # 核心：无视动画等待，直接获取元素 (针对首页轮播图)
        options.set_capability("appium:settings[waitForIdleTimeout]", 0)
        # 测试结束后不要杀掉 App，方便观察最后停在哪里
        options.set_capability("appium:shouldTerminateApp", False)
        # 已经手动安装，跳过服务端安装，避免超时
        options.set_capability("appium:skipServerInstallation", True)

        # 连接到本地运行的 Appium Server
        appium_server_url = config.APPIUM_SERVER_URL
        
        # 创建 WebDriver 实例
        self.driver = webdriver.Remote(appium_server_url, options=options)
        self.driver.implicitly_wait(10) # 隐式等待 10 秒
        print("✅ App 启动成功！")

        # 每次运行测试时，新建一个以当前时间命名的文件夹用来存截图
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.screenshot_dir = f"appium_screenshots/{current_time}"
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
        print(f"📁 本次运行的截图将保存在: {self.screenshot_dir}/")

    def test_app_login_flow(self):
        """
        测试用例：执行登录流程
        """
        print("🚀 开始执行测试用例：登录流程")
        
        try:
            # 1. 等待并点击“其他方式登录”图标
            # 注意：如果你的应用启动后不在这个页面，可以把这段注释掉
            print("⏳ 等待首页完全加载...")
            time.sleep(5)
            print("⏳ 正在寻找并点击'其他方式登录'图标...")
            # 注意：这里的 418 1275 是在 720x1600 分辨率下的估算位置
            # 如果在首页点不到，需要根据实际截图重新测算这个按钮的坐标
            os.system(f"adb -s {config.DEVICE_NAME} shell input tap 418 1275")
            time.sleep(5)
            
            # 截图保存当前状态
            step1_pic = os.path.join(self.screenshot_dir, "01_after_click_icon.png")
            # 规避 Appium 原生截图 API 卡死的问题，改用 adb 截图
            os.system(f"adb -s {config.DEVICE_NAME} shell screencap -p /data/local/tmp/sc.png")
            os.system(f"adb -s {config.DEVICE_NAME} pull /data/local/tmp/sc.png {step1_pic}")
            print(f"📸 已保存截图：{step1_pic}")
            
            # 2. 找到账号输入框并输入
            print("⏳ 正在寻找并输入账号...")
            time.sleep(4)  # 强制等待 4 秒，让页面完全加载完毕
            
            # 由于底层 UiAutomation 在此页面极其容易崩溃死锁，改用 ADB 坐标点击和输入规避
            print("👆 使用坐标点击账号输入框...")
            os.system(f"adb -s {config.DEVICE_NAME} shell input tap 360 384")
            time.sleep(1)
            print("⌨️ 正在输入账号...")
            os.system(f"adb -s {config.DEVICE_NAME} shell input text {config.TEST_ACCOUNT}")
            
            # 输入密码
            print("👆 使用坐标点击密码输入框...")
            # 密码框通常在账号框下方，大约 y 增加 120 像素左右
            os.system(f"adb -s {config.DEVICE_NAME} shell input tap 360 500")
            time.sleep(1)
            print("⌨️ 正在输入密码...")
            os.system(f"adb -s {config.DEVICE_NAME} shell input text {config.TEST_PASSWORD}")

            # 3. 收起键盘（极其重要）
            # 使用 ADB 输入文本时，有时键盘会弹出，有时不会。
            # 为了确保登录按钮在屏幕最下方，我们强制发送收起键盘的指令，并等待 UI 稳定
            print("⌨️ 尝试收起键盘（确保按钮回落到最底部）...")
            os.system(f"adb -s {config.DEVICE_NAME} shell input keyevent 4") # 返回键，用来收起真实设备的软键盘
            time.sleep(2)
            
            # 4. 点击登录按钮
            print("👆 正在点击最底部的登录按钮...")
            # 键盘收起后，紫色的登录按钮会在屏幕偏下方 (Y=1400左右)
            os.system(f"adb -s {config.DEVICE_NAME} shell input tap 360 1400")
            
            # 等待登录结果加载
            time.sleep(4)
            
            # 截图保存登录后状态
            step2_pic = os.path.join(self.screenshot_dir, "02_after_login.png")
            os.system(f"adb -s {config.DEVICE_NAME} shell screencap -p /data/local/tmp/sc.png")
            os.system(f"adb -s {config.DEVICE_NAME} pull /data/local/tmp/sc.png {step2_pic}")
            print(f"📸 已保存登录结果截图：{step2_pic}")
            
        except Exception as e:
            print(f"❌ 测试过程中出现异常：{e}")
            error_pic = os.path.join(self.screenshot_dir, "error.png")
            os.system(f"adb -s {config.DEVICE_NAME} shell screencap -p /data/local/tmp/sc.png")
            os.system(f"adb -s {config.DEVICE_NAME} pull /data/local/tmp/sc.png {error_pic}")
            print(f"📸 已保存异常现场截图：{error_pic}")
            raise

    def tearDown(self):
        """
        测试结束后的清理工作
        """
        print("🛑 测试结束，关闭 App 并断开连接。")
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    unittest.main()
