import os
import pytest
from datetime import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config import config

@pytest.fixture(scope="session")
def screenshot_dir():
    """
    Session 级别的 fixture：固定使用 outputs/screenshots 目录，
    每次运行测试都会直接覆盖同名的旧截图文件。
    """
    dir_path = os.path.join("outputs", "screenshots")
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    print(f"\n[INFO] 本次运行的截图将保存在 (并覆盖旧文件): {dir_path}/")
    return dir_path


@pytest.fixture(scope="function")
def driver(screenshot_dir):
    """
    Function 级别的 fixture：每次跑用例前，启动一次 App；用例结束后，关闭 App
    如果希望 App 不必每个用例重启，可以把 scope 改为 "class" 或 "session"
    """
    print("\n[INFO] 正在连接 Appium Server 并启动 App...")
    
    options = UiAutomator2Options()
    options.platform_name = config.PLATFORM_NAME
    options.device_name = config.DEVICE_NAME
    options.app_package = config.APP_PACKAGE
    options.app_activity = config.APP_ACTIVITY
    options.no_reset = config.NO_RESET
    options.automation_name = config.AUTOMATION_NAME

    # 连接到本地运行的 Appium Server
    _driver = webdriver.Remote(config.APPIUM_SERVER_URL, options=options)
    _driver.implicitly_wait(10)
    print("[INFO] App 启动成功！")
    
    yield _driver  # 将 driver 对象传递给测试用例
    
    print("\n[INFO] 测试结束，关闭 App 并断开连接。")
    if _driver:
        _driver.quit()
