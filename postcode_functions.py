"""Functions that interact with the Postcode API."""
import os
import json
import requests as req


CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    # This function is used in Task 3, you can ignore it for now.
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    # This function is used in Task 3, you can ignore it for now.
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=4)


def validate_postcode(postcode: str) -> bool:
    """checks if the postcode is valid"""
    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")

    cache = load_cache()
    if postcode in cache and "valid" in cache[postcode]:
        return cache[postcode]["valid"]

    response = req.get(
        f"https://api.postcodes.io/postcodes/{postcode}/validate", timeout=5)

    if response.status_code != 200:
        raise req.RequestException("Unable to access API.")

    data = response.json()

    if postcode not in cache:
        cache[postcode] = {}
    cache[postcode]["valid"] = data["result"]
    save_cache(cache)

    return data["result"]


def get_postcode_for_location(lat: float, long: float) -> str:
    """get postcode for a location by longitude and latitude"""
    if not isinstance(lat, float):
        raise TypeError("Function expects two floats.")
    if not isinstance(long, float):
        raise TypeError("Function expects two floats.")

    response = req.get(
        f"https://api.postcodes.io/postcodes?lon={long}&lat={lat}", timeout=5)

    if response.status_code != 200:
        raise req.RequestException("Unable to access API.")

    data = response.json()
    if data["result"] is None:
        raise ValueError("No relevant postcode found.")
    return data["result"][0]["postcode"]


def get_postcode_completions(postcode_start: str) -> list[str]:
    """gets the postcode completions"""
    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")

    cache = load_cache()
    if postcode_start in cache and "completions" in cache[postcode_start]:
        return cache[postcode_start]["completions"]

    response = req.get(
        f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete", timeout=5)

    if response.status_code != 200:
        raise req.RequestException("Unable to access API.")
    data = response.json()

    if postcode_start not in cache:
        cache[postcode_start] = {}
    cache[postcode_start]["completions"] = data["result"]
    save_cache(cache)

    return data["result"]


def get_postcodes_details(postcodes: list[str]) -> dict:
    """gets the details of postcodes from a list of postcodes"""
    if not isinstance(postcodes, list):
        raise TypeError("Function expects a list of strings.")

    for postcode in postcodes:
        if not isinstance(postcode, str):
            raise TypeError("Function expects a list of strings.")

    response = req.post("https://api.postcodes.io/postcodes",
                        json={"postcodes": postcodes}, timeout=5)

    if response.status_code != 200:
        raise req.RequestException("Unable to access API.")
    data = response.json()
    return data["result"]
