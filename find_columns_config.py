import re

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Search for lines that contain column definitions
print('Searching for column configurations...\n')

in_caption_analyzer = False
for i, line in enumerate(lines, 1):
    # Look for caption-analyzer section
    if 'caption-analyzer' in line.lower() or 'title-analyzer' in line.lower():
        in_caption_analyzer = True
        print(f'[Line {i}] Found caption/title-analyzer reference:')
        print(f'  {line.strip()[:100]}')
    
    # Look for column patterns like 'original_title', 'improved_title'
    if any(col in line for col in ['original_title', 'improved_title', 'issues_found', 'virality_after', 'changes_made', 'header:']):
        print(f'[Line {i}] Column config: {line.strip()[:120]}')

# Also search for table headers rendering
print('\n\nSearching for table header patterns...')
for i, line in enumerate(lines, 1):
    if 'th>' in line or 'header' in line.lower():
        if 'caption' in line.lower() or (i > 100 and i < 200):  # likely around caption analyzer
            print(f'[Line {i}] {line.strip()[:100]}')
