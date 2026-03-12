@echo off
cd /d c:\Users\gideo\Desktop\Django\Capstone

echo Adding legaltrack/settings.py and render.yaml...
git add legaltrack/settings.py render.yaml

echo Committing with improved IPv4 resolution...
git commit -m "Fix: Improve serverless IPv4 DNS resolution with AF_INET explicit family and debug logging"

echo Pushing to master...
git push origin master

echo Done! Render will auto-redeploy.
pause
