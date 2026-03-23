import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check for various things
has_html_tag = '<html' in content
has_script_tags = '<script' in content
has_fetch = 'fetch' in content
has_captions_embedded = 'Открою вам ужас' in content
has_json_data = 'content-captions' in content

print("HTML Structure Analysis:")
print(f"  Has <html> tag: {has_html_tag}")
print(f"  Has <script> tags: {has_script_tags}")
print(f"  Has fetch() calls: {has_fetch}")
print(f"  Has captions embedded: {has_captions_embedded}")
print(f"  References content-captions: {has_json_data}")
print(f"\n  File size: {len(content)} bytes")
print(f"  First 500 chars:\n{content[:500]}")
