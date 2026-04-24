import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """
    所有 Page 类的基类，封装了 WebDriver 的底层常用操作（查找元素、点击、输入、截图等）
    """
    def __init__(self, driver, screenshot_dir="outputs/screenshots/default"):
        self.driver = driver
        self.screenshot_dir = screenshot_dir

    def find_element(self, locator, timeout=10):
        """显示等待，查找单个元素"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_elements(self, locator, timeout=10):
        """显示等待，查找一组元素"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def click(self, locator, timeout=10):
        """显示等待元素可点击，并执行点击操作"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def input_text(self, locator, text, timeout=10):
        """清空输入框并输入文本"""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    def save_screenshot(self, filename):
        """保存截图到当前测试的专属目录"""
        filepath = os.path.join(self.screenshot_dir, filename)
        self.driver.save_screenshot(filepath)
        print(f"[截图保存] {filepath}")

    def sleep(self, seconds):
        """封装 time.sleep"""
        time.sleep(seconds)
