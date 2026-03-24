@echo off
cd /d C:\Users\maxim\ClaudeOS\Content\deploy
git add content-carousels.json
git commit -m "Update carousels with Telegram CTA in last slide"
git push origin master
