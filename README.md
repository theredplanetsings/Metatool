# Metadata Tool

This is a simple GUI-based tool for viewing and saving metadata of files. The tool is built using Python and Tkinter.

## Features

- Select a file and view its metadata.
- Metadata includes file path, size, type, permissions, owner, group, creation time, modification time, access time, and parent folder.
- Save metadata to a file in different formats (TXT, JSON, CSV).
- Resizable metadata window with read-only text box.
- Error handling for file operations.
- File filters to limit the types of files that can be selected.

## Requirements

- Python 3.x
- Tkinter (usually included with Python installations)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/theredplanetsings/metadata-tool.git
    ```
2. Navigate to the project directory:
    ```sh
    cd metadata-tool
    ```

## Usage

1. Run the `metatool.py` script:
    ```sh
    python metatool.py
    ```
2. Use the GUI to select a file and view its metadata.
3. Save the metadata to a file in the desired format.

## Code Overview

### `metatool.py`

#### Functions

- `format_size(size)`: Converts file size to a human-readable format.
- `get_file_metadata(file_path)`: Retrieves metadata for the specified file.
- `write_metadata_to_file(metadata, file_format='txt')`: Writes metadata to a file in the specified format (TXT, JSON, CSV).
- `select_file()`: Opens a file dialog to select a file and displays the file path in the text box.
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
