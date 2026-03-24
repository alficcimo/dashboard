@echo off
cd /d C:\Users\maxim\ClaudeOS\Content\deploy
git add content-carousels.json
git commit -m "Update carousels with Telegram CTA"
git push origin master
echo Done
