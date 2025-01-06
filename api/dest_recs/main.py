import argparse
import os
from dotenv import load_dotenv

from dest_recs.utils import debug_print
from .places_api import search_nearby_businesses, get_place_details, get_coordinates_from_address, text_search_businesses
from .ai_analysis import analyze_reviews

def display_businesses(businesses):
    """Display businesses with an index for selection"""
    for idx, business in enumerate(businesses, 1):
        print(f"{idx}. {business.get('name')} - {business.get('vicinity')}")
        print(f"   Rating: {business.get('rating', 'N/A')}")
        print()

def get_user_choice(max_choice):
    """Get valid input from user"""
    while True:
        try:
            choice = int(input(f"Enter a number (1-{max_choice}) to see details, or 0 to exit: "))
            if 0 <= choice <= max_choice:
                return choice
            print(f"Please enter a number between 0 and {max_choice}")
        except ValueError:
            print("Please enter a valid number")

def display_place_details(details, gemini_key, debug=False):
    """Display detailed information about a place with AI analysis"""
    result = details.get('result', {})
    print("\n" + "="*50)
    print(f"Name: {result.get('name')}")
    print(f"Address: {result.get('formatted_address')}")
    print(f"Phone: {result.get('formatted_phone_number', 'N/A')}")
    print(f"Rating: {result.get('rating', 'N/A')}")
    
    # Get AI analysis first
    reviews = result.get('reviews', [])
    if reviews:
        print("\nAnalyzing reviews...")
        analysis = analyze_reviews(gemini_key, result.get('name'), reviews)
        if analysis:
            print(f"\nAI RECOMMENDATION FOR {result.get('name')} ({result.get('rating', 'N/A')}/5)")
            print("-" * 20)
            print(analysis)
    
    print("="*50 + "\n")

    # Ask if user wants to see the reviews
    if reviews:
        show_reviews = input("Would you like to see the actual reviews? (y/n): ").lower()
        if show_reviews == 'y':
            print("\nReviews:")
            for review in reviews:
                print("\n---")
                print(f"Rating: {review.get('rating')}/5")
                print(f"Review: {review.get('text')}")
                print(f"Time: {review.get('relative_time_description')}")
            print("\n" + "="*50 + "\n")

    return reviews is not None
    
def get_search_keyword():
    """Get optional keyword from user"""
    print("\nYou can search for specific types of businesses (e.g., 'pizza', 'coffee', 'bar')")
    keyword = input("Enter a search term (or press Enter to skip): ").strip()
    return keyword if keyword else None

def get_location():
    """Get location input from user"""
    print("\nHow would you like to specify the location?")
    print("1. Use Grand Rapids, MI (default)")
    print("2. Enter a zip code")
    print("3. Enter an address")
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1" or choice == "":
            return (42.9634, -85.6681)  # Grand Rapids coordinates
        elif choice in ["2", "3"]:
            address = input("Enter your zip code or address: ").strip()
            return address
        else:
            print("Please enter 1, 2, or 3")

def main(debug=False):
    try:
        debug_print("Inside main function...", debug=debug)
        load_dotenv()
        places_api_key = os.getenv('GOOGLE_PLACES_API_KEY')
        gemini_api_key = os.getenv('GOOGLE_AI_API_KEY')
        
        debug_print(f"API keys loaded: Places API {'✓' if places_api_key else '✗'}, Gemini {'✓' if gemini_api_key else '✗'}", debug=debug)
        
        if not all([places_api_key, gemini_api_key]):
            print("Missing required API keys in .env file!")
            return
            
        # Get location from user
        location = get_location()
        
        # Convert address to coordinates if needed
        if isinstance(location, str):
            debug_print(f"Converting address to coordinates...", debug=debug)
            location = get_coordinates_from_address(places_api_key, location, debug=debug)
            if not location:
                print("Could not find coordinates for that address!")
                return
            debug_print(f"Location coordinates: {location}", debug=debug)
        
        debug_print("Searching for nearby businesses...", debug=debug)
        
        # Get optional keyword from user
        keyword = get_search_keyword()
        
        # Get initial business listings
        results = search_nearby_businesses(places_api_key, location, radius=5000, keyword=keyword, debug=debug)
        
        if not results or not results.get('results'):
            print("No nearby results found, trying text search...")
            results = text_search_businesses(places_api_key, keyword, location)
            
        if not results or not results.get('results'):
            if keyword:
                print(f"No businesses found matching '{keyword}'!")
                print("Try:")
                print("1. Using a different search term")
                print("2. Checking the spelling")
                print("3. Using a broader search term (e.g., 'mexican' instead of 'cantina')")
            else:
                print("No businesses found!")
            return

        businesses = results.get('results', [])
        
        while True:
            # Display the list of businesses
            print("\nNearby Businesses:")
            display_businesses(businesses)
            
            # Get user choice
            choice = get_user_choice(len(businesses))
            
            # Exit if user chooses 0
            if choice == 0:
                print("Goodbye!")
                break
                
            # Get and display details for selected business
            selected_business = businesses[choice - 1]
            place_id = selected_business.get('place_id')
            
            print(f"\nFetching details for {selected_business.get('name')}...")
            details = get_place_details(places_api_key, place_id)
            
            if details and details.get('status') == 'OK':
                has_reviews = display_place_details(details, gemini_api_key, debug=debug)
                if not has_reviews:
                    print("This place doesn't have any reviews yet.")
            else:
                print("Sorry, couldn't fetch details for this place.")
            
            # Ask if user wants to continue
            continue_choice = input("\nWould you like to check another business? (y/n): ").lower()
            if continue_choice != 'y':
                print("Goodbye!")
                break

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        print(traceback.format_exc())

def parse_args():
    parser = argparse.ArgumentParser(description='Restaurant recommendation tool')
    parser.add_argument('--debug', '-d', action='store_true', 
                       help='Enable debug output')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    debug_print("Script starting...", debug=args.debug)
    main(debug=args.debug)