import os
import stat
import pwd
import grp
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

__author__ = "https://gitwdhub.com/theredplanetsings"
__date__ = "11/10/2024"

def format_size(size):
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def get_file_metadata(file_path):
    try:
        metadata = {}
        metadata['File Path'] = file_path
        metadata['Absolute Path'] = os.path.abspath(file_path)
        metadata['Size'] = format_size(os.path.getsize(file_path))
        metadata['File Type'] = 'Directory' if os.path.isdir(file_path) else 'File'
        metadata['Permissions'] = stat.filemode(os.stat(file_path).st_mode)
        metadata['Owner'] = pwd.getpwuid(os.stat(file_path).st_uid).pw_name
        metadata['Group'] = grp.getgrgid(os.stat(file_path).st_gid).gr_name
        metadata['Creation Time'] = datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y_%m_%d_%H:%M")
        metadata['Modification Time'] = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y_%m_%d_%H:%M")
        metadata['Access Time'] = datetime.fromtimestamp(os.path.getatime(file_path)).strftime("%Y_%m_%d_%H:%M")
        metadata['Parent Folder'] = os.path.dirname(file_path)
        return metadata
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get metadata: {e}")
        return None

def write_metadata_to_file(metadata, file_format='txt'):
    try:
        current_time = datetime.now().strftime("%Y_%m_%d_%H_%M")
        output_file = f"metadata_{current_time}.{file_format}"
        with open(output_file, 'w') as f:
            if file_format == 'txt':
                for key, value in metadata.items():
                    f.write(f"{key}: {value}\n")
            elif file_format == 'json':
                import json
                json.dump(metadata, f, indent=4)
            elif file_format == 'csv':
                import csv
                writer = csv.writer(f)
                for key, value in metadata.items():
                    writer.writerow([key, value])
        messagebox.showinfo("Success", f"Metadata written to {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to write metadata: {e}")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if file_path:
        metadata_text.delete('1.0', tk.END)
        metadata_text.insert(tk.END, file_path)

def display_metadata(metadata, text_widget):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete('1.0', tk.END)
    for key, value in metadata.items():
        text_widget.insert(tk.END, f"{key}: {value}\n")
    text_widget.config(state=tk.DISABLED)

def on_view_metadata():
    file_path = metadata_text.get('1.0', tk.END).strip()
    if file_path:
        if file_path in metadata_windows:
            try:
                metadata_windows[file_path].deiconify()
            except tk.TclError:
                create_metadata_window(get_file_metadata(file_path), file_path)
        else:
            metadata = get_file_metadata(file_path)
            if metadata:
                create_metadata_window(metadata, file_path)
    else:
        messagebox.showwarning("Warning", "No file path provided. Please select a file first.")

def create_metadata_window(metadata, file_path):
    metadata_window = tk.Toplevel(root)
    metadata_window.title(f"Metadata for {os.path.basename(file_path)}")
    metadata_window.geometry("400x400")
    metadata_window.resizable(True, True)

    metadata_display_text = tk.Text(metadata_window, wrap='word')
    metadata_display_text.pack(pady=10, expand=True, fill='both')
    display_metadata(metadata, metadata_display_text)
    
    save_button = tk.Button(metadata_window, text="Save to File", command=lambda: write_metadata_to_file(metadata))
    save_button.pack(pady=10)

    metadata_windows[file_path] = metadata_window

    def on_close():
        del metadata_windows[file_path]
        metadata_window.destroy()

    metadata_window.protocol("WM_DELETE_WINDOW", on_close)
    
def on_exit():
    root.quit()
def adjust_textbox_height(event):
    lines = int(metadata_text.index('end-1c').split('.')[0])
    metadata_text.config(height=lines)

#Creates the main window
root = tk.Tk()
root.title("Metadata Tool")
root.geometry("400x500")
root.resizable(False, False)

#Creates and places the widgets
select_button = tk.Button(root, text="Select File", command=select_file)
select_button.pack(pady=10)

path_label = tk.Label(root, text="Enter Filepath")
path_label.pack(pady=5)

metadata_text = tk.Text(root, wrap='none', height=1, width=50)
metadata_text.pack(pady=10)
metadata_text.bind('<KeyRelease>', adjust_textbox_height)

view_button = tk.Button(root, text="View Metadata", command=on_view_metadata)
view_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=on_exit)
exit_button.place(x=330, y=10)

#Initialises global variables to store current metadata and file path
metadata_windows = {}

#Runs the application
root.mainloop()
