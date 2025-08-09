# FileUtilityApp

A utility for conveniently combining and comparing files and folders based on Tkinter. It works on Windows and can be on macOS and Linux.

## Features

- Combining multiple files or all files in a selected folder
- Filtering by extension and recursive traversal of subfolders
- Optional splitting of the result by number of lines or size (MB)
- Byte-by-byte comparison of two files
- Comparison of two folders with output of different, missing and additional files, as well as recursive traversal of subfolders

---
## Requirements

- Python 3.6 and higher
- The 'tkinter` library (usually included in the standard Python package)
- Standard modules `os` and `filecmp`
---
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com /<your-username>/file-utility-app.git
   cd file-utility-app
   ```
2. Create and activate a virtual environment:

   Linux/macOS:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   Windows (PowerShell):
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install the dependencies (if additional packages are needed):
   ```bash
   pip install -r requirements.txt
   ```
   > There are no additional packages in the current version — `tkinter`, `os` and `filecmp` are included in the standard library.

---
## Launch

```bash
python fff.txt
```
If you renamed the file, for example, to `file_utility_app.py `:
```bash
python file_utility_app.py
```
---
## Usage

### Merge Files mode

1. Select the "Merge files" option.
2. In the "Files" section/Folder" select what exactly you want to add:
   - **Files** — the dialog for selecting individual files opens.
   - **Folder** — opens a directory tree with the ability to filter by extension and recursion.
3. If desired, specify the file extension and enable "Including subfolders".
4. Add the files to the list and delete any unnecessary ones by clicking "Delete selected".
5. To split the result, check the box "Divide the result into parts", specify "lines" (lines) or "mb" (megabytes) and the number.
6. Click **Merge** and specify the name of the output file.

### Compare Files/Folders mode

1. Switch to "Compare files/Folders".
2. Use the "Select first" and "Select second" buttons to specify two paths (files or folders).
3. Click **Compare**.
4. The result (identical or a list of differences) will be displayed in the text area.

---
## Screenshots

<img src="2.png" alt="Merge files" width="600"/>  
<img src="1.png" alt="File/folder comparison" width="600"/>
---