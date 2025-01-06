import google.generativeai as genai

def analyze_reviews(api_key, business_name, reviews):
    """
    Analyze reviews using Gemini API to provide a recommendation summary
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    # Calculate average rating
    ratings = [review.get('rating', 0) for review in reviews]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    # Prepare review content for analysis
    reviews_text = "\n".join([
        f"Rating: {review.get('rating')}/5\nReview: {review.get('text')}\n"
        for review in reviews
    ])
    
    prompt = f"""
    For {business_name} (Average Rating: {avg_rating:.1f}/5):
    
    {reviews_text}
    
    Please provide:
    1. A brief summary of the overall sentiment
    2. A clear recommendation (Should someone visit {business_name}?)
    3. Either a short reasoning for your recommendation OR 2-3 key pros and cons

    Keep your response concise and conversational.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error getting AI analysis: {e}")
        return None