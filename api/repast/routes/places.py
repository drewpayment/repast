# repast/routes/places.py
from repast.config import get_settings
from flask import Blueprint, request, jsonify
from ..services.places import search_nearby_businesses, get_place_details
from ..services.ai import analyze_reviews
from ..middleware.auth import require_api_key

bp = Blueprint('places', __name__, url_prefix='/api')

@bp.route('/search', methods=['POST'])
@require_api_key
def search():
    data = request.get_json()
    location = data.get('location')
    keyword = data.get('keyword')
    
    settings = get_settings()
    debug = settings.DEBUG == 'true'
    
    results = search_nearby_businesses(location, keyword=keyword, debug=debug)
    return jsonify(results)

@bp.route('/place-details/<place_id>', methods=['GET'])
@require_api_key
def get_place_details_route(place_id):
    settings = get_settings()
    debug = settings.DEBUG == 'true'
    
    details = get_place_details(place_id, debug=debug)
    if details and details.get('status') == 'OK':
        reviews = details.get('result', {}).get('reviews', [])
        if reviews:
            analysis = analyze_reviews(
                details['result'].get('name'),
                reviews
            )
            details['ai_analysis'] = analysis
            
    return jsonify(details)