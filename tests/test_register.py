import pytest
from pages.register_page import RegisterPage
from utils.random_data import generate_us_phone

class TestRegister:
    """
    注册模块测试用例01
    """
    
    @pytest.mark.register
    @pytest.mark.smoke
    def test_mobile_register_flow(self, driver, screenshot_dir):
        """
        测试用例：执行完整的手机号注册流程
        """
        print("\n🚀 开始执行测试用例：手机号注册流程")
        
        # 1. 实例化注册页面对象
        register_page = RegisterPage(driver, screenshot_dir)
        
        # 模拟注册用的测试数据
        # 这里改为随机生成一个美国手机号
        test_phone = generate_us_phone()
        test_code = "123456"  # 假设你们环境有万能验证码，或者需要手动/接口读取
        test_pwd = "password123"
        
        try:
            # 2. 调用封装好的注册业务流
            register_page.register_flow(test_phone, test_code, test_pwd)
            
            # 3. 补充断言：验证注册是否成功
            # TODO: 注册成功后通常会跳转到首页，或者提示“注册成功”的 Toast
            # 可以在这里添加对跳转后页面独有元素的查找，作为断言
            
            print("🎉 注册流程执行完毕，没有发生报错！")
            
        except Exception as e:
            # 异常截图现场保存
            print(f"❌ 注册测试用例失败：{e}")
            register_page.save_screenshot("error_test_mobile_register_flow.png")
            raise
