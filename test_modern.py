import zipfile
import json
import uuid

def gen_id():
    return uuid.uuid4().hex[:26]

content = [
    {
        "id": gen_id(),
        "title": "Sheet 1",
        "class": "sheet",
        "rootTopic": {
            "id": gen_id(),
            "class": "topic",
            "title": "测试",
            "children": {
                "attached": [
                    {
                        "id": gen_id(),
                        "class": "topic",
                        "title": "子节点 1"
                    }
                ]
            }
        }
    }
]

with zipfile.ZipFile(r"D:\用例文件\test_modern.xmind", "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("content.json", json.dumps(content))
    z.writestr("metadata.json", "{}")
