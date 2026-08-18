import time
from common.adb_utils import AdbUtils
from appium.webdriver.common.appiumby import AppiumBy

class HomePage:
    """
    首页页面对象 (Page Object)
    封装首页相关的操作，例如底部导航栏切换
    """
    
    def __init__(self, driver):
        self.driver = driver

    def click_tab_1(self):
        print("👆 切换到 Tab 1 (语音/电话)")
        self.driver.find_element(AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="so.fun.test:id/flutter_tabbar_container"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ImageView[1]').click()
        time.sleep(6)

    def click_tab_2(self):
        print("👆 切换到 Tab 2 (发现/星球)")
        self.driver.find_element(AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="so.fun.test:id/flutter_tabbar_container"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ImageView[2]').click()
        time.sleep(6)

    def click_tab_3(self):
        print("👆 切换到 Tab 3 (主麦/语音房)")
        self.driver.find_element(AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="so.fun.test:id/flutter_tabbar_container"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ImageView[3]').click()
        time.sleep(6)

    def click_tab_4(self):
        print("👆 切换到 Tab 4 (消息/聊天)")
        self.driver.find_element(AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="so.fun.test:id/flutter_tabbar_container"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ImageView[4]').click()
        time.sleep(6)

    def click_tab_5(self):
        print("👆 切换到 Tab 5 (个人中心)")
        self.driver.find_element(AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="so.fun.test:id/flutter_tabbar_container"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ImageView[5]').click()
        time.sleep(6)

    # --- 语聊房 (Tab 3) 顶部导航 ---

    def click_top_tab_mine(self):
        """点击顶部 'Mine' Tab"""
        print("👆 切换到顶部 'Mine' Tab")
        self.driver.find_element(AppiumBy.XPATH, '//android.view.View[@content-desc="Mine \n Tab 1 of 3"]').click()
        time.sleep(1)

    def click_top_tab_party(self):
        """点击顶部 'Party' Tab (默认中间)"""
        print("👆 切换到顶部 'Party' Tab")
        self.driver.find_element(AppiumBy.XPATH, '//android.view.View[@content-desc="Party \n Tab 2 of 3"]').click()
        time.sleep(1)

    def click_top_tab_activity(self):
        """点击顶部 'Activity' Tab"""
        print("👆 切换到顶部 'Activity' Tab")
        self.driver.find_element(AppiumBy.XPATH, '//android.view.View[@content-desc="Activity \n Tab 3 of 3"]').click()
        time.sleep(1)

    def click_search_icon(self):
        """点击顶部搜索图标 (放大镜)"""
        print("👆 点击顶部搜索图标")
        self.driver.find_element(AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="so.fun.test:id/flutter_tabbar_container"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView/android.view.View[1]/android.widget.ImageView[1]').click()
        time.sleep(2)

    def click_leaderboard_icon(self):
        """点击顶部排行榜图标 (奖杯)"""
        print("👆 点击顶部排行榜图标")
        self.driver.find_element(AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="so.fun.test:id/flutter_tabbar_container"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView/android.view.View[1]/android.widget.ImageView[2]').click()
        time.sleep(2)

