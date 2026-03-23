import urllib.request
import json

files_to_check = [
    'content-captions.json',
    'content-ideas.json',
    'content-titles.json',
]

base_url = 'https://raw.githubusercontent.com/alficcimo/dashboard/master/'

for filename in files_to_check:
    try:
        url = base_url + filename
        with urllib.request.urlopen(url, timeout=5) as response:
            content = response.read().decode('utf-8')
            data = json.loads(content)
            
            # Check for captions specifically in content-captions.json
            if filename == 'content-captions.json':
                has_captions = any('Открою' in item.get('caption', '') for item in data)
                print(f"{filename}: OK ({len(data)} items, has updated captions: {has_captions})")
            else:
                print(f"{filename}: OK ({len(data)} items)")
                
    except Exception as e:
        print(f"{filename}: ERROR - {e}")
