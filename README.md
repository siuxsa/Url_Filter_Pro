# URL Filter Pro 🔍

A powerful terminal-based tool for intelligent URL filtering with multiple filtering strategies and colorful interface.

![Demo Banner](https://raw.githubusercontent.com/siuxsa/Url_Filter_Pro/refs/heads/main/Assest/Screenshot%202025-03-05%20223425.png)

## Features 🚀

1. **Keyword-based Filtering**  
   - Filter URLs containing specified keywords
   - Keep one unique URL per keyword while preserving non-matching URLs
   - Case-sensitive keyword matching

2. **Parameter-based Filtering**  
   - Analyze URLs based on query parameters
   - Keep one unique URL per parameter name
   - Ignores parameter values for filtering

3. **Parameter Value Filtering**  
   - Search for keywords within parameter names/values
   - Show URLs containing keywords in query parameters
   - Full parameter content scanning

4. **Parameter Presence Filtering**  
   - Separate URLs with parameters from clean URLs
   - Filter out all parameter-less URLs

## Installation ⚙️

**Requirements:**  
- Python 3.6+
- Linux/macOS terminal (recommended)
- Windows: Use WSL/PowerShell with [pygments](https://pypi.org/project/pygments/)

```bash
# Install required packages
pip install colorama
```

## Usage 🖥️

```bash
python3 url_filter_pro.py
```
## Key Benefits 💡

  - Efficiency: Process thousands of URLs in seconds

  - Precision: Multiple filtering strategies for different needs

  - Flexibility: Combine with other CLI tools (grep, awk, etc.)

  - Organization: Clean up URL lists for penetration testing

  - Audit: Identify tracking parameters in marketing URLs

  - Research: Analyze URL structures for web scraping

<br></br>

HAPPY HUNTING--🍃
