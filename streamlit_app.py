import streamlit as st
import pandas as pd
import io
from pathlib import Path

st.set_page_config(page_title="File Category Detector", layout="wide")
st.title("📁 File Category Detector")
st.write("Upload files to detect their categories and download the results.")

# Dictionary for category detection based on file extensions
CATEGORY_MAP = {
    '.pdf': 'Document',
    '.doc': 'Document',
    '.docx': 'Document',
    '.txt': 'Document',
    '.xlsx': 'Spreadsheet',
    '.xls': 'Spreadsheet',
    '.csv': 'Spreadsheet',
    '.jpg': 'Image',
    '.jpeg': 'Image',
    '.png': 'Image',
    '.gif': 'Image',
    '.mp4': 'Video',
    '.avi': 'Video',
    '.mov': 'Video',
    '.mp3': 'Audio',
    '.wav': 'Audio',
    '.flac': 'Audio',
    '.zip': 'Archive',
    '.rar': 'Archive',
    '.7z': 'Archive',
}

def detect_category(filename: str) -> str:
    """Detect file category based on extension."""
    ext = Path(filename).suffix.lower()
    return CATEGORY_MAP.get(ext, 'Other')

# Initialize session state for uploaded files
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

if 'results' not in st.session_state:
    st.session_state.results = pd.DataFrame(columns=['Filename', 'Detected Category'])

# File uploader widget
uploaded_files = st.file_uploader(
    "Drop files here or click to select",
    accept_multiple_files=True,
    type=None
)

if uploaded_files:
    # Process uploaded files
    results_data = []
    for uploaded_file in uploaded_files:
        filename = uploaded_file.name
        category = detect_category(filename)
        results_data.append({
            'Filename': filename,
            'Detected Category': category
        })
    
    # Update session state
    st.session_state.results = pd.DataFrame(results_data)

# Display results table
if not st.session_state.results.empty:
    st.subheader("Results")
    st.dataframe(
        st.session_state.results,
        use_container_width=True,
        hide_index=True
    )
    
    # Download CSV button
    csv_data = st.session_state.results.to_csv(index=False)
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv_data,
        file_name="file_categories.csv",
        mime="text/csv"
    )
else:
    st.info("👆 Upload files to get started!")
