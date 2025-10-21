# 4chan API Scripts

Two Python scripts to fetch and filter posts from 4chan boards with different approaches and dependencies.

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

## Script Options

This repository contains two different approaches to accessing 4chan data:

### 1. `4chan-api-pychan-api.py` - Using PyChan Library
**Easy to use, feature-rich**
- Uses the `pychan` third-party library
- Simplified API with built-in error handling
- Automatic rate limiting and retry logic
- Clean object-oriented interface
- Better for beginners

### 2. `4chan-api-official-api.py` - Raw Official API
**Direct API access, more control**
- Uses only the official 4chan API endpoints
- Raw HTTP requests with `requests` library
- More configurable time ranges and keywords
- No external dependencies (except requests)
- Better for advanced users who want full control

## Installation

### For `4chan-api-pychan-api.py` (PyChan version):
```bash
pip install pychan
```

### For `4chan-api-official-api.py` (Raw API version):
```bash
pip install requests
```
*Note: `requests` is usually pre-installed with Python*

## Usage

### Running the PyChan Version (`4chan-api-pychan-api.py`):
```bash
python 4chan-api-pychan-api.py
```

**Features:**
- Automatically searches /pol/ board
- Fixed date range (yesterday to today)
- Predefined keywords: trump, election, vote, biden, government, president, policy, democrat, republican
- Easy to use but less customizable

### Running the Raw API Version (`4chan-api-official-api.py`):
```bash
python 4chan-api-official-api.py
```

**Features:**
- Fully configurable time ranges (edit the script to modify)
- Customizable keywords list
- Can change board (pol, b, g, etc.)  
- More detailed output and error handling
- No external library dependencies

### How to run either file:

**Using VS Code (Recommended):**
1. Open the folder in VS Code
2. Open the VS Code terminal: Press `Ctrl + `` (backtick) or go to Terminal → New Terminal
3. Run either script:
   ```bash
   python 4chan-api-pychan-api.py
   ```
   or
   ```bash
   python 4chan-api-official-api.py
   ```


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

### PyChan Library Documentation:
For complete documentation of the pychan library, please visit:
https://github.com/cooperwalbrun/pychan?tab=readme-ov-file

### Official 4chan API Documentation:
For the official 4chan API specification and catalog documentation:
https://github.com/4chan/4chan-API/blob/master/pages/Catalog.md

## Configuration

### PyChan Version (`4chan-api-pychan-api.py`):
- **No configuration needed** - runs with default settings
- Searches for predefined political keywords
- Fixed time range (recent posts)

### Raw API Version (`4chan-api-official-api.py`):
Edit the configuration section at the top of the file:

```python
# Keywords to search for
KEYWORDS = ["trump", "election", "vote", "biden"]

# Time range
START_DATE = datetime.now(timezone.utc) - timedelta(hours=6)  # Last 6 hours
END_DATE = datetime.now(timezone.utc)

# Board to search
BOARD = "pol"
```

## Output

Both scripts generate files in the `output/` directory:

### PyChan Version:
- `pol_filtered_YYYYMMDD_HHMMSS.json` - Machine-readable JSON format
- `pol_filtered_YYYYMMDD_HHMMSS.txt` - Human-readable text format

### Raw API Version:
- `pol_filtered_raw_YYYYMMDD_HHMMSS.json` - Machine-readable JSON format  
- `pol_filtered_raw_YYYYMMDD_HHMMSS.txt` - Human-readable text format

Each filtered post includes:
- Thread title and information
- Post timestamp and poster name
- Direct links to the thread and specific post
- Matched keywords
- Full post text (cleaned of HTML tags and 4chan quote links)

## Which Script Should I Use?

**Choose `4chan-api-pychan-api.py` (PyChan) if:**
- ✅ You want something that "just works"
- ✅ You're new to programming
- ✅ You don't need to customize settings much
- ✅ You want built-in error handling

**Choose `4chan-api-official-api.py` (Raw API) if:**
- ✅ You want full control over time ranges
- ✅ You want to customize keywords easily
- ✅ You want to search different boards
- ✅ You prefer minimal dependencies
- ✅ You want to understand how the API works