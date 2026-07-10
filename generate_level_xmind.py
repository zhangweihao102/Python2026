import xmind
import os

def create_xmind_file():
    file_path = r"D:\用例文件\端内活跃等级测试用例.xmind"
    
    if os.path.exists(file_path):
        os.remove(file_path)
        
    workbook = xmind.load(file_path)
    sheet = workbook.getPrimarySheet()
    sheet.setTitle("活跃等级测试用例")
    
    root_topic = sheet.getRootTopic()
    root_topic.setTitle("端内活跃等级 (荣誉&魅力)")

    data = [
        {
            "title": "1. 荣誉等级(消费者) Exp提升测试",
            "cases": [
                {"title": "TC-01: 金币消费提升Exp [P0]", "details": ["操作: 消费金币", "预期: 1 Coins = 1 Exp，无上限"]},
                {"title": "TC-02: 金币充值提升Exp [P0]", "details": ["操作: 充值金币", "预期: 10 Coins = 1 Exp，无上限"]},
                {"title": "TC-03: 进入房间提升Exp及上限 [P1]", "details": ["操作: 连续进入不同房间", "预期: 每次+1 Exp，达到20次后触发日上限不再增加"]},
                {"title": "TC-04: 分享房间提升Exp及上限 [P1]", "details": ["操作: 连续分享房间", "预期: 每次+2 Exp，达到10次后触发日上限(20Exp)不再增加"]}
            ]
        },
        {
            "title": "2. 魅力等级(生产者) Exp提升测试",
            "cases": [
                {"title": "TC-05: 获得钻石提升Exp [P0]", "details": ["操作: 收到打赏获得钻石", "预期: 1 Coins/钻石 = 1 Exp，无上限"]},
                {"title": "TC-06: 麦上时间提升Exp及上限 [P1]", "details": ["操作: 在麦上持续停留", "预期: 每1min+10 Exp，累计20min后触发日上限(200Exp)不再增加"]},
                {"title": "TC-07: 发布动态提升Exp及上限 [P1]", "details": ["操作: 连续发布动态", "预期: 每条+5 Exp，累计发布4条后触发日上限(20Exp)不再增加"]}
            ]
        },
        {
            "title": "3. 升级机制与通知测试",
            "cases": [
                {"title": "TC-08: 经验值跨级溢出处理 [P0]", "details": ["操作: 处于临界点时获得大额Exp", "预期: 支持连续跨级，剩余经验值准确计入新等级进度条"]},
                {"title": "TC-09: 荣誉等级晋级官方消息 [P0]", "details": ["操作: 触发荣誉等级升级", "预期: 收到通知 [ 你的荣誉等级已提升至 Lv.#number ]"]},
                {"title": "TC-10: 魅力等级晋级官方消息 [P0]", "details": ["操作: 触发魅力等级升级", "预期: 收到通知 [ 你的魅力等级已提升至 Lv.#number ]"]}
            ]
        },
        {
            "title": "4. 边界与体验测试",
            "cases": [
                {"title": "TC-11: H5 页面加载与数据同步 [P1]", "details": ["操作: 客户端升级后立即打开H5活跃等级页", "预期: 页面加载正常，等级与Exp数据实时同步无延迟"]},
                {"title": "TC-12: 日上限跨天重置逻辑 [P1]", "details": ["操作: 达到日上限后，等待服务器跨天再次操作", "预期: 次日额度重置，可正常获得Exp"]}
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
