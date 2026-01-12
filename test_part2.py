"""
Test script for Part 2 functions:
- calculate_total_revenue
- region_wise_sales
"""

from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, calculate_total_revenue, region_wise_sales

def main():
    print("=" * 80)
    print("Testing Part 2 Functions")
    print("=" * 80)
    print()
    
    # Read and parse data
    print("1. Reading and parsing data...")
    raw_lines = read_sales_data('data/sales_data.txt')
    transactions = parse_transactions(raw_lines)
    print(f"   ✓ Parsed {len(transactions)} transactions")
    print()
    
    # Test calculate_total_revenue
    print("2. Testing calculate_total_revenue(transactions)...")
    print("-" * 80)
    total_revenue = calculate_total_revenue(transactions)
    print(f"   Total Revenue: ${total_revenue:,.2f}")
    print(f"   Type: {type(total_revenue).__name__}")
    assert isinstance(total_revenue, float), "Should return float"
    assert total_revenue > 0, "Total revenue should be positive"
    print("   ✓ Function works correctly")
    print()
    
    # Test region_wise_sales
    print("3. Testing region_wise_sales(transactions)...")
    print("-" * 80)
    region_stats = region_wise_sales(transactions)
    print(f"   Regions found: {list(region_stats.keys())}")
    print()
    
    # Verify structure
    print("   Verifying output structure...")
    for region, stats in region_stats.items():
        print(f"   {region}:")
        assert 'total_sales' in stats, f"Missing 'total_sales' in {region}"
        assert 'transaction_count' in stats, f"Missing 'transaction_count' in {region}"
        assert 'percentage' in stats, f"Missing 'percentage' in {region}"
        
        print(f"     total_sales: ${stats['total_sales']:,.2f}")
        print(f"     transaction_count: {stats['transaction_count']}")
        print(f"     percentage: {stats['percentage']}%")
        print()
    
    # Verify sorting (descending by total_sales)
    print("   Verifying sorting (descending by total_sales)...")
    regions_list = list(region_stats.keys())
    for i in range(len(regions_list) - 1):
        current_sales = region_stats[regions_list[i]]['total_sales']
        next_sales = region_stats[regions_list[i + 1]]['total_sales']
        assert current_sales >= next_sales, f"Not sorted correctly: {regions_list[i]} ({current_sales}) < {regions_list[i + 1]} ({next_sales})"
    print("   ✓ Regions are sorted by total_sales in descending order")
    print()
    
    # Verify percentages sum to approximately 100%
    print("   Verifying percentages...")
    total_percentage = sum(stats['percentage'] for stats in region_stats.values())
    print(f"   Total percentage: {total_percentage:.2f}%")
    assert 99.0 <= total_percentage <= 101.0, f"Percentages should sum to ~100%, got {total_percentage}%"
    print("   ✓ Percentages sum correctly")
    print()
    
    print("=" * 80)
    print("✓✓✓ ALL TESTS PASSED ✓✓✓")
    print("=" * 80)

if __name__ == "__main__":
    main()

