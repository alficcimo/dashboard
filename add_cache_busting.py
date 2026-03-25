#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Add cache-busting headers and meta tags to prevent browser caching issues
Run this once to add permanent cache-busting to index.html
"""
import re
from datetime import datetime

def add_cache_busting():
    # Read index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Cache-busting meta tags
    cache_meta = '''<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate, max-age=0">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">'''
    
    # Check if already has cache control
    if 'Cache-Control' in content:
        print('[SKIP] Cache-busting already present in index.html')
        return False
    
    # Find </head> and insert meta tags before it
    if '</head>' in content:
        content = content.replace('</head>', f'{cache_meta}\n    </head>')
        print('[ADDED] Cache-Control meta tags to <head>')
    else:
        print('[ERROR] Could not find </head> tag')
        return False
    
    # Add cache-busting to script tags - append ?v=timestamp to force reload
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # For any inline scripts that reference files, add cache bust
    # e.g., fetch('content-captions.json') -> fetch('content-captions.json?_=timestamp')
    content = re.sub(
        r"fetch\('([^']+)\.json'\)",
        f"fetch('\\1.json?_={timestamp}')",
        content
    )
    
    print(f'[ADDED] Cache-bust parameter to fetch calls: ?_={timestamp}')
    
    # Write updated content
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('[SUCCESS] Cache-busting implementation complete')
    return True

if __name__ == '__main__':
    add_cache_busting()
