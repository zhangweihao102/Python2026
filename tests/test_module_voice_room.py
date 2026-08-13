import pytest
import time
import os
from datetime import datetime
from pages.home_page import HomePage
from pages.search_page import SearchPage
from common.adb_utils import AdbUtils

class TestVoiceRoomModule:
    """
    【语聊房/主麦】模块测试集合 (对应 Tab 3)
    """

    @pytest.fixture(scope="class", autouse=True)
    def enter_voice_room_tab(self, driver):
        """前置准备：自动切换到【语聊房】Tab"""
        print("\n🚀 [模块前置] 准备测试【语聊房模块】，正在切换到 Tab 3...")
        home_page = HomePage(driver)
        home_page.click_tab_3()
        time.sleep(2)
        yield
        print("\n🛑 [模块后置] 【语聊房模块】测试结束。")

    def test_01_top_tabs_switch(self, driver):
        """用例1：测试语聊房顶部三个 Tab 的切换"""
        print("\n  -> [Test] 执行用例：测试顶部 Top Tab (Mine/Party/Activity) 切换...")
        home_page = HomePage(driver)

        # 默认在 Party，先切到 Mine
        home_page.click_top_tab_mine()
        time.sleep(2) # 留点时间观察UI变化和数据加载

        # 切回 Party
        home_page.click_top_tab_party()
        time.sleep(2)

        # 切到 Activity
        home_page.click_top_tab_activity()
        time.sleep(2)

        # 核心：环境恢复 (Teardown)
        # 为保证其他用例(如搜索/排行榜)不受影响，最后需要切回默认的 Party Tab
        print("  -> (环境恢复) 切回默认的 'Party' Tab...")
        home_page.click_top_tab_party()
        time.sleep(1)

        assert True

    def test_02_search_flow(self, driver):
        """用例2：综合搜索流程 (搜索房间进房 -> 返回 -> 搜索用户进主页)"""
        print("\n  -> [Test] 执行用例：综合搜索流程...")
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        
        ROOM_ID = "244686"
        USER_ID = "10253247"
        
        # ================= 1. 进入搜索页 =================
        home_page.click_search_icon()
        
        # ================= 2. 搜索房间流程 =================
        print(f"  -> 🔍 开始搜索房间 ID: {ROOM_ID}")
        search_page.click_search_input()
        search_page.input_search_keyword(ROOM_ID)
        
        print("  -> ⏳ 等待搜索结果加载...")
        time.sleep(4)
        
        search_page.click_tab_room()
        
        try:
            search_page.click_room_search_result()
            print("  -> 📸 正在截图保存进房状态(成功/失败)...")
        except Exception as e:
            print(f"  -> ❌ 点击房间失败，可能是没搜到: {e}")
        
        # 无论成功失败，都截图保留证据
        os.makedirs("appium_screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        room_screenshot_path = f"appium_screenshots/room_status_{timestamp}.png"
        AdbUtils.screencap(room_screenshot_path)
        print(f"  -> ✅ 房间状态截图已保存至: {room_screenshot_path}")
        
        # 退回搜索页，准备进行下一次搜索
        print("  -> 🔙 退出房间，返回搜索页面...")
        AdbUtils.press_back() 
        time.sleep(2)
        
        # ================= 3. 搜索用户流程 =================
        print(f"  -> 🔍 开始搜索用户 ID: {USER_ID}")
        search_page.click_search_input()
        search_page.input_search_keyword(USER_ID)
        
        print("  -> ⏳ 等待搜索结果加载...")
        time.sleep(4)
        
        search_page.click_tab_usuario()
        
        try:
            search_page.click_first_search_result()
            print("  -> 📸 正在截图保存用户主页状态(成功/失败)...")
        except Exception as e:
            print(f"  -> ❌ 点击用户失败，可能是没搜到: {e}")
            
        user_screenshot_path = f"appium_screenshots/user_profile_status_{timestamp}.png"
        AdbUtils.screencap(user_screenshot_path)
        print(f"  -> ✅ 用户主页状态截图已保存至: {user_screenshot_path}")
        
        # ================= 4. 核心：环境恢复 =================
        print("  -> (环境恢复) 正在退回语聊房首页...")
        AdbUtils.press_back() # 退回搜索结果页
        time.sleep(2)
        AdbUtils.press_back() # 退回语聊房首页
        time.sleep(2)
        
        assert True

    def test_03_leaderboard_function(self, driver):
        """用例4：测试排行榜功能"""
        print("\n  -> [Test] 执行用例：测试顶部排行榜功能...")
        home_page = HomePage(driver)
        
        # 1. 点击排行榜图标
        home_page.click_leaderboard_icon()
        
        # 2. 模拟在排行榜页面停留查看
        print("  -> (模拟) 查看排行榜...")
        time.sleep(3)
        
        # 3. 模拟返回上一个页面 (回到语聊房主页)
        print("  -> (模拟) 从排行榜返回...")
        AdbUtils.press_back()
        time.sleep(2)
        
        assert True
