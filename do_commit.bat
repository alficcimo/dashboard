@echo off
cd /d C:\Users\maxim\ClaudeOS\Content\deploy
git add index.html
git commit -m "Fix: React.createElement, no Babel"
git push origin main
echo DONE
