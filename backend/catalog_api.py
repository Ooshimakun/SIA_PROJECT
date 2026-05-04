import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import requests

load_dotenv()
app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# These headers act as our authentication badge for Supabase
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

@app.route('/update_stock', methods=['POST'])
def update_stock():
    data = request.get_json()
    book_id = data.get('book_id')

    # 1. Fetch book via REST API (GET)
    fetch_url = f"{SUPABASE_URL}/rest/v1/books?id=eq.{book_id}&select=*"
    res = requests.get(fetch_url, headers=HEADERS)
    books_data = res.json()

    if not books_data:
        return jsonify({"status": "error", "message": "Book ID not found in database."}), 404

    book = books_data[0]

    # 2. Check stock and update
    if book["stock"] > 0:
        new_stock = book["stock"] - 1
        
        # 3. Perform UPDATE via REST API (PATCH)
        update_url = f"{SUPABASE_URL}/rest/v1/books?id=eq.{book_id}"
        requests.patch(update_url, headers=HEADERS, json={"stock": new_stock})
        
        print(f"[SYSTEM LOG] Stock for '{book['title']}' updated. Remaining: {new_stock}")
        return jsonify({"status": "success", "book_title": book["title"]}), 200
    else:
        return jsonify({"status": "error", "message": f"'{book['title']}' is currently out of stock."}), 400
    
@app.route('/books', methods=['GET'])
def get_all_books():
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    # This securely asks Supabase for all books and sends them to your frontend
    response = requests.get(f"{SUPABASE_URL}/rest/v1/books?select=*", headers=headers)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(port=5002, debug=True)