import time
from common.adb_utils import AdbUtils
from appium.webdriver.common.appiumby import AppiumBy

class SearchPage:
    """搜索页面对象"""

    def __init__(self, driver=None):
        self.driver = driver

    def click_search_input(self):
        """点击顶部搜索输入框"""
        print("👆 点击搜索输入框")
        self.driver.find_element(AppiumBy.XPATH, '//android.widget.EditText').click()
        time.sleep(1)

    def input_search_keyword(self, keyword):
        """输入搜索关键词"""
        print(f"⌨️ 输入搜索关键词: {keyword}")
        el = self.driver.find_element(AppiumBy.XPATH, '//android.widget.EditText')
        el.clear()
        el.send_keys(keyword)
        # 输入后通常需要按回车进行搜索，这里发送回车键事件
        time.sleep(1)
        AdbUtils.keyevent(66) # 66 是 Enter 键
        time.sleep(2)

    def click_tab_room(self):
        """点击 'Room' (房间) 选项卡"""
        print("👆 切换到 'Room' 选项卡")
        self.driver.find_element(AppiumBy.XPATH, '//android.view.View[@content-desc="Room \n Tab 1 of 2"]').click()
        time.sleep(2)

    def click_room_search_result(self):
        """点击搜索结果列表的房间项"""
        print("👆 点击搜索出的房间结果")
        self.driver.find_element(AppiumBy.XPATH, '//android.view.View[@content-desc="来我房间 \n Chat \n 1 \n 100"]').click()
        time.sleep(4) # 进房通常需要加载时间

    def click_tab_usuario(self):
        """点击 'Usuario' (个人用户) 选项卡"""
        print("👆 切换到 'Usuario' 选项卡")
        self.driver.find_element(AppiumBy.XPATH, '//android.view.View[@content-desc="User Tab 2 of 2"]').click()
        time.sleep(2)

    def click_first_search_result(self):
        """点击搜索结果列表的第一项"""
        print("👆 点击搜索结果第一项")
        self.driver.find_element(AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="dsl12345678910 \n ID：10253247"]').click()
        time.sleep(3) # 进入个人主页通常需要一点加载时间
