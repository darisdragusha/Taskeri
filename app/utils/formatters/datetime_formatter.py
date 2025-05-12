"""
Utility functions for standardized datetime formatting across the application.
"""
from datetime import datetime
from typing import Optional, Union

# Default format for human-readable dates (e.g., "May 12, 2025")
DATE_FORMAT = "%B %d, %Y"

# Default format for human-readable datetimes (e.g., "May 12, 2025 14:30")
DATETIME_FORMAT = "%B %d, %Y %H:%M"

# ISO format for API responses (e.g., "2025-05-12T14:30:25")
API_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


def format_datetime(dt: Optional[Union[datetime, str]], format_string: str = API_DATETIME_FORMAT) -> Optional[str]:
    """
    Format a datetime object or string to a standardized string format.
    
    Args:
        dt: Datetime object or string to format
        format_string: Format string to use (defaults to API_DATETIME_FORMAT)
        
    Returns:
        Formatted datetime string or None if input is None
    """
    if dt is None:
        return None
        
    # If already a string, try to parse it to datetime first
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
        except ValueError:
            # If we can't parse it, return the string as is
            return dt
            
    # Format the datetime object
    return dt.strftime(format_string)


def format_date(dt: Optional[Union[datetime, str]]) -> Optional[str]:
    """
    Format a datetime object or string to a standardized date string (without time).
    
    Args:
        dt: Datetime object or string to format
        
    Returns:
        Formatted date string or None if input is None
    """
    return format_datetime(dt, DATE_FORMAT)


def to_api_datetime(dt: Optional[Union[datetime, str]]) -> Optional[str]:
    """
    Format a datetime object or string to a standardized API datetime string (ISO format).
    
    Args:
        dt: Datetime object or string to format
        
    Returns:
        ISO formatted datetime string or None if input is None
    """
    if dt is None:
        return None
        
    # If already a string, try to parse it to datetime first
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
        except ValueError:
            # If we can't parse it, return the string as is
            return dt
    
    # Format using isoformat for maximum compatibility
    return dt.isoformat()