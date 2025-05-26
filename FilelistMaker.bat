@echo off
setlocal enabledelayedexpansion

echo === File List Generator (CMD) ===
set /p choice=Do you want to generate the file list in the current directory? (y/n): 

if /i "%choice%"=="y" (
    set "target=%cd%"
) else (
    set /p target=Enter full path of the target directory: 
    if not exist "%target%" (
        echo.
        echo ❌ The directory does not exist.
        pause
        exit /b
    )
)

set "filelist=%target%\filelist.txt"
set "errors="

> "%filelist%" (
    echo %target%
)

rem List files in root
for /f "delims=" %%F in ('dir "%target%" /a:-d /b 2^>nul') do (
    echo %target%\%%F >> "%filelist%"
)

rem List folders and files inside them
for /f "delims=" %%D in ('dir "%target%" /a:d /s /b 2^>nul') do (
    echo %%D >> "%filelist%"
    pushd "%%D" >nul 2>&1
    if errorlevel 1 (
        set "errors=!errors!%%D;"
    ) else (
        for /f "delims=" %%F in ('dir /a:-d /b 2^>nul') do (
            echo %%D\%%F >> "%filelist%"
        )
        popd >nul
    )
)

echo.
echo ✅ File list saved to: %filelist%

if defined errors (
    echo.
    echo ⚠️ Warning: Some folders could not be accessed:
    for %%E in (!errors!) do (
        echo  - %%E
    )
)

pause
