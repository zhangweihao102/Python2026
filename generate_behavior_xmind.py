import xmind
import os

def create_xmind_file():
    file_path = r"D:\用例文件\新注册用户行为路径红包测试用例.xmind"
    
    if os.path.exists(file_path):
        os.remove(file_path)
        
    workbook = xmind.load(file_path)
    sheet = workbook.getPrimarySheet()
    sheet.setTitle("行为红包测试用例")
    
    root_topic = sheet.getRootTopic()
    root_topic.setTitle("新注册用户-行为路径&红包")

    data = [
        {
            "title": "1. UI与基础元素测试 (模块重点)",
            "cases": [
                {"title": "TC-01: 领取前弹窗UI核对 [P1]", "details": ["前置条件: 触发任意红包场景", "操作: 观察领取前弹窗", "预期: 头像/昵称官方标识，对应文案，含领取和关闭按钮"]},
                {"title": "TC-02: 领取后弹窗UI核对 [P1]", "details": ["前置条件: 点击领取", "操作: 观察领取后弹窗", "预期: 动效展示，千分位金币数，可直接消费提示"]},
                {"title": "TC-03: 跳转交互测试 [P2]", "details": ["前置条件: 已领取状态", "操作: 点击跳转提示", "预期: 成功跳转金币记录页"]}
            ]
        },
        {
            "title": "2. 九大场景触发逻辑测试",
            "cases": [
                {"title": "TC-04: 场景一 - 完成注册进入App [P0]", "details": ["操作: 注册后进App等1s", "预期: 文案Welcome，领100~300金币，限1次"]},
                {"title": "TC-05: 场景二 - 首次进入房间 [P0]", "details": ["操作: 首次进房等5s", "预期: 文案explore party，领100~400金币，限1次"]},
                {"title": "TC-06: 场景三 - 首次在房间内上麦 [P0]", "details": ["操作: 首次上麦", "预期: 文案first voice chat，领100~600金币，限1次"]},
                {"title": "TC-07: 场景四 - 首次房间内发公屏 [P0]", "details": ["操作: 首次发公屏", "预期: 文案first say hi，领100~200金币，限1次"]},
                {"title": "TC-08: 场景五 - 首次订阅房间 [P0]", "details": ["操作: 首次订阅房间", "预期: 文案following Party，固定领100金币，限1次"]},
                {"title": "TC-09: 场景六 - 首次关注任意用户 [P0]", "details": ["操作: 首次关注用户", "预期: 文案following 1 friend，固定领100金币，限1次"]},
                {"title": "TC-10: 场景七 - 首次拉起游戏面板 [P1]", "details": ["操作: 首次打开游戏面板", "预期: 文案game play，领100~400金币，限1次"]},
                {"title": "TC-11: 场景七 - 首次完成游戏投注 [P1]", "details": ["操作: 首次投注", "预期: 文案game play，领300~1100金币，限1次"]},
                {"title": "TC-12: 场景八 - 新增用户次日回流 [P0]", "details": ["操作: 注册次日回流等1s", "预期: 文案Welcome back，领120~600金币。与签到冲突时优先红包"]},
                {"title": "TC-13: 场景九 - 首次收到礼物 [P0]", "details": ["操作: 首次收到付费礼物", "预期: 文案receive gift，领50~220金币，限1次"]}
            ]
        },
        {
            "title": "3. 防刷与机制限制 (安全重点)",
            "cases": [
                {"title": "TC-14: 硬件指纹限制 [P0]", "details": ["操作: 同一IMEI切换新账号触发", "预期: 触发【静默失效】(不下发不展示不报错)"]},
                {"title": "TC-15: 模拟器与多开环境检测 [P0]", "details": ["操作: 在模拟器/Root/多开环境触发", "预期: 触发【静默失效】"]},
                {"title": "TC-16: IP聚集度限制 [P1]", "details": ["操作: 同IP段1小时内超阈值后触发", "预期: 触发【静默失效】"]},
                {"title": "TC-17: 每日红包总上限限制 [P1]", "details": ["操作: 当日累计下发达后台上限后触发", "预期: 触发【静默失效】"]}
            ]
        },
        {
            "title": "4. 数据统计测试",
            "cases": [
                {"title": "TC-18: 核心字段与多维度统计核对 [P1]", "details": ["操作: 多端多包名下触发红包", "预期: 按包名、端统计金币发放总数与发放总人数准确"]},
                {"title": "TC-19: 九大场景明细统计核对 [P1]", "details": ["操作: 九大场景触发并领取", "预期: 注册/进房/上麦等9个场景对应的发放金币数和人数均准确"]}
            ]
        },
        {
            "title": "5. 边界与异常测试",
            "cases": [
                {"title": "TC-20: 弹窗阻断与重入 [P1]", "details": ["操作: 弹窗未领取直接关闭", "预期: 需确认是否允许再次触发闭环"]},
                {"title": "TC-21: 金币入账核对 [P0]", "details": ["操作: 领取成功后查明细", "预期: 余额增加，流水明细清晰标注类型"]},
                {"title": "TC-22: 非平台发放红包区分 [P2]", "details": ["操作: 领取普通用户红包", "预期: 头像昵称展示真实用户，不可展示官方标识"]}
            ]
        }
    ]

    for module in data:
        module_topic = root_topic.addSubTopic()
        module_topic.setTitle(module["title"])
        for case in module["cases"]:
            case_topic = module_topic.addSubTopic()
            case_topic.setTitle(case["title"])
            for detail in case["details"]:
                detail_topic = case_topic.addSubTopic()
                detail_topic.setTitle(detail)

    xmind.save(workbook, file_path)

if __name__ == "__main__":
    create_xmind_file()
