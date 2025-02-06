@echo off
chcp 65001 >nul

REM 현재 날짜 및 어제 날짜 계산
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value ^| find "LocalDateTime"') do set datetime=%%I
set today=%datetime:~2,6%
set yesterday=

REM 어제 날짜 계산 (Windows에서는 간단한 방법이 없으므로 PowerShell 사용)
for /f %%I in ('powershell -command "& {(Get-Date).AddDays(-1).ToString('yyMMdd')}"') do set yesterday=%%I

REM 1. Run Python 스크립트
"C:\Users\HERO\anaconda3\envs\db\python.exe" "E:\OneDrive\Github\inundata.github.io\_posts\upload-data\db-pull.py"

REM 2. Git 작업 시작
cd /d "E:\OneDrive\Github\inundata.github.io"

REM Git LFS에서 오늘과 어제의 파일 삭제
for %%F in (temperature_%yesterday%.xlsx temperature_wide_%yesterday%.xlsx temperature_%today%.xlsx temperature_wide_%today%.xlsx) do (
    if exist "%%F" (
        git lfs rm --cached "%%F"
        del "%%F"
    )
)

REM 변경사항 반영
git add .
git commit -m "자동 업데이트: %date% %time%"

REM Git LFS에서 사용되지 않는 파일 정리
echo y | git lfs prune

REM Git 히스토리 정리 (LFS 파일 삭제 후 불필요한 기록 삭제)
echo y | git reflog expire --expire=now --all
echo y | git gc --prune=now

REM GitHub로 Push
@REM git config --global credential.credentialStore dpapi
git push -u origin main

echo 작업 완료!
pause
