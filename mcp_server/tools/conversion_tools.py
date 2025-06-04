from typing import Literal

def convert_length(
    value: float, 
    from_unit: Literal["meters", "feet"], 
    to_unit: Literal["meters", "feet"]
) -> float:
    """
    Convert length between meters and feet.
    
    Args:
        value: The length value to convert
        from_unit: Convert from "meters" or "feet" 
        to_unit: Convert to "meters" or "feet"
    
    Returns:
        The converted length value
    """
    if value < 0:
        raise ValueError("Length cannot be negative")
    
    if from_unit == to_unit:
        return value
    
    if from_unit == "meters" and to_unit == "feet":
        return round(value * 3.28084, 4)
    
    if from_unit == "feet" and to_unit == "meters":
        return round(value / 3.28084, 4)

def convert_temperature(
    value: float,
    from_unit: Literal["celsius", "fahrenheit", "kelvin"],
    to_unit: Literal["celsius", "fahrenheit", "kelvin"]
) -> float:
    """
    Convert temperature between Celsius, Fahrenheit, and Kelvin.
    
    Args:
        value: Temperature value to convert
        from_unit: Convert from "celsius", "fahrenheit", or "kelvin"
        to_unit: Convert to "celsius", "fahrenheit", or "kelvin"
        
    Returns:
        The converted temperature value
    """
    if from_unit == to_unit:
        return value
    
    # Convert to Celsius first
    if from_unit == "fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "kelvin":
        celsius = value - 273.15
    else:
        celsius = value
    
    # Convert from Celsius to target
    if to_unit == "fahrenheit":
        result = celsius * 9/5 + 32
    elif to_unit == "kelvin":
        result = celsius + 273.15
    else:
        result = celsius
    
    return round(result, 2)
