import pytest
from pages.login_page import LoginPage
from config import config

class TestLogin:
    """
    登录模块测试用例
    """
    
    @pytest.mark.login
    @pytest.mark.smoke
    def test_uchat_login_flow(self, driver, screenshot_dir):
        """
        测试用例：执行完整的 UChat 登录流程
        这里用到的 `driver` 和 `screenshot_dir` 是从 conftest.py 里自动注入的
        """
        print("\n[INFO] 开始执行测试用例：UChat 登录流程")
        
        # 1. 实例化登录页面对象 (POM 核心)
        login_page = LoginPage(driver, screenshot_dir)
        
        try:
            # 2. 调用页面对象封装好的业务流程
            login_page.login_flow(config.TEST_ACCOUNT, config.TEST_PASSWORD)
            
            # 3. 补充断言：验证是否登录成功
            # TODO: 建议使用 WebDriverWait 查找登录成功后独有的元素
            # 比如首页底部导航栏的某个按钮是否存在
            # assert login_page.find_element((AppiumBy.ID, "com.uchat.test:id/home_nav")).is_displayed()
            
            print("[INFO] 登录流程执行完毕，没有发生报错！")
            
        except Exception as e:
            # 如果用例执行失败，在异常里截图保存现场
            print(f"[ERROR] 测试用例失败：{e}")
            login_page.save_screenshot("error_test_uchat_login_flow.png")
            raise
