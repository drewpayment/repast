import requests

from repast.utils import debug_print

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
    
def get_coordinates_from_address(api_key, address, debug=False):
    """Convert an address (or zip code) to coordinates using Google's Geocoding API"""
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    params = {
        'key': api_key,
        'address': address
    }
    
    try:
        debug_print("\nGeocoding Debug Info:", debug=debug)
        debug_print(f"Input address: {address}", debug=debug)
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        result = response.json()
        
        debug_print(f"Geocoding status: {result.get('status')}", debug=debug)
        
        if result['status'] == 'OK':
            location = result['results'][0]['geometry']['location']
            formatted_address = result['results'][0]['formatted_address']
            debug_print(f"Formatted address: {formatted_address}", debug=debug)
            debug_print(f"Returned coordinates: ({location['lat']}, {location['lng']})", debug=debug)
            return (location['lat'], location['lng'])
        else:
            debug_print(f"Error: {result.get('status')}", debug=debug)
            if result.get('error_message'):
                debug_print(f"Error message: {result.get('error_message')}", debug=debug)
            return None
            
    except requests.exceptions.RequestException as e:
        debug_print(f"Error making request: {e}", debug=debug)
        return None
    
def text_search_businesses(api_key, query, location=None):
    """
    Search for businesses using Google Places Text Search API
    """
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    params = {
        'key': api_key,
        'query': query,
        'type': 'restaurant'
    }
    
    if location:
        params['location'] = f"{location[0]},{location[1]}"
        params['radius'] = 5000  # 5km radius
    
    print(f"\nText Search Debug Info:")
    print(f"Query: {query}")
    if location:
        print(f"Near location: {location}")
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        result = response.json()
        
        print(f"Status: {result.get('status')}")
        print(f"Results found: {len(result.get('results', []))}")
        
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None