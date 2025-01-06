# Note Typewriter

A modern, sleek note-taking application with rich features and a beautiful UI.

## Features

- 🎨 Modern and clean user interface
- 📝 Rich text editing with Markdown support
- 🔍 Full-text search functionality
- 🏷️ Tag system for note organization
- 💾 Auto-save feature
- 👀 Live Markdown preview
- 📱 Responsive and resizable panels

## Installation

1. Make sure you have Python 3.7+ installed on your system
2. Clone this repository
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

### Basic Operations

- **Create a new note**: Click the "New Note" button
- **Save a note**: Click "Save" or wait for auto-save (every 30 seconds)
- **Delete a note**: Select a note and click "Delete"
- **Search notes**: Type in the search bar to filter notes
- **Add tags**: Enter comma-separated tags in the tags field
- **Preview Markdown**: Click "Toggle Preview" to see rendered Markdown

### Keyboard Shortcuts

- `Ctrl+S`: Save current note
- `Ctrl+F`: Focus search bar
- `Ctrl+N`: New note

### Notes Storage

Notes are stored locally in a SQLite database located in your home directory at:
- Windows: `%USERPROFILE%\.note_typewriter\notes.db`
- Linux/Mac: `~/.note_typewriter/notes.db`

## Contributing

Feel free to submit issues and enhancement requests! 