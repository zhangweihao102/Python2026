import unittest
import time
import os
from datetime import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AppiumDemoTest(unittest.TestCase):
    
    def setUp(self):
        """
        初始化 Appium WebDriver 并启动 App
        """
        print("🔄 正在连接 Appium Server 并启动 App...")
        
        # 配置 Appium 连接参数 (Desired Capabilities)
        options = UiAutomator2Options()
        # 设备信息
        options.platform_name = 'Android'
        # 设备名称，可通过 adb devices 获取
        options.device_name = 'A9GVVB2B16009567' 
        
        # 目标 App 信息
        # 被测 App 的包名
        options.app_package = 'com.uchat.test'
        # 被测 App 的启动 Activity
        options.app_activity = 'com.chat.login.ui.login.LoginActivity'
        
        # 其他配置
        options.no_reset = True # 不要重置 App 数据
        options.automation_name = 'UiAutomator2' # 使用 UiAutomator2 引擎

        # 连接到本地运行的 Appium Server
        appium_server_url = 'http://127.0.0.1:4723'
        
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
            # 根据你抓取到的 resource-id: com.uchat.test:id/ivOtherId
            print("⏳ 正在寻找并点击'其他方式登录'图标...")
            other_login_icon = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((AppiumBy.ID, "com.uchat.test:id/ivOtherId"))
            )
            other_login_icon.click()
            print("👆 已点击'其他方式登录'图标")
            
            # 等待页面跳转动画
            time.sleep(2)
            
            # 截图保存当前状态
            step1_pic = os.path.join(self.screenshot_dir, "01_after_click_icon.png")
            self.driver.save_screenshot(step1_pic)
            print(f"📸 已保存截图：{step1_pic}")
            
            # 2. 寻找账号输入框并输入
            print("⏳ 正在寻找并输入账号...")
            # 你的提示里没有单独列出账号框，通常它叫 et_phone 或 et_account，我先假设它的 ID 叫 et_account，
            # 或者如果是通过 text="Email/Phone" 之类的提示，我们可以通过 class 定位。
            # 为了稳妥，我们通过找所有的 EditText 来定位：第一个通常是账号，第二个是密码 (et_pwd)
            account_inputs = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
            )
            
            if len(account_inputs) >= 2:
                # 第一个是账号输入框
                account_inputs[0].send_keys("10150903")
                print("⌨️ 已输入账号")
                
                # 第二个是密码输入框 (也可以通过资源 ID 直接定位)
                pwd_input = self.driver.find_element(AppiumBy.ID, "com.uchat.test:id/et_pwd")
                pwd_input.send_keys("123456")
                print("⌨️ 已输入密码")
            else:
                # fallback，直接根据刚才抓取的 ID 尝试填密码
                pwd_input = self.driver.find_element(AppiumBy.ID, "com.uchat.test:id/et_pwd")
                pwd_input.send_keys("123456")
                print("⌨️ 仅找到了密码框并输入密码")

            # 3. 点击密码显示图标（眼睛图标）
            print("👆 点击显示密码图标...")
            pwd_visible_icon = self.driver.find_element(AppiumBy.ID, "com.uchat.test:id/iv_pwd_visible")
            pwd_visible_icon.click()
            time.sleep(1)
            
            # 4. 点击登录按钮
            print("👆 正在点击登录按钮...")
            login_btn = self.driver.find_element(AppiumBy.ID, "com.uchat.test:id/tv_login")
            login_btn.click()
            
            # 等待登录结果加载
            time.sleep(4)
            
            # 截图保存登录后状态
            step2_pic = os.path.join(self.screenshot_dir, "02_after_login.png")
            self.driver.save_screenshot(step2_pic)
            print(f"📸 已保存登录结果截图：{step2_pic}")
            
        except Exception as e:
            print(f"❌ 测试过程中出现异常：{e}")
            error_pic = os.path.join(self.screenshot_dir, "error.png")
            self.driver.save_screenshot(error_pic)
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
