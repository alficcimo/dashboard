with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()
    if 'Caption Analyzer' in content:
        print('SUCCESS: Caption Analyzer found')
    else:
        print('FAIL: Still Title Analyzer')
    # Find and print the line
    for i, line in enumerate(content.split('\n'), 1):
        if 'Analyzer' in line:
            print(f'Line {i}: {line.strip()[:100]}')
