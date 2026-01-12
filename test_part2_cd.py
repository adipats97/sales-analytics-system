"""
Test script for Part 2 functions (c and d):
- top_selling_products
- customer_analysis
"""

from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, top_selling_products, customer_analysis

def main():
    print("=" * 80)
    print("Testing Part 2 Functions (c & d)")
    print("=" * 80)
    print()
    
    # Read and parse data
    print("1. Reading and parsing data...")
    raw_lines = read_sales_data('data/sales_data.txt')
    transactions = parse_transactions(raw_lines)
    print(f"   ✓ Parsed {len(transactions)} transactions")
    print()
    
    # Test top_selling_products
    print("2. Testing top_selling_products(transactions, n=5)...")
    print("-" * 80)
    top_products = top_selling_products(transactions, n=5)
    print(f"   Returned {len(top_products)} products")
    print()
    
    # Verify structure
    print("   Verifying output structure...")
    assert isinstance(top_products, list), "Should return a list"
    assert len(top_products) == 5, f"Should return 5 products, got {len(top_products)}"
    
    for i, product_tuple in enumerate(top_products):
        assert isinstance(product_tuple, tuple), f"Item {i} should be a tuple"
        assert len(product_tuple) == 3, f"Tuple {i} should have 3 elements"
        product_name, total_quantity, total_revenue = product_tuple
        assert isinstance(product_name, str), f"ProductName should be string"
        assert isinstance(total_quantity, int), f"TotalQuantity should be int"
        assert isinstance(total_revenue, float), f"TotalRevenue should be float"
        print(f"   {i+1}. {product_name}: Quantity={total_quantity}, Revenue=${total_revenue:,.2f}")
    
    # Verify sorting (descending by quantity)
    print()
    print("   Verifying sorting (descending by TotalQuantity)...")
    for i in range(len(top_products) - 1):
        current_qty = top_products[i][1]
        next_qty = top_products[i + 1][1]
        assert current_qty >= next_qty, f"Not sorted correctly: {top_products[i][0]} ({current_qty}) < {top_products[i+1][0]} ({next_qty})"
    print("   ✓ Products are sorted by TotalQuantity in descending order")
    print()
    
    # Test with different n
    print("3. Testing top_selling_products(transactions, n=10)...")
    top_10 = top_selling_products(transactions, n=10)
    assert len(top_10) == 10, f"Should return 10 products, got {len(top_10)}"
    print(f"   ✓ Returned {len(top_10)} products correctly")
    print()
    
    # Test customer_analysis
    print("4. Testing customer_analysis(transactions)...")
    print("-" * 80)
    customer_stats = customer_analysis(transactions)
    print(f"   Customers found: {len(customer_stats)}")
    print()
    
    # Verify structure
    print("   Verifying output structure...")
    required_keys = ['total_spent', 'purchase_count', 'avg_order_value', 'products_bought']
    
    for customer_id, stats in list(customer_stats.items())[:3]:  # Check first 3
        print(f"   {customer_id}:")
        for key in required_keys:
            assert key in stats, f"Missing key '{key}' in customer {customer_id}"
        
        assert isinstance(stats['total_spent'], float), "total_spent should be float"
        assert isinstance(stats['purchase_count'], int), "purchase_count should be int"
        assert isinstance(stats['avg_order_value'], float), "avg_order_value should be float"
        assert isinstance(stats['products_bought'], list), "products_bought should be list"
        
        # Verify products_bought contains unique items
        assert len(stats['products_bought']) == len(set(stats['products_bought'])), \
            f"products_bought should contain unique items for {customer_id}"
        
        # Verify avg_order_value calculation
        expected_avg = round(stats['total_spent'] / stats['purchase_count'], 2)
        assert abs(stats['avg_order_value'] - expected_avg) < 0.01, \
            f"avg_order_value incorrect for {customer_id}: expected {expected_avg}, got {stats['avg_order_value']}"
        
        print(f"     total_spent: ${stats['total_spent']:,.2f}")
        print(f"     purchase_count: {stats['purchase_count']}")
        print(f"     avg_order_value: ${stats['avg_order_value']:,.2f}")
        print(f"     products_bought: {stats['products_bought']}")
        print()
    
    # Verify sorting (descending by total_spent)
    print("   Verifying sorting (descending by total_spent)...")
    customers_list = list(customer_stats.keys())
    for i in range(len(customers_list) - 1):
        current_spent = customer_stats[customers_list[i]]['total_spent']
        next_spent = customer_stats[customers_list[i + 1]]['total_spent']
        assert current_spent >= next_spent, \
            f"Not sorted correctly: {customers_list[i]} (${current_spent}) < {customers_list[i+1]} (${next_spent})"
    print("   ✓ Customers are sorted by total_spent in descending order")
    print()
    
    print("=" * 80)
    print("✓✓✓ ALL TESTS PASSED ✓✓✓")
    print("=" * 80)

if __name__ == "__main__":
    main()

