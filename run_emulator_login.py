import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from pages.login_page import LoginPage
from config import config

# ================= 常用模拟器设备名/端口 =================
# MuMu 模拟器:     127.0.0.1:7555
# 夜神模拟器 (Nox): 127.0.0.1:62001  (或 52001)
# 雷电模拟器:       127.0.0.1:5555
# 逍遥模拟器:       127.0.0.1:21503
# Android Studio:  emulator-5554
# ========================================================

# 您可以根据实际使用的模拟器修改这里的端口
EMULATOR_DEVICE_NAME = "127.0.0.1:16480"

def run_emulator_login():
    print(f"\n[INFO] 准备连接模拟器: {EMULATOR_DEVICE_NAME}")
    
    # 1. 配置 Appium 启动参数
    options = UiAutomator2Options()
    options.platform_name = config.PLATFORM_NAME
    options.device_name = EMULATOR_DEVICE_NAME
    options.app_package = config.APP_PACKAGE
    options.app_activity = config.APP_ACTIVITY
    options.no_reset = config.NO_RESET
    options.automation_name = config.AUTOMATION_NAME

    # 截图保存目录
    screenshot_dir = os.path.join("outputs", "screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    driver = None
    try:
        # 2. 连接 Appium Server
        driver = webdriver.Remote(config.APPIUM_SERVER_URL, options=options)
        driver.implicitly_wait(10)
        print("[INFO] 成功连接到模拟器并启动 App！")

        # 3. 实例化页面对象 (复用现有的 POM)
        login_page = LoginPage(driver, screenshot_dir)

        # 4. 执行登录流程
        print("\n[INFO] 开始在模拟器上执行 UChat 登录流程...")
        login_page.login_flow(config.TEST_ACCOUNT, config.TEST_PASSWORD)
        print("\n[INFO] 模拟器登录流程执行完毕！")

    except Exception as e:
        print(f"\n[ERROR] 模拟器登录执行失败: {e}")
    finally:
        if driver:
            driver.quit()
            print("[INFO] 已断开与模拟器的连接。")

if __name__ == "__main__":
    run_emulator_login()
