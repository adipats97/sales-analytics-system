"""
Data processor module for cleaning and validating sales data.
"""

from typing import List, Dict, Tuple
from datetime import datetime


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


def validate_record(record: Dict[str, str]) -> Tuple[bool, str]:
    """
    Validate a sales record according to the cleaning criteria.
    
    Args:
        record: Dictionary containing record fields
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if TransactionID starts with 'T'
    transaction_id = record.get('TransactionID', '').strip()
    if not transaction_id.startswith('T'):
        return False, f"TransactionID '{transaction_id}' does not start with 'T'"
    
    # Check if CustomerID is missing or empty
    customer_id = record.get('CustomerID', '').strip()
    if not customer_id:
        return False, "Missing CustomerID"
    
    # Check if Region is missing or empty
    region = record.get('Region', '').strip()
    if not region:
        return False, "Missing Region"
    
    # Check Quantity
    try:
        quantity_str = record.get('Quantity', '').strip()
        quantity = clean_numeric_value(quantity_str) if ',' in quantity_str else float(quantity_str)
        if quantity <= 0:
            return False, f"Quantity ({quantity}) is less than or equal to 0"
    except (ValueError, AttributeError):
        return False, f"Invalid Quantity: {record.get('Quantity', '')}"
    
    # Check UnitPrice
    try:
        unit_price_str = record.get('UnitPrice', '').strip()
        unit_price = clean_numeric_value(unit_price_str) if ',' in unit_price_str else float(unit_price_str)
        if unit_price <= 0:
            return False, f"UnitPrice ({unit_price}) is less than or equal to 0"
    except (ValueError, AttributeError):
        return False, f"Invalid UnitPrice: {record.get('UnitPrice', '')}"
    
    return True, ""


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

