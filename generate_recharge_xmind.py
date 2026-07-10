import os
import time
import shutil
import zipfile
import xml.etree.ElementTree as ET
import uuid

def create_xmind_file():
    template_path = r"D:\用例文件\端内贵族VIP测试用例.xmind"
    file_path = r"D:\用例文件\充值套餐展示列表优化测试用例.xmind"
    temp_dir = r"D:\用例文件\temp_recharge"
    
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
        title_elem.text = "充值套餐测试用例"
    
    root_topic = sheet.find('./xmind:topic', ns)
    root_title = root_topic.find('./xmind:title', ns)
    if root_title is not None:
        root_title.text = "【优化】充值套餐展示列表测试用例"
    
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
            "title": "1. 管理后台配置功能测试",
            "cases": [
                {"title": "TC-01: 附加信息文案配置-新增 [P0]", "details": ["前置条件: 登录管理后台", "操作步骤: 为套餐配置附加信息文案", "预期结果: 配置成功，保存后生效"]},
                {"title": "TC-02: 附加信息文案配置-修改 [P0]", "details": ["前置条件: 套餐已有附加信息文案", "操作步骤: 修改附加信息文案内容", "预期结果: 修改成功，立即生效"]},
                {"title": "TC-03: 附加信息文案配置-删除/清空 [P0]", "details": ["前置条件: 套餐已有附加信息文案", "操作步骤: 清空附加信息文案", "预期结果: 清空成功，前端不再展示"]},
                {"title": "TC-04: 购买次数上限配置-新增 [P0]", "details": ["前置条件: 登录管理后台", "操作步骤: 为套餐配置购买次数上限", "预期结果: 配置成功，保存后生效"]},
                {"title": "TC-05: 购买次数上限配置-修改 [P0]", "details": ["前置条件: 套餐已有购买次数上限", "操作步骤: 修改购买次数上限值", "预期结果: 修改成功，立即生效"]},
                {"title": "TC-06: 购买次数上限配置-删除/清空 [P0]", "details": ["前置条件: 套餐已有购买次数上限", "操作步骤: 清空购买次数上限", "预期结果: 清空成功，取消此限制"]},
                {"title": "TC-07: 多国家/多App配置-Woho [P1]", "details": ["前置条件: 管理后台支持多App", "操作步骤: 为Woho配置套餐", "预期结果: 配置正确应用到Woho"]},
                {"title": "TC-08: 多国家/多App配置-Sofun [P1]", "details": ["前置条件: 管理后台支持多App", "操作步骤: 为Sofun配置套餐", "预期结果: 配置正确应用到Sofun"]},
                {"title": "TC-09: 不同货币套餐配置-美元 [P1]", "details": ["前置条件: 管理后台支持多货币", "操作步骤: 配置美元套餐", "预期结果: 美元套餐配置正确"]},
                {"title": "TC-10: 不同货币套餐配置-印度卢比 [P1]", "details": ["前置条件: 管理后台支持多货币", "操作步骤: 配置印度卢比套餐", "预期结果: 印度卢比套餐配置正确"]}
            ]
        },
        {
            "title": "2. 附加信息文案展示测试",
            "cases": [
                {"title": "TC-11: 有附加信息文案-展示验证 [P0]", "details": ["前置条件: 套餐已配置附加信息文案", "操作步骤: 用户进入充值页面", "预期结果: 展示辅助信息色块+文案"]},
                {"title": "TC-12: 无附加信息文案-不展示验证 [P0]", "details": ["前置条件: 套餐未配置附加信息文案", "操作步骤: 用户进入充值页面", "预期结果: 该位置留空，不展示任何内容"]},
                {"title": "TC-13: 修改文案后-实时更新验证 [P0]", "details": ["前置条件: 修改了附加信息文案", "操作步骤: 用户刷新/重新进入充值页面", "预期结果: 展示最新文案内容"]},
                {"title": "TC-14: 全局展示验证-所有用户可见 [P0]", "details": ["前置条件: 套餐已配置附加信息文案", "操作步骤: 不同用户查看该套餐", "预期结果: 所有用户都能看到相同文案"]},
                {"title": "TC-15: 样式展示验证-辅助信息色块 [P1]", "details": ["前置条件: 套餐已配置附加信息文案", "操作步骤: 查看UI展示", "预期结果: 辅助信息色块样式符合Demo要求"]}
            ]
        },
        {
            "title": "3. 购买次数上限展示测试",
            "cases": [
                {"title": "TC-16: 有购买次数上限-展示在队首 [P0]", "details": ["前置条件: 套餐已配置购买次数上限", "操作步骤: 用户进入充值页面", "预期结果: 该套餐展示于套餐列表队首"]},
                {"title": "TC-17: 无购买次数上限-不特殊展示 [P0]", "details": ["前置条件: 套餐未配置购买次数上限", "操作步骤: 用户进入充值页面", "预期结果: 按正常排序展示"]},
                {"title": "TC-18: 购买次数未达上限-套餐正常展示 [P0]", "details": ["前置条件: 用户购买次数 < 上限", "操作步骤: 用户查看充值套餐", "预期结果: 套餐正常展示"]},
                {"title": "TC-19: 购买次数达到上限-套餐消失 [P0]", "details": ["前置条件: 用户购买次数 = 上限", "操作步骤: 用户查看充值套餐", "预期结果: 该套餐从列表中消失"]},
                {"title": "TC-20: 购买次数超过上限-套餐消失 [P0]", "details": ["前置条件: 用户购买次数 > 上限", "操作步骤: 用户查看充值套餐", "预期结果: 该套餐从列表中消失"]},
                {"title": "TC-21: 修改上限后-展示逻辑更新 [P0]", "details": ["前置条件: 修改了购买次数上限", "操作步骤: 用户刷新/重新进入充值页面", "预期结果: 按新上限判断展示"]}
            ]
        },
        {
            "title": "4. 购买次数上限用户判定测试",
            "cases": [
                {"title": "TC-22: 每个用户单独判定-用户A达上限 [P0]", "details": ["前置条件: 用户A购买次数达上限，用户B未达上限", "操作步骤: 用户A和用户B分别查看", "预期结果: 用户A看不到套餐，用户B能看到"]},
                {"title": "TC-23: 每个用户单独判定-用户B未达上限 [P0]", "details": ["前置条件: 用户A购买次数达上限，用户B未达上限", "操作步骤: 用户A和用户B分别查看", "预期结果: 用户A看不到套餐，用户B能看到"]},
                {"title": "TC-24: 新用户-初始次数为0 [P0]", "details": ["前置条件: 新注册用户", "操作步骤: 新用户第一次进入充值页面", "预期结果: 套餐正常展示（次数为0）"]},
                {"title": "TC-25: 购买次数统计-累计计算 [P1]", "details": ["前置条件: 用户多次购买该套餐", "操作步骤: 验证购买次数统计", "预期结果: 次数累计正确"]}
            ]
        },
        {
            "title": "5. 套餐购买流程测试",
            "cases": [
                {"title": "TC-26: 有附加信息套餐-购买流程正常 [P0]", "details": ["前置条件: 套餐有附加信息文案", "操作步骤: 用户完成购买流程", "预期结果: 购买成功，金币到账正确"]},
                {"title": "TC-27: 有购买上限套餐-购买次数未达上限 [P0]", "details": ["前置条件: 用户购买次数 < 上限", "操作步骤: 用户购买该套餐", "预期结果: 购买成功，次数+1"]},
                {"title": "TC-28: 有购买上限套餐-购买次数达上限 [P0]", "details": ["前置条件: 用户购买次数 = 上限", "操作步骤: 用户尝试购买该套餐", "预期结果: 套餐已消失，无法购买"]},
                {"title": "TC-29: 实际到账金币数验证 [P0]", "details": ["前置条件: 用户购买套餐", "操作步骤: 验证到账金币数", "预期结果: 到账 = 标准金币 + 赠送金币"]},
                {"title": "TC-30: 购买次数实时更新验证 [P1]", "details": ["前置条件: 用户刚购买了有上限套餐", "操作步骤: 再次查看套餐列表", "预期结果: 如果达上限则套餐消失"]}
            ]
        },
        {
            "title": "6. 多套餐组合场景测试",
            "cases": [
                {"title": "TC-31: 多个有上限套餐-都展示在队首 [P0]", "details": ["前置条件: 多个套餐都配置了购买上限", "操作步骤: 用户查看充值页面", "预期结果: 所有有上限套餐展示在队首"]},
                {"title": "TC-32: 部分有上限、部分无上限套餐 [P0]", "details": ["前置条件: 混合类型套餐", "操作步骤: 用户查看充值页面", "预期结果: 有上限套餐在队首，无上限套餐在后面"]},
                {"title": "TC-33: 部分有附加信息、部分无附加信息 [P1]", "details": ["前置条件: 混合类型套餐", "操作步骤: 用户查看充值页面", "预期结果: 有配置的展示，无配置的不展示"]},
                {"title": "TC-34: 有上限+有附加信息套餐 [P1]", "details": ["前置条件: 套餐同时配置两项", "操作步骤: 用户查看并购买", "预期结果: 展示在队首且显示附加信息"]}
            ]
        },
        {
            "title": "7. 边界场景与异常测试",
            "cases": [
                {"title": "TC-35: 购买次数上限=1-购买后消失 [P0]", "details": ["前置条件: 套餐上限=1，用户未购买过", "操作步骤: 用户购买一次", "预期结果: 购买后套餐消失"]},
                {"title": "TC-36: 购买次数上限=0-不展示 [P2]", "details": ["前置条件: 套餐上限=0", "操作步骤: 用户查看充值页面", "预期结果: 验证边界值处理"]},
                {"title": "TC-37: 购买次数上限很大值-性能验证 [P2]", "details": ["前置条件: 配置很大的上限值", "操作步骤: 验证系统性能", "预期结果: 系统正常处理"]},
                {"title": "TC-38: 附加信息文案过长-展示验证 [P2]", "details": ["前置条件: 配置很长的附加信息文案", "操作步骤: 查看前端展示", "预期结果: 展示正常，无样式错乱"]},
                {"title": "TC-39: 特殊字符文案-展示验证 [P2]", "details": ["前置条件: 配置含特殊字符的文案", "操作步骤: 查看前端展示", "预期结果: 展示正常，字符正确"]},
                {"title": "TC-40: 清空上限后-套餐回到正常位置 [P1]", "details": ["前置条件: 清空套餐购买上限", "操作步骤: 用户查看充值页面", "预期结果: 套餐回到正常排序位置"]}
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
