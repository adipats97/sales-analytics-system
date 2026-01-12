"""
Data processor module for cleaning and validating sales data.
"""

from typing import List, Dict, Tuple, Optional
from datetime import datetime


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    
    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    
    Expected Output Format:
    [
        {
            'TransactionID': 'T001',
            'Date': '2024-12-01',
            'ProductID': 'P101',
            'ProductName': 'Laptop',
            'Quantity': 2,           # int type
            'UnitPrice': 45000.0,    # float type
            'CustomerID': 'C001',
            'Region': 'North'
        },
        ...
    ]
    
    Requirements:
    - Split by pipe delimiter '|'
    - Handle commas within ProductName (remove or replace)
    - Remove commas from numeric fields and convert to proper types
    - Convert Quantity to int
    - Convert UnitPrice to float
    - Skip rows with incorrect number of fields
    """
    expected_fields = ['TransactionID', 'Date', 'ProductID', 'ProductName', 
                      'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    expected_field_count = len(expected_fields)
    
    transactions = []
    
    for line in raw_lines:
        # Split by pipe delimiter
        fields = [field.strip() for field in line.split('|')]
        
        # Skip rows with incorrect number of fields
        if len(fields) != expected_field_count:
            continue
        
        try:
            # Create transaction dictionary
            transaction = {}
            for i, field_name in enumerate(expected_fields):
                transaction[field_name] = fields[i]
            
            # Handle commas within ProductName (remove commas)
            if 'ProductName' in transaction:
                transaction['ProductName'] = transaction['ProductName'].replace(',', '')
            
            # Remove commas from Quantity and convert to int
            quantity_str = transaction.get('Quantity', '0').replace(',', '')
            transaction['Quantity'] = int(float(quantity_str))
            
            # Remove commas from UnitPrice and convert to float
            unit_price_str = transaction.get('UnitPrice', '0').replace(',', '')
            transaction['UnitPrice'] = float(unit_price_str)
            
            transactions.append(transaction)
        except (ValueError, TypeError):
            # Skip rows that can't be converted properly
            continue
    
    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters

    Parameters:
    - transactions: list of transaction dictionaries
    - region: filter by specific region (optional)
    - min_amount: minimum transaction amount (Quantity * UnitPrice) (optional)
    - max_amount: maximum transaction amount (optional)

    Returns: tuple (valid_transactions, invalid_count, filter_summary)

    Expected Output Format:
    (
        [list of valid filtered transactions],
        5,  # count of invalid transactions
        {
            'total_input': 100,
            'invalid': 5,
            'filtered_by_region': 20,
            'filtered_by_amount': 10,
            'final_count': 65
        }
    )

    Validation Rules:
    - Quantity must be > 0
    - UnitPrice must be > 0
    - All required fields must be present
    - TransactionID must start with 'T'
    - ProductID must start with 'P'
    - CustomerID must start with 'C'

    Filter Display:
    - Print available regions to user before filtering
    - Print transaction amount range (min/max) to user
    - Show count of records after each filter applied
    """
    required_fields = ['TransactionID', 'Date', 'ProductID', 'ProductName', 
                      'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    
    total_input = len(transactions)
    valid_transactions = []
    invalid_count = 0
    
    # Validate transactions
    for transaction in transactions:
        is_valid = True
        
        # Check all required fields are present
        for field in required_fields:
            if field not in transaction or not transaction[field]:
                is_valid = False
                break
        
        if not is_valid:
            invalid_count += 1
            continue
        
        # Check TransactionID starts with 'T'
        transaction_id = str(transaction.get('TransactionID', '')).strip()
        if not transaction_id.startswith('T'):
            is_valid = False
        
        # Check ProductID starts with 'P'
        product_id = str(transaction.get('ProductID', '')).strip()
        if not product_id.startswith('P'):
            is_valid = False
        
        # Check CustomerID starts with 'C'
        customer_id = str(transaction.get('CustomerID', '')).strip()
        if not customer_id.startswith('C'):
            is_valid = False
        
        # Check Quantity > 0
        try:
            quantity = transaction.get('Quantity', 0)
            if isinstance(quantity, str):
                quantity = int(float(quantity.replace(',', '')))
            if quantity <= 0:
                is_valid = False
        except (ValueError, TypeError):
            is_valid = False
        
        # Check UnitPrice > 0
        try:
            unit_price = transaction.get('UnitPrice', 0)
            if isinstance(unit_price, str):
                unit_price = float(unit_price.replace(',', ''))
            if unit_price <= 0:
                is_valid = False
        except (ValueError, TypeError):
            is_valid = False
        
        if is_valid:
            valid_transactions.append(transaction)
        else:
            invalid_count += 1
    
    # Filter Display: Print available regions
    if valid_transactions:
        available_regions = sorted(set(t.get('Region', '') for t in valid_transactions if t.get('Region')))
        print(f"\nAvailable regions: {', '.join(available_regions)}")
        
        # Calculate transaction amounts
        amounts = [t.get('Quantity', 0) * t.get('UnitPrice', 0) for t in valid_transactions]
        if amounts:
            min_transaction_amount = min(amounts)
            max_transaction_amount = max(amounts)
            print(f"Transaction amount range: ${min_transaction_amount:,.2f} - ${max_transaction_amount:,.2f}")
    
    filtered_by_region = 0
    filtered_by_amount = 0
    
    # Apply region filter
    if region is not None:
        before_region_filter = len(valid_transactions)
        valid_transactions = [t for t in valid_transactions if t.get('Region', '').strip() == str(region).strip()]
        filtered_by_region = before_region_filter - len(valid_transactions)
        print(f"After region filter ('{region}'): {len(valid_transactions)} records")
    
    # Apply amount filters
    if min_amount is not None or max_amount is not None:
        before_amount_filter = len(valid_transactions)
        filtered_transactions = []
        for t in valid_transactions:
            amount = t.get('Quantity', 0) * t.get('UnitPrice', 0)
            if min_amount is not None and amount < min_amount:
                continue
            if max_amount is not None and amount > max_amount:
                continue
            filtered_transactions.append(t)
        valid_transactions = filtered_transactions
        filtered_by_amount = before_amount_filter - len(valid_transactions)
        filter_msg = []
        if min_amount is not None:
            filter_msg.append(f"min=${min_amount:,.2f}")
        if max_amount is not None:
            filter_msg.append(f"max=${max_amount:,.2f}")
        print(f"After amount filter ({', '.join(filter_msg)}): {len(valid_transactions)} records")
    
    final_count = len(valid_transactions)
    
    filter_summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': final_count
    }
    
    return (valid_transactions, invalid_count, filter_summary)


def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    Returns: float (total revenue)
    
    Expected Output: Single number representing sum of (Quantity * UnitPrice)
    Example: 1545000.50
    """
    total_revenue = 0.0
    
    for transaction in transactions:
        try:
            quantity = transaction.get('Quantity', 0)
            unit_price = transaction.get('UnitPrice', 0.0)
            
            # Ensure quantity and unit_price are numeric
            if isinstance(quantity, str):
                quantity = int(float(quantity.replace(',', '')))
            if isinstance(unit_price, str):
                unit_price = float(unit_price.replace(',', ''))
            
            revenue = quantity * unit_price
            total_revenue += revenue
        except (ValueError, TypeError, KeyError):
            # Skip transactions with invalid data
            continue
    
    return float(total_revenue)


def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns: dictionary with region statistics

    Expected Output Format:
    {
        'North': {
            'total_sales': 450000.0,
            'transaction_count': 15,
            'percentage': 29.13
        },
        'South': {...},
        ...
    }

    Requirements:
    - Calculate total sales per region
    - Count transactions per region
    - Calculate percentage of total sales
    - Sort by total_sales in descending order
    """
    # Calculate total revenue first (for percentage calculation)
    total_revenue = calculate_total_revenue(transactions)
    
    # Initialize region statistics
    region_stats = {}
    
    # Process each transaction
    for transaction in transactions:
        try:
            region = transaction.get('Region', '').strip()
            if not region:
                continue
            
            quantity = transaction.get('Quantity', 0)
            unit_price = transaction.get('UnitPrice', 0.0)
            
            # Ensure quantity and unit_price are numeric
            if isinstance(quantity, str):
                quantity = int(float(quantity.replace(',', '')))
            if isinstance(unit_price, str):
                unit_price = float(unit_price.replace(',', ''))
            
            sales_amount = quantity * unit_price
            
            # Initialize region if not exists
            if region not in region_stats:
                region_stats[region] = {
                    'total_sales': 0.0,
                    'transaction_count': 0
                }
            
            # Update region statistics
            region_stats[region]['total_sales'] += sales_amount
            region_stats[region]['transaction_count'] += 1
            
        except (ValueError, TypeError, KeyError):
            # Skip transactions with invalid data
            continue
    
    # Calculate percentage for each region
    for region in region_stats:
        if total_revenue > 0:
            percentage = (region_stats[region]['total_sales'] / total_revenue) * 100
            region_stats[region]['percentage'] = round(percentage, 2)
        else:
            region_stats[region]['percentage'] = 0.0
    
    # Sort by total_sales in descending order
    # Convert to list of tuples, sort, then convert back to dict
    sorted_regions = sorted(
        region_stats.items(),
        key=lambda x: x[1]['total_sales'],
        reverse=True
    )
    
    # Create ordered dictionary
    result = {}
    for region, stats in sorted_regions:
        result[region] = stats
    
    return result


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    Returns: list of tuples
    
    Expected Output Format:
    [
        ('Laptop', 45, 2250000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Mouse', 38, 19000.0),
        ...
    ]
    
    Requirements:
    - Aggregate by ProductName
    - Calculate total quantity sold
    - Calculate total revenue for each product
    - Sort by TotalQuantity descending
    - Return top n products
    """
    # Dictionary to aggregate product data
    product_stats = {}
    
    # Process each transaction
    for transaction in transactions:
        try:
            product_name = transaction.get('ProductName', '').strip()
            if not product_name:
                continue
            
            quantity = transaction.get('Quantity', 0)
            unit_price = transaction.get('UnitPrice', 0.0)
            
            # Ensure quantity and unit_price are numeric
            if isinstance(quantity, str):
                quantity = int(float(quantity.replace(',', '')))
            if isinstance(unit_price, str):
                unit_price = float(unit_price.replace(',', ''))
            
            # Initialize product if not exists
            if product_name not in product_stats:
                product_stats[product_name] = {
                    'total_quantity': 0,
                    'total_revenue': 0.0
                }
            
            # Aggregate quantities and revenue
            product_stats[product_name]['total_quantity'] += quantity
            product_stats[product_name]['total_revenue'] += quantity * unit_price
            
        except (ValueError, TypeError, KeyError):
            # Skip transactions with invalid data
            continue
    
    # Convert to list of tuples: (ProductName, TotalQuantity, TotalRevenue)
    product_list = []
    for product_name, stats in product_stats.items():
        product_list.append((
            product_name,
            stats['total_quantity'],
            stats['total_revenue']
        ))
    
    # Sort by TotalQuantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)
    
    # Return top n products
    return product_list[:n]


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics

    Expected Output Format:
    {
        'C001': {
            'total_spent': 95000.0,
            'purchase_count': 3,
            'avg_order_value': 31666.67,
            'products_bought': ['Laptop', 'Mouse', 'Keyboard']
        },
        'C002': {...},
        ...
    }

    Requirements:
    - Calculate total amount spent per customer
    - Count number of purchases
    - Calculate average order value
    - List unique products bought
    - Sort by total_spent descending
    """
    # Dictionary to store customer statistics
    customer_stats = {}
    
    # Process each transaction
    for transaction in transactions:
        try:
            customer_id = transaction.get('CustomerID', '').strip()
            if not customer_id:
                continue
            
            quantity = transaction.get('Quantity', 0)
            unit_price = transaction.get('UnitPrice', 0.0)
            product_name = transaction.get('ProductName', '').strip()
            
            # Ensure quantity and unit_price are numeric
            if isinstance(quantity, str):
                quantity = int(float(quantity.replace(',', '')))
            if isinstance(unit_price, str):
                unit_price = float(unit_price.replace(',', ''))
            
            # Calculate transaction amount
            transaction_amount = quantity * unit_price
            
            # Initialize customer if not exists
            if customer_id not in customer_stats:
                customer_stats[customer_id] = {
                    'total_spent': 0.0,
                    'purchase_count': 0,
                    'products_bought': set()  # Use set to track unique products
                }
            
            # Update customer statistics
            customer_stats[customer_id]['total_spent'] += transaction_amount
            customer_stats[customer_id]['purchase_count'] += 1
            if product_name:
                customer_stats[customer_id]['products_bought'].add(product_name)
            
        except (ValueError, TypeError, KeyError):
            # Skip transactions with invalid data
            continue
    
    # Calculate average order value and convert set to sorted list
    for customer_id, stats in customer_stats.items():
        # Calculate average order value
        if stats['purchase_count'] > 0:
            stats['avg_order_value'] = round(stats['total_spent'] / stats['purchase_count'], 2)
        else:
            stats['avg_order_value'] = 0.0
        
        # Convert products_bought set to sorted list
        stats['products_bought'] = sorted(list(stats['products_bought']))
    
    # Sort by total_spent in descending order
    # Convert to list of tuples, sort, then convert back to dict
    sorted_customers = sorted(
        customer_stats.items(),
        key=lambda x: x[1]['total_spent'],
        reverse=True
    )
    
    # Create ordered dictionary
    result = {}
    for customer_id, stats in sorted_customers:
        result[customer_id] = stats
    
    return result


def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    Returns: dictionary sorted by date
    
    Expected Output Format:
    {
        '2024-12-01': {
            'revenue': 125000.0,
            'transaction_count': 8,
            'unique_customers': 6
        },
        '2024-12-02': {...},
        ...
    }
    
    Requirements:
    - Group by date
    - Calculate daily revenue
    - Count daily transactions
    - Count unique customers per day
    - Sort chronologically
    """
    # Dictionary to store daily statistics
    daily_stats = {}
    
    # Process each transaction
    for transaction in transactions:
        try:
            date = transaction.get('Date', '').strip()
            if not date:
                continue
            
            customer_id = transaction.get('CustomerID', '').strip()
            quantity = transaction.get('Quantity', 0)
            unit_price = transaction.get('UnitPrice', 0.0)
            
            # Ensure quantity and unit_price are numeric
            if isinstance(quantity, str):
                quantity = int(float(quantity.replace(',', '')))
            if isinstance(unit_price, str):
                unit_price = float(unit_price.replace(',', ''))
            
            # Calculate transaction revenue
            revenue = quantity * unit_price
            
            # Initialize date if not exists
            if date not in daily_stats:
                daily_stats[date] = {
                    'revenue': 0.0,
                    'transaction_count': 0,
                    'unique_customers': set()
                }
            
            # Update daily statistics
            daily_stats[date]['revenue'] += revenue
            daily_stats[date]['transaction_count'] += 1
            if customer_id:
                daily_stats[date]['unique_customers'].add(customer_id)
            
        except (ValueError, TypeError, KeyError):
            # Skip transactions with invalid data
            continue
    
    # Convert set to count and sort chronologically
    result = {}
    for date in sorted(daily_stats.keys()):  # Sort chronologically
        stats = daily_stats[date]
        result[date] = {
            'revenue': stats['revenue'],
            'transaction_count': stats['transaction_count'],
            'unique_customers': len(stats['unique_customers'])
        }
    
    return result


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    Returns: tuple (date, revenue, transaction_count)
    
    Expected Output Format:
    ('2024-12-15', 185000.0, 12)
    """
    # Use daily_sales_trend to get daily statistics
    daily_stats = daily_sales_trend(transactions)
    
    if not daily_stats:
        return (None, 0.0, 0)
    
    # Find the date with maximum revenue
    peak_date = max(daily_stats.keys(), key=lambda d: daily_stats[d]['revenue'])
    peak_stats = daily_stats[peak_date]
    
    return (
        peak_date,
        peak_stats['revenue'],
        peak_stats['transaction_count']
    )


def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns: list of tuples

    Expected Output Format:
    [
        ('Webcam', 4, 12000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Headphones', 7, 10500.0),
        ...
    ]

    Requirements:
    - Find products with total quantity < threshold
    - Include total quantity and revenue
    - Sort by TotalQuantity ascending
    """
    # Dictionary to aggregate product data
    product_stats = {}
    
    # Process each transaction
    for transaction in transactions:
        try:
            product_name = transaction.get('ProductName', '').strip()
            if not product_name:
                continue
            
            quantity = transaction.get('Quantity', 0)
            unit_price = transaction.get('UnitPrice', 0.0)
            
            # Ensure quantity and unit_price are numeric
            if isinstance(quantity, str):
                quantity = int(float(quantity.replace(',', '')))
            if isinstance(unit_price, str):
                unit_price = float(unit_price.replace(',', ''))
            
            # Initialize product if not exists
            if product_name not in product_stats:
                product_stats[product_name] = {
                    'total_quantity': 0,
                    'total_revenue': 0.0
                }
            
            # Aggregate quantities and revenue
            product_stats[product_name]['total_quantity'] += quantity
            product_stats[product_name]['total_revenue'] += quantity * unit_price
            
        except (ValueError, TypeError, KeyError):
            # Skip transactions with invalid data
            continue
    
    # Filter products with total quantity < threshold
    low_performers = []
    for product_name, stats in product_stats.items():
        if stats['total_quantity'] < threshold:
            low_performers.append((
                product_name,
                stats['total_quantity'],
                stats['total_revenue']
            ))
    
    # Sort by TotalQuantity ascending
    low_performers.sort(key=lambda x: x[1])
    
    return low_performers


def clean_product_name(product_name: str) -> str:
    """
    Remove commas from product names.
    
    Args:
        product_name: Product name that may contain commas
    
    Returns:
        Cleaned product name without commas
    """
    return product_name.replace(',', '')


def clean_numeric_value(value: str) -> float:
    """
    Remove commas from numeric strings and convert to float.
    
    Args:
        value: Numeric string that may contain commas
    
    Returns:
        Float value
    """
    return float(value.replace(',', ''))


def clean_and_validate_data(raw_lines: List[str]) -> Tuple[List[Dict], List[Dict], int, int]:
    """
    Clean and validate sales data from raw file lines.
    
    Args:
        raw_lines: List of lines from the sales data file
    
    Returns:
        Tuple of (valid_records, invalid_records, total_parsed, invalid_count)
    """
    if not raw_lines:
        return [], [], 0, 0
    
    # Parse header (strip BOM if present)
    header_line = raw_lines[0].strip()
    # Remove BOM (Byte Order Mark) if present
    if header_line.startswith('\ufeff'):
        header_line = header_line[1:]
    headers = [h.strip() for h in header_line.split('|')]
    
    valid_records = []
    invalid_records = []
    total_parsed = 0
    
    # Process each data line
    for line in raw_lines[1:]:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        total_parsed += 1
        
        # Split by pipe delimiter
        fields = [f.strip() for f in line.split('|')]
        
        # Create record dictionary
        record = {}
        for i, header in enumerate(headers):
            if i < len(fields):
                record[header] = fields[i]
            else:
                record[header] = ''
        
        # Clean ProductName (remove commas)
        if 'ProductName' in record:
            record['ProductName'] = clean_product_name(record['ProductName'])
        
        # Validate record first (before cleaning numeric fields)
        is_valid, error_msg = validate_record(record)
        
        if is_valid:
            # Clean numeric fields (remove commas and convert to proper types)
            try:
                quantity_str = record['Quantity']
                if ',' in quantity_str:
                    record['Quantity'] = int(clean_numeric_value(quantity_str))
                else:
                    record['Quantity'] = int(float(quantity_str))
            except (ValueError, AttributeError, TypeError):
                invalid_records.append({**record, 'Error': 'Invalid Quantity format'})
                continue
            
            try:
                unit_price_str = record['UnitPrice']
                if ',' in unit_price_str:
                    record['UnitPrice'] = float(clean_numeric_value(unit_price_str))
                else:
                    record['UnitPrice'] = float(unit_price_str)
            except (ValueError, AttributeError, TypeError):
                invalid_records.append({**record, 'Error': 'Invalid UnitPrice format'})
                continue
            
            valid_records.append(record)
        else:
            invalid_records.append({**record, 'Error': error_msg})
    
    invalid_count = len(invalid_records)
    
    return valid_records, invalid_records, total_parsed, invalid_count


def calculate_sales_statistics(valid_records: List[Dict]) -> Dict:
    """
    Calculate sales statistics from valid records.
    
    Args:
        valid_records: List of valid sales records
    
    Returns:
        Dictionary containing various sales statistics
    """
    if not valid_records:
        return {
            'total_revenue': 0,
            'total_transactions': 0,
            'average_transaction_value': 0,
            'top_product': None,
            'top_region': None,
            'top_customer': None
        }
    
    # Calculate total revenue
    total_revenue = sum(record['Quantity'] * record['UnitPrice'] for record in valid_records)
    total_transactions = len(valid_records)
    average_transaction_value = total_revenue / total_transactions if total_transactions > 0 else 0
    
    # Find top product by revenue
    product_revenue = {}
    for record in valid_records:
        product = record.get('ProductName', 'Unknown')
        revenue = record['Quantity'] * record['UnitPrice']
        product_revenue[product] = product_revenue.get(product, 0) + revenue
    
    top_product = max(product_revenue.items(), key=lambda x: x[1]) if product_revenue else (None, 0)
    
    # Find top region by revenue
    region_revenue = {}
    for record in valid_records:
        region = record.get('Region', 'Unknown')
        revenue = record['Quantity'] * record['UnitPrice']
        region_revenue[region] = region_revenue.get(region, 0) + revenue
    
    top_region = max(region_revenue.items(), key=lambda x: x[1]) if region_revenue else (None, 0)
    
    # Find top customer by revenue
    customer_revenue = {}
    for record in valid_records:
        customer = record.get('CustomerID', 'Unknown')
        revenue = record['Quantity'] * record['UnitPrice']
        customer_revenue[customer] = customer_revenue.get(customer, 0) + revenue
    
    top_customer = max(customer_revenue.items(), key=lambda x: x[1]) if customer_revenue else (None, 0)
    
    result = {
        'total_revenue': total_revenue,
        'total_transactions': total_transactions,
        'average_transaction_value': average_transaction_value,
        'top_product': {'name': top_product[0], 'revenue': top_product[1]} if top_product[0] else None,
        'top_region': {'name': top_region[0], 'revenue': top_region[1]} if top_region[0] else None,
        'top_customer': {'id': top_customer[0], 'revenue': top_customer[1]} if top_customer[0] else None,
        'product_revenue': product_revenue,
        'region_revenue': region_revenue,
        'customer_revenue': customer_revenue
    }
    return result

