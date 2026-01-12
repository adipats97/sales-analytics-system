"""
API handler module for fetching product information from external APIs.
Uses DummyJSON API: https://dummyjson.com/products
"""

import requests
from typing import Dict, Optional, List
import json


def fetch_product_info(product_id: str, api_base_url: str = 'https://dummyjson.com/products') -> Optional[Dict]:
    """
    Fetch product information from DummyJSON API.
    
    Args:
        product_id: Product ID (e.g., 'P101' -> extracts 101, 'P102' -> extracts 102)
        api_base_url: Base URL for the API (default: DummyJSON)
    
    Returns:
        Dictionary containing product information, or None if fetch fails
        
    Example response:
        {
            'product_id': 'P101',
            'api_status': 'success',
            'data': {
                'id': 1,
                'title': 'iPhone 9',
                'description': 'An apple mobile...',
                'price': 549,
                'category': 'smartphones',
                'brand': 'Apple',
                'rating': 4.69,
                'stock': 94
            }
        }
    """
    # Extract numeric ID from product_id (e.g., 'P101' -> 101)
    try:
        # Remove 'P' prefix and convert to int
        numeric_id = int(product_id.replace('P', '').replace('p', ''))
    except (ValueError, AttributeError):
        return {
            'product_id': product_id,
            'api_status': 'error',
            'message': f'Invalid product ID format: {product_id}'
        }
    
    # Construct API URL for single product
    api_url = f"{api_base_url}/{numeric_id}"
    
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Return standardized product info structure
            return {
                'product_id': product_id,
                'api_status': 'success',
                'data': data
            }
        elif response.status_code == 404:
            return {
                'product_id': product_id,
                'api_status': 'error',
                'error_code': 404,
                'message': f'Product not found (ID: {numeric_id})'
            }
        else:
            return {
                'product_id': product_id,
                'api_status': 'error',
                'error_code': response.status_code,
                'message': 'API request failed'
            }
    except requests.exceptions.RequestException as e:
        # Return error if API is unavailable
        return {
            'product_id': product_id,
            'api_status': 'error',
            'message': f'API request failed: {str(e)}'
        }
    except Exception as e:
        return {
            'product_id': product_id,
            'api_status': 'error',
            'message': str(e)
        }


def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    
    Expected Output Format:
    [
        {
            'id': 1,
            'title': 'iPhone 9',
            'category': 'smartphones',
            'brand': 'Apple',
            'price': 549,
            'rating': 4.69
        },
        ...
    ]
    
    Requirements:
    - Fetch all available products (use limit=100)
    - Handle connection errors with try-except
    - Return empty list if API fails
    - Print status message (success/failure)
    """
    api_url = 'https://dummyjson.com/products?limit=100'
    
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"✓ Successfully fetched {len(products)} products from API")
            return products
        else:
            print(f"✗ API request failed with status code: {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        print("✗ Connection error: Unable to connect to API")
        return []
    except requests.exceptions.Timeout:
        print("✗ Timeout error: API request took too long")
        return []
    except requests.exceptions.RequestException as e:
        print(f"✗ Request error: {str(e)}")
        return []
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        return []


def search_products(query: str, api_base_url: str = 'https://dummyjson.com/products') -> Optional[Dict]:
    """
    Search products by query string.
    
    Args:
        query: Search query string
        api_base_url: Base URL for the API (default: DummyJSON)
    
    Returns:
        Dictionary containing matching products, or None if fetch fails
    """
    api_url = f"{api_base_url}/search?q={query}"
    
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                'api_status': 'error',
                'error_code': response.status_code,
                'message': 'Search failed'
            }
    except requests.exceptions.RequestException as e:
        return {
            'api_status': 'error',
            'message': f'API request failed: {str(e)}'
        }
    except Exception as e:
        return {
            'api_status': 'error',
            'message': str(e)
        }


def fetch_multiple_products(product_ids: list, api_base_url: str = 'https://dummyjson.com/products') -> Dict[str, Dict]:
    """
    Fetch information for multiple products.
    
    Args:
        product_ids: List of product IDs to fetch (e.g., ['P101', 'P102'])
        api_base_url: Base URL for the API (default: DummyJSON)
    
    Returns:
        Dictionary mapping product IDs to their information
    """
    results = {}
    for product_id in product_ids:
        results[product_id] = fetch_product_info(product_id, api_base_url)
    return results


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    Parameters: api_products from fetch_all_products()
    Returns: dictionary mapping product IDs to info
    
    Expected Output Format:
    {
        1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},
        2: {'title': 'iPhone X', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.44},
        ...
    }
    """
    product_mapping = {}
    
    for product in api_products:
        if isinstance(product, dict) and 'id' in product:
            product_id = product['id']
            product_mapping[product_id] = {
                'title': product.get('title', ''),
                'category': product.get('category', ''),
                'brand': product.get('brand', ''),
                'rating': product.get('rating', 0.0)
            }
    
    return product_mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    Parameters:
    - transactions: list of transaction dictionaries
    - product_mapping: dictionary from create_product_mapping()
    Returns: list of enriched transaction dictionaries
    
    Expected Output Format (each transaction):
    {
        'TransactionID': 'T001',
        'Date': '2024-12-01',
        'ProductID': 'P101',
        'ProductName': 'Laptop',
        'Quantity': 2,
        'UnitPrice': 45000.0,
        'CustomerID': 'C001',
        'Region': 'North',
        # NEW FIELDS ADDED FROM API:
        'API_Category': 'laptops',
        'API_Brand': 'Apple',
        'API_Rating': 4.7,
        'API_Match': True  # True if enrichment successful, False otherwise
    }
    
    Enrichment Logic:
    - Extract numeric ID from ProductID (P101 → 101, P5 → 5)
    - If ID exists in product_mapping, add API fields
    - If ID doesn't exist, set API_Match to False and other fields to None
    - Handle all errors gracefully
    
    File Output:
    - Save enriched data to 'data/enriched_sales_data.txt'
    - Use same pipe-delimited format
    - Include new columns in header
    """
    enriched_transactions = []
    
    for transaction in transactions:
        # Create a copy of the transaction
        enriched = transaction.copy()
        
        # Extract numeric ID from ProductID (P101 → 101, P5 → 5)
        try:
            product_id_str = transaction.get('ProductID', '')
            # Remove 'P' prefix (case insensitive) and convert to int
            numeric_id = int(product_id_str.replace('P', '').replace('p', '').replace('P', ''))
        except (ValueError, AttributeError, TypeError):
            numeric_id = None
        
        # Check if product exists in mapping
        if numeric_id is not None and numeric_id in product_mapping:
            product_info = product_mapping[numeric_id]
            enriched['API_Category'] = product_info.get('category', '')
            enriched['API_Brand'] = product_info.get('brand', '')
            enriched['API_Rating'] = product_info.get('rating', 0.0)
            enriched['API_Match'] = True
        else:
            # Product not found in mapping
            enriched['API_Category'] = None
            enriched['API_Brand'] = None
            enriched['API_Rating'] = None
            enriched['API_Match'] = False
        
        enriched_transactions.append(enriched)
    
    # Save enriched data to file
    save_enriched_data(enriched_transactions)
    
    return enriched_transactions


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file

    Expected File Format:
    TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
    T001|2024-12-01|P101|Laptop|2|45000.0|C001|North|laptops|Apple|4.7|True
    ...

    Requirements:
    - Create output file with all original + new fields
    - Use pipe delimiter
    - Handle None values appropriately
    """
    import os
    
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Define header
    header = 'TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match'
    
    # Prepare lines
    lines = [header]
    
    for transaction in enriched_transactions:
        # Extract all fields in order
        fields = [
            str(transaction.get('TransactionID', '')),
            str(transaction.get('Date', '')),
            str(transaction.get('ProductID', '')),
            str(transaction.get('ProductName', '')),
            str(transaction.get('Quantity', '')),
            str(transaction.get('UnitPrice', '')),
            str(transaction.get('CustomerID', '')),
            str(transaction.get('Region', '')),
            str(transaction.get('API_Category', '')) if transaction.get('API_Category') is not None else '',
            str(transaction.get('API_Brand', '')) if transaction.get('API_Brand') is not None else '',
            str(transaction.get('API_Rating', '')) if transaction.get('API_Rating') is not None else '',
            str(transaction.get('API_Match', False))
        ]
        
        # Join with pipe delimiter
        line = '|'.join(fields)
        lines.append(line)
    
    # Write to file
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"✓ Enriched data saved to {filename}")
    except Exception as e:
        print(f"✗ Error saving enriched data: {str(e)}")


def get_unique_product_ids(records: list) -> list:
    """
    Extract unique product IDs from sales records.
    
    Args:
        records: List of sales records
    
    Returns:
        List of unique product IDs
    """
    product_ids = set()
    for record in records:
        if 'ProductID' in record:
            product_ids.add(record['ProductID'])
    return sorted(list(product_ids))

