import os
import time
import shutil
import zipfile
import xml.etree.ElementTree as ET
import uuid

def create_xmind_file():
    template_path = r"D:\用例文件\端内贵族VIP测试用例.xmind"
    file_path = r"D:\用例文件\send_gift重构测试用例.xmind"
    temp_dir = r"D:\用例文件\temp_send_gift"
    
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
        title_elem.text = "send_gift重构测试用例"
    
    root_topic = sheet.find('./xmind:topic', ns)
    root_title = root_topic.find('./xmind:title', ns)
    if root_title is not None:
        root_title.text = "send_gift 重构测试用例"
    
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
            "title": "1. P0 功能测试清单",
            "cases": [
                {"title": "TC-01: 单人房间钻石礼物 [P0]", "details": ["操作步骤: 送礼者、收礼者、旁观者同时在线；普通房间送 1 件付费礼物。", "预期结果: 响应、余额、订单、礼物/财务日志一致；3类客户端各仅收1次正确房间广播。"]},
                {"title": "TC-02: 多收件人 + 多数量 [P0]", "details": ["操作步骤: 多人收件、数量大于1，覆盖拆单/拆流水。", "预期结果: 总额=单价×数量×有效收件人数；每位收件人展示、日志及相关收益正确。"]},
                {"title": "TC-03: 背包礼物 [P0]", "details": ["操作步骤: is_rucksack=1，验证库存充足与不足场景。", "预期结果: 库存正确减扣，不重复扣钻石；订单、房间广播与普通礼物协议兼容。"]},
                {"title": "TC-04: 单聊 / 无 room_id [P0]", "details": ["操作步骤: 覆盖单聊、个人通知或非房间来源场景。", "预期结果: 仅目标用户收到个人消息；不得误广播到旧房间或空房间。"]},
                {"title": "TC-05: 多终端与离线 [P0]", "details": ["操作步骤: 收件人分别 app、client、web 在线；再测试无连接/断线中场景。", "预期结果: 在线端正确路由；离线不导致 consumer 卡死、异常重试或阻塞后续消息。"]},
                {"title": "TC-06: 礼物广播字段 [P0]", "details": ["操作步骤: 验证 child_action=gift、comboFinish、品牌、贵族、VIP、勋章等字段。", "预期结果: 字段存在性、类型和值与旧客户端兼容；comboFinish的字符串化语义不变。"]},
                {"title": "TC-07: 房型及队列路由 [P0]", "details": ["操作步骤: 普通、直播、元宇宙等实际已启用房型各测 1 次。", "预期结果: 进入预期 Redis List，目标房间正确收包，不跨房下发。"]},
                {"title": "TC-08: 幸运礼物 [P0]", "details": ["操作步骤: 覆盖 g_type=37 的中奖、房间通知及全局通知。", "预期结果: 订单前缀、中奖结果、通知范围正确；失败演练符合“3次retry后dead”规则。"]},
                {"title": "TC-09: 大范围 / 全服通知 [P0]", "details": ["操作步骤: 触发需要多房间 fanout 的礼物场景。", "预期结果: IM每轮最多200房间、heavy continuation续批；无漏房、重房、长期阻塞普通房间消息。"]},
                {"title": "TC-10: 重复请求 [P0]", "details": ["操作步骤: 同 uid 并发点击、网络超时后重试、相同业务订单号重放。", "预期结果: 发送锁和幂等保护生效：无双扣、双单、双广播、重复 showlove/PK 等副作用。"]}
            ]
        },
        {
            "title": "2. 参数、业务与协议边界测试",
            "cases": [
                {"title": "TC-11: 数量 number 边界", "details": ["操作步骤: 覆盖空、0、负数、非数字、1、9999、10000。", "预期结果: 当前校验上限为 9999；非法输入不可产生订单、扣费或消息。"]},
                {"title": "TC-12: 收件人 pw_uid 边界", "details": ["操作步骤: 覆盖空、无效 uid、重复 uid、多人、本人、注销冷静期、神秘用户。", "预期结果: 人数、金额、可见性与错误码正确；不允许的关系不得绕过校验。"]},
                {"title": "TC-13: 礼物与权限边界", "details": ["操作步骤: 覆盖不存在/关闭、免费礼物、多收件人免费、金豆、背包、房间限制、守护、CP/漫游等级。", "预期结果: 免费礼物仅单收件人；购买限制、房间限制和账户状态全部在扣费前拦截。"]},
                {"title": "TC-14: 礼物红包边界", "details": ["操作步骤: 覆盖 red_packet_order_id 缺失、重复送、多人、错收件人、自己送自己、礼物或数量不匹配。", "预期结果: 关系、单人限制、订单关联严格一致，不可重复领取或错配。"]},
                {"title": "TC-15: 来源与扩展字段边界", "details": ["操作步骤: 覆盖 source、source_model、click_from、business_orderid、is_all_mic、涂鸦/抽奖/红包字段。", "预期结果: iOS的source=5覆盖逻辑、聊天室/单聊来源、旧字段兼容不回归。"]},
                {"title": "TC-16: 资金边界", "details": ["操作步骤: 覆盖余额刚好、少1、支付账户异常、收件人账户异常、优惠券、多人+多数量。", "预期结果: 金额计算、余额指纹、流水及失败回滚一致；任何失败均不可留下半成品订单。"]},
                {"title": "TC-17: 文本与 JSON 边界", "details": ["操作步骤: 覆盖 gift_tips 含 emoji、引号、脚本字符、超长文本；graffiti_img_id、draw_process。", "预期结果: 接口、Redis payload 与 Socket JSON 不解析失败、不截断协议、不产生前端注入风险。"]}
            ]
        },
        {
            "title": "3. 异步故障演练",
            "cases": [
                {"title": "TC-18: Kaihei 通用送礼 consumer 故障", "details": ["操作步骤: 暂停后发礼物，观察队列积压；恢复后检查衍生业务。", "预期结果: 主送礼资金语义不变；队列可恢复消费，最终结果不重复、不遗漏。"]},
                {"title": "TC-19: IM 房间 consumer 故障", "details": ["操作步骤: 暂停 RoomPushQueueConsumerProcess，发同房间/跨房间礼物；记录队列。", "预期结果: Redis List增长符合发送量，恢复后drain；同房间顺序和房间隔离正确。"]},
                {"title": "TC-20: IM task worker 或 handler 异常", "details": ["操作步骤: 制造 task 投递失败或 handler 失败，观察 reliable pending/processing/retry/dead。", "预期结果: 可靠任务按处理策略可恢复或入dead；无无限循环、无静默丢失。"]},
                {"title": "TC-21: 幸运通知失败演练", "details": ["操作步骤: 仅针对 luck_gift_award_send_notice 连续制造失败。", "预期结果: 最多3次重试，第4次进入_dead；中奖资金结果不被重复执行。"]},
                {"title": "TC-22: Redis 断开或慢响应演练", "details": ["操作步骤: 在 Kaihei RPUSH 与 IM BLPOP/task 投递阶段分别注入短暂异常。", "预期结果: 无进程忙等、持续重启；恢复后可按order_id定位链路状态。普通礼物不要求自动重投。"]},
                {"title": "TC-23: 全服 fanout 中断演练", "details": ["操作步骤: 在大量房间续批期间制造 worker 中断。", "预期结果: heavy queue 状态可观测；恢复后无大量普通任务饥饿，按实际策略核对漏/重。"]}
            ]
        },
        {
            "title": "4. 压测方案",
            "cases": [
                {"title": "TC-24: 压测-热房间", "details": ["操作步骤: 同一 room_id、大量在线旁观者、连续礼物/连击。", "预期结果: 同房间保序、combo正确、单个Redis List与单房fanout无延迟长尾。"]},
                {"title": "TC-25: 压测-多房间均匀", "details": ["操作步骤: 大量 room_id 均匀发礼物。", "预期结果: Kaihei通用队列4个分片分布、IM各队列负载均衡、无单分片长期积压。"]},
                {"title": "TC-26: 压测-同 uid 高并发", "details": ["操作步骤: 同一送礼者多线程重试，同时混入不同 uid。", "预期结果: 用户锁、余额与订单幂等；重点统计双扣/重复广播为 0。"]},
                {"title": "TC-27: 压测-多人 + 大数量", "details": ["操作步骤: 多收件人，number取高值但不超过9999。", "预期结果: 数据库写放大、金额计算、订单/流水完整性、API P99正常。"]},
                {"title": "TC-28: 压测-全局广播", "details": ["操作步骤: 触发多房间/全服通知的大额或活动礼物。", "预期结果: 200房间分批与heavy continuation正常；普通房间消息不被拖慢。"]},
                {"title": "TC-29: 压测-幸运礼物高频", "details": ["操作步骤: 持续触发中奖与通知。", "预期结果: 中奖通知 retry/dead、通知重复数、队列回落、资金结果一致。"]},
                {"title": "TC-30: 压测-稳态运行", "details": ["操作步骤: 混合真实比例的房间、单聊、背包、普通/幸运礼物，持续30-60分钟。", "预期结果: Redis、MySQL、Swoole内存和FD无持续爬升，consumer无异常重启。"]}
            ]
        },
        {
            "title": "5. 上线前阻断项与指标核对",
            "cases": [
                {"title": "TC-31: 资金与订单一致性核对", "details": ["操作步骤: 验证所有压测与演练中的金额、数量、收件人数、订单/日志数量相符。", "预期结果: 绝对不允许双扣、双单、金额差异、库存错误。"]},
                {"title": "TC-32: 消息下发一致性核对", "details": ["操作步骤: 验证目标端各收到一次，字段与客户端协议兼容。", "预期结果: 绝对不允许丢消息、重复消息、错房间/错用户、字段类型变化。"]},
                {"title": "TC-33: 异步稳定性核对", "details": ["操作步骤: 验证消费恢复后队列回落；验证 retry/dead 状态。", "预期结果: 绝对不允许持续积压、消费者退出、死信增长无处置。"]},
                {"title": "TC-34: 业务副作用幂等性核对", "details": ["操作步骤: 验证 showlove、usercp、房间 PK、首送记录、幸运礼物通知等执行次数。", "预期结果: 绝对不允许重复计数、错序、失败重放造成业务重复。"]}
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
