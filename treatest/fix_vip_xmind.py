import zipfile

file_path = r"D:\用例文件\端内贵族VIP测试用例.xmind"

manifest_content = """<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns="urn:xmind:xmap:xmlns:manifest:1.0">
    <file-entry full-path="content.xml" media-type="text/xml"/>
    <file-entry full-path="styles.xml" media-type="text/xml"/>
    <file-entry full-path="comments.xml" media-type="text/xml"/>
</manifest>"""

with zipfile.ZipFile(file_path, 'a') as z:
    z.writestr("META-INF/manifest.xml", manifest_content)
