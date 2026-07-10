import xmind
import os

def create_xmind_file():
    file_path = r"D:\用例文件\端内贵族VIP测试用例.xmind"
    
    if os.path.exists(file_path):
        os.remove(file_path)
        
    workbook = xmind.load(file_path)
    sheet = workbook.getPrimarySheet()
    sheet.setTitle("贵族VIP测试用例")
    
    root_topic = sheet.getRootTopic()
    root_topic.setTitle("端内贵族VIP体系")

    data = [
        {
            "title": "1. 贵族开通与购买流 (核心)",
            "cases": [
                {"title": "TC-01: 正常购买与扣费 [P0]", "details": ["操作: 余额充足下购买VIP1至VIP5", "预期: 扣费准确，即时生效对应等级"]},
                {"title": "TC-02: 余额不足购买拦截 [P0]", "details": ["操作: 余额不足尝试购买", "预期: 拦截并提示，引导充值"]},
                {"title": "TC-03: 时效计算与过期逻辑 [P0]", "details": ["操作: 购买后等待30个自然日", "预期: 当日生效，满30天后自动失效，回收特权装扮"]}
            ]
        },
        {
            "title": "2. 视觉UI与物料展示",
            "cases": [
                {"title": "TC-04: 物料分级与档位展示 [P1]", "details": ["操作: 查验座驾/勋章/资料卡/框/气泡", "预期: 严格分5个档位，等级越高视觉越高级"]},
                {"title": "TC-05: 语义背景与本地化核对 [P1]", "details": ["操作: 核对命名及设计元素", "预期: Nawab/Mansab/Vizier/Maharaja/Shahanshah 匹配印度/波斯文化设定"]}
            ]
        },
        {
            "title": "3. 贵族专属特权测试 (核心)",
            "cases": [
                {"title": "TC-06: 基础特权 (VIP1+) [P0]", "details": ["操作: 佩戴勋章/公屏发言/访问/密码锁定", "预期: 勋章外显，彩色名字，访客留痕，密码可用"]},
                {"title": "TC-07: 隐私特权 (VIP2+) [P0]", "details": ["操作: 开启隐私访问，查排行榜", "预期: 访客记录隐身，排行榜不展示"]},
                {"title": "TC-08: 房间防管控 (VIP3+) [P0]", "details": ["操作: 房主尝试禁麦VIP3+", "预期: 禁麦失败，提示防禁麦生效；强关注可用"]},
                {"title": "TC-09: 社交突破 (VIP4+) [P0]", "details": ["操作: 向拦截私聊用户发消息", "预期: 无视拦截，私聊消息直接触达"]},
                {"title": "TC-10: 终极防踢 (VIP5) [P0]", "details": ["操作: 房主尝试踢出VIP5", "预期: 踢出失败，防踢特权生效"]}
            ]
        },
        {
            "title": "4. 边界与交互异常",
            "cases": [
                {"title": "TC-11: 特权冲突界定 [P1]", "details": ["操作: 房主特权 vs VIP5防踢", "预期: 需确认绝对优先级规则并严格执行"]},
                {"title": "TC-12: 跨级购买与续费 [P1]", "details": ["操作: 续费同级或升级高级别", "预期: 续费顺延30天；升级按折算规则替换特权"]},
                {"title": "TC-13: 封禁状态表现 [P2]", "details": ["操作: 封禁VIP账号", "预期: 时效照常扣减，特权冻结隐藏"]}
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
