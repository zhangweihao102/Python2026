import zipfile
import json
import pandas as pd
import re

def extract_priority(title):
    match = re.search(r'\[(P[0-9])\]', title)
    if match:
        p = match.group(1)
        mapping = {'P0': '高', 'P1': '中', 'P2': '低', 'P3': '低'}
        title_clean = title.replace(match.group(0), '').strip()
        return mapping.get(p, '中'), title_clean
    return '中', title

def parse_node(node, path_names, cases):
    title = node.get('title', '').strip()
    
    # Check if it's a test case (leaf node that has details as children)
    children_attached = node.get('children', {}).get('attached', [])
    
    is_case = title.startswith('TC-') or len(path_names) >= 2 and len(children_attached) > 0 and all('前置条件' in c.get('title', '') or '操作' in c.get('title', '') or '预期' in c.get('title', '') for c in children_attached)
    
    if is_case:
        priority, clean_title = extract_priority(title)
        precondition = []
        steps = []
        expected = []
        
        for child in children_attached:
            child_title = child.get('title', '').strip()
            if child_title.startswith('前置条件'):
                precondition.append(child_title.replace('前置条件:', '').replace('前置条件：', '').strip())
            elif child_title.startswith('操作'):
                steps.append(child_title.replace('操作步骤:', '').replace('操作步骤：', '').replace('操作:', '').replace('操作：', '').strip())
            elif child_title.startswith('预期'):
                expected.append(child_title.replace('预期结果:', '').replace('预期结果：', '').replace('预期:', '').replace('预期：', '').strip())
            else:
                # Fallback, just put in steps
                steps.append(child_title)
                
        cases.append({
            '用例目录': '/'.join(path_names),
            '用例名称': clean_title,
            '前置条件': '\n'.join(precondition),
            '用例步骤': '\n'.join(steps),
            '预期结果': '\n'.join(expected),
            '优先级': priority
        })
    else:
        new_path = path_names + [title] if title else path_names
        for child in children_attached:
            parse_node(child, new_path, cases)
        
        # Also check detached children for the root
        for child in node.get('children', {}).get('detached', []):
            parse_node(child, path_names, cases)

def main():
    file_path = r"D:\用例\sofun1.3迭代.xmind"
    cases = []
    
    with zipfile.ZipFile(file_path, 'r') as z:
        content = json.loads(z.read('content.json').decode('utf-8'))
        
        for sheet in content:
            root_topic = sheet.get('rootTopic', {})
            parse_node(root_topic, [], cases)
            
    df = pd.DataFrame(cases)
    
    # TAPD specific columns mapping if needed, but these are standard
    output_path = r"D:\用例文件\sofun1.3迭代_TAPD导入.xlsx"
    df.to_excel(output_path, index=False)
    print(f"Excel generated at: {output_path}")
    print(f"Total test cases extracted: {len(cases)}")
    print(df.head())

if __name__ == "__main__":
    main()
