import os
import re
import zipfile

import xmind

MD_PATH = r"D:\用例文件\AI 图生视频 & 图片 测试用例.md"
XMIND_PATH = r"D:\用例文件\AI 图生视频 & 图片 测试用例.xmind"

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
    current_case = None

    for line in lines:
        if line.startswith("## ") and not line.startswith("## 用例统计"):
            title = line[3:].strip()
            current_module = {"title": title, "cases": []}
            modules.append(current_module)
            current_case = None
            continue

        if current_module is None:
            continue

        if line.startswith("### TC-"):
            current_case = {"title": line[4:].strip(), "details": []}
            current_module["cases"].append(current_case)
            continue

        if current_case is None:
            continue

        if line.startswith("- 前置条件:") or line.startswith("- 操作步骤:") or line.startswith("- 预期结果:"):
            current_case["details"].append(line[2:].strip())
            continue

        if line.startswith("  - ") and current_case["details"]:
            current_case["details"][-1] += "；" + line[4:].strip()

    return modules


def create_xmind(modules):
    if os.path.exists(XMIND_PATH):
        os.remove(XMIND_PATH)

    workbook = xmind.load(XMIND_PATH)
    sheet = workbook.getPrimarySheet()
    sheet.setTitle("测试用例")

    root = sheet.getRootTopic()
    root.setTitle("AI 图生视频 & 图片 测试用例")

    for module in modules:
        module_topic = root.addSubTopic()
        module_topic.setTitle(module["title"])
        for case in module["cases"]:
            case_topic = module_topic.addSubTopic()
            case_topic.setTitle(case["title"])
            for detail in case["details"]:
                detail_topic = case_topic.addSubTopic()
                detail_topic.setTitle(detail)

    xmind.save(workbook, XMIND_PATH)

    with zipfile.ZipFile(XMIND_PATH, "a") as z:
        names = z.namelist()
        if "META-INF/manifest.xml" not in names:
            z.writestr("META-INF/manifest.xml", MANIFEST)


if __name__ == "__main__":
    modules = parse_markdown(MD_PATH)
    case_count = sum(len(m["cases"]) for m in modules)
    create_xmind(modules)
    print(f"modules={len(modules)} cases={case_count}")
    print(f"saved={XMIND_PATH}")
