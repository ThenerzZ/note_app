# Note Typewriter v0.1.0

A modern, sleek note-taking application with rich text editing capabilities and a dark theme.


## Quick Start (Windows)
1. Download `NoteTypewriter-v0.1.0-windows.zip` from the [releases page](../../releases)
2. Extract the zip file
3. Run `Note Typewriter.exe`

## Features

### Text Editing
- Rich text formatting:
  - Bold (Ctrl+B)
  - Italic (Ctrl+I)
  - Underline (Ctrl+U)
  - Font selection
  - Font size adjustment (Ctrl++ to increase, Ctrl+- to decrease)
  - Text alignment (Left, Center, Right)
  - Bullet and numbered lists

### Note Organization
- Category-based organization:
  - All Notes
  - Personal
  - Work
  - Ideas
  - Tasks
- Tag support for better organization
- Full-text search functionality (Ctrl+F)
- Auto-save every 30 seconds

### Markdown Support
- Code blocks with syntax highlighting for:
  - Python
  - JavaScript
  - HTML/CSS
  - Java
  - C++
  - SQL
  - Bash
- Task checkboxes
- Tables
- Image drag & drop
- Live preview (Ctrl+P)
- Full preview mode (Ctrl+Shift+P)

### Export Options
- Markdown (.md)
- HTML (.html)
- PDF (.pdf)
- Word (.docx)

## System Requirements
- Windows 10 or later
- 4GB RAM recommended
- 100MB free disk space

## Data Storage
Notes are stored locally in `%APPDATA%\Note Typewriter\notes.db`

## Keyboard Shortcuts
| Action | Shortcut |
|--------|----------|
| New note | Ctrl+N |
| Save note | Ctrl+S |
| Search | Ctrl+F |
| Bold | Ctrl+B |
| Italic | Ctrl+I |
| Underline | Ctrl+U |
| Increase font size | Ctrl++ |
| Decrease font size | Ctrl+- |
| Toggle preview | Ctrl+P |
| Full preview | Ctrl+Shift+P |

## Known Issues
- PDF export requires wkhtmltopdf to be installed separately
- Some special characters in file names may cause export issues

## Development

### Building from Source
1. Ensure you have Python 3.8 or higher installed
2. Clone the repository:
```bash
git clone https://github.com/yourusername/note_typewriter.git
cd note_typewriter
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the application:
```bash
python main.py
```

### Building the Windows Executable
1. Run the build script:
```bash
.\build_windows.bat
```
2. The executable will be created in the `dist` folder

## Version History

### v0.1.0 (Initial Release)
- Modern dark theme with pink accents
- Rich text editing with formatting toolbar
- Markdown support with live preview
- Category and tag organization
- Full-text search
- Auto-save functionality
- Multiple export formats
- Keyboard shortcuts
- Windows standalone executable 