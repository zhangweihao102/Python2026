import re

with open('d:\\Pytest1\\treatest\\MeterSphere测试平台搭建流程.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove [¶](#...) from headings
content = re.sub(r'\[¶\]\(#[^)]+\)', '', content)

# 2. Change [![alt](img_url)](img_url) to just ![alt](img_url)
content = re.sub(r'\[!\[([^\]]*)\]\([^)]+\)\]\(([^)]+)\)', r'![\1](\2)', content)

# 3. Remove javascript and footer junk at the end
junk_index = content.find('var target=document.getElementById')
if junk_index != -1:
    content = content[:junk_index]

# 4. Normalize spacing
# Replace multiple empty lines with a single empty line
content = re.sub(r'\n{3,}', '\n\n', content)

# Remove leading/trailing whitespaces on lines
lines = content.split('\n')
cleaned_lines = [line.strip() if not line.startswith('    ') else line for line in lines]
content = '\n'.join(cleaned_lines)

# Fix code blocks spaces
content = re.sub(r'```\n\s*\n', '```\n', content)
content = re.sub(r'\n\s*\n```', '\n```', content)

with open('d:\\Pytest1\\treatest\\MeterSphere测试平台搭建流程.md', 'w', encoding='utf-8') as f:
    f.write(content.strip() + '\n')
