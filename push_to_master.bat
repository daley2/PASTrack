@echo off
cd /d c:\Users\gideo\Desktop\Django\Capstone
echo Adding all changes...
git add -A
echo Committing changes...
git commit -m "Fix: IPv4 resolution for Supabase on Vercel, migrations in build" --allow-empty
echo Pushing to master...
git push origin master
echo Done. Check Vercel dashboard for redeployment.
pause
