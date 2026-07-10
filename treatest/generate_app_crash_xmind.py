import xmind
import os

def create_crash_test_xmind():
    """
    分析Android崩溃日志并生成测试用例Xmind文件
    崩溃原因：WindowManager添加窗口失败，DeadObjectException
    """
    file_path = r"D:\用例文件\App窗口崩溃测试用例.xmind"
    
    # 如果文件已存在，先删除
    if os.path.exists(file_path):
        os.remove(file_path)
        
    workbook = xmind.load(file_path)
    sheet = workbook.getPrimarySheet()
    sheet.setTitle("测试用例")
    
    root_topic = sheet.getRootTopic()
    root_topic.setTitle("App窗口崩溃（DeadObjectException）测试用例")

    # 测试用例数据结构
    test_data = [
        {
            "title": "1. 崩溃日志分析与复现测试 (核心)",
            "cases": [
                {
                    "title": "TC-01: 日志分析 - 崩溃场景确认 [P0]",
                    "details": [
                        "前置条件: 拥有完整的崩溃日志堆栈",
                        "操作步骤: 1. 分析堆栈信息  2. 确认崩溃发生在Activity Resume阶段  3. 查看进程运行时长（Process-Runtime: 5089970ms ≈ 85分钟）",
                        "预期结果: 确认崩溃发生在WindowManager添加窗口时，DeadObjectException，可能由SystemServer或WindowManagerService异常导致。"
                    ]
                },
                {
                    "title": "TC-02: 复现测试 - 长时间运行后切换Activity [P0]",
                    "details": [
                        "前置条件: App在前台运行较长时间（60分钟+）",
                        "操作步骤: 1. 保持App前台运行  2. 期间进行正常用户操作  3. 尝试触发Activity Resume/重新进入App",
                        "预期结果: 尝试复现Window添加失败的崩溃。"
                    ]
                },
                {
                    "title": "TC-03: 复现测试 - 内存压力场景 [P0]",
                    "details": [
                        "前置条件: 设备内存不足，开启多个大型App",
                        "操作步骤: 1. 在后台开启多个消耗内存的应用  2. 操作待测App，频繁切换页面  3. 监控是否发生DeadObjectException",
                        "预期结果: 在内存压力下，验证是否容易触发WindowManager通信异常。"
                    ]
                }
            ]
        },
        {
            "title": "2. WindowManager与Binder机制测试",
            "cases": [
                {
                    "title": "TC-04: Binder压力 - 高频窗口操作 [P1]",
                    "details": [
                        "前置条件: App正常启动",
                        "操作步骤: 1. 频繁快速地打开/关闭Dialog/Toast/PopupWindow  2. 同时频繁切换Activity  3. 持续操作10分钟",
                        "预期结果: 不应出现WindowManager添加窗口失败，不应出现DeadObjectException。"
                    ]
                },
                {
                    "title": "TC-05: 异常恢复 - Activity异常销毁后重建 [P1]",
                    "details": [
                        "前置条件: 开启开发者选项中的\"不保留活动\"",
                        "操作步骤: 1. 进入任意页面  2. 按Home键退到后台  3. 立即重新进入App  4. 反复多次",
                        "预期结果: Activity正常重建，窗口添加成功，无崩溃。"
                    ]
                },
                {
                    "title": "TC-06: 多窗口模式 - 分屏/自由窗口 [P2]",
                    "details": [
                        "前置条件: 设备支持多窗口模式",
                        "操作步骤: 1. 进入分屏模式  2. 在分屏状态下操作App  3. 调整窗口大小  4. 切换全屏/分屏",
                        "预期结果: 窗口切换正常，无添加窗口失败崩溃。"
                    ]
                }
            ]
        },
        {
            "title": "3. Activity生命周期与内存测试",
            "cases": [
                {
                    "title": "TC-07: 生命周期 - 快速切换页面 [P0]",
                    "details": [
                        "前置条件: 登录成功进入首页",
                        "操作步骤: 1. 在不同页面间快速来回切换  2. 监控Logcat中WindowManager相关日志  3. 持续5分钟",
                        "预期结果: 所有Activity正常onResume/onPause，无窗口添加异常。"
                    ]
                },
                {
                    "title": "TC-08: 内存泄漏 - 长时间运行监控 [P1]",
                    "details": [
                        "前置条件: 连接Android Studio Profiler",
                        "操作步骤: 1. 记录初始内存占用  2. 进行正常业务操作1小时  3. 观察内存曲线  4. 触发GC并检查是否有Activity/Window泄漏",
                        "预期结果: 无明显内存泄漏，内存能正常回收。"
                    ]
                },
                {
                    "title": "TC-09: 配置变更 - 屏幕旋转/语言切换 [P1]",
                    "details": [
                        "前置条件: 在任意页面",
                        "操作步骤: 1. 旋转屏幕  2. 切换系统语言  3. 切换深色/浅色模式",
                        "预期结果: Activity重建正常，窗口重新添加成功，无崩溃。"
                    ]
                }
            ]
        },
        {
            "title": "4. 登录流程专项测试 (与当前项目相关)",
            "cases": [
                {
                    "title": "TC-10: 登录成功 - 页面跳转窗口添加 [P0]",
                    "details": [
                        "前置条件: 在登录页面",
                        "操作步骤: 1. 输入账号密码  2. 点击登录按钮  3. 观察从登录页跳转到首页的过程",
                        "预期结果: 登录成功，页面正常跳转，首页Window正常添加，无崩溃。"
                    ]
                },
                {
                    "title": "TC-11: 登录重试 - 多次登录失败后成功 [P1]",
                    "details": [
                        "前置条件: 在登录页面",
                        "操作步骤: 1. 输入错误密码点击登录3次  2. 第4次输入正确密码登录",
                        "预期结果: 最终登录成功，无Window相关崩溃。"
                    ]
                },
                {
                    "title": "TC-12: 弱网登录 - 网络超时后恢复 [P1]",
                    "details": [
                        "前置条件: 使用Charles/Fiddler模拟弱网/超时",
                        "操作步骤: 1. 在弱网环境下点击登录  2. 等待超时  3. 恢复网络后重新登录",
                        "预期结果: 网络恢复后登录成功，窗口正常显示。"
                    ]
                }
            ]
        },
        {
            "title": "5. 异常与边界场景测试",
            "cases": [
                {
                    "title": "TC-13: 进程被杀 - 从最近任务恢复 [P0]",
                    "details": [
                        "前置条件: App在前台",
                        "操作步骤: 1. 按Home键退到后台  2. 通过adb shell或最近任务杀掉App进程  3. 从桌面图标重新打开App",
                        "预期结果: App正常重启，Splash/首页正常显示，无窗口添加失败。"
                    ]
                },
                {
                    "title": "TC-14: 权限弹窗 - 系统弹窗交互 [P2]",
                    "details": [
                        "前置条件: 新安装App或清除权限",
                        "操作步骤: 1. 操作到需要权限的功能  2. 在系统权限弹窗弹出时快速操作App  3. 拒绝/允许权限后继续操作",
                        "预期结果: 权限交互正常，后续Window添加不受影响。"
                    ]
                },
                {
                    "title": "TC-15: 快速连续启动 - 冷启动竞争 [P2]",
                    "details": [
                        "前置条件: App未运行",
                        "操作步骤: 1. 快速连续多次点击桌面App图标  2. 观察App启动行为",
                        "预期结果: App正常启动一次，不会出现多个实例或窗口添加异常。"
                    ]
                }
            ]
        },
        {
            "title": "6. 不同设备与系统版本适配",
            "cases": [
                {
                    "title": "TC-16: 机型适配 - Redmi/MIUI设备 [P0]",
                    "details": [
                        "前置条件: Redmi手机（与崩溃日志机型一致）",
                        "操作步骤: 1. 在Redmi/sunstone设备上安装App  2. 执行完整登录流程  3. 长时间运行测试",
                        "预期结果: 重点覆盖Redmi MIUI设备，验证是否仍出现DeadObjectException。"
                    ]
                },
                {
                    "title": "TC-17: 系统版本 - Android 14/13/12 [P1]",
                    "details": [
                        "前置条件: 不同Android系统版本的测试机",
                        "操作步骤: 在Android 12/13/14设备上执行上述关键测试用例",
                        "预期结果: 各系统版本下均无窗口添加崩溃。"
                    ]
                },
                {
                    "title": "TC-18: 低内存设备 - 512MB/1GB RAM机型 [P2]",
                    "details": [
                        "前置条件: 低内存配置的测试设备",
                        "操作步骤: 在低内存设备上执行主要业务流程",
                        "预期结果: 即使在内存紧张情况下，也应优雅降级，而非直接崩溃。"
                    ]
                }
            ]
        },
        {
            "title": "7. 修复验证测试",
            "cases": [
                {
                    "title": "TC-19: 修复验证 - 添加try-catch保护 [P0]",
                    "details": [
                        "前置条件: 开发已添加WindowManager.addView的异常捕获",
                        "操作步骤: 1. 回归测试所有上述用例  2. 重点验证崩溃场景",
                        "预期结果: 即使出现DeadObjectException，App也不会崩溃，而是尝试恢复或提示用户。"
                    ]
                },
                {
                    "title": "TC-20: 修复验证 - 检查Window Token有效性 [P0]",
                    "details": [
                        "前置条件: 开发已添加Window Token有效性检查",
                        "操作步骤: 在Activity生命周期关键节点（onResume）添加Token检查",
                        "预期结果: 在添加Window前检查Activity状态是否有效，避免无效的Window操作。"
                    ]
                },
                {
                    "title": "TC-21: 修复验证 - 长时间稳定性回归 [P0]",
                    "details": [
                        "前置条件: 修复版本已打包",
                        "操作步骤: 1. 安装修复版本  2. 进行Monkey测试或自动化长时间运行  3. 持续24小时",
                        "预期结果: 相同场景下不再出现该类型崩溃。"
                    ]
                }
            ]
        }
    ]

    # 构建Xmind结构
    for module in test_data:
        module_topic = root_topic.addSubTopic()
        module_topic.setTitle(module["title"])
        for case in module["cases"]:
            case_topic = module_topic.addSubTopic()
            case_topic.setTitle(case["title"])
            for detail in case["details"]:
                detail_topic = case_topic.addSubTopic()
                detail_topic.setTitle(detail)

    # 保存文件
    xmind.save(workbook, file_path)
    print(f"Xmind测试用例文件已保存至: {file_path}")

if __name__ == "__main__":
    create_crash_test_xmind()
