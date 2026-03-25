import json

try:
    with open('content-title-analyzer.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if data and isinstance(data, list) and len(data) > 0:
        print('Columns found:')
        for key in data[0].keys():
            print(f'  - {key}')
        print(f'\nTotal items: {len(data)}')
        print(f'Sample item:\n{json.dumps(data[0], indent=2, ensure_ascii=False)[:300]}')
    else:
        print('File is empty or not a list')
except FileNotFoundError:
    print('content-title-analyzer.json not found')
except json.JSONDecodeError:
    print('Invalid JSON')
except Exception as e:
    print(f'Error: {e}')
