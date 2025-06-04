import re
import secrets
import string
from typing import Literal

def count_words(text: str) -> dict:
    """
    Count words, characters, and lines in a text.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary with word count, character count, and line count
    """
    if not text:
        return {"words": 0, "characters": 0, "lines": 0}
    
    # Count words (split by whitespace, filter empty strings)
    words = len([word for word in text.split() if word.strip()])
    
    # Count characters (including spaces)
    characters = len(text)
    
    # Count lines
    lines = len(text.split('\n'))
    
    return {
        "words": words,
        "characters": characters,
        "lines": lines
    }

def generate_password(
    length: int = 12,
    include_symbols: bool = True,
    include_numbers: bool = True,
    include_uppercase: bool = True
) -> str:
    """
    Generate a secure random password.
    
    Args:
        length: Password length (minimum 4, maximum 128)
        include_symbols: Include special characters
        include_numbers: Include numbers
        include_uppercase: Include uppercase letters
        
    Returns:
        Generated password string
    """
    if length < 4 or length > 128:
        raise ValueError("Password length must be between 4 and 128 characters")
    
    # Start with lowercase letters
    characters = string.ascii_lowercase
    
    # Add character sets based on options
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_numbers:
        characters += string.digits
    if include_symbols:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Generate password ensuring at least one character from each enabled set
    password = []
    
    # Ensure we have at least one from each enabled category
    password.append(secrets.choice(string.ascii_lowercase))
    if include_uppercase:
        password.append(secrets.choice(string.ascii_uppercase))
    if include_numbers:
        password.append(secrets.choice(string.digits))
    if include_symbols:
        password.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
    
    # Fill the rest randomly
    for _ in range(length - len(password)):
        password.append(secrets.choice(characters))
    
    # Shuffle the password list
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)