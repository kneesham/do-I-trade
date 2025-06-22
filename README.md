# EMR Data Gather

A Python project for gathering and analyzing market data from eBay, focusing on clothing brands and their market performance.

## Project Overview

This project uses web scraping with Playwright to analyze eBay listings for various clothing brands and product categories. It helps identify popular brands and items that are selling well on the eBay marketplace.

## Prerequisites

- Python 3.9 or higher
- macOS, Windows, or Linux

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd emr-data-gather
```

### 2. Set Up Python Virtual Environment

The project uses a Python virtual environment to manage dependencies. A virtual environment has already been configured for this project.

**On macOS/Linux:**
```bash
# The virtual environment is located at: .venv/
# Python executable: .venv/bin/python
# Pip executable: .venv/bin/pip
```

**On Windows:**
```bash
# The virtual environment would be located at: .venv\
# Python executable: .venv\Scripts\python.exe
# Pip executable: .venv\Scripts\pip.exe
```

### 3. Install Dependencies

Install all required Python packages using the requirements.txt file:

**On macOS/Linux:**
```bash
.venv/bin/pip install -r requirements.txt
```

**On Windows:**
```bash
.venv\Scripts\pip install -r requirements.txt
```

Alternatively, you can install packages individually:

**On macOS/Linux:**
```bash
.venv/bin/pip install playwright
.venv/bin/pip install pytest
.venv/bin/pip install pytest-playwright
```

**On Windows:**
```bash
.venv\Scripts\pip install playwright
.venv\Scripts\pip install pytest
.venv\Scripts\pip install pytest-playwright
```

### 4. Install Playwright Browsers

After installing Playwright, you need to install the browser binaries:

**On macOS/Linux:**
```bash
.venv/bin/playwright install
```

**On Windows:**
```bash
.venv\Scripts\playwright install
```

## Project Structure

```
emr-data-gather/
├── README.md
├── requirements.txt                     # Python dependencies
├── python/
│   ├── main.py                           # Main Playwright tests
│   ├── test_ebay_market_cloths.py       # eBay market analysis script
│   └── examples/
│       └── test_playwright_first_example.py  # Basic Playwright example
└── .venv/                               # Python virtual environment
```

## Usage

### Running the eBay Market Analysis

**On macOS/Linux:**
```bash
.venv/bin/python python/test_ebay_market_cloths.py
```

**On Windows:**
```bash
.venv\Scripts\python python\test_ebay_market_cloths.py
```

### Running Basic Playwright Tests

**On macOS/Linux:**
```bash
.venv/bin/python python/main.py
```

**On Windows:**
```bash
.venv\Scripts\python python\main.py
```

### Running with Pytest

If you have pytest installed, you can run the tests using:

**On macOS/Linux:**
```bash
.venv/bin/pytest python/
```

**On Windows:**
```bash
.venv\Scripts\pytest python\
```

## Features

- **eBay Market Analysis**: Scrapes eBay for clothing brand performance data
- **Multi-threaded Processing**: Uses concurrent futures for efficient data gathering
- **Comprehensive Brand Coverage**: Analyzes 100+ popular clothing brands
- **Product Category Classification**: Organizes items into 30+ clothing categories
- **Market Insights**: Provides data on sold listings and pricing trends

## Troubleshooting

### Pip Not Found Error

If you encounter "pip not found" when running `pip` commands:

1. Make sure you're using the full path to pip in the virtual environment
2. On macOS/Linux: Use `.venv/bin/pip` instead of just `pip`
3. On Windows: Use `.venv\Scripts\pip` instead of just `pip`

### Playwright Browser Installation Issues

If Playwright browsers fail to install:

1. Try installing with system permissions
2. Check your internet connection
3. Run: `.venv/bin/playwright install --help` for more options

### Python Version Issues

Ensure you have Python 3.9 or higher:

```bash
.venv/bin/python --version
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure everything works
5. Submit a pull request

## License

[Add your license information here]