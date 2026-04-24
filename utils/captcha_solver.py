import os
import ddddocr
from PIL import Image

class CaptchaSolver:
    """
    处理滑块/拼图等复杂验证码的工具类
    """
    def __init__(self):
        # 初始化 ddddocr，专门用于滑块缺口识别
        self.det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
        
    def get_slide_distance(self, background_path, target_path):
        """
        计算滑块需要滑动的距离
        :param background_path: 带缺口的背景大图路径
        :param target_path: 滑块小图路径
        :return: 需要滑动的 X 轴像素距离
        """
        try:
            with open(target_path, 'rb') as f:
                target_bytes = f.read()
            with open(background_path, 'rb') as f:
                background_bytes = f.read()

            # 使用 ddddocr 的 slide_match 功能计算缺口位置
            # res 是一个字典，包含 'target_y' 和 'target' (一个列表 [min_x, min_y, max_x, max_y])
            res = self.det.slide_match(target_bytes, background_bytes, simple_target=True)
            
            # 返回目标缺口的最小 X 坐标，即为需要滑动的距离
            if 'target' in res and len(res['target']) >= 1:
                return res['target'][0]
            else:
                print("❌ 未能识别到滑块缺口位置")
                return 0
        except Exception as e:
            print(f"❌ 计算滑动距离时发生错误: {e}")
            return 0
            
    def crop_element_image(self, screenshot_path, element, save_path):
        """
        从全屏截图中，根据元素的 bounds 裁剪出元素的局部图片
        :param screenshot_path: 全屏截图路径
        :param element: WebDriver 的 WebElement 对象
        :param save_path: 裁剪后保存的路径
        :return: 成功返回 True
        """
        try:
            # 获取元素的坐标和尺寸 (字典格式，包含 x, y, width, height)
            rect = element.rect
            left = int(rect['x'])
            top = int(rect['y'])
            right = int(rect['x'] + rect['width'])
            bottom = int(rect['y'] + rect['height'])
            
            # 打开全屏截图并裁剪
            img = Image.open(screenshot_path)
            element_img = img.crop((left, top, right, bottom))
            element_img.save(save_path)
            return True
        except Exception as e:
            print(f"❌ 裁剪元素图片失败: {e}")
            return False
