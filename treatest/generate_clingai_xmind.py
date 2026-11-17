import os
import zipfile

import xmind

MD_PATH = r"d:\Pytest1\treatest\ClingAI视频图片交换个人签到测试用例.md"
XMIND_PATH = r"D:\用例文件\ClingAI视频图片交换个人签到测试用例.xmind"

MANIFEST = """<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns="urn:xmind:xmap:xmlns:manifest:1.0">
    <file-entry full-path="content.xml" media-type="text/xml"/>
    <file-entry full-path="styles.xml" media-type="text/xml"/>
    <file-entry full-path="comments.xml" media-type="text/xml"/>
</manifest>"""


def parse_markdown(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    modules = []
    current_module = None
    current_group = None
    current_case = None

    def ensure_group():
        nonlocal current_group
        if current_group is None:
            current_group = {"title": None, "cases": []}
            current_module["groups"].append(current_group)
        return current_group

    for line in lines:
        if line.startswith("## "):
            current_module = {"title": line[3:].strip(), "groups": []}
            modules.append(current_module)
            current_group = None
            current_case = None
            continue

        if current_module is None:
            continue

        if line.startswith("### TC-"):
            group = ensure_group()
            current_case = {"title": line[4:].strip(), "details": []}
            group["cases"].append(current_case)
            continue

        if line.startswith("### "):
            current_group = {"title": line[4:].strip(), "cases": []}
            current_module["groups"].append(current_group)
            current_case = None
            continue

        if current_case is None:
            continue

        if line.startswith("- 前置条件:") or line.startswith("- 操作步骤:") or line.startswith("- 预期结果:"):
            current_case["details"].append(line[2:].strip())
            continue

        if line.startswith("  - ") and current_case["details"]:
            current_case["details"][-1] += "；" + line[4:].strip()

    return modules


def add_case(parent, case):
    case_topic = parent.addSubTopic()
    case_topic.setTitle(case["title"])
    for detail in case["details"]:
        detail_topic = case_topic.addSubTopic()
        detail_topic.setTitle(detail)


def create_xmind(modules):
    os.makedirs(os.path.dirname(XMIND_PATH), exist_ok=True)
    if os.path.exists(XMIND_PATH):
        os.remove(XMIND_PATH)

    workbook = xmind.load(XMIND_PATH)
    sheet = workbook.getPrimarySheet()
    sheet.setTitle("测试用例")

    root = sheet.getRootTopic()
    root.setTitle("ClingAI 视频图片交换个人签到")

    case_count = 0
    for module in modules:
        groups = [g for g in module["groups"] if g["cases"]]
        if not groups:
            continue
        module_topic = root.addSubTopic()
        module_topic.setTitle(module["title"])
        named = [g for g in groups if g["title"]]
        unnamed = [g for g in groups if not g["title"]]
        for group in unnamed:
            for case in group["cases"]:
                add_case(module_topic, case)
                case_count += 1
        for group in named:
            group_topic = module_topic.addSubTopic()
            group_topic.setTitle(group["title"])
            for case in group["cases"]:
                add_case(group_topic, case)
                case_count += 1

    xmind.save(workbook, XMIND_PATH)

    with zipfile.ZipFile(XMIND_PATH, "a") as z:
        if "META-INF/manifest.xml" not in z.namelist():
            z.writestr("META-INF/manifest.xml", MANIFEST)

    return case_count


if __name__ == "__main__":
    modules = parse_markdown(MD_PATH)
    count = create_xmind(modules)
    print(f"cases={count}")
    print(f"saved={XMIND_PATH}")
    print(f"size={os.path.getsize(XMIND_PATH)}")
