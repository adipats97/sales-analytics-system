# Sales Analytics System

A comprehensive Python-based sales data analytics system that processes sales transactions, integrates with external APIs, performs data analysis, and generates detailed reports.

## Overview

This system is designed to:
- Read and clean messy sales transaction files with various data quality issues
- Fetch real-time product information from external APIs
- Analyze sales patterns and customer behavior
- Generate comprehensive reports for business decision-making

## Project Structure

```
sales-analytics-system/
├── README.md
├── main.py
├── utils/
│   ├── file_handler.py
│   ├── data_processor.py
│   └── api_handler.py
├── data/
│   └── sales_data.txt
├── output/
└── requirements.txt
```

## Features

### Data Cleaning
- Handles pipe-delimited (`|`) file format
- Manages non-UTF-8 encoding issues
- Removes commas from product names (e.g., "Mouse,Wireless" → "MouseWireless")
- Removes commas from numeric values (e.g., "1,500" → 1500)
- Validates and removes invalid records:
  - Missing CustomerID or Region
  - Quantity ≤ 0
  - UnitPrice ≤ 0
  - TransactionID not starting with 'T'
- Skips empty lines

### API Integration
- Fetches product information from external APIs
- Handles API failures gracefully with fallback to mock data
- Supports batch product information retrieval

### Analytics
- Calculates total revenue
- Computes average transaction value
- Identifies top products, regions, and customers by revenue
- Provides detailed revenue breakdowns by product and region

### Report Generation
- Comprehensive sales analytics report
- Data cleaning summary
- Sales statistics and top performers
- Product and region revenue breakdowns
- Invalid records summary
- API integration status

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/adipats97/sales-analytics-system.git
   cd sales-analytics-system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Ensure data file is present:**
   - Place your `sales_data.txt` file in the `data/` directory
   - The file should be in pipe-delimited format with the following structure:
     ```
     TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region
     ```

2. **Run the system:**
   ```bash
   python main.py
   ```

3. **View the report:**
   - The report will be displayed in the console
   - A detailed report will also be saved to `output/sales_report.txt`

## Data Format

The system expects a pipe-delimited file with the following columns:
- `TransactionID`: Must start with 'T'
- `Date`: Transaction date (YYYY-MM-DD format)
- `ProductID`: Product identifier
- `ProductName`: Product name (commas will be removed)
- `Quantity`: Number of items (must be > 0)
- `UnitPrice`: Price per unit (must be > 0, commas will be removed)
- `CustomerID`: Customer identifier (required)
- `Region`: Sales region (required)

## Data Cleaning Criteria

### Records Removed (Invalid):
- Missing CustomerID or Region
- Quantity ≤ 0
- UnitPrice ≤ 0
- TransactionID not starting with 'T'

### Records Cleaned and Kept (Valid):
- Commas in ProductName: Removed, record kept
- Commas in numbers: Removed, converted to numeric, record kept
- Empty lines: Skipped

## Output

The system generates a comprehensive report including:
- Data cleaning summary (total parsed, invalid removed, valid after cleaning)
- Sales statistics (total revenue, transactions, average transaction value)
- Top performers (product, region, customer)
- Product revenue breakdown
- Region revenue breakdown
- Invalid records summary
- API integration status

## Dependencies

- Python 3.7+
- requests (for API integration)

## Error Handling

The system includes robust error handling for:
- File reading errors (encoding issues, file not found)
- Data validation errors
- API connection failures (falls back to mock data)
- Invalid data formats

## Example Output

```
================================================================================
SALES ANALYTICS REPORT
================================================================================
Generated on: 2024-12-30 10:30:00

--------------------------------------------------------------------------------
DATA CLEANING SUMMARY
--------------------------------------------------------------------------------
Total records parsed: 80
Invalid records removed: 10
Valid records after cleaning: 70

--------------------------------------------------------------------------------
SALES STATISTICS
--------------------------------------------------------------------------------
Total Revenue: $2,345,678.90
Total Transactions: 70
Average Transaction Value: $33,509.70
...
```

## Contributing

This is an assignment project. For questions or issues, please refer to the assignment guidelines.

## License

This project is created for educational purposes as part of a Python programming assignment.

