@echo off
echo Attempting to delete contents of the folder...

:: First, try to delete the folder and recreate it
rd /s /q "C:\Project\engineeringcodeAuto\automation-project\generated" 2>nul
md "C:\Project\engineeringcodeAuto\automation-project\generated" 2>nul

:: Check if deletion was successful
if exist "C:\Project\engineeringcodeAuto\automation-project\generated" (
    echo Folder contents cleared successfully.
) else (
    echo Failed to clear folder contents. It might be locked by another process.
)

pause
