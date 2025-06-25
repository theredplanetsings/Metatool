import os
import stat
import streamlit as st
import pandas as pd
from datetime import datetime
import json
import csv
import io
import platform

__author__ = "https://github.com/theredplanetsings"
__date__ = "06/25/2025"

def format_size(size):
    """Format file size in human readable format"""
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def get_file_metadata(file_path):
    """Extract metadata from a file"""
    try:
        metadata = {}
        file_stat = os.stat(file_path)
        
        metadata['File Name'] = os.path.basename(file_path)
        metadata['File Path'] = file_path
        metadata['Absolute Path'] = os.path.abspath(file_path)
        metadata['Size'] = format_size(os.path.getsize(file_path))
        metadata['File Type'] = 'Directory' if os.path.isdir(file_path) else 'File'
        metadata['Permissions'] = stat.filemode(file_stat.st_mode)
        
        # Handle owner/group based on platform
        if platform.system() != 'Windows':
            try:
                import pwd
                import grp
                metadata['Owner'] = pwd.getpwuid(file_stat.st_uid).pw_name
                metadata['Group'] = grp.getgrgid(file_stat.st_gid).gr_name
            except ImportError:
                metadata['Owner'] = str(file_stat.st_uid)
                metadata['Group'] = str(file_stat.st_gid)
        else:
            metadata['Owner'] = 'N/A (Windows)'
            metadata['Group'] = 'N/A (Windows)'
        
        metadata['Creation Time'] = datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
        metadata['Modification Time'] = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
        metadata['Access Time'] = datetime.fromtimestamp(os.path.getatime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
        metadata['Parent Folder'] = os.path.dirname(file_path)
        
        # Add file extension if it's a file
        if not os.path.isdir(file_path):
            metadata['Extension'] = os.path.splitext(file_path)[1] or 'No extension'
        
        return metadata
    except Exception as e:
        st.error(f"Failed to get metadata for {file_path}: {e}")
        return None

def export_metadata_to_format(metadata_list, file_format='json'):
    """Export metadata to various formats"""
    if file_format == 'json':
        output = json.dumps(metadata_list, indent=4)
        return output, 'application/json', 'json'
    
    elif file_format == 'csv':
        if not metadata_list:
            return "", 'text/csv', 'csv'
        
        # Create CSV with all unique keys
        all_keys = set()
        for metadata in metadata_list:
            all_keys.update(metadata.keys())
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=list(all_keys))
        writer.writeheader()
        for metadata in metadata_list:
            writer.writerow(metadata)
        
        return output.getvalue(), 'text/csv', 'csv'
    
    elif file_format == 'txt':
        output = ""
        for i, metadata in enumerate(metadata_list):
            output += f"=== File {i+1} Metadata ===\n"
            for key, value in metadata.items():
                output += f"{key}: {value}\n"
            output += "\n"
        return output, 'text/plain', 'txt'

def display_metadata_card(metadata, index):
    """Display metadata in a card format"""
    with st.container():
        st.markdown(f"""
        <div style="
            border: 1px solid #ddd; 
            border-radius: 10px; 
            padding: 15px; 
            margin: 10px 0; 
            background-color: #f9f9f9;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
        <h4 style="color: #333; margin-top: 0;">📁 {metadata.get('File Name', 'Unknown File')}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Create two columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**File Information:**")
            st.write(f"• **Type:** {metadata.get('File Type', 'N/A')}")
            st.write(f"• **Size:** {metadata.get('Size', 'N/A')}")
            st.write(f"• **Extension:** {metadata.get('Extension', 'N/A')}")
            st.write(f"• **Permissions:** {metadata.get('Permissions', 'N/A')}")
        
        with col2:
            st.write("**Timestamps:**")
            st.write(f"• **Created:** {metadata.get('Creation Time', 'N/A')}")
            st.write(f"• **Modified:** {metadata.get('Modification Time', 'N/A')}")
            st.write(f"• **Accessed:** {metadata.get('Access Time', 'N/A')}")
        
        # Path information in full width
        st.write("**Path Information:**")
        st.write(f"• **Location:** {metadata.get('File Path', 'N/A')}")
        st.write(f"• **Parent Folder:** {metadata.get('Parent Folder', 'N/A')}")
        
        if platform.system() != 'Windows':
            st.write(f"• **Owner:** {metadata.get('Owner', 'N/A')}")
            st.write(f"• **Group:** {metadata.get('Group', 'N/A')}")

def main():
    st.set_page_config(
        page_title="Metadata Tool",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("File Metadata Analyzer")
    st.markdown("**Upload multiple files to analyze and compare their metadata**")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("Controls")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Choose files to analyze",
            accept_multiple_files=True,
            help="Select one or more files to analyze their metadata"
        )
        
        if uploaded_files:
            st.success(f"Selected {len(uploaded_files)} file(s)")
        
        st.markdown("---")
        
        # Export options
        if uploaded_files:
            st.header("Export Options")
            export_format = st.selectbox(
                "Export format",
                ["json", "csv", "txt"],
                help="Choose format for exporting metadata"
            )
            
            if st.button("📥 Export All Metadata"):
                # Process all files and export
                all_metadata = []
                for uploaded_file in uploaded_files:
                    # Save uploaded file temporarily
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    metadata = get_file_metadata(temp_path)
                    if metadata:
                        all_metadata.append(metadata)
                    
                    # Clean up temp file
                    try:
                        os.remove(temp_path)
                    except:
                        pass
                
                if all_metadata:
                    export_data, mime_type, file_ext = export_metadata_to_format(all_metadata, export_format)
                    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M")
                    filename = f"metadata_export_{current_time}.{file_ext}"
                    
                    st.download_button(
                        label=f"Download {export_format.upper()}",
                        data=export_data,
                        file_name=filename,
                        mime=mime_type
                    )
    
    # Main content area
    if not uploaded_files:
        st.info("👆 Please upload files using the sidebar to get started")
        st.markdown("""
        ### Features:
        - 📁 **Multi-file support**: Analyze multiple files simultaneously
        - 🔍 **Detailed metadata**: File size, permissions, timestamps, and more
        - 📊 **Side-by-side comparison**: Compare metadata across multiple files
        - 📥 **Export options**: Export metadata in JSON, CSV, or TXT format
        - 🌐 **Cross-platform**: Works on Windows, macOS, and Linux
        """)
    else:
        # Process and display metadata for each file
        st.header(f"Analyzing {len(uploaded_files)} file(s)")
        
        # Create tabs for better organization when many files
        if len(uploaded_files) > 3:
            tab_names = [f"File {i+1}" for i in range(len(uploaded_files))]
            tabs = st.tabs(tab_names)
            
            for i, (uploaded_file, tab) in enumerate(zip(uploaded_files, tabs)):
                with tab:
                    # Save uploaded file temporarily
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    metadata = get_file_metadata(temp_path)
                    if metadata:
                        display_metadata_card(metadata, i)
                        
                        # Individual file export
                        col1, col2, col3 = st.columns([1, 1, 2])
                        with col1:
                            if st.button(f"Export JSON", key=f"json_{i}"):
                                export_data, _, _ = export_metadata_to_format([metadata], 'json')
                                st.download_button(
                                    label="Download JSON",
                                    data=export_data,
                                    file_name=f"{uploaded_file.name}_metadata.json",
                                    mime="application/json",
                                    key=f"download_json_{i}"
                                )
                    
                    # Clean up temp file
                    try:
                        os.remove(temp_path)
                    except:
                        pass
        else:
            # Display all files in main area for easier comparison
            for i, uploaded_file in enumerate(uploaded_files):
                # Save uploaded file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                metadata = get_file_metadata(temp_path)
                if metadata:
                    display_metadata_card(metadata, i)
                
                # Clean up temp file
                try:
                    os.remove(temp_path)
                except:
                    pass
                
                # Add separator between files
                if i < len(uploaded_files) - 1:
                    st.markdown("---")

if __name__ == "__main__":
    main()
