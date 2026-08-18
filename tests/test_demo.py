import pytest
import time

class TestDemoModule:
    """
    业务测试模块示例
    这里面的用例会自动使用 conftest.py 里的 driver fixture
    """
    
    def test_01_swipe_homepage(self, driver):
        """
        测试用例 1: 首页滑动测试
        """
        print("\n[Test Case] 开始测试：滑动首页")
        # 此时的 driver 已经是确保处于登录状态的了，不需要关心登录逻辑
        
        # 模拟一个滑动操作 (x1, y1) 到 (x2, y2)
        print("模拟向下滑动刷新...")
        driver.swipe(360, 1000, 360, 200, 500)
        time.sleep(2)
        
        # 简单断言验证
        assert driver.current_package == "so.fun.test", "当前应用包名不正确！"
        print("[Test Case] 滑动首页测试完成！")

    def test_02_check_profile(self, driver):
        """
        测试用例 2: 查看个人资料页
        """
        print("\n[Test Case] 开始测试：查看个人主页")
        # 直接继续在上一个用例的基础（已登录）上进行操作
        time.sleep(2)
        print("[Test Case] 查看个人主页测试完成！")
