@echo off
echo Attempting to delete contents of the folder...
timeout /t 3 >nul

:: Unlock the folder by ending any processes using it
echo Checking for locked processes...
handle64.exe "C:\Project\engineeringcodeAuto\automation-project\generated" > nul
::

LOCK ALL TASK and run tighter debug, note restart dummy way debug ** adjustmentPS do folder reader better`
