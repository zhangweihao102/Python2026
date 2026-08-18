import pytest
import time
from pages.home_page import HomePage
from common.adb_utils import AdbUtils

class TestMessageModule:
    """
    【消息/聊天】模块测试集合 (对应 Tab 4)
    """

    @pytest.fixture(scope="class", autouse=True)
    def enter_message_tab(self, driver):
        """
        前置准备：在执行本类所有测试用例前，自动切换到【消息】Tab。
        scope="class" 表示这个切换动作在这个类里只执行一次。
        autouse=True 表示自动调用，用例里不需要手动写。
        """
        print("\n🚀 [模块前置] 准备测试【消息模块】，正在切换到 Tab 4...")
        home_page = HomePage(driver)
        home_page.click_tab_4()
        # 停顿一下等待页面加载
        time.sleep(2)
        yield
        print("\n🛑 [模块后置] 【消息模块】测试结束。")

    def test_01_check_message_list(self, driver):
        """用例1：检查消息列表是否正常"""
        print("\n  -> [Test] 执行用例：检查消息列表...")
        # 这里写消息列表具体的断言或点击逻辑
        # AdbUtils.tap(x, y) 
        time.sleep(1)
        assert True

    def test_02_send_new_message(self, driver):
        """用例2：测试发送新消息功能"""
        print("\n  -> [Test] 执行用例：发送新消息...")
        # 因为前置 fixture 已经切过来了，这里直接就是消息页面，随便操作
        time.sleep(1)
        assert True
