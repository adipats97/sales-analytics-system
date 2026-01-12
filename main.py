"""
Main module for the Sales Analytics System.
Orchestrates data reading, cleaning, API integration, analysis, and report generation.
"""

import os
import sys
from datetime import datetime
from utils.file_handler import read_file, write_file, ensure_output_directory
from utils.data_processor import clean_and_validate_data, calculate_sales_statistics
from utils.api_handler import get_unique_product_ids, fetch_multiple_products


def generate_report(valid_records: list, invalid_records: list, statistics: dict, 
                   product_info: dict = None) -> str:
    """
    Generate a comprehensive sales analytics report.
    
    Args:
        valid_records: List of valid sales records
        invalid_records: List of invalid sales records
        statistics: Dictionary containing sales statistics
        product_info: Optional dictionary of product information from API
    
    Returns:
        Formatted report string
    """
    report = []
    report.append("=" * 80)
    report.append("SALES ANALYTICS REPORT")
    report.append("=" * 80)
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Data Cleaning Summary
    report.append("-" * 80)
    report.append("DATA CLEANING SUMMARY")
    report.append("-" * 80)
    report.append(f"Total records parsed: {len(valid_records) + len(invalid_records)}")
    report.append(f"Invalid records removed: {len(invalid_records)}")
    report.append(f"Valid records after cleaning: {len(valid_records)}")
    report.append("")
    
    # Sales Statistics
    report.append("-" * 80)
    report.append("SALES STATISTICS")
    report.append("-" * 80)
    report.append(f"Total Revenue: ${statistics['total_revenue']:,.2f}")
    report.append(f"Total Transactions: {statistics['total_transactions']}")
    report.append(f"Average Transaction Value: ${statistics['average_transaction_value']:,.2f}")
    report.append("")
    
    # Top Performers
    report.append("-" * 80)
    report.append("TOP PERFORMERS")
    report.append("-" * 80)
    if statistics['top_product']:
        report.append(f"Top Product by Revenue: {statistics['top_product']['name']} "
                      f"(${statistics['top_product']['revenue']:,.2f})")
    if statistics['top_region']:
        report.append(f"Top Region by Revenue: {statistics['top_region']['name']} "
                      f"(${statistics['top_region']['revenue']:,.2f})")
    if statistics['top_customer']:
        report.append(f"Top Customer by Revenue: {statistics['top_customer']['id']} "
                      f"(${statistics['top_customer']['revenue']:,.2f})")
    report.append("")
    
    # Product Revenue Breakdown
    if statistics.get('product_revenue'):
        report.append("-" * 80)
        report.append("PRODUCT REVENUE BREAKDOWN")
        report.append("-" * 80)
        sorted_products = sorted(statistics['product_revenue'].items(), 
                                key=lambda x: x[1], reverse=True)
        for product, revenue in sorted_products[:10]:  # Top 10 products
            report.append(f"{product}: ${revenue:,.2f}")
        report.append("")
    
    # Region Revenue Breakdown
    if statistics.get('region_revenue'):
        report.append("-" * 80)
        report.append("REGION REVENUE BREAKDOWN")
        report.append("-" * 80)
        sorted_regions = sorted(statistics['region_revenue'].items(), 
                               key=lambda x: x[1], reverse=True)
        for region, revenue in sorted_regions:
            report.append(f"{region}: ${revenue:,.2f}")
        report.append("")
    
    # Invalid Records Summary
    if invalid_records:
        report.append("-" * 80)
        report.append("INVALID RECORDS SUMMARY")
        report.append("-" * 80)
        error_counts = {}
        for record in invalid_records:
            error = record.get('Error', 'Unknown error')
            error_counts[error] = error_counts.get(error, 0) + 1
        
        for error, count in error_counts.items():
            report.append(f"{error}: {count} record(s)")
        report.append("")
    
    # API Integration Status
    if product_info:
        report.append("-" * 80)
        report.append("API INTEGRATION STATUS")
        report.append("-" * 80)
        success_count = sum(1 for info in product_info.values() 
                          if info and info.get('api_status') == 'success')
        mock_count = sum(1 for info in product_info.values() 
                        if info and info.get('api_status') == 'mock')
        error_count = sum(1 for info in product_info.values() 
                         if info and info.get('api_status') == 'error')
        
        report.append(f"Products fetched successfully: {success_count}")
        report.append(f"Products using mock data: {mock_count}")
        report.append(f"Products with API errors: {error_count}")
        report.append("")
    
    report.append("=" * 80)
    
    return "\n".join(report)


def main():
    """
    Main function to orchestrate the sales analytics system.
    """
    # File paths
    data_file = os.path.join('data', 'sales_data.txt')
    output_dir = 'output'
    output_file = os.path.join(output_dir, 'sales_report.txt')
    
    print("Sales Analytics System")
    print("=" * 80)
    print()
    
    # Step 1: Read the sales data file
    print("Step 1: Reading sales data file...")
    raw_lines = read_file(data_file)
    
    if raw_lines is None:
        print("Error: Could not read sales data file.")
        sys.exit(1)
    
    print(f"Successfully read {len(raw_lines)} lines from file.")
    print()
    
    # Step 2: Clean and validate data
    print("Step 2: Cleaning and validating data...")
    valid_records, invalid_records, total_parsed, invalid_count = clean_and_validate_data(raw_lines)
    
    print(f"Total records parsed: {total_parsed}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_records)}")
    print()
    
    # Step 3: Fetch product information from API
    print("Step 3: Fetching product information from API...")
    unique_product_ids = get_unique_product_ids(valid_records)
    print(f"Found {len(unique_product_ids)} unique products.")
    
    # Fetch product info (using mock API for demonstration)
    product_info = fetch_multiple_products(unique_product_ids[:5])  # Limit to 5 for demo
    print(f"Fetched information for {len(product_info)} products.")
    print()
    
    # Step 4: Calculate sales statistics
    print("Step 4: Calculating sales statistics...")
    statistics = calculate_sales_statistics(valid_records)
    print("Statistics calculated successfully.")
    print()
    
    # Step 5: Generate report
    print("Step 5: Generating comprehensive report...")
    report = generate_report(valid_records, invalid_records, statistics, product_info)
    
    # Step 6: Save report to file
    print("Step 6: Saving report to file...")
    ensure_output_directory(output_dir)
    
    if write_file(output_file, report):
        print(f"Report saved successfully to: {output_file}")
    else:
        print("Error: Could not save report to file.")
    
    # Also print report to console
    print()
    print(report)
    
    print()
    print("=" * 80)
    print("Sales Analytics System completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()

