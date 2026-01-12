"""
Main module for the Sales Analytics System.
Orchestrates data reading, cleaning, API integration, analysis, and report generation.
"""

import os
import sys
from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    generate_sales_report
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data
)


def main():
    """
    Main execution function

    Workflow:
    1. Print welcome message
    2. Read sales data file (handle encoding)
    3. Parse and clean transactions
    4. Display filter options to user
       - Show available regions
       - Show transaction amount range
       - Ask if user wants to filter (y/n)
    5. If yes, ask for filter criteria and apply
    6. Validate transactions
    7. Display validation summary
    8. Perform all data analyses (call all functions from Part 2)
    9. Fetch products from API
    10. Enrich sales data with API info
    11. Save enriched data to file
    12. Generate comprehensive report
    13. Print success message with file locations

    Error Handling:
    - Wrap entire process in try-except
    - Display user-friendly error messages
    - Don't let program crash on errors
    """
    try:
        # Welcome message
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)
        print()
        
        # Step 1: Read sales data file
        print("[1/10] Reading sales data...")
        try:
            raw_lines = read_sales_data('data/sales_data.txt')
            if not raw_lines:
                print("✗ Error: No data read from file")
                return
            print(f"✓ Successfully read {len(raw_lines)} transactions")
        except Exception as e:
            print(f"✗ Error reading sales data: {str(e)}")
            return
        print()
        
        # Step 2: Parse and clean transactions
        print("[2/10] Parsing and cleaning data...")
        try:
            transactions = parse_transactions(raw_lines)
            if not transactions:
                print("✗ Error: No transactions parsed")
                return
            print(f"✓ Parsed {len(transactions)} records")
        except Exception as e:
            print(f"✗ Error parsing transactions: {str(e)}")
            return
        print()
        
        # Step 3: Display filter options
        print("[3/10] Filter Options Available:")
        try:
            # Get available regions and amount range from transactions
            regions = sorted(set(t.get('Region', '') for t in transactions if t.get('Region')))
            amounts = [t.get('Quantity', 0) * t.get('UnitPrice', 0) for t in transactions 
                      if isinstance(t.get('Quantity'), (int, float)) and isinstance(t.get('UnitPrice'), (int, float))]
            
            if amounts:
                min_amount = min(amounts)
                max_amount = max(amounts)
                print(f"Regions: {', '.join(regions)}")
                print(f"Amount Range: ₹{min_amount:,.2f} - ₹{max_amount:,.2f}")
            else:
                print(f"Regions: {', '.join(regions)}")
                print("Amount Range: N/A")
        except Exception as e:
            print(f"✗ Error getting filter options: {str(e)}")
            regions = []
            amounts = []
        
        print()
        filter_choice = input("Do you want to filter data? (y/n): ").strip().lower()
        print()
        
        # Step 4: Apply filters if requested
        region_filter = None
        min_amount_filter = None
        max_amount_filter = None
        
        if filter_choice == 'y':
            try:
                # Ask for region filter
                if regions:
                    region_input = input(f"Enter region to filter (or press Enter to skip): ").strip()
                    if region_input and region_input in regions:
                        region_filter = region_input
                
                # Ask for amount filters
                min_input = input("Enter minimum amount (or press Enter to skip): ").strip()
                if min_input:
                    try:
                        min_amount_filter = float(min_input)
                    except ValueError:
                        print("Invalid minimum amount, skipping...")
                
                max_input = input("Enter maximum amount (or press Enter to skip): ").strip()
                if max_input:
                    try:
                        max_amount_filter = float(max_input)
                    except ValueError:
                        print("Invalid maximum amount, skipping...")
                
                print()
            except Exception as e:
                print(f"✗ Error getting filter input: {str(e)}")
                print("Continuing without filters...")
                print()
        else:
            print()
        
        # Step 5: Validate transactions
        print("[4/10] Validating transactions...")
        try:
            if filter_choice == 'y' and (region_filter or min_amount_filter is not None or max_amount_filter is not None):
                valid_transactions, invalid_count, filter_summary = validate_and_filter(
                    transactions,
                    region=region_filter,
                    min_amount=min_amount_filter,
                    max_amount=max_amount_filter
                )
            else:
                valid_transactions, invalid_count, filter_summary = validate_and_filter(transactions)
            
            print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")
        except Exception as e:
            print(f"✗ Error validating transactions: {str(e)}")
            # Continue with all transactions if validation fails
            valid_transactions = transactions
            invalid_count = 0
        print()
        
        # Step 6: Perform all data analyses
        print("[5/10] Analyzing sales data...")
        try:
            # Call all analysis functions (they don't need to be stored, just called)
            total_revenue = calculate_total_revenue(valid_transactions)
            region_stats = region_wise_sales(valid_transactions)
            top_products = top_selling_products(valid_transactions, n=5)
            customer_stats = customer_analysis(valid_transactions)
            daily_trend = daily_sales_trend(valid_transactions)
            peak_day = find_peak_sales_day(valid_transactions)
            low_performers = low_performing_products(valid_transactions, threshold=10)
            
            print("✓ Analysis complete")
        except Exception as e:
            print(f"✗ Error during analysis: {str(e)}")
        print()
        
        # Step 7: Fetch products from API
        print("[6/10] Fetching product data from API...")
        try:
            api_products = fetch_all_products()
            if api_products:
                print(f"✓ Fetched {len(api_products)} products")
            else:
                print("✗ No products fetched from API")
                api_products = []
        except Exception as e:
            print(f"✗ Error fetching products: {str(e)}")
            api_products = []
        print()
        
        # Step 8: Enrich sales data
        print("[7/10] Enriching sales data...")
        enriched_transactions = []
        try:
            if api_products:
                product_mapping = create_product_mapping(api_products)
                enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
                
                # Calculate enrichment stats
                total_enriched = len(enriched_transactions)
                successful = sum(1 for t in enriched_transactions if t.get('API_Match') == True)
                success_rate = (successful / total_enriched * 100) if total_enriched > 0 else 0
                print(f"✓ Enriched {successful}/{total_enriched} transactions ({success_rate:.1f}%)")
            else:
                print("✗ Skipping enrichment (no API products available)")
                enriched_transactions = valid_transactions
        except Exception as e:
            print(f"✗ Error enriching data: {str(e)}")
            enriched_transactions = valid_transactions
        print()
        
        # Step 9: Save enriched data (already done in enrich_sales_data, but confirm)
        print("[8/10] Saving enriched data...")
        try:
            enriched_file = 'data/enriched_sales_data.txt'
            if os.path.exists(enriched_file):
                print(f"✓ Saved to: {enriched_file}")
            else:
                print("✗ Enriched data file not found")
        except Exception as e:
            print(f"✗ Error checking enriched data file: {str(e)}")
        print()
        
        # Step 10: Generate comprehensive report
        print("[9/10] Generating report...")
        try:
            report_file = 'output/sales_report.txt'
            generate_sales_report(valid_transactions, enriched_transactions, report_file)
            if os.path.exists(report_file):
                print(f"✓ Report saved to: {report_file}")
            else:
                print("✗ Report file not found")
        except Exception as e:
            print(f"✗ Error generating report: {str(e)}")
        print()
        
        # Step 11: Success message
        print("[10/10] Process Complete!")
        print("=" * 40)
        print()
        print("Generated Files:")
        if os.path.exists('data/enriched_sales_data.txt'):
            print(f"  - data/enriched_sales_data.txt")
        if os.path.exists('output/sales_report.txt'):
            print(f"  - output/sales_report.txt")
        print()
        print("=" * 40)
        
    except KeyboardInterrupt:
        print("\n\n✗ Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
