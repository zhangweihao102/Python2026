import os
import time
import shutil
import zipfile
import xml.etree.ElementTree as ET
import uuid

def create_xmind_file():
    template_path = r"D:\用例文件\端内贵族VIP测试用例.xmind"
    file_path = r"D:\用例文件\语聊APP全量测试用例.xmind"
    temp_dir = r"D:\用例文件\temp_xmind_full"
    
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
        title_elem.text = "语聊APP全量测试用例"
    
    root_topic = sheet.find('./xmind:topic', ns)
    root_title = root_topic.find('./xmind:title', ns)
    if root_title is not None:
        root_title.text = "【语聊APP】全量测试用例"
    
    # 清空原有 topics
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
            "title": "1. 登录注册与用户体系",
            "cases": [
                {"title": "TC-01: 登录注册方式 [P0]", "details": ["前置条件: 无", "操作步骤: 测试手机号/验证码登录注册；测试第三方登录（Google/Facebook/Apple）", "预期结果: 均能成功注册及登录，数据落库正确"]},
                {"title": "TC-02: 个人资料管理 [P1]", "details": ["前置条件: 已登录", "操作步骤: 测试头像上传与裁剪；测试昵称修改与敏感词过滤；测试性别、生日等基本信息编辑", "预期结果: 资料更新成功，主页同步展示"]},
                {"title": "TC-03: 账号注销与风控 [P0]", "details": ["前置条件: 已登录", "操作步骤: 测试账号注销流程及冷却期；验证新设备登录风控及拉黑用户限制", "预期结果: 注销期间无法正常使用；被拉黑后无权限操作"]}
            ]
        },
        {
            "title": "2. 语音房核心功能",
            "cases": [
                {"title": "TC-04: 房间创建与管理 [P0]", "details": ["前置条件: 有建房权限", "操作步骤: 测试创建公开/加密房间；测试房间标题、公告修改；设置房间背景", "预期结果: 房间创建成功并能在列表展示，信息修改实时生效"]},
                {"title": "TC-05: 麦位管理 (上/下麦) [P0]", "details": ["前置条件: 在语音房中", "操作步骤: 用户自由上麦/申请上麦；房主抱人上麦/踢人下麦；麦位锁定/解锁/闭麦", "预期结果: 麦位状态变化正确，UI同步刷新"]},
                {"title": "TC-06: 语音与连麦质量 [P0]", "details": ["前置条件: 多人在麦上", "操作步骤: 测试正常语聊延迟与音质；测试断网/弱网下的语音重连；测试后台运行/锁屏时的语音保持", "预期结果: 音质清晰无明显杂音，断网重连顺畅，后台不掉线"]}
            ]
        },
        {
            "title": "3. 互动与消息系统",
            "cases": [
                {"title": "TC-07: 房间公屏聊天 [P1]", "details": ["前置条件: 在语音房中", "操作步骤: 测试发送文本、表情、图片；测试消息敏感词过滤；测试公屏消息滚屏", "预期结果: 消息发送成功，敏感词被替换或拦截，列表滚动正常"]},
                {"title": "TC-08: 私聊(IM)功能 [P0]", "details": ["前置条件: 两个互相加好友或陌生人", "操作步骤: 测试私聊文本、语音、图片收发；测试消息已读/未读状态；测试防骚扰限制", "预期结果: 消息收发即时，状态正确，未关注人触发防骚扰逻辑"]}
            ]
        },
        {
            "title": "4. 礼物与经济系统",
            "cases": [
                {"title": "TC-09: 充值系统 [P0]", "details": ["前置条件: 金币余额不足", "操作步骤: 测试内购流程(Google/Apple)；测试三方支付；验证断网掉单、漏单补发机制", "预期结果: 支付成功后金币实时到账，掉单有补单机制"]},
                {"title": "TC-10: 礼物打赏 [P0]", "details": ["前置条件: 有足够金币，在语音房中", "操作步骤: 测试单发/连发/全麦打赏；测试礼物动效展示（普通/全屏礼物）", "预期结果: 金币正确扣除，礼物动效展示无卡顿，流水记录正确"]},
                {"title": "TC-11: 幸运玩法与背包 [P1]", "details": ["前置条件: 有足够金币", "操作步骤: 测试盲盒/奖池抽奖；验证中奖概率与跑马灯公告；测试背包物品发放与使用", "预期结果: 抽奖逻辑正常，奖品正确放入背包，跑马灯全服广播"]}
            ]
        },
        {
            "title": "5. 社交与关系链",
            "cases": [
                {"title": "TC-12: 关注与粉丝 [P1]", "details": ["前置条件: 浏览他人主页", "操作步骤: 测试关注、取消关注；查看粉丝列表及关注列表", "预期结果: 关注状态实时刷新，列表排序正确"]},
                {"title": "TC-13: 家族/公会系统 [P2]", "details": ["前置条件: 无家族状态", "操作步骤: 测试创建、申请加入、审批、退出家族；测试家族任务与榜单", "预期结果: 家族生命周期流转正常，任务数据统计准确"]}
            ]
        },
        {
            "title": "6. 性能、兼容与APP系统",
            "cases": [
                {"title": "TC-14: 兼容性适配 [P0]", "details": ["前置条件: 不同机型", "操作步骤: 测试主流机型与系统版本（Android 10-14, iOS 15-17）；测试刘海屏/折叠屏适配", "预期结果: UI不重叠不截断，功能均可用"]},
                {"title": "TC-15: 性能与稳定性 [P0]", "details": ["前置条件: 自动化工具/Monkey", "操作步骤: 测试长时间挂机语音房（CPU/内存/耗电）；Monkey压力测试", "预期结果: 无明显发热发烫，无内存泄漏，无Crash/ANR"]},
                {"title": "TC-16: 权限与推送 [P1]", "details": ["前置条件: 新安装APP", "操作步骤: 测试麦克风、相机、相册等权限申请与拒绝；测试APP内推送与系统离线Push", "预期结果: 拒绝权限有合理引导，Push能成功唤起APP"]}
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
