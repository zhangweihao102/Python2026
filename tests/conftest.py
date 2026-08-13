import pytest
import time
import os
import io
import sys
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config import config
from pages.login_page import LoginPage
from pages.home_page import HomePage

# 强制将控制台输出编码设置为 utf-8，解决 Windows 终端下 Emoji 打印报错的问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

@pytest.fixture(scope="session")
def driver():
    """
    全局 WebDriver Fixture。
    整个 Pytest 测试会话（Session）期间只启动一次 Appium Driver，
    并在这里判断是否需要执行登录，保证所有的测试用例拿到的都是“已登录”状态的 Driver。
    """
    print("\n🚀 [Session Setup] 正在初始化 Appium Driver...")
    
    options = UiAutomator2Options()
    options.platform_name = config.PLATFORM_NAME
    options.device_name = config.DEVICE_NAME 
    options.app_package = config.APP_PACKAGE
    options.app_activity = config.APP_ACTIVITY
    options.no_reset = config.NO_RESET
    options.automation_name = config.AUTOMATION_NAME
    
    # 为了让你能看到完整的启动过程，这里我们注释掉“不重启”的配置
    # 这样每次运行都会重新拉起 App
    # options.set_capability("appium:dontStopAppOnReset", True)
    # options.set_capability("appium:forceAppLaunch", False)
    
    # 规避系统和动画相关问题
    options.set_capability("appium:disableWindowAnimation", True)
    options.set_capability("appium:settings[waitForIdleTimeout]", 0)
    options.set_capability("appium:shouldTerminateApp", False)
    options.set_capability("appium:skipServerInstallation", True)

    d = webdriver.Remote(config.APPIUM_SERVER_URL, options=options)
    d.implicitly_wait(10)
    
    # 给 App 一点缓冲时间
    time.sleep(3) 
    
    # 判断当前页面状态
    current_activity = d.current_activity
    print(f"ℹ️ 当前 App Activity: {current_activity}")
    
    # 这里通过判断当前是不是启动页或者登录页，来决定要不要执行自动登录
    # 你可以根据实际情况添加更多的 activity 判断
    if "LoginActivity" in current_activity or "SplashActivity" in current_activity or "GuideActivity" in current_activity:
        print("⚠️ 检测到当前处于未登录状态或启动页，准备执行自动登录...")
        login_page = LoginPage(d)
        login_page.do_login(config.TEST_ACCOUNT, config.TEST_PASSWORD)
        
        print("🔄 登录完成，开始执行底部 Tab 切换遍历...")
        home_page = HomePage(d)
        home_page.click_tab_1()
        home_page.click_tab_2()
        home_page.click_tab_4()
        home_page.click_tab_5()
        
        print("✅ 遍历完成，默认切换到语聊房 (Tab 3) 及其 Party 选项卡...")
        home_page.click_tab_3()
        home_page.click_top_tab_party()
        
        # --- 新增：等待底层连接就绪 ---
        print("⏳ 登录及初始化完毕，等待 6 秒让 WebSocket 长链接及接口完全就绪...")
        time.sleep(6)
    else:
        print("✅ 检测到当前已经处于登录状态（或在 App 内部页面），直接进入业务测试！")

    # 将准备好的 driver 交给各个测试用例使用
    yield d

    # 所有测试用例执行完毕后，执行清理工作
    print("\n🛑 [Session Teardown] 所有测试执行完毕，关闭 Driver...")
    d.quit()
