# Metadata Tool

A comprehensive file metadata analyzer available in both GUI (Tkinter) and web app (Streamlit) versions.

## Features

### Core Features
- Extract detailed file metadata including path, size, type, permissions, timestamps
- Cross-platform support (Windows, macOS, Linux)
- Multiple export formats (TXT, JSON, CSV)
- Error handling for file operations

### Streamlit Web App Features (NEW!)
- **Web-based interface** - No installation required for end users
- **Multi-file support** - Analyze multiple files simultaneously
- **Side-by-side comparison** - Compare metadata across files
- **Modern UI** - Clean, responsive design with file cards
- **Bulk export** - Export all metadata at once
- **Individual exports** - Export metadata for specific files

### Legacy Tkinter GUI Features
- Traditional desktop application interface
- Single file analysis
- Resizable metadata windows

## Requirements

### For Streamlit Web App
- Python 3.7+
- streamlit>=1.28.0
- pandas>=1.5.0

### For Tkinter GUI
- Python 3.x
- Tkinter (usually included with Python installations)

## Installation & Usage

### Streamlit Web App (Recommended)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the web app:**
   ```bash
   streamlit run streamlit_metatool.py
   ```

3. **Open your browser** and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

4. **Upload files** using the sidebar file uploader

5. **Analyze and compare** metadata across multiple files

6. **Export results** in your preferred format (JSON, CSV, TXT)

### Legacy Tkinter GUI

1. **Run the desktop application:**
   ```bash
   python metatool.py
   ```

2. **Select a file** using the file dialog

3. **View metadata** in a popup window

4. **Save metadata** to a file in your desired format

## File Structure

```
Metatool/
├── streamlit_metatool.py    # New Streamlit web app
├── metatool.py             # Original Tkinter GUI
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── LICENSE               # License information
```

## Code Overview

### `streamlit_metatool.py` (New Web App)

#### Key Features
- **Multi-file upload**: Process multiple files simultaneously
- **Responsive design**: Cards layout for easy comparison
- **Export functionality**: Bulk and individual file exports
- **Cross-platform metadata**: Handles Windows/Unix differences gracefully

#### Main Functions
- `get_file_metadata(file_path)`: Enhanced metadata extraction with platform handling
- `display_metadata_card(metadata, index)`: Modern card-based UI display
- `export_metadata_to_format(metadata_list, format)`: Flexible export system
- `main()`: Streamlit app structure and flow

### `metatool.py` (Legacy GUI)

#### Functions
- `format_size(size)`: Converts file size to human-readable format
- `get_file_metadata(file_path)`: Retrieves metadata for specified file
- `write_metadata_to_file(metadata, file_format)`: Writes metadata to file
- `display_metadata(metadata, text_widget)`: Displays metadata in the specified text widget.
- `on_view_metadata()`: Handles the "View Metadata" button click event.
- `create_metadata_window(metadata, file_path)`: Creates a new window to display metadata.
- `on_exit()`: Handles the "Exit" button click event.
- `adjust_textbox_height(event)`: Adjusts the height of the text box based on its content.

#### Global Variables

- `metadata_windows`: A dictionary to store references to open metadata windows.

## Author

- [theredplanetsings](https://github.com/theredplanetsings)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
