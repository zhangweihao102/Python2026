import os
import time
import shutil
import zipfile
import xml.etree.ElementTree as ET
import uuid

def create_xmind_file():
    template_path = r"D:\用例文件\端内贵族VIP测试用例.xmind"
    file_path = r"D:\用例文件\幸运礼物奖池优化测试用例.xmind"
    temp_dir = r"D:\用例文件\temp_lottery"
    
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
        title_elem.text = "幸运礼物奖池测试用例"
    
    root_topic = sheet.find('./xmind:topic', ns)
    root_title = root_topic.find('./xmind:title', ns)
    if root_title is not None:
        root_title.text = "【优化】幸运礼物奖池测试用例"
    
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
            "title": "1. 用户类型划分测试 (核心逻辑)",
            "cases": [
                {"title": "TC-01: 类型0-新用户判断-注册≤3天 [P0]", "details": ["前置条件: 新注册用户", "操作步骤: 注册≤3天的用户使用幸运礼物", "预期结果: 判断为类型0"]},
                {"title": "TC-02: 类型0-新用户判断-参与次数≤20次 [P0]", "details": ["前置条件: 用户历史参与≤20次", "操作步骤: 该用户使用幸运礼物", "预期结果: 判断为类型0"]},
                {"title": "TC-03: 类型0-新用户判断-礼物≤14000金币 [P0]", "details": ["前置条件: 用户历史幸运礼物≤14000金币", "操作步骤: 该用户使用幸运礼物", "预期结果: 判断为类型0"]},
                {"title": "TC-04: 类型1-盈利用户判断-7天有效次数≥150 [P0]", "details": ["前置条件: 用户7天有效抽奖≥150次，ROI≥95%*150%", "操作步骤: 该用户使用幸运礼物", "预期结果: 判断为类型1"]},
                {"title": "TC-05: 类型1-盈利用户判断-ROI≥95%*150% [P0]", "details": ["前置条件: 满足7天次数，ROI≥95%*150%", "操作步骤: 该用户使用幸运礼物", "预期结果: 判断为类型1"]},
                {"title": "TC-06: 类型2-亏损用户判断-7天有效次数≥150 [P0]", "details": ["前置条件: 用户7天有效抽奖≥150次，ROI≤96%*60%", "操作步骤: 该用户使用幸运礼物", "预期结果: 判断为类型2"]},
                {"title": "TC-07: 类型2-亏损用户判断-ROI≤96%*60% [P0]", "details": ["前置条件: 满足7天次数，ROI≤96%*60%", "操作步骤: 该用户使用幸运礼物", "预期结果: 判断为类型2"]},
                {"title": "TC-08: 类型3-普通用户判断 [P0]", "details": ["前置条件: 用户不符合类型0、1、2的条件", "操作步骤: 该用户使用幸运礼物", "预期结果: 判断为类型3"]}
            ]
        },
        {
            "title": "2. 有效抽奖次数计算测试",
            "cases": [
                {"title": "TC-09: 有效次数公式验证-单一金额 [P0]", "details": ["前置条件: 用户只抽700金币礼物100次", "操作步骤: 计算有效抽奖次数", "预期结果: 有效次数 = (700*100)^2 / (700^2*100) = 100"]},
                {"title": "TC-10: 有效次数公式验证-两种金额 [P0]", "details": ["前置条件: 用户抽700金币100次，1400金币100次", "操作步骤: 计算有效抽奖次数", "预期结果: 有效次数 = (700*100+1400*100)^2 / (700^2*100 + 1400^2*100) = 180"]},
                {"title": "TC-11: 有效次数公式验证-多种金额 [P1]", "details": ["前置条件: 用户抽多种不同金额礼物", "操作步骤: 验证公式计算正确性", "预期结果: 符合公式计算结果"]}
            ]
        },
        {
            "title": "3. 各类型用户奖池概率测试",
            "cases": [
                {"title": "TC-12: 类型0-新用户奖池概率验证 [P0]", "details": ["前置条件: 类型0用户使用幸运礼物", "操作步骤: 多次抽奖并统计各倍数中奖次数", "预期结果: 概率符合类型0配置，合计期望≈0.92"]},
                {"title": "TC-13: 类型1-盈利用户奖池概率验证 [P0]", "details": ["前置条件: 类型1用户使用幸运礼物", "操作步骤: 多次抽奖并统计各倍数中奖次数", "预期结果: 概率符合类型1配置，合计期望≈0.602"]},
                {"title": "TC-14: 类型2-亏损用户奖池概率验证 [P0]", "details": ["前置条件: 类型2用户使用幸运礼物", "操作步骤: 多次抽奖并统计各倍数中奖次数", "预期结果: 概率符合类型2配置，合计期望≈1.05"]},
                {"title": "TC-15: 类型3-普通用户奖池概率验证 [P0]", "details": ["前置条件: 类型3用户使用幸运礼物", "操作步骤: 多次抽奖并统计各倍数中奖次数", "预期结果: 概率符合类型3配置，合计期望≈0.87"]}
            ]
        },
        {
            "title": "4. 用户类型切换测试",
            "cases": [
                {"title": "TC-16: 用户从类型0切换到类型3 [P0]", "details": ["前置条件: 类型0用户参与超过20次或消费超14000金币", "操作步骤: 继续使用幸运礼物", "预期结果: 用户类型切换为类型3"]},
                {"title": "TC-17: 用户从类型3切换到类型1 [P0]", "details": ["前置条件: 类型3用户7天内有效次数≥150且ROI达标", "操作步骤: 继续使用幸运礼物", "预期结果: 用户类型切换为类型1"]},
                {"title": "TC-18: 用户从类型3切换到类型2 [P0]", "details": ["前置条件: 类型3用户7天内有效次数≥150且ROI达标亏损", "操作步骤: 继续使用幸运礼物", "预期结果: 用户类型切换为类型2"]},
                {"title": "TC-19: 用户从类型1切换回类型3 [P0]", "details": ["前置条件: 类型1用户7天数据不再满足盈利条件", "操作步骤: 继续使用幸运礼物", "预期结果: 用户类型切换为类型3"]},
                {"title": "TC-20: 用户从类型2切换回类型3 [P0]", "details": ["前置条件: 类型2用户7天数据不再满足亏损条件", "操作步骤: 继续使用幸运礼物", "预期结果: 用户类型切换为类型3"]}
            ]
        },
        {
            "title": "5. ROI计算验证测试",
            "cases": [
                {"title": "TC-21: ROI计算公式验证-正常情况 [P0]", "details": ["前置条件: 用户有抽奖记录", "操作步骤: 计算ROI = 返还金币 / 消耗金币", "预期结果: ROI计算正确"]},
                {"title": "TC-22: ROI边界值-95%*150%阈值验证 [P0]", "details": ["前置条件: 用户ROI在阈值附近", "操作步骤: 验证类型判断是否准确", "预期结果: 符合阈值判断"]},
                {"title": "TC-23: ROI边界值-96%*60%阈值验证 [P0]", "details": ["前置条件: 用户ROI在阈值附近", "操作步骤: 验证类型判断是否准确", "预期结果: 符合阈值判断"]}
            ]
        },
        {
            "title": "6. 统计报表功能测试",
            "cases": [
                {"title": "TC-24: 0池统计数据验证 [P0]", "details": ["前置条件: 有类型0用户参与", "操作步骤: 查看报表-0池数据", "预期结果: 人数、次数、消耗、返还、返奖率正确"]},
                {"title": "TC-25: 1池统计数据验证 [P0]", "details": ["前置条件: 有类型1用户参与", "操作步骤: 查看报表-1池数据", "预期结果: 人数、次数、消耗、返还、返奖率正确"]},
                {"title": "TC-26: 2池统计数据验证 [P0]", "details": ["前置条件: 有类型2用户参与", "操作步骤: 查看报表-2池数据", "预期结果: 人数、次数、消耗、返还、返奖率正确"]},
                {"title": "TC-27: 3池统计数据验证 [P0]", "details": ["前置条件: 有类型3用户参与", "操作步骤: 查看报表-3池数据", "预期结果: 人数、次数、消耗、返还、返奖率正确"]},
                {"title": "TC-28: 整体返奖率验证 [P0]", "details": ["前置条件: 有所有类型用户参与", "操作步骤: 查看报表-整体数据", "预期结果: 整体返奖率=总返还/总消耗，≤97%"]},
                {"title": "TC-29: 按日期统计数据验证 [P1]", "details": ["前置条件: 选择不同日期", "操作步骤: 查看不同日期的统计数据", "预期结果: 各日期数据准确"]}
            ]
        },
        {
            "title": "7. 边界场景与异常测试",
            "cases": [
                {"title": "TC-30: 整体投产上限控制-≥97% [P0]", "details": ["前置条件: 整体返奖率接近97%", "操作步骤: 继续有用户抽奖", "预期结果: 验证是否有上限控制机制"]},
                {"title": "TC-31: 送礼人随机返奖-87%期望 [P1]", "details": ["前置条件: 大量用户参与", "操作步骤: 统计送礼人返奖", "预期结果: 长期期望≈87%"]},
                {"title": "TC-32: 收礼人固定返奖-10% [P1]", "details": ["前置条件: 收礼人获得礼物", "操作步骤: 验证收礼人返奖", "预期结果: 固定10%返奖"]},
                {"title": "TC-33: 用户切换类型时的抽奖体验 [P1]", "details": ["前置条件: 用户刚好切换类型", "操作步骤: 用户在切换时点抽奖", "预期结果: 抽奖流畅，无异常"]},
                {"title": "TC-34: 大数据量下性能测试 [P2]", "details": ["前置条件: 高并发场景", "操作步骤: 模拟大量用户同时抽奖", "预期结果: 系统响应正常，无延迟或报错"]},
                {"title": "TC-35: 数据一致性验证 [P2]", "details": ["前置条件: 有用户抽奖记录", "操作步骤: 对比用户记录与报表数据", "预期结果: 数据一致"]}
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
