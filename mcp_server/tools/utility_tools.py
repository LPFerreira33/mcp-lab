import pytz
from datetime import datetime, date

def calculate_age(birth_date: str) -> dict:
    """
    Calculate age from birth date.
    
    Args:
        birth_date: Birth date in YYYY-MM-DD format
        
    Returns:
        Dictionary with age in years, months, and days
    """
    try:
        birth = datetime.strptime(birth_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Birth date must be in YYYY-MM-DD format")
    
    today = date.today()
    
    if birth > today:
        raise ValueError("Birth date cannot be in the future")
    
    # Calculate years
    years = today.year - birth.year
    
    # Adjust if birthday hasn't occurred this year
    if today.month < birth.month or (today.month == birth.month and today.day < birth.day):
        years -= 1
    
    # Calculate months
    months = today.month - birth.month
    if today.day < birth.day:
        months -= 1
    if months < 0:
        months += 12
    
    # Calculate days
    if today.day >= birth.day:
        days = today.day - birth.day
    else:
        # Get days in previous month
        if today.month == 1:
            prev_month_year = today.year - 1
            prev_month = 12
        else:
            prev_month_year = today.year
            prev_month = today.month - 1
        
        # Simple day calculation (could be more precise with calendar module)
        days_in_prev_month = 31 if prev_month in [1,3,5,7,8,10,12] else 30
        if prev_month == 2:
            days_in_prev_month = 29 if prev_month_year % 4 == 0 else 28
            
        days = days_in_prev_month - birth.day + today.day
    
    return {
        "years": years,
        "months": months, 
        "days": days
    }

def get_timezone_info(timezone_name: str) -> dict:
    """
    Get current time and information for a specific timezone.
    
    Args:
        timezone_name: Timezone name (e.g., 'America/New_York', 'Europe/London', 'Asia/Tokyo')
        
    Returns:
        Dictionary with timezone information and current time
    """
    try:
        tz = pytz.timezone(timezone_name)
    except pytz.exceptions.UnknownTimeZoneError:
        # Return some common timezones as suggestions
        common_timezones = [
            'America/New_York', 'America/Los_Angeles', 'America/Chicago',
            'Europe/London', 'Europe/Paris', 'Europe/Berlin',
            'Asia/Tokyo', 'Asia/Shanghai', 'Asia/Kolkata',
            'Australia/Sydney', 'UTC'
        ]
        raise ValueError(f"Unknown timezone. Try one of: {', '.join(common_timezones)}")
    
    # Get current time in the timezone
    current_time = datetime.now(tz)
    utc_time = datetime.now(pytz.UTC)
    
    # Calculate offset from UTC
    offset = current_time.utcoffset()
    offset_hours = offset.total_seconds() / 3600
    
    return {
        "timezone": timezone_name,
        "current_time": current_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "utc_offset": f"{offset_hours:+.1f} hours",
        "is_dst": current_time.dst() != pytz.timedelta(0),
        "utc_time": utc_time.strftime("%Y-%m-%d %H:%M:%S UTC")
    }