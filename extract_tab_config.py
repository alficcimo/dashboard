import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the tabs configuration
tabs_match = re.search(r'const\s+tabs\s*=\s*\[(.*?)\];', content, re.DOTALL)
if tabs_match:
    tabs_section = tabs_match.group(1)
    # Find caption analyzer tab
    caption_match = re.search(r"id:\s*'caption-analyzer'[^}]*?}", tabs_section, re.DOTALL)
    if caption_match:
        print('Caption Analyzer Tab Config:')
        print(caption_match.group(0)[:300])
    else:
        print('Caption Analyzer tab not found')
else:
    print('Tabs configuration not found')

# Also look for columns configuration
columns_match = re.search(r"'caption-analyzer':\s*\[(.*?)\]", content, re.DOTALL)
if columns_match:
    print('\nCaption Analyzer Columns:')
    print(columns_match.group(0)[:500])
