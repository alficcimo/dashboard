@echo off
cd /d "C:\Users\maxim\ClaudeOS\Content\deploy"
"C:\Program Files\Git\cmd\git.exe" add index.html standalone.html captions-only.html test-react.html
"C:\Program Files\Git\cmd\git.exe" commit -m "Fix: Add diagnostic React test files and simplified captions dashboard"
"C:\Program Files\Git\cmd\git.exe" push origin master
echo Done!
