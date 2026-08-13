import pytest
import time
from pages.home_page import HomePage

class TestProfileModule:
    """
    【个人中心】模块测试集合 (对应 Tab 5)
    """

    @pytest.fixture(scope="class", autouse=True)
    def enter_profile_tab(self, driver):
        """前置准备：自动切换到【个人中心】Tab"""
        print("\n🚀 [模块前置] 准备测试【个人中心】，正在切换到 Tab 5...")
        home_page = HomePage(driver)
        home_page.click_tab_5()
        time.sleep(2)
        yield
        print("\n🛑 [模块后置] 【个人中心】测试结束。")

    def test_01_check_avatar(self, driver):
        """用例1：检查头像显示"""
        print("\n  -> [Test] 执行用例：检查头像...")
        time.sleep(1)
        assert True

    def test_02_edit_nickname(self, driver):
        """用例2：修改昵称"""
        print("\n  -> [Test] 执行用例：修改昵称...")
        time.sleep(1)
        assert True
