"""
Test script to demonstrate the three required functions:
1. read_sales_data
2. parse_transactions
3. validate_and_filter
"""

from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, validate_and_filter

def main():
    print("=" * 80)
    print("Testing Required Functions")
    print("=" * 80)
    print()
    
    # Test 1: read_sales_data
    print("1. Testing read_sales_data(filename)")
    print("-" * 80)
    raw_lines = read_sales_data('data/sales_data.txt')
    print(f"✓ Read {len(raw_lines)} raw lines from file")
    print(f"✓ First line: {raw_lines[0][:60]}...")
    print(f"✓ Last line: {raw_lines[-1][:60]}...")
    print()
    
    # Test 2: parse_transactions
    print("2. Testing parse_transactions(raw_lines)")
    print("-" * 80)
    transactions = parse_transactions(raw_lines)
    print(f"✓ Parsed {len(transactions)} transactions")
    if transactions:
        first = transactions[0]
        print(f"✓ First transaction keys: {list(first.keys())}")
        print(f"✓ First transaction: {first}")
        print(f"✓ Quantity type: {type(first['Quantity']).__name__} (value: {first['Quantity']})")
        print(f"✓ UnitPrice type: {type(first['UnitPrice']).__name__} (value: {first['UnitPrice']})")
    print()
    
    # Test 3: validate_and_filter (no filters)
    print("3. Testing validate_and_filter(transactions)")
    print("-" * 80)
    valid, invalid_count, summary = validate_and_filter(transactions)
    print(f"✓ Valid transactions: {len(valid)}")
    print(f"✓ Invalid count: {invalid_count}")
    print(f"✓ Summary: {summary}")
    print()
    
    # Test 4: validate_and_filter (with region filter)
    print("4. Testing validate_and_filter(transactions, region='North')")
    print("-" * 80)
    valid_north, invalid_count, summary = validate_and_filter(transactions, region='North')
    print(f"✓ Valid transactions after region filter: {len(valid_north)}")
    print(f"✓ Summary: {summary}")
    print()
    
    # Test 5: validate_and_filter (with amount filters)
    print("5. Testing validate_and_filter(transactions, min_amount=10000, max_amount=100000)")
    print("-" * 80)
    valid_amount, invalid_count, summary = validate_and_filter(transactions, min_amount=10000, max_amount=100000)
    print(f"✓ Valid transactions after amount filter: {len(valid_amount)}")
    print(f"✓ Summary: {summary}")
    print()
    
    print("=" * 80)
    print("All tests completed successfully!")
    print("=" * 80)

if __name__ == "__main__":
    main()

