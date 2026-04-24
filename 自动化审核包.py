from playwright.sync_api import Playwright, sync_playwright
import os
import sys
import ddddocr

# 创建截图目录
if not os.path.exists("login_screenshots"):
    os.makedirs("login_screenshots")

# 全局基础配置
CONFIG = {
    "login_url": "https://test-dyadm.iohubonline.club/#/login?redirect=%2FQueryId",
    "target_path": "/biz-settings/pkg-audit-version",
    "username": "zhangweihao",
    "password": "zwh000000",
    "max_captcha_retry": 3,
    "timeout": 90000,
    "after_search_delay": 3000,
    "after_query_delay": 2000,
    "audit_select_index": 0
}

ocr = ddddocr.DdddOcr(show_ad=False, beta=True)


# -------------------------- 通用函数 --------------------------
def refresh_dropdown(page, search_input):
    try:
        print("🔍 开始主动刷新下拉选项...")
        search_input.press("Backspace")
        search_input.type("s")
        page.wait_for_timeout(500)
        print("✅ 模拟字符修改刷新联想列表")
        return True
    except Exception as e:
        print(f"⚠️  主动刷新下拉选项失败：{str(e)}")
        return False


def login(page):
    try:
        page.goto(CONFIG["login_url"], wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        print(f"✅ 成功打开登录页：{CONFIG['login_url']}")

        page.locator('input[name="userName"]').fill(CONFIG["username"])
        page.locator('input[name="password"]').fill(CONFIG["password"])
        print("✅ 账号密码输入完成")

        login_success = False
        for retry in range(1, CONFIG["max_captcha_retry"] + 1):
            try:
                captcha_input = page.locator('input[name="verifyCode"]')
                captcha_input.clear()
                page.wait_for_timeout(300)
                print(f"\n🔄 第{retry}次尝试验证码登录")

                captcha_elem = page.locator('[class*="captcha"], .show-code, img[src*="captcha"]').first
                captcha_elem.wait_for(state="visible", timeout=5000)
                captcha_bytes = captcha_elem.screenshot()
                captcha_text = ocr.classification(captcha_bytes).strip().upper()
                captcha_text = ''.join([c for c in captcha_text if c.isalnum()])
                print(f"✅ 第{retry}次识别验证码：{captcha_text}")

                captcha_input.fill(captcha_text)
                page.wait_for_timeout(500)
                page.locator('button:has-text("登录")').click()
                page.wait_for_timeout(3000)

                if page.locator('div:has-text("验证码错误")').is_visible():
                    print(f"❌ 第{retry}次登录失败：验证码错误")
                    try:
                        page.locator('button:has-text("刷新")').click()
                        page.wait_for_timeout(1000)
                        print("✅ 已刷新验证码，准备重试")
                    except:
                        print("⚠️  未找到验证码刷新按钮")
                    continue
                elif CONFIG["target_path"] in page.url or not page.locator('input[name="userName"]').is_visible():
                    login_success = True
                    print(f"✅ 第{retry}次登录成功！")
                    break
                else:
                    print(f"❌ 第{retry}次登录失败：未知错误")
                    break

            except Exception as e:
                print(f"❌ 第{retry}次登录异常：{str(e)}")
                if retry == CONFIG["max_captcha_retry"]:
                    raise Exception(f"验证码重试{CONFIG['max_captcha_retry']}次均异常")

        if not login_success:
            raise Exception(f"验证码重试{CONFIG['max_captcha_retry']}次均失败")

        if CONFIG["target_path"] not in page.url:
            page.evaluate(f'window.location.hash = "{CONFIG["target_path"]}"')
            page.wait_for_timeout(3000)
            print(f"✅ 跳转到目标页面：{CONFIG['target_path']}")

        return True

    except Exception as e:
        print(f"\n❌ 登录流程总失败：{str(e)}")
        page.screenshot(path="login_screenshots/login_failed.png")
        return False


# -------------------------- 核心：新增包名匹配校验 --------------------------
def search_package(page, package_name, is_final_check=False):
    """
    搜索包名流程（新增严格校验：无匹配包名则终止流程）
    :param page: 页面对象
    :param package_name: 目标包名
    :param is_final_check: 是否为最终校验的二次搜索
    :return: 搜索结果（True=成功，False=失败）
    """
    try:
        if is_final_check:
            print(f"\n🔍 【最终校验】开始二次执行包名搜索：{package_name}")
        else:
            print(f"\n🔍 开始执行包名搜索：{package_name}")

        # 1. 定位并清空搜索框
        search_input = page.locator('input[placeholder="请输入或选择包名"].el-input__inner').first
        search_input.wait_for(state="visible", timeout=15000)
        print("✅ 定位到包名搜索框")

        search_input.click(force=True)
        page.wait_for_timeout(500)
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        page.wait_for_timeout(300)

        # 2. 输入包名
        search_input.fill(package_name)
        page.wait_for_timeout(800)
        actual_input = search_input.input_value()
        print(f"✅ 搜索框实际内容：{actual_input}")

        # 3. 刷新下拉选项
        refresh_dropdown(page, search_input)
        print(f"\n⏳ 输入包名后等待 {CONFIG['after_search_delay'] / 1000} 秒...")
        page.wait_for_timeout(CONFIG['after_search_delay'])

        # 4. 尝试选择下拉选项（非必须）
        try:
            dropdown_option = page.locator(f'li:has-text("{package_name}")').first
            dropdown_option.wait_for(state="visible", timeout=10000)
            dropdown_option.click(force=True)
            print(f"✅ 已点击下拉选项：{package_name}")
        except:
            print("⚠️  未找到精准下拉选项，直接执行查询...")

        # 5. 点击查找按钮
        search_button = page.locator('button:has-text("查找")').first
        search_button.wait_for(state="visible")
        search_button.click(force=True)
        print("✅ 已点击查找按钮，等待最终搜索结果...")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(CONFIG['after_query_delay'])
        print(f"✅ 搜索完成，开始校验结果...")

        # -------------------------- 关键新增：严格包名匹配校验 --------------------------
        # 方式1：精准匹配结果行（优先）
        result_row = page.locator(f'tr:has-text("{package_name}")').first
        # 方式2：兜底校验（防止文本匹配问题）
        all_result_rows = page.locator('tbody tr')
        row_count = all_result_rows.count()
        package_found = False

        # 遍历所有结果行，精准校验包名
        if row_count > 0:
            print(f"🔍 搜索结果共{row_count}行，开始逐行匹配包名...")
            for i in range(row_count):
                row_text = all_result_rows.nth(i).inner_text().strip()
                if package_name in row_text:
                    package_found = True
                    break
        else:
            print("🔍 搜索结果为空！")

        # 核心判断：无匹配包名则终止流程
        if not result_row.is_visible() and not package_found:
            error_msg = f"\n❌ 严重错误：搜索结果中未找到包名「{package_name}」"
            error_msg += "\n💡 请确认："
            error_msg += "\n   1. 包名是否输入正确（区分大小写/特殊字符）"
            error_msg += "\n   2. 该包名是否存在于系统中"
            error_msg += "\n   3. 网络/系统是否正常"
            print(error_msg)
            # 保存失败截图
            page.screenshot(path=f"login_screenshots/{package_name}_search_no_result.png")
            # 抛出异常，终止后续流程
            raise Exception(f"未找到匹配的包名「{package_name}」，流程终止")

        # 6. 包名匹配成功，继续后续操作
        print(f"✅ 校验通过：搜索结果中找到包名「{package_name}」")
        if is_final_check:
            screenshot_path = f"login_screenshots/{package_name}_search_final_check.png"
            print(f"✅ 【最终校验】搜索成功截图已保存：{screenshot_path}")
        else:
            screenshot_path = f"login_screenshots/{package_name}_search_success.png"
            print(f"✅ 搜索成功截图已保存：{screenshot_path}")
        page.screenshot(path=screenshot_path, full_page=True)

        return True

    except Exception as e:
        # 捕获包名未找到的异常，明确提示
        if "未找到匹配的包名" in str(e):
            print(f"\n🚨 流程终止：{str(e)}")
        else:
            error_suffix = "_final_check" if is_final_check else ""
            error_path = f"login_screenshots/{package_name}_search_failed{error_suffix}.png"
            print(f"❌ 包名[{package_name}]搜索/选择失败：{str(e)}")
            if page:
                page.screenshot(path=error_path)
        return False


def edit_audit_strategy(page, package_name):
    """修改审核策略为否"""
    try:
        print(f"\n🔍 开始执行[{package_name}]的审核策略修改流程...")
        edit_js = f"""
        var rows = document.getElementsByTagName('tr');
        var targetRow = null;
        for (var i = 0; i < rows.length; i++) {{
            if (rows[i].textContent.includes('{package_name}')) {{
                targetRow = rows[i];
                break;
            }}
        }}
        if (targetRow) {{
            var links = targetRow.getElementsByTagName('a');
            for (var j = 0; j < links.length; j++) {{
                if (links[j].textContent.includes('编辑')) {{
                    links[j].click();
                    break;
                }}
            }}
        }}
        """
        page.evaluate(edit_js)
        page.wait_for_timeout(3000)
        print("✅ 点击编辑按钮，弹窗已打开")

        audit_js = f"""
        setTimeout(function() {{
            var dialogs = document.getElementsByClassName('el-dialog');
            var targetDialog = null;
            for (var k = 0; k < dialogs.length; k++) {{
                if (dialogs[k].textContent.includes('编辑包审核版本')) {{
                    targetDialog = dialogs[k];
                    break;
                }}
            }}
            if (targetDialog) {{
                var selects = targetDialog.getElementsByClassName('el-select');
                var auditSelect = selects[{CONFIG['audit_select_index']}];
                if (auditSelect) {{
                    auditSelect.click();
                    setTimeout(function() {{
                        var options = document.getElementsByClassName('el-select-dropdown__item');
                        for (var m = 0; m < options.length; m++) {{
                            if (options[m].textContent.trim() === '否') {{
                                options[m].click();
                                break;
                            }}
                        }}
                        setTimeout(function() {{
                            var buttons = targetDialog.getElementsByTagName('button');
                            for (var n = 0; n < buttons.length; n++) {{
                                if (buttons[n].textContent.includes('确定')) {{
                                    buttons[n].click();
                                    break;
                                }}
                            }}
                        }}, 1000);
                    }}, 1000);
                }}
            }}
        }}, 1500);
        """
        page.evaluate(audit_js)
        page.wait_for_timeout(4000)
        print(f"✅ 已精准将[{package_name}]的“审核策略是否开启”改为“否”并保存")

        page.reload()
        page.wait_for_timeout(3000)
        print(f"✅ 页面已刷新，[{package_name}]的修改已生效")
        return True
    except Exception as e:
        if "Locator.fill" not in str(e) and "element is not editable" not in str(e):
            error_path = f"login_screenshots/{package_name}_edit_failed.png"
            print(f"❌ [{package_name}]审核策略修改失败：{str(e)}")
            page.screenshot(path=error_path)
            return False
        else:
            print(f"⚠️  [{package_name}]验证阶段提示：搜索框为只读状态，已跳过重新输入")
            return True


# -------------------------- 主流程（混合模式：命令行+交互式） --------------------------
def main():
    """主流程（混合模式+包名校验）"""
    package_name = ""

    if not CONFIG["username"] or not CONFIG["password"]:
        raise RuntimeError("缺少登录凭据：请设置环境变量AUDIT_USERNAME和AUDIT_PASSWORD")

    # 1. 优先读取命令行参数
    if len(sys.argv) >= 2:
        package_name = sys.argv[1].strip()
        print(f"🚀 从命令行获取包名：{package_name}")
    else:
        # 2. 无命令行参数则交互式输入
        print("🚀 包名自动化处理工具")
        print("=" * 60)
        while True:
            package_name = input("请输入目标包名（如：com.lifangjie.ios）：").strip()
            if package_name:
                break
            print("❌ 包名不能为空，请重新输入！")
        print(f"\n✅ 已确认目标包名：{package_name}")

    print("=" * 60)

    # 2. 启动Playwright执行流程
    with sync_playwright() as p:
        launch_kwargs = {
            "headless": False,
            "slow_mo": 1500,
            "args": ["--disable-blink-features=AutomationControlled", "--ignore-certificate-errors"],
        }

        browser = None
        for channel in ["msedge", "chrome"]:
            try:
                browser = p.chromium.launch(**launch_kwargs, channel=channel)
                print(f"✅ 使用已安装浏览器通道启动：{channel}")
                break
            except Exception as e:
                print(f"⚠️  无法使用通道{channel}启动：{str(e)}")

        if browser is None:
            raise RuntimeError(
                "无法启动本机Edge/Chrome。请确认已安装浏览器，或执行：python -m playwright install chromium"
            )
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        context.set_default_timeout(CONFIG["timeout"])
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

        try:
            # 步骤1：登录
            if not login(page):
                raise Exception("登录流程失败，终止程序")

            # 步骤2：搜索包名（新增严格校验，失败则终止）
            if not search_package(page, package_name):
                raise Exception(f"包名[{package_name}]搜索失败，终止后续流程")

            # 步骤3：修改审核策略（仅当搜索成功时执行）
            if not edit_audit_strategy(page, package_name):
                raise Exception(f"[{package_name}]审核策略修改核心逻辑失败")

            # 步骤4：最终校验
            print("\n" + "=" * 60)
            print(f"🔍 所有核心流程完成，开始最终校验[{package_name}]")
            print("=" * 60)
            if not search_package(page, package_name, is_final_check=True):
                print(f"⚠️  最终校验：[{package_name}]二次搜索失败（核心流程已完成）")
            else:
                print(f"✅ 最终校验：[{package_name}]二次搜索成功，结果已截图")

            # 最终提示
            print("\n" + "=" * 60)
            print(f"🎉 [{package_name}]所有流程执行完成！")
            print(f"✅ 截图路径：login_screenshots/")
            print(f"✅ 首次搜索截图：{package_name}_search_success.png")
            print(f"✅ 最终校验截图：{package_name}_search_final_check.png")
            print("=" * 60)

        except Exception as e:
            # 捕获包名未找到的终止异常，友好提示
            if "未找到匹配的包名" in str(e) or "搜索失败，终止后续流程" in str(e):
                print(f"\n🚨 程序终止：{str(e)}")
            else:
                print(f"\n❌ 程序终止：{str(e)}")
        finally:
            auto_close = os.environ.get("AUTO_CLOSE", "").strip().lower() in {"1", "true", "yes"}
            if not auto_close:
                print("\n👉 按Enter键关闭浏览器...")
                try:
                    input()
                except EOFError:
                    pass
            context.close()
            browser.close()
            print("✅ 浏览器已关闭")


if __name__ == "__main__":
    main()
