# 🛒 Freak Sales Scraping Project

This project scrapes product sales from multiple e-commerce websites and generates an interactive HTML file with the product information.

## Supported Stores

- Mathom
- Dracotienda
- DungeonMarvels

## Requirements

- 🐍 Python 3.7 or higher

## Installation

Follow these steps to set up and run the project on your local machine.

### 1. Clone this repository

Open a terminal and run the following command to clone the repository:

```bash
git clone https://github.com/javicrcls/freak-scraper.git
cd freak-scraper
```
### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Install Playwright browsers
```bash
python -m playwright install
```

## Usage

To run the script and scrape all supported stores:
```bash
python main.py <keyword>
```

For example, to search for products related to “Arkham Horror”:
```bash
python main.py "Arkham Horror"
```

To scrape a specific store, use the --store option:
```bash
python main.py <keyword> --store <store_name>
```

