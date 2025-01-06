@echo off
setlocal enabledelayedexpansion

echo Installing build dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller pillow

echo Creating application icon...
python create_icon.py
if not exist "app_icon.ico" (
    echo Failed to create icon file
    pause
    exit /b 1
)

echo Building executable...
python -m PyInstaller --clean --noconfirm note_typewriter.spec

echo Creating distribution folder...
if not exist "dist" mkdir dist

echo Moving files to distribution folder...
if exist "dist\Note Typewriter.exe" (
    echo Executable already exists in dist folder
) else (
    move "dist\Note Typewriter\Note Typewriter.exe" "dist\" 2>nul
    if errorlevel 1 (
        echo Failed to move executable
        pause
        exit /b 1
    )
)

echo Cleaning up build files...
rmdir /s /q "build" 2>nul
rmdir /s /q "dist\Note Typewriter" 2>nul

echo Build complete! The executable is in the dist folder.
echo You can now run "Note Typewriter.exe" from the dist folder.
pause 