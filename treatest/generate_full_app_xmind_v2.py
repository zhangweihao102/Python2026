import os
import time
import shutil
import zipfile
import xml.etree.ElementTree as ET
import uuid

def create_xmind_file():
    template_path = r"D:\用例文件\端内贵族VIP测试用例.xmind"
    file_path = r"D:\用例文件\语聊APP全量测试用例.xmind"
    temp_dir = r"D:\用例文件\temp_xmind_full_v2"
    
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
        title_elem.text = "语聊APP全量测试用例 (详细版)"
    
    root_topic = sheet.find('./xmind:topic', ns)
    root_title = root_topic.find('./xmind:title', ns)
    if root_title is not None:
        root_title.text = "【语聊APP】全量测试用例 V2.0"
    
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
            "title": "1. 账号与用户体系 (详细)",
            "cases": [
                {"title": "1.1 注册与登录", "details": [
                    "TC: 手机号注册 - 验证码获取频率限制、时效性、格式校验 [P0]",
                    "TC: 手机号登录 - 正常登录、密码错误上限锁定、设备更换提醒 [P0]",
                    "TC: 第三方登录 - Google/Facebook/Apple/Line 授权登录与信息拉取 [P0]",
                    "TC: 第三方登录 - 授权取消或失败时的错误提示与回退逻辑 [P1]",
                    "TC: 游客模式 - 游客限制（不可发言、充值、建房）及转正逻辑 [P1]"
                ]},
                {"title": "1.2 个人资料管理", "details": [
                    "TC: 头像上传 - 相册选择/拍照、图片裁剪、大小限制、敏感图审核 [P1]",
                    "TC: 昵称修改 - 长度限制(1-15字符)、特殊符号支持、敏感词拦截、修改频率限制 [P1]",
                    "TC: 基本信息 - 性别(一旦设定不可改/可改一次)、生日(星座自动计算)、地区、个性签名限制 [P1]",
                    "TC: 资料展示 - 本人主页与他人视角主页展示差异验证 [P2]"
                ]},
                {"title": "1.3 账号安全与风控", "details": [
                    "TC: 账号绑定/解绑 - 手机号换绑、三方账号绑定与解绑逻辑 [P0]",
                    "TC: 账号注销 - 15天/30天冷却期计算、注销期间数据隐藏、注销后悔机制 [P0]",
                    "TC: 黑名单机制 - 加入黑名单后（不可私聊、看不到动态、不能进同一个房） [P0]",
                    "TC: 设备风控 - 同设备多开、频繁注册、模拟器登录识别与拦截 [P1]"
                ]}
            ]
        },
        {
            "title": "2. 语音房核心功能 (详细)",
            "cases": [
                {"title": "2.1 房间创建与设置", "details": [
                    "TC: 创建房间 - 房间名敏感词、房间标签/分类选择、网络封面上传 [P0]",
                    "TC: 房间模式 - 语聊模式、K歌模式、交友模式、游戏模式的切换与差异 [P1]",
                    "TC: 房间加密 - 设置4-6位数字密码、密码验证错误上限、房主取消密码 [P0]",
                    "TC: 房间公告 - 公告字数限制、滚动播放速度、修改后实时下发 [P1]",
                    "TC: 房间背景 - 静态图/动态背景(MP4/SVGA)切换、全麦位适配 [P2]"
                ]},
                {"title": "2.2 麦位操作与权限", "details": [
                    "TC: 上下麦 - 用户主动申请/自由上麦、房主抱麦/踢麦下位、断网自动掉麦 [P0]",
                    "TC: 麦位控制 - 闭麦(自己禁音)、封麦(房主禁该麦位)、锁麦(不允许上麦) [P0]",
                    "TC: 麦位展示 - 上麦波纹动效(有人说话时)、麦克风状态图标实时同步 [P1]",
                    "TC: 管理员权限 - 房主设置/取消管理员、管理员权限边界（不可解散房间、可踢人等） [P0]"
                ]},
                {"title": "2.3 音视频底层质量", "details": [
                    "TC: 音质测试 - 多人(8-12人)同时讲话混音、回声消除(AEC)、降噪(ANS) [P0]",
                    "TC: 网络切换 - 4G/5G/WiFi切换不掉线、弱网(丢包率20%)下的声音连贯性 [P0]",
                    "TC: 后台保活 - APP退至后台、锁屏状态下能持续听见声音且麦克风收音正常 [P0]",
                    "TC: 冲突处理 - 语聊中接听系统电话/微信语音，挂断后语音流自动恢复 [P1]"
                ]}
            ]
        },
        {
            "title": "3. 互动与聊天系统 (详细)",
            "cases": [
                {"title": "3.1 房间公屏聊天", "details": [
                    "TC: 文本消息 - 最大字符限制、空格处理、URL防诱导点击拦截、敏感词变*** [P0]",
                    "TC: 表情/图片 - 默认Emoji、动态表情(GIF/SVGA)、相册选图发送及大图预览 [P1]",
                    "TC: 进房提示 - 进房欢迎语(不同等级VIP不同样式)、高等级进房全服跑马灯 [P1]",
                    "TC: 公屏滚屏 - 新消息自动到底部、向上滑动查看历史时暂停自动滚动 [P2]"
                ]},
                {"title": "3.2 IM 私聊功能", "details": [
                    "TC: 消息类型 - 文本、语音条(最长60s、上滑取消)、图片、礼物消息 [P0]",
                    "TC: 状态同步 - 发送中/发送成功/失败红叹号、已读/未读状态实时更新 [P0]",
                    "TC: 离线消息 - 对方离线时的消息缓存，上线后漫游消息拉取完整性 [P1]",
                    "TC: 防骚扰 - 陌生人私聊条数限制、防欺诈提示框、仅接收关注人消息设置 [P0]"
                ]}
            ]
        },
        {
            "title": "4. 礼物与经济系统 (详细)",
            "cases": [
                {"title": "4.1 充值与金币", "details": [
                    "TC: 内购(IAP/GP) - 正常拉起支付、支付成功金币到账、汇率转换正确 [P0]",
                    "TC: 异常支付 - 支付中途取消、支付成功但网络断开导致的回调失败 [P0]",
                    "TC: 补单机制 - 杀进程重启APP、重新进入充值页时的漏单补发测试 [P0]",
                    "TC: 第三方支付 - 印度UPI/中东本地支付跳转、回调延迟时的状态展示 [P1]"
                ]},
                {"title": "4.2 礼物打赏与动效", "details": [
                    "TC: 礼物发送 - 单发、选择数量发送(x10, x66, x99)、全麦打赏(一键送全麦) [P0]",
                    "TC: 动效展示 - SVGA/MP4 高级礼物全屏播放，多个高价值礼物排队播放逻辑 [P0]",
                    "TC: 连击功能 - 礼物连击(Combo)计时器，连击UI展示与金币连续扣除准确性 [P1]",
                    "TC: 并发打赏 - 房间内多人同时送礼时，消息通道防阻塞、动效不卡死 [P1]"
                ]},
                {"title": "4.3 幸运礼物与奖池", "details": [
                    "TC: 盲盒/抽奖 - 单抽/十连抽金币扣除、库存/背包物品增加准确性 [P0]",
                    "TC: 奖池逻辑 - 大奖爆出全服横幅跑马灯、分层奖池（新用户池/亏损池）命中概率 [P0]",
                    "TC: 背包系统 - 收到碎片合成完整物品、背包礼物过期倒计时清理、从背包送礼 [P1]"
                ]}
            ]
        },
        {
            "title": "5. 榜单与等级特权 (详细)",
            "cases": [
                {"title": "5.1 等级与经验值", "details": [
                    "TC: 财富等级 - 消费金币增加经验值、跨级升级动效展示、对应等级勋章解锁 [P0]",
                    "TC: 魅力/活跃等级 - 收礼增加魅力值、每日在线时长增加活跃度，数值准确性 [P1]",
                    "TC: 特权验证 - 达到特定等级解锁防踢、隐身进房、专属进场特效 [P0]"
                ]},
                {"title": "5.2 排行榜系统", "details": [
                    "TC: 榜单分类 - 日榜/周榜/月榜切换，财富榜/魅力榜/房间榜数据隔离 [P0]",
                    "TC: 数据刷新 - 送礼后榜单排名实时/准实时(缓存5分钟)变化验证 [P0]",
                    "TC: 边界显示 - 榜单前3名特殊UI、未上榜用户的“未上榜/距上一名差X金币”提示 [P1]"
                ]},
                {"title": "5.3 贵族/VIP系统", "details": [
                    "TC: VIP开通与续费 - 首次开通价格、到期自动降级、续费叠加有效期 [P0]",
                    "TC: VIP特权 - 专属客服、聊天气泡、专属礼物折扣、防禁言特权实际生效情况 [P0]"
                ]}
            ]
        },
        {
            "title": "6. 社交、动态与匹配 (详细)",
            "cases": [
                {"title": "6.1 动态/朋友圈", "details": [
                    "TC: 发布动态 - 纯文本/图文/语音/视频动态发布，上传进度及失败重试 [P1]",
                    "TC: 互动操作 - 点赞/取消点赞、评论(盖楼)、分享动态到三方/房间内 [P1]",
                    "TC: 列表刷新 - 关注流/推荐流下拉刷新、上拉加载更多(分页)、屏蔽某人动态 [P2]"
                ]},
                {"title": "6.2 语音匹配/交友", "details": [
                    "TC: 1V1 匹配 - 点击匹配、动画展示、匹配成功后的 RTC 建立及倒计时 [P0]",
                    "TC: 匹配策略 - 异性优先匹配、同城优先匹配算法准确性验证 [P1]",
                    "TC: 匹配异常 - 匹配中途取消、匹配成功对方挂断、无匹配对象时的超时提示 [P1]"
                ]},
                {"title": "6.3 家族/公会", "details": [
                    "TC: 家族管理 - 创建条件(等级/金币限制)、族长审批成员、设置副族长、踢人 [P1]",
                    "TC: 家族任务 - 每日打卡、流水任务进度条更新、达标后发放宝箱奖励 [P2]",
                    "TC: 家族PK - 家族战(PK)期间积分条变化、胜负结算与惩罚动效 [P1]"
                ]}
            ]
        },
        {
            "title": "7. 客户端性能、兼容与安全 (详细)",
            "cases": [
                {"title": "7.1 兼容性与适配", "details": [
                    "TC: 系统版本 - Android(10-14)、iOS(14-17) 核心主流程无阻断 [P0]",
                    "TC: 屏幕适配 - 挖孔屏/刘海屏沉浸式状态栏不遮挡、折叠屏展开/合上UI自适应 [P0]",
                    "TC: 语言与本地化 - 阿语(RTL从右到左排版)、印地语/英语超长文本UI不截断 [P0]"
                ]},
                {"title": "7.2 性能与资源消耗", "details": [
                    "TC: CPU/内存 - 满麦房间持续播放动效30分钟，内存增长在合理范围，无OOM [P0]",
                    "TC: 耗电与发热 - 连麦1小时耗电量与主流竞品对比，机身不严重发烫降频 [P1]",
                    "TC: 流畅度(FPS) - 房间内多礼物狂刷时滑动公屏的帧率(FPS > 45) [P1]"
                ]},
                {"title": "7.3 权限与Push系统", "details": [
                    "TC: 权限申请 - 首次使用麦克风/相册时的系统弹窗，拒绝后的二次合理引导 [P0]",
                    "TC: 离线推送(Push) - 杀掉APP后，接收私聊消息能正常弹出系统通知栏 [P0]",
                    "TC: 唤醒跳转 - 点击Push通知能精准跳转到对应私聊页/语音房 [P0]"
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
