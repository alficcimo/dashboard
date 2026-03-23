import json

with open('content-captions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

has_captions = any('Открою вам ужас' in item.get('caption', '') for item in data)
print('File HAS updated captions' if has_captions else 'File does NOT have updated captions')
print(f'Number of captions: {len(data)}')
if data:
    print(f'First caption preview: {data[0]["caption"][:100]}...')
