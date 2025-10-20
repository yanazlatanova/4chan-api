# 4chan API Script

A simple Python script to fetch and filter posts from 4chan's /pol/ board using the pychan library.

## Prerequisites

- Python 3.x
- VS Code (recommended code editor): https://code.visualstudio.com/

### Checking if Python is installed

To check if Python is installed on your system, open a terminal/command prompt and run:

```bash
python --version
```

or

```bash
python3 --version
```

If Python is installed, you'll see a version number (e.g., `Python 3.9.7`). If not, you'll get an error message.

### Installing Python

If you don't have Python installed, download it from the official website:
https://www.python.org/downloads/

Make sure to check "Add Python to PATH" during installation on Windows.

## Installation

The only installation step required is to install the `pychan` library:

```bash
pip install pychan
```

## Usage

Run the script with Python:

```bash
python 4chan-api.py
```

### How to run the Python file

**Using VS Code:**
1. Open the folder in VS Code
2. Open the VS Code terminal: Press `Ctrl + `` (backtick) or go to Terminal → New Terminal
3. In the VS Code terminal, run:
   ```bash
   python 4chan-api.py
   ```

The script will:
- Fetch posts from the /pol/ board
- Filter posts from the current date
- Search for specific keywords (trump, election, vote, biden, government, president, policy, democrat, republican)
- Save matching posts to both JSON and readable text files


**Alternative method:**
1. **Open a terminal/command prompt:**
   - On Windows: Press `Win + R`, type `cmd`, and press Enter
   - On Mac: Press `Cmd + Space`, type "Terminal", and press Enter
   - On Linux: Press `Ctrl + Alt + T`

2. **Navigate to the script directory:**
   ```bash
   cd path/to/your/4chan-api-folder
   ```

3. **Run the script:**
   ```bash
   python 4chan-api.py
   ```

   If the above doesn't work, try:
   ```bash
   python3 4chan-api.py
   ```

## Documentation

For complete documentation of the pychan library, please visit:
https://github.com/cooperwalbrun/pychan?tab=readme-ov-file

## Output

The script generates two files when matches are found:
- `pol_filtered_YYYYMMDD_HHMMSS.json` - Machine-readable JSON format
- `pol_filtered_YYYYMMDD_HHMMSS.txt` - Human-readable text format

Each filtered post includes:
- Thread title and information
- Post timestamp and poster name
- Direct links to the thread and specific post
- Matched keywords
- Full post text