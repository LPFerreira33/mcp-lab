import os
import requests

ITEM_TRACKER_API = os.environ.get("ITEM_TRACKER_API", "http://localhost:3310")

def add_item(name: str, quantity: int, replacement_date: str, storage_name: str = "", expiration_date: str = None) -> str:
    """
    Add a new item to the Item Tracker.

    Args:
        name (str): Name of the item.
        quantity (int): Quantity of the item.
        replacement_date (str): Replacement date in YYYY-MM-DD format.
        storage_name (str, optional): Storage location. Defaults to "".
        expiration_date (str, optional): Expiration date in YYYY-MM-DD format. Defaults to None.

    Returns:
        str: Result message.
    """
    payload = {
        "name": name,
        "quantity": quantity,
        "replacement_date": replacement_date,
        "storage_name": storage_name,
        "expiration_date": expiration_date,
    }
    resp = requests.post(f"{ITEM_TRACKER_API}/items/", json=payload)
    if resp.ok:
        return f"Item '{name}' added successfully."
    return f"Failed to add item: {resp.text}"

def edit_item(item_id: int, name: str = None, quantity: int = None, replacement_date: str = None, storage_name: str = None, expiration_date: str = None) -> str:
    """
    Edit an existing item in the Item Tracker.

    Args:
        item_id (int): ID of the item to edit.
        name (str, optional): New name.
        quantity (int, optional): New quantity.
        replacement_date (str, optional): New replacement date.
        storage_name (str, optional): New storage location.
        expiration_date (str, optional): New expiration date.

    Returns:
        str: Result message.
    """
    payload = {}
    if name is not None:
        payload["name"] = name
    if quantity is not None:
        payload["quantity"] = quantity
    if replacement_date is not None:
        payload["replacement_date"] = replacement_date
    if storage_name is not None:
        payload["storage_name"] = storage_name
    if expiration_date is not None:
        payload["expiration_date"] = expiration_date

    if not payload:
        return "No fields to update."

    resp = requests.patch(f"{ITEM_TRACKER_API}/items/{item_id}", json=payload)
    if resp.ok:
        return f"Item {item_id} updated successfully."
    return f"Failed to update item: {resp.text}"

def remove_item(item_id: int) -> str:
    """
    Remove an item from the Item Tracker.

    Args:
        item_id (int): ID of the item to remove.

    Returns:
        str: Result message.
    """
    resp = requests.delete(f"{ITEM_TRACKER_API}/items/{item_id}")
    if resp.ok:
        return f"Item {item_id} removed successfully."
    return f"Failed to remove item: {resp.text}"