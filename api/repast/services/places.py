from repast.utils import debug_print
import requests
from ..config import get_settings

def search_nearby_businesses(api_key, location, radius=5000, keyword=None, debug=False):
    """
    Search for businesses near a specific location using Google Places API
    """
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    params = {
        'key': api_key,
        'location': f"{location[0]},{location[1]}",
        'radius': radius
    }
    
    if keyword:
        params['keyword'] = keyword
        params['type'] = 'restaurant'
    
    # Debug information
    debug_print("\nAPI Request Debug Info:", debug=debug)
    debug_print(f"Search coordinates: {location}", debug=debug)
    debug_print(f"Search radius: {radius}m", debug=debug)
    debug_print(f"Search parameters: {', '.join(f'{k}: {v}' for k, v in params.items() if k != 'key')}", debug=debug)
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        result = response.json()
        
        debug_print("\nAPI Response Debug Info:", debug=debug)
        debug_print(f"Status: {result.get('status')}", debug=debug)
        debug_print(f"Results found: {len(result.get('results', []))}", debug=debug)
        
        # Distance check debug
        if result.get('results') and debug:
            debug_print("\nDistance from search point:", debug=debug)
            for place in result.get('results'):
                place_loc = place.get('geometry', {}).get('location', {})
                if place_loc:
                    lat_diff = abs(location[0] - place_loc.get('lat', 0))
                    lng_diff = abs(location[1] - place_loc.get('lng', 0))
                    debug_print(f"{place.get('name')}: Lat diff {lat_diff:.4f}, Lng diff {lng_diff:.4f}", debug=debug)
        
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def get_place_details(api_key, place_id):
    """
    Get detailed information about a place using its place_id
    
    Args:
        api_key (str): Your Google Places API key
        place_id (str): The Google Places ID of the location
        
    Returns:
        dict: JSON response containing place details including reviews
    """
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    params = {
        'key': api_key,
        'place_id': place_id,
        'fields': 'name,rating,formatted_phone_number,formatted_address,reviews,url,website'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None