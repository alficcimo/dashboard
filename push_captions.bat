@echo off
cd /d C:\Users\maxim\ClaudeOS\Content\deploy
git add content-captions.json
git commit -m "Update captions JSON"
git push origin master
echo DONE
