from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage

class LoginPage(BasePage):
    """
    登录页面模型 (Page Object)
    将登录页面上的所有【元素定位器】和【页面操作】封装在这里
    """
    
    # ================= 元素定位器 (Locators) =================
    OTHER_LOGIN_ICON = (AppiumBy.ID, "com.uchat.test:id/ivOtherId")
    ALL_EDIT_TEXTS = (AppiumBy.CLASS_NAME, "android.widget.EditText")
    PWD_INPUT = (AppiumBy.ID, "com.uchat.test:id/et_pwd")
    PWD_VISIBLE_ICON = (AppiumBy.ID, "com.uchat.test:id/iv_pwd_visible")
    LOGIN_BTN = (AppiumBy.ID, "com.uchat.test:id/tv_login")

    # ================= 页面操作方法 =================
    def click_other_login(self):
        """点击其他方式登录图标"""
        print("[INFO] 正在寻找并点击'其他方式登录'图标...")
        try:
            self.click(self.OTHER_LOGIN_ICON, timeout=5)
            self.sleep(2)  # 等待跳转动画
            self.save_screenshot("01_after_click_icon.png")
            print("[INFO] 成功点击'其他方式登录'图标")
        except Exception as e:
            print("[WARN] 未找到'其他方式登录'图标，可能已经处于登录页面。")

    def input_credentials(self, account, pwd):
        """输入账号和密码"""
        print("[INFO] 正在寻找并输入账号密码...")
        # 找页面里所有的输入框
        inputs = self.find_elements(self.ALL_EDIT_TEXTS)
        if len(inputs) >= 2:
            inputs[0].send_keys(account)
            print(f"[INFO] 已输入账号: {account}")
            
            self.input_text(self.PWD_INPUT, pwd)
            print("[INFO] 已输入密码: ******")
        else:
            # Fallback：只通过资源 ID 定位密码框
            self.input_text(self.PWD_INPUT, pwd)
            print("[INFO] 仅找到了密码框并输入密码: ******")

    def click_pwd_visible(self):
        """点击显示密码的眼睛图标"""
        print("[INFO] 点击显示密码图标...")
        self.click(self.PWD_VISIBLE_ICON)
        self.sleep(1)

    def click_login(self):
        """点击登录按钮"""
        print("[INFO] 正在点击登录按钮...")
        self.click(self.LOGIN_BTN)
        self.sleep(8)  # 增加等待时间，确保完全进入 App 首页（可根据实际网络情况调整）
        
        # 加上时间戳保存截图
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.save_screenshot(f"02_after_login_{timestamp}.png")

    # ================= 业务流程组合 =================
    def login_flow(self, account, pwd):
        """
        组合操作：执行完整的登录业务流
        """
        self.click_other_login()
        self.input_credentials(account, pwd)
        self.click_pwd_visible()
        self.click_login()
