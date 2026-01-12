"""
File handler module for reading and writing files.
Handles encoding issues and file operations.
"""

import os
from typing import List, Optional


def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    
    Expected Output Format:
    ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]
    
    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()
                # Remove header row (first line)
                if lines:
                    lines = lines[1:]
                # Remove empty lines and strip whitespace
                raw_lines = [line.strip() for line in lines if line.strip()]
                return raw_lines
        except UnicodeDecodeError:
            # Try next encoding
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []
        except Exception as e:
            # If all encodings fail, try the last one and return empty list
            if encoding == encodings[-1]:
                print(f"Error reading file: {e}")
                return []
            continue
    
    return []


def read_file(file_path: str, encoding: str = 'utf-8') -> Optional[List[str]]:
    """
    Read a file with error handling for encoding issues.
    
    Args:
        file_path: Path to the file to read
        encoding: File encoding (default: utf-8)
    
    Returns:
        List of lines from the file, or None if file cannot be read
    """
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.readlines()
    except UnicodeDecodeError:
        # Try with latin-1 encoding if utf-8 fails
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.readlines()
        except Exception as e:
            print(f"Error reading file with latin-1 encoding: {e}")
            return None
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> bool:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        encoding: File encoding (default: utf-8)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False


def ensure_output_directory(output_dir: str) -> bool:
    """
    Ensure the output directory exists.
    
    Args:
        output_dir: Path to the output directory
    
    Returns:
        True if directory exists or was created, False otherwise
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating output directory: {e}")
        return False

