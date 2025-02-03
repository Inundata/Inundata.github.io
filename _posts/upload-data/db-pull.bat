REM 1️.run python
"C:\Users\HERO\anaconda3\envs\db\python.exe" "E:\OneDrive\Github\[i-MAES]\[Collaborate]\[Workspace]\000. github_page\Inundata.github.io\_posts\upload-data\db-pull.py"

REM 2️.run git
cd /d "E:\OneDrive\Github\[i-MAES]\[Collaborate]\[Workspace]\000. github_page\Inundata.github.io"
git add .
git commit -m "자동 업데이트: %date% %time%"
git push -u origin main

echo 작업 완료!
pause