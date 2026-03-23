import re

with open('current_index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check each line for quote balance
for i, line in enumerate(lines, 1):
    if '<script' in line:
        in_script = True
        start_line = i
    if '</script>' in line:
        break
    
    # Count quotes (excluding escaped quotes)
    single_quotes = line.count("'") - line.count("\\'")
    
    if single_quotes % 2 != 0:
        print(f"Line {i}: ODD quotes ({single_quotes})")
        print(f"  Content: {line.strip()[:100]}")

# Also check for incomplete string literals
print("\nLooking for potentially broken strings...")
for i, line in enumerate(lines, 1):
    if i < 100:  # Focus on early lines
        continue
    if i > 200:
        break
    # Look for lines with Cyrillic text
    if any(ord(c) > 127 for c in line):
        single_quotes = line.count("'")
        if single_quotes % 2 != 0:
            print(f"Line {i} (has Cyrillic): {line.strip()[:80]}")
