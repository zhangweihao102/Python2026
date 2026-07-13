import os
import time
import shutil
import zipfile
import xml.etree.ElementTree as ET
import uuid

def create_xmind_file():
    template_path = r"D:\用例文件\端内贵族VIP测试用例.xmind"
    file_path = r"D:\用例文件\语聊APP全量测试用例.xmind"
    temp_dir = r"D:\用例文件\temp_xmind_full_v3"
    
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
        title_elem.text = "语聊APP全量测试用例 (含游戏模块)"
    
    root_topic = sheet.find('./xmind:topic', ns)
    root_title = root_topic.find('./xmind:title', ns)
    if root_title is not None:
        root_title.text = "【语聊APP】全量测试用例 V3.0 (含游戏)"
    
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
            "title": "1. 账号与用户体系",
            "cases": [
                {"title": "1.1 注册与登录", "details": [
                    "TC: 手机号注册 - 验证码频率限制、格式校验 [P0]",
                    "TC: 第三方登录 - Google/Facebook/Apple 授权登录与失败回退 [P0]",
                    "TC: 游客模式 - 游客限制（不可发言、充值）及转正逻辑 [P1]"
                ]},
                {"title": "1.2 账号安全与资料", "details": [
                    "TC: 个人资料 - 头像敏感图审核、昵称敏感词拦截、他人视角展示 [P1]",
                    "TC: 账号注销 - 冷却期计算、注销期间数据隐藏 [P0]",
                    "TC: 设备风控 - 同设备多开、模拟器登录识别与黑名单限制 [P1]"
                ]}
            ]
        },
        {
            "title": "2. 语音房核心功能",
            "cases": [
                {"title": "2.1 房间与麦位管理", "details": [
                    "TC: 房间设置 - 房间模式切换、密码加密、公告滚动与背景适配 [P0]",
                    "TC: 麦位控制 - 自由上下麦、房主抱/踢/锁/闭麦，断网自动掉麦 [P0]",
                    "TC: 音视频质量 - 混音、回声消除(AEC)、弱网连贯性、后台锁屏保活 [P0]"
                ]}
            ]
        },
        {
            "title": "3. 互动与聊天系统",
            "cases": [
                {"title": "3.1 消息收发", "details": [
                    "TC: 公屏聊天 - 文本拦截、动态表情、高等级进房特效、防诱导URL [P0]",
                    "TC: IM私聊 - 文本/语音条收发、已读未读状态、离线消息漫游拉取 [P0]",
                    "TC: 防骚扰 - 陌生人私聊条数限制、防欺诈提示框 [P0]"
                ]}
            ]
        },
        {
            "title": "4. 礼物与经济系统",
            "cases": [
                {"title": "4.1 充值与打赏", "details": [
                    "TC: 充值系统 - 内购/三方支付、断网掉单与漏单补发机制 [P0]",
                    "TC: 礼物发送 - 单发/连发Combo/全麦打赏，全屏SVGA动效排队播放 [P0]",
                    "TC: 幸运玩法 - 盲盒抽奖概率、分层奖池命中、跑马灯全服广播 [P0]"
                ]}
            ]
        },
        {
            "title": "5. 语聊房游戏模块 (重点补充)",
            "cases": [
                {"title": "5.1 房间游戏入口与面板", "details": [
                    "TC: 游戏入口可见性 - 房主/管理员/上麦者/围观者是否均可见游戏Icon [P0]",
                    "TC: 游戏面板加载 - 首次打开加载速度、游戏列表分类(自研/三方)展示 [P1]",
                    "TC: 权限控制 - 仅房主可开启全局游戏，或允许全员发起邀请 [P0]",
                    "TC: 悬浮与收起 - 游戏面板半屏展示与收起到侧边悬浮窗的切换流畅度 [P1]"
                ]},
                {"title": "5.2 自研游戏 (如：转盘/掷骰子/猜拳/Ludo)", "details": [
                    "TC: 核心玩法闭环 - 房主发起 -> 麦上玩家参与 -> 倒计时结束 -> 展示结果 [P0]",
                    "TC: 状态同步 - 多人视角下的动画同步性，结果是否完全一致无延迟 [P0]",
                    "TC: 异常退出 - 游戏进行中玩家掉线/下麦，该玩家状态处理及游戏是否中断 [P0]",
                    "TC: 资源消耗 - 连续进行多局游戏，观察内存是否泄漏、UI是否卡顿 [P1]",
                    "TC: 麦位联动 - 游戏结果惩罚（如输了自动闭麦1分钟/扣除金币）逻辑生效 [P1]"
                ]},
                {"title": "5.3 三方H5/小游戏 (如：Zego/声网小游戏、外部H5)", "details": [
                    "TC: 容器加载 - WebView/Cocos/Unity容器加载速度，加载失败的降级或重试提示 [P0]",
                    "TC: 账号授权与鉴权 - Token自动获取与传递，免密登入三方游戏大厅 [P0]",
                    "TC: 资产打通 - 使用APP金币兑换游戏币，或直接使用金币下注，流水账单核对 [P0]",
                    "TC: 音频冲突处理 - 三方游戏背景音/音效 与 语聊房麦上语音 的混音测试，避免互相屏蔽 [P0]",
                    "TC: 生命周期管理 - 切换后台、接听电话、杀进程时，H5游戏的暂停、断线重连与结算状态 [P0]"
                ]},
                {"title": "5.4 游戏与房间业务的边界", "details": [
                    "TC: 房主解散房间 - 游戏进行中房主解散房间，游戏强行结算或安全销毁 [P1]",
                    "TC: 全屏礼物遮挡 - 游戏中有人赠送全屏SVGA礼物，动效层级与游戏层级的遮挡关系 [P1]",
                    "TC: 公屏消息同步 - 游戏重大结果（如大赢家）自动发送房间公屏消息验证 [P2]"
                ]}
            ]
        },
        {
            "title": "6. 社交、动态与榜单",
            "cases": [
                {"title": "6.1 榜单与社交", "details": [
                    "TC: 等级与排行榜 - 跨级动效、日周月榜切换与缓存时效 [P0]",
                    "TC: 动态与匹配 - 动态图文发布、1V1匹配算法与中途取消 [P1]",
                    "TC: 家族系统 - 家族审批、流水任务进度更新、家族PK胜负结算 [P1]"
                ]}
            ]
        },
        {
            "title": "7. 客户端性能、兼容与安全",
            "cases": [
                {"title": "7.1 兼容与性能", "details": [
                    "TC: 兼容适配 - 主流Android/iOS机型、阿语RTL排版、折叠屏自适应 [P0]",
                    "TC: 性能与消耗 - 满麦动效防OOM、长耗电对比、礼物狂刷FPS测试 [P0]",
                    "TC: 权限与推送 - 权限拒绝二次引导、杀APP后Push精准跳转唤醒 [P0]"
                ]}
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
