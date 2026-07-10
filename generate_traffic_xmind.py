import xmind
import os

def create_xmind_file():
    file_path = r"D:\用例文件\【冷启动】流量调度测试用例.xmind"
    
    if os.path.exists(file_path):
        os.remove(file_path)
        
    workbook = xmind.load(file_path)
    sheet = workbook.getPrimarySheet()
    sheet.setTitle("流量调度测试用例")
    
    root_topic = sheet.getRootTopic()
    root_topic.setTitle("【冷启动】流量调度")

    data = [
        {
            "title": "1. 触发机制与过滤规则测试",
            "cases": [
                {"title": "TC-01: 基础触发条件达成 [P0]", "details": ["前置条件: 未处于静默或风控", "操作: 满足人数、留存、增长率条件", "预期: 触发调度，全服横幅+房间红包"]},
                {"title": "TC-02: 过滤规则 - 静默房间 [P0]", "details": ["前置条件: 满足基础条件", "操作: 所有人无音源输入", "预期: 过滤，不触发；恢复后可触发"]},
                {"title": "TC-03: 过滤规则 - 风控房间 [P0]", "details": ["前置条件: 满足基础条件", "操作: 命中硬件/IP风控", "预期: 过滤，永不触发；解除后可触发"]},
                {"title": "TC-04: 增长权重独立满足 [P1]", "details": ["前置条件: 满足基础权重", "操作: 仅公屏增长或仅金币增长>100%", "预期: 均能正常触发"]},
                {"title": "TC-05: 留存权重边界值 [P1]", "details": ["前置条件: 满足基础条件", "操作: 总人数=5且留存刚超对照组", "预期: 高于时触发，低于或<5时不触发"]}
            ]
        },
        {
            "title": "2. 全服横幅广播测试",
            "cases": [
                {"title": "TC-06: 横幅展示与点击跳转 [P0]", "details": ["前置条件: 触发调度", "操作: 查看顶部横幅并在5s内点击", "预期: 展示头像文案及闪动红包，点击跳转，超时消失"]},
                {"title": "TC-07: 多房间命中轮播逻辑 [P1]", "details": ["前置条件: ≥2个房间同时触发", "操作: 观察全服横幅", "预期: 依次排队轮播展示，单次1条"]}
            ]
        },
        {
            "title": "3. 房间内延时红包测试",
            "cases": [
                {"title": "TC-08: 红包倒计时与弹窗展示 [P0]", "details": ["前置条件: 触发调度", "操作: 观察右下角红包", "预期: 60s倒计时，结束后弹窗显示平台头像文案"]},
                {"title": "TC-09: 领取红包 - 默认勾选订阅 [P0]", "details": ["前置条件: 弹窗展示", "操作: 保持勾选点击领取", "预期: 得金币，订阅房间，公屏发Say Hi，加关注列表"]},
                {"title": "TC-10: 领取红包 - 取消勾选订阅 [P0]", "details": ["前置条件: 弹窗展示", "操作: 取消勾选点击领取", "预期: 仅得金币，不订阅，不发消息"]},
                {"title": "TC-11: 弹窗关闭与重置 [P0]", "details": ["前置条件: 弹窗展示", "操作: 点击x关闭", "预期: 弹窗关闭；新一轮触发则重新倒计时"]},
                {"title": "TC-12: 倒计时中断恢复 [P1]", "details": ["前置条件: 倒计时中", "操作: 退出重进房间", "预期: 继续剩余时间或按规则重置，不卡死"]},
                {"title": "TC-13: 并发领取测试 [P2]", "details": ["前置条件: 弹窗展示", "操作: 多用户同时领取", "预期: 金币独立发放，公屏消息发送，服务端防刷"]}
            ]
        },
        {
            "title": "4. 房主专属通知与外显测试",
            "cases": [
                {"title": "TC-14: 端内官方消息通知核对 [P0]", "details": ["前置条件: 触发调度", "操作: 房主查看官方消息", "预期: 收到含时间戳的通知，仅房主可见"]},
                {"title": "TC-15: 房间内公屏通知核对 [P0]", "details": ["前置条件: 触发调度", "操作: 房主/管理/用户查看公屏", "预期: 公屏展示专属提示，仅房主和管理员可见"]},
                {"title": "TC-16: 房间列表 Hot+红包 标识 [P0]", "details": ["前置条件: 触发调度", "操作: 查看房间列表", "预期: 展示Hot+红包，2min后消失"]},
                {"title": "TC-17: 持续命中时间戳覆盖 [P0]", "details": ["前置条件: 标识未满2min", "操作: 再次触发", "预期: 覆盖时间戳，重置2min倒计时"]}
            ]
        },
        {
            "title": "5. 数据统计测试",
            "cases": [
                {"title": "TC-18: 调度触发核心数据核对 [P1]", "details": ["前置条件: 多次触发", "操作: 查看后台报表", "预期: 日期、触发次数、触发房间数统计准确"]},
                {"title": "TC-19: 房间转化数据核对 [P1]", "details": ["前置条件: 引流期间用户进出/打赏", "操作: 查看后台报表", "预期: 峰值人数、金币消耗人数准确"]}
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
