import zipfile
import json
import xml.etree.ElementTree as ET

def extract_xmind(file_path):
    with zipfile.ZipFile(file_path, 'r') as z:
        if 'content.json' in z.namelist():
            print("Found content.json")
            content = json.loads(z.read('content.json').decode('utf-8'))
            print(json.dumps(content[0]['rootTopic'], ensure_ascii=False, indent=2)[:1000])
        elif 'content.xml' in z.namelist():
            print("Found content.xml")
            xml_content = z.read('content.xml').decode('utf-8')
            root = ET.fromstring(xml_content)
            print("Root tags:", [child.tag for child in root])
        else:
            print("Unknown format")
            print(z.namelist())

extract_xmind(r"D:\用例\sofun1.3迭代.xmind")
