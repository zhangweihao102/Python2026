import os

# ================= Appium 服务配置 =================
APPIUM_SERVER_URL = 'http://127.0.0.1:4723'

# ================= 设备与应用配置 =================
PLATFORM_NAME = 'Android'
DEVICE_NAME = '10CDAB0GEC0057Q'  # 你的测试设备ID
APP_PACKAGE = 'so.fun.test'    # 测试包名
APP_ACTIVITY = 'com.chat.login.ui.login.LoginActivity'  # 启动 Activity
AUTOMATION_NAME = 'UiAutomator2'
NO_RESET = True

# ================= 测试账号数据 =================
# 建议优先从环境变量获取，没有则使用默认值
TEST_ACCOUNT = os.environ.get("UCHAT_ACCOUNT", "10249147")
TEST_PASSWORD = os.environ.get("UCHAT_PASSWORD", "123456")
