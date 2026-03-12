@echo off
cd /d c:\Users\gideo\Desktop\Django\Capstone

echo [1/3] Adding changes...
git add legaltrack/settings.py render.yaml
echo.

echo [2/3] Committing - SKIP migrations during build, only at runtime...
git commit -m "Fix: Skip migrations during build (avoid IPv6 errors), only install + collectstatic"
echo.

echo [3/3] Pushing to trigger Render rebuild...
git push origin master
echo.

echo ===== DEPLOYMENT STRATEGY CHANGED =====
echo - Build will NOT try to migrate (no DB connection needed)
echo - App will start even if DB unreachable
echo - IPv4 resolution still enabled for when app runs
echo - You can manually run migrations after app starts
echo.
echo Next step: Check Render logs for [DEBUG-IPv4] output
echo.
pause
