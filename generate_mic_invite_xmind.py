import os
import time
import shutil
import zipfile
import xml.etree.ElementTree as ET
import uuid

def create_xmind_file():
    template_path = r"D:\用例文件\端内贵族VIP测试用例.xmind"
    file_path = r"D:\用例文件\上麦邀请优化测试用例.xmind"
    temp_dir = r"D:\用例文件\temp_xmind"
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    shutil.copy(template_path, file_path)
    
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    with zipfile.ZipFile(file_path, 'r') as zf:
        zf.extractall(temp_dir)
    
    content_xml_path = os.path.join(temp_dir, 'content.xml')
    tree = ET.parse(content_xml_path)
    root = tree.getroot()
    
    ns = {'xmind': 'urn:xmind:xmap:xmlns:content:2.0'}
    ET.register_namespace('', 'urn:xmind:xmap:xmlns:content:2.0')
    ET.register_namespace('xhtml', 'http://www.w3.org/1999/xhtml')
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    ET.register_namespace('svg', 'http://www.w3.org/2000/svg')
    ET.register_namespace('fo', 'http://www.w3.org/1999/XSL/Format')
    
    sheet = root.find('.//xmind:sheet', ns)
    title_elem = sheet.find('./xmind:title', ns)
    if title_elem is not None:
        title_elem.text = "上麦邀请测试用例"
    
    root_topic = sheet.find('./xmind:topic', ns)
    root_title = root_topic.find('./xmind:title', ns)
    if root_title is not None:
        root_title.text = "【优化】上麦邀请测试用例"
    
    # 找到 children -> topics，然后清空
    children = root_topic.find('./xmind:children', ns)
    if children is not None:
        topics_container = children.find('./xmind:topics', ns)
        if topics_container is not None:
            for child in list(topics_container):
                topics_container.remove(child)
        else:
            topics_container = ET.SubElement(children, '{urn:xmind:xmap:xmlns:content:2.0}topics')
            topics_container.set('type', 'attached')
    else:
        children = ET.SubElement(root_topic, '{urn:xmind:xmap:xmlns:content:2.0}children')
        topics_container = ET.SubElement(children, '{urn:xmind:xmap:xmlns:content:2.0}topics')
        topics_container.set('type', 'attached')
    
    test_cases = [
        {
            "title": "1. 用户识别与筛选测试 (核心逻辑)",
            "cases": [
                {"title": "TC-01: 目标用户识别 - 当日无上麦行为 [P0]", "details": ["前置条件: 新用户或当日上麦行为=0的用户", "操作步骤: 1. 登录APP  2. 进入他人语音房  3. 停留超过配置时间", "预期结果: 触发上麦邀请浮窗展示"]},
                {"title": "TC-02: 过滤用户 - 当日已有上麦成功记录 [P0]", "details": ["前置条件: 用户当日【邀请上麦成功次数】≥1", "操作步骤: 进入他人语音房并停留超过配置时间", "预期结果: 不触发上麦邀请浮窗"]},
                {"title": "TC-03: 配置生效 - 阈值参数修改验证 [P1]", "details": ["前置条件: 修改配置将触发阈值从1改为其他值", "操作步骤: 验证不同阈值下的用户过滤逻辑", "预期结果: 系统按新配置值执行筛选"]}
            ]
        },
        {
            "title": "2. 前置条件验证测试",
            "cases": [
                {"title": "TC-04: 房间状态 - 允许游客上麦 [P0]", "details": ["前置条件: 目标用户符合识别条件", "操作步骤: 进入【允许游客上麦】的房间", "预期结果: 满足前置条件，停留超时后触发邀请"]},
                {"title": "TC-05: 房间状态 - 禁止游客上麦 [P0]", "details": ["前置条件: 目标用户符合识别条件", "操作步骤: 进入【禁止游客上麦】的房间", "预期结果: 不触发邀请"]},
                {"title": "TC-06: 麦位状态 - 有空麦位且未上锁 [P0]", "details": ["前置条件: 目标用户符合识别条件，房间允许游客上麦", "操作步骤: 进入有空麦位且麦位未锁的房间", "预期结果: 满足前置条件，停留超时后触发邀请"]},
                {"title": "TC-07: 麦位状态 - 麦位已满 [P0]", "details": ["前置条件: 目标用户符合识别条件，房间允许游客上麦", "操作步骤: 进入麦位已满的房间", "预期结果: 不触发邀请"]},
                {"title": "TC-08: 麦位状态 - 麦位已上锁 [P0]", "details": ["前置条件: 目标用户符合识别条件，房间允许游客上麦", "操作步骤: 进入麦位已上锁的房间", "预期结果: 不触发邀请"]}
            ]
        },
        {
            "title": "3. 触发时机与异常处理",
            "cases": [
                {"title": "TC-09: 停留计时 - 超过配置时间触发 [P0]", "details": ["前置条件: 所有前置条件满足", "操作步骤: 进入房间后停留超过配置时间（暂定3秒）", "预期结果: 到达时间点后自动弹出邀请浮窗"]},
                {"title": "TC-10: 未超时时 - 不触发邀请 [P0]", "details": ["前置条件: 所有前置条件满足", "操作步骤: 进入房间后在配置时间内离开或进行其他操作", "预期结果: 不触发邀请浮窗"]},
                {"title": "TC-11: 麦上无人 - 不触发邀请 [P0]", "details": ["前置条件: 所有其他条件满足", "操作步骤: 进入麦上无人的房间", "预期结果: 命中不触发规则，即使停留超时也不展示邀请"]},
                {"title": "TC-12: 本人房间 - 不触发邀请 [P0]", "details": ["前置条件: 用户是房主", "操作步骤: 进入自己的房间", "预期结果: 不触发邀请"]}
            ]
        },
        {
            "title": "4. 邀请样式与UI展示测试",
            "cases": [
                {"title": "TC-13: 身份展示 - 房主管理员均在/均不在 [P0]", "details": ["前置条件: 触发邀请浮窗", "操作步骤: 房主和管理员均在或均不在房间", "预期结果: 展示【房主】身份"]},
                {"title": "TC-14: 身份展示 - 房主不在管理员在 [P0]", "details": ["前置条件: 触发邀请浮窗", "操作步骤: 房主不在，管理员在房间", "预期结果: 展示【管理员】身份"]},
                {"title": "TC-15: 身份展示 - 房主在管理员不在 [P0]", "details": ["前置条件: 触发邀请浮窗", "操作步骤: 房主在，管理员不在房间", "预期结果: 展示【房主】身份"]},
                {"title": "TC-16: UI元素 - 浮窗内容完整展示 [P1]", "details": ["前置条件: 触发邀请浮窗", "操作步骤: 检查浮窗各元素", "预期结果: 展示：房主/管理员头像、昵称、身份、预设话术、上麦主Btn、关闭X"]}
            ]
        },
        {
            "title": "5. 交互与功能测试",
            "cases": [
                {"title": "TC-17: 自动消失 - 5秒后自动关闭 [P0]", "details": ["前置条件: 邀请浮窗已展示", "操作步骤: 不进行任何操作，等待5秒", "预期结果: 浮窗自动消失"]},
                {"title": "TC-18: 手动关闭 - 点击X按钮 [P0]", "details": ["前置条件: 邀请浮窗已展示", "操作步骤: 点击右上角【X】按钮", "预期结果: 浮窗立即关闭"]},
                {"title": "TC-19: 上麦操作 - 未获取麦克风权限 [P0]", "details": ["前置条件: 邀请浮窗已展示，用户未授权麦克风", "操作步骤: 点击【Join&Chat】按钮", "预期结果: 走正常的权限获取流程"]},
                {"title": "TC-20: 上麦操作 - 已获取麦克风权限 [P0]", "details": ["前置条件: 邀请浮窗已展示，用户已授权麦克风", "操作步骤: 点击【Join&Chat】按钮", "预期结果: 上语音麦成功"]},
                {"title": "TC-21: 麦位分配 - 按顺序选位 [P1]", "details": ["前置条件: 房间有多个空麦位", "操作步骤: 通过邀请上麦", "预期结果: 按麦序由低到高依次分配"]}
            ]
        },
        {
            "title": "6. 边界Case与冲突处理",
            "cases": [
                {"title": "TC-22: 冲突处理 - 仍有空麦位 [P0]", "details": ["前置条件: 用户点击上麦时，有其他用户同时手动上麦", "操作步骤: 模拟并发上麦，操作后仍有空麦位", "预期结果: 依次上下一个空麦位，上麦成功"]},
                {"title": "TC-23: 冲突处理 - 无空麦位 [P0]", "details": ["前置条件: 用户点击上麦时，麦位刚好被占满", "操作步骤: 模拟并发上麦，操作后无空麦位", "预期结果: 提示：Opps, the seat is full. Your request has been added to the waiting list."]},
                {"title": "TC-24: 快速进出房间 - 多次触发邀请 [P2]", "details": ["前置条件: 目标用户符合条件", "操作步骤: 快速进出多个满足条件的房间", "预期结果: 验证是否有防抖动或频率限制机制"]},
                {"title": "TC-25: 网络异常 - 弱网/断网场景 [P2]", "details": ["前置条件: 目标用户符合条件，网络异常", "操作步骤: 在弱网/断网状态下进入房间", "预期结果: 验证异常处理，恢复后是否重试"]}
            ]
        }
    ]
    
    for module in test_cases:
        module_topic = ET.SubElement(topics_container, '{urn:xmind:xmap:xmlns:content:2.0}topic')
        module_topic.set('id', str(uuid.uuid4()))
        module_topic.set('timestamp', str(int(time.time() * 1000)))
        module_title = ET.SubElement(module_topic, '{urn:xmind:xmap:xmlns:content:2.0}title')
        module_title.text = module["title"]
        
        module_children = ET.SubElement(module_topic, '{urn:xmind:xmap:xmlns:content:2.0}children')
        module_topics = ET.SubElement(module_children, '{urn:xmind:xmap:xmlns:content:2.0}topics')
        module_topics.set('type', 'attached')
        
        for case in module["cases"]:
            case_topic = ET.SubElement(module_topics, '{urn:xmind:xmap:xmlns:content:2.0}topic')
            case_topic.set('id', str(uuid.uuid4()))
            case_topic.set('timestamp', str(int(time.time() * 1000)))
            case_title = ET.SubElement(case_topic, '{urn:xmind:xmap:xmlns:content:2.0}title')
            case_title.text = case["title"]
            
            case_children = ET.SubElement(case_topic, '{urn:xmind:xmap:xmlns:content:2.0}children')
            case_topics = ET.SubElement(case_children, '{urn:xmind:xmap:xmlns:content:2.0}topics')
            case_topics.set('type', 'attached')
            
            for detail in case["details"]:
                detail_topic = ET.SubElement(case_topics, '{urn:xmind:xmap:xmlns:content:2.0}topic')
                detail_topic.set('id', str(uuid.uuid4()))
                detail_topic.set('timestamp', str(int(time.time() * 1000)))
                detail_title = ET.SubElement(detail_topic, '{urn:xmind:xmap:xmlns:content:2.0}title')
                detail_title.text = detail
    
    tree.write(content_xml_path, encoding='utf-8', xml_declaration=True)
    
    with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for foldername, subfolders, filenames in os.walk(temp_dir):
            for filename in filenames:
                file_path_full = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path_full, temp_dir)
                zf.write(file_path_full, arcname)
    
    shutil.rmtree(temp_dir)
    
    print(f"Xmind file saved to {file_path}")

if __name__ == "__main__":
    create_xmind_file()
