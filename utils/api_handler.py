"""
API handler module for fetching product information from external APIs.
"""

import requests
from typing import Dict, Optional
import json


def fetch_product_info(product_id: str, api_url: str = None) -> Optional[Dict]:
    """
    Fetch product information from an external API.
    
    Args:
        product_id: Product ID to fetch information for
        api_url: Optional API URL (if None, uses a mock API)
    
    Returns:
        Dictionary containing product information, or None if fetch fails
    """
    # If no API URL provided, use a mock API service
    if api_url is None:
        # Using JSONPlaceholder or a similar mock API
        # For demonstration, we'll use a mock response
        api_url = f"https://jsonplaceholder.typicode.com/posts/{product_id[-1]}"
    
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Return a standardized product info structure
            return {
                'product_id': product_id,
                'api_status': 'success',
                'data': data
            }
        else:
            return {
                'product_id': product_id,
                'api_status': 'error',
                'error_code': response.status_code,
                'message': 'API request failed'
            }
    except requests.exceptions.RequestException as e:
        # Return mock data if API is unavailable (for offline development)
        return {
            'product_id': product_id,
            'api_status': 'mock',
            'message': 'Using mock data (API unavailable)',
            'mock_data': {
                'name': f'Product {product_id}',
                'category': 'Electronics',
                'description': f'Product information for {product_id}'
            }
        }
    except Exception as e:
        return {
            'product_id': product_id,
            'api_status': 'error',
            'message': str(e)
        }


def fetch_multiple_products(product_ids: list, api_url: str = None) -> Dict[str, Dict]:
    """
    Fetch information for multiple products.
    
    Args:
        product_ids: List of product IDs to fetch
        api_url: Optional API URL
    
    Returns:
        Dictionary mapping product IDs to their information
    """
    results = {}
    for product_id in product_ids:
        results[product_id] = fetch_product_info(product_id, api_url)
    return results


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

