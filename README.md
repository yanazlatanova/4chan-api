# 4chan Archive Analysis Tool

A Python tool to analyze archived threads from 4chan boards using the pychan library, with keyword filtering and country-specific analysis.

## Prerequisites

- Python 3.x
- VS Code (recommended code editor): https://code.visualstudio.com/

### Installing Python

If you don't have Python installed, download it from:
https://www.python.org/downloads/

Make sure to check "Add Python to PATH" during installation on Windows.

## Main Tool: `4chan-api-pychan-archived.py`

This is the primary script for analyzing **archived threads** from 4chan boards. It fetches historical data and filters posts based on keywords and country flags.

### Key Features:
- ✅ **Archived Thread Analysis** - Accesses historical 4chan data
- ✅ **Country Filtering** - Filter posts by poster's country flag (e.g., Denmark)
- ✅ **Keyword Matching** - Search for specific terms in post content
- ✅ **Dual Output** - Generates both JSON and human-readable text files
- ✅ **Comprehensive Statistics** - Shows detailed analysis results

### Other Scripts (Brief Overview):
- `4chan-api-pychan-api.py` - Analyzes live threads using pychan (basic version)
- `4chan-api-official-api.py` - Uses official 4chan API for live threads (advanced control)

## Installation

Install the required library:
```bash
pip install pychan
```

## Usage

### Running the Archive Analysis Tool:

```bash
python 4chan-api-pychan-archived.py
```

**Quick Start:**
1. Open the folder in VS Code
2. Open terminal: Press `Ctrl + `` (backtick) or Terminal → New Terminal
3. Run: `python 4chan-api-pychan-archived.py`

The script will create an `output_pychan_archived/` folder and save results there.

## Configuration !!!

Edit the configuration section at the top of `4chan-api-pychan-archived.py`:

```python
# Keywords to search for
keywords = ["immigrants", "border", "refugees", "asylum", "migration", "illegal", "visa", "citizenship", "deportation"]

# Board to search
board = "pol"  

# Thread processing limit
max_threads = 800  # Real maximum: 3000

# Country filter (optional)
filter_country = "Denmark"  # Set to None for all countries
```

### Important: `max_threads` Setting

- **Default**: `max_threads = 800` (processes 800 out of 3000 available archived threads)
- **Real Maximum**: 3000 archived threads are available on /pol/
- **For Complete Analysis**: Set `max_threads = 3000` to process all archived threads
- **Trade-off**: Higher numbers = more comprehensive data but longer processing time

### Country Filtering

Set `filter_country` to filter posts by poster's country flag:
- `"Denmark"` - Only Danish posts
- `"United States"` - Only US posts  
- `None` - All countries

## Output

The script generates two types of files in the `output_pychan_archived/` directory:

### Generated Files:
- **JSON Format**: `pol_archived_filtered_YYYYMMDD_HHMMSS.json` - Machine-readable data
- **Text Format**: `pol_archived_filtered_YYYYMMDD_HHMMSS.txt` - Human-readable analysis

### Each Filtered Post Includes:
- Thread title and board information
- Post timestamp and poster details (name, ID, country flag)
- Direct URLs to thread and specific post
- Matched keywords that triggered the filter
- Full post content
- File attachments (if any)
- Statistics (original posts, unique threads, country breakdown)

## Example Usage Scenarios

1. **Analyze Danish Immigration Discourse**: 
   - Set `filter_country = "Denmark"`
   - Use immigration-related keywords
   - Process recent archived threads (`max_threads = 800`)

2. **Complete Historical Analysis**:
   - Set `max_threads = 3000` for full coverage
   - Set `filter_country = None` for all countries
   - Expect longer processing time but comprehensive data

3. **Quick Sample Analysis**:
   - Set `max_threads = 100` for fast results
   - Focus on specific keywords of interest

## Documentation

**PyChan Library**: https://github.com/cooperwalbrun/pychan?tab=readme-ov-file
**4chan API**: https://github.com/4chan/4chan-API/blob/master/pages/Catalog.md