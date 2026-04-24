from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from core.base_page import BasePage
from utils.captcha_solver import CaptchaSolver
import os

class RegisterPage(BasePage):
    """
    注册页面模型 (Page Object)
    封装手机号注册流程所需的元素和操作
    """
    
    # ================= 元素定位器 (Locators) =================
    # TODO: 下面其他元素的 ID 还需要你抓取替换
    
    # 手机号注册入口按钮 (从启动页进入注册页的图标)
    REGISTER_ENTRY_BTN = (AppiumBy.ID, "com.uchat.test:id/ivOther")
    
    # 国家/地区选择区域
    AREA_CODE_LAYOUT = (AppiumBy.ID, "com.uchat.test:id/areaCodeLayout")
    
    # 手机号输入框
    PHONE_INPUT = (AppiumBy.ID, "com.uchat.test:id/etPhone")
    
    # Next (下一步/发送验证码) 按钮
    NEXT_BTN = (AppiumBy.ID, "com.uchat.test:id/tv_send_phone")
    
    # 弹出的图形校验复选框
    CAPTCHA_CHECKBOX = (AppiumBy.ID, "checkbox")
    
    # 拼图验证码的大背景图 (包含滑块)
    CAPTCHA_BG_IMAGE = (AppiumBy.XPATH, "//android.widget.Image[contains(@text, 'Image-based CAPTCHA')]")
    
    # 拼图/图形验证码弹窗中的 Skip 按钮
    CAPTCHA_SKIP_BTN = (AppiumBy.XPATH, "//*[@text='Skip']")
    
    # 验证码输入框
    CODE_INPUT = (AppiumBy.ID, "com.uchat.test:id/et_verify_code")
    
    # 设置密码输入框
    PWD_INPUT = (AppiumBy.ID, "com.uchat.test:id/et_password")
    
    # 勾选同意用户协议/隐私政策复选框
    AGREE_CHECKBOX = (AppiumBy.ID, "com.uchat.test:id/cb_agree")
    
    # 注册(完成)按钮
    REGISTER_BTN = (AppiumBy.ID, "com.uchat.test:id/btn_register")

    # ================= 页面操作方法 =================
    def click_register_entry(self):
        """点击登录页面的注册入口"""
        print("⏳ 正在点击注册入口...")
        try:
            self.click(self.REGISTER_ENTRY_BTN, timeout=5)
            self.sleep(1)
        except Exception:
            print("⚠️ 没找到专用的注册入口按钮，如果是同页面输入则忽略此步。")

    def click_area_code(self):
        """点击国家/区号选择区域"""
        print("👆 正在点击国家/区号选择区域...")
        try:
            self.click(self.AREA_CODE_LAYOUT, timeout=5)
            self.sleep(1)
        except Exception:
            print("⚠️ 没找到区号选择区域。")

    def input_phone(self, phone):
        """输入手机号"""
        print(f"⌨️ 正在输入手机号: {phone}")
        self.input_text(self.PHONE_INPUT, phone)

    def click_next(self):
        """点击 Next (下一步/获取验证码)"""
        print("👆 点击 Next 按钮...")
        self.click(self.NEXT_BTN)
        self.sleep(2) # 等待短信发送或页面跳转

    def click_captcha_checkbox(self):
        """处理图形校验弹窗"""
        print("🔍 检测是否有图形校验弹窗...")
        try:
            # 1. 有些时候是一个 checkbox，给 5 秒等待
            self.click(self.CAPTCHA_CHECKBOX, timeout=5)
            print("✅ 已点击图形校验复选框")
            self.sleep(2)
        except Exception:
            print("⚠️ 未检测到 checkbox 图形校验弹窗。")
            
        try:
            # 2. 无法抓取内部小图，整张大图是渲染出来的
            print("🔍 尝试寻找拼图验证码背景图...")
            bg_element = self.find_element(self.CAPTCHA_BG_IMAGE, timeout=5)
            print("✅ 找到拼图验证码弹窗，准备执行图像识别和滑动解锁")
            
            # 2.1 截取当前屏幕，并裁剪出大图区域保存
            full_screen_path = os.path.join(self.screenshot_dir, "captcha_fullscreen.png")
            self.driver.save_screenshot(full_screen_path)
            
            captcha_img_path = os.path.join(self.screenshot_dir, "captcha_bg.png")
            solver = CaptchaSolver()
            if solver.crop_element_image(full_screen_path, bg_element, captcha_img_path):
                # 2.2 ddddocr 要求有一张纯背景大图和一张单独的滑块小图
                # 但这种 App 把滑块和背景嵌在一张图里，普通的 slide_match 无法直接使用
                # 为了不让流程卡死，这里我们退回到使用 "Skip" 按钮，或者固定滑动一段距离
                # 真实的解决需要定制化的图像处理算法来把小方块抠出来
                
                # 尝试点击左下角的刷新按钮 (根据你截图，左下角有三个图标，中间那个圆圈箭头可能是刷新)
                print("⚠️ 因为无法分离大图和小图，尝试直接滑动固定距离（这通常会失败）...")
                
                # 假设滑块初始在背景图最右侧，我们要把它拖到左侧的蓝色阴影处
                rect = bg_element.rect
                # 假设滑块在最右侧 10% 的位置，垂直居中
                start_x = rect['x'] + int(rect['width'] * 0.85)
                start_y = rect['y'] + int(rect['height'] * 0.5)
                
                # 假设目标阴影在最左侧 20% 的位置
                end_x = rect['x'] + int(rect['width'] * 0.2)
                
                # 执行滑动动作
                actions = ActionChains(self.driver)
                actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
                actions.w3c_actions.pointer_action.pointer_down()
                actions.w3c_actions.pointer_action.move_to_location(end_x, start_y)
                actions.w3c_actions.pointer_action.pointer_up()
                actions.perform()
                
                print(f"👉 已执行盲猜滑动解锁动作")
                self.sleep(3)
                
                # 滑动完不管成功与否，再尝试点一次 Skip 保底
                try:
                    self.click(self.CAPTCHA_SKIP_BTN, timeout=3)
                    print("✅ 成功点击 Skip 跳过图形校验")
                except Exception:
                    pass
            
        except Exception as e:
            print(f"⚠️ 未检测到拼图校验弹窗或滑动失败。({e})")

    def input_verify_code(self, code):
        """输入验证码"""
        print(f"⌨️ 输入验证码: {code}")
        self.input_text(self.CODE_INPUT, code)

    def input_password(self, pwd):
        """输入设置密码"""
        print("⌨️ 输入注册密码: ******")
        self.input_text(self.PWD_INPUT, pwd)

    def check_agree_policy(self):
        """勾选同意协议"""
        print("👆 勾选同意隐私政策...")
        try:
            self.click(self.AGREE_CHECKBOX, timeout=3)
        except Exception:
            print("⚠️ 没找到同意协议复选框，跳过勾选。")

    def click_register(self):
        """点击注册按钮"""
        print("👆 点击注册按钮...")
        self.click(self.REGISTER_BTN)
        self.sleep(4)  # 等待注册接口返回结果
        self.save_screenshot("after_register_click.png")

    # ================= 业务流程组合 =================
    def register_flow(self, phone, verify_code, pwd):
        """
        组合操作：执行手机号注册业务流（目前只跑到输入手机号并点击Next）
        """
        self.click_register_entry()
        
        # 如果你们 App 默认不是美国区号，可能需要放开下面这行去选区号
        # self.click_area_code()
        
        self.input_phone(phone)
        
        # 点击 Next 按钮 (通常会发送验证码并跳转到输入验证码页面)
        self.click_next()
        
        # 处理弹出的图形验证复选框
        self.click_captcha_checkbox()
        
        print("🛑 临时中断：前面的流程已执行完毕，后续需要补充验证码、密码等元素的 ID。")
        # self.input_verify_code(verify_code)
        # self.input_password(pwd)
        # self.check_agree_policy()
        # self.click_register()
