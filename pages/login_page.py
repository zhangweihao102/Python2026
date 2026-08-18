import time
from common.adb_utils import AdbUtils
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

class LoginPage:
    """
    登录页面对象 (Page Object)
    专门存放登录页面的所有操作，将业务逻辑与具体的定位/点击细节解耦
    """
    
    def __init__(self, driver):
        self.driver = driver

    def click_other_login_method(self):
        """首页：点击'其他方式登录'"""
        print("👆 等待 'Sign in with Google' 登录首页完全加载...")
        time.sleep(5)  # 启动后增加等待时间，确保首页完全加载完毕

        print("👆 正在点击'其他方式登录'图标...")
        el = self.driver.find_element(AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="so.fun.test:id/ivOtherId"]')
        el.click()
        time.sleep(5)  # 等待动画和页面跳转

    def input_account(self, account):
        """登录页：输入账号"""
        print("⌨️ 正在输入账号...")
        el = self.driver.find_element(AppiumBy.XPATH, '//android.widget.EditText[@resource-id="so.fun.test:id/et_id"]')
        el.click()
        el.clear()
        el.send_keys(account)
        time.sleep(1)

    def input_password(self, password):
        """输入密码并收起键盘"""
        print(f"⌨️ 输入密码: {'*' * len(password)}")
        el = self.driver.find_element(AppiumBy.XPATH, '//android.widget.EditText[@resource-id="so.fun.test:id/et_pwd"]')
        el.click()
        el.clear()
        el.send_keys(password)
        
        print("🔙 输入完成，正在收起软键盘...")
        # 调用底层 ADB 工具强制收起键盘
        AdbUtils.press_back()
        time.sleep(2)  # 给键盘收起的动画留出充足时间

    def hide_keyboard(self):
        """收起键盘（确保底部按钮位置正确）"""
        print("⌨️ 尝试收起键盘...")
        AdbUtils.keyevent(4)  # 返回键，用于收起软键盘
        time.sleep(2)

    def click_login_btn(self):
        """登录页：点击底部的紫色登录按钮"""
        print("👆 正在点击最底部的登录按钮...")
        el = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@resource-id="so.fun.test:id/tv_login"]')
        el.click()
        time.sleep(6)  # 等待登录结果加载及可能的权限弹窗

    def handle_permission_popup(self):
        """处理首次登录后的通知权限弹窗"""
        print("🔍 检查是否有通知权限弹窗...")
        try:
            # 设置一个较短的隐式等待，专门用于找弹窗，避免没弹窗时卡住太久
            self.driver.implicitly_wait(3)
            allow_btn = self.driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]')
            print("👆 发现通知权限弹窗，点击'始终允许'...")
            allow_btn.click()
            time.sleep(2)
        except NoSuchElementException:
            print("✅ 未发现通知权限弹窗，继续执行。")
        finally:
            # 恢复全局的隐式等待时间（这里假设全局设为 10 秒，你也可以根据 conftest.py 调整）
            self.driver.implicitly_wait(10)

    def do_login(self, account, password):
        """
        组合动作：执行完整的登录业务流
        """
        print("\n--- 🏁 开始自动登录流程 ---")
        self.click_other_login_method()
        self.input_account(account)
        self.input_password(password)
        # 注释掉强制收起键盘的操作，避免触发物理返回键退出页面
        # self.hide_keyboard()
        self.click_login_btn()
        self.handle_permission_popup()
        print("--- 🏁 登录流程执行完毕 ---\n")
