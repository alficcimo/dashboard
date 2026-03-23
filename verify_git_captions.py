with open('index_from_git.html', 'r', encoding='utf-8') as f:
    content = f.read()

if 'Открою вам ужас' in content:
    print("SUCCESS: Captions ARE in the pushed version!")
    # Find first occurrence
    idx = content.find('Открою вам ужас')
    print(f"Found at position: {idx}")
    print(f"Context: ...{content[max(0,idx-50):idx+100]}...")
else:
    print("Captions NOT found in pushed version")
    # Check what captions-related content is there
    if 'caption' in content:
        print("But 'caption' field exists in HTML")
        idx = content.find('caption')
        print(f"First caption reference at: {idx}")
