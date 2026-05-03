from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# 1. Load the environment variables from the .env file
load_dotenv()

app = Flask(__name__)
# Enable CORS so the HTML frontend can interact with this API
CORS(app) 

# 2. Use os.getenv() to build your URLs securely
# If it can't find the .env variable, it defaults to the localhost string just in case
CATALOG_BASE_URL = os.getenv("CATALOG_API_URL", "http://127.0.0.1:5002")
NOTIFICATION_BASE_URL = os.getenv("NOTIFICATION_API_URL", "http://127.0.0.1:5003")

CATALOG_URL = f"{CATALOG_BASE_URL}/update_stock"
NOTIFICATION_URL = f"{NOTIFICATION_BASE_URL}/send_reminder"

@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.get_json()
    student_id = data.get('student_id')
    book_id = data.get('book_id')

    if not student_id or not book_id:
        return jsonify({"error": "Missing student_id or book_id"}), 400

    # Step 1: Check Catalog System
    try:
        # 3. Added timeout=5 to prevent the server from hanging indefinitely
        catalog_res = requests.post(CATALOG_URL, json={"book_id": book_id}, timeout=5)
        catalog_data = catalog_res.json()
    except requests.exceptions.RequestException as e:
        print(f"Catalog Connection Error: {e}")
        return jsonify({"error": "Catalog System offline."}), 503

    if catalog_res.status_code != 200:
        return jsonify({"error": catalog_data.get("message", "Catalog error")}), 400

    book_title = catalog_data["book_title"]

    # Step 2: Trigger Notification System
    try:
        # 3. Added timeout=5 here as well
        notify_res = requests.post(NOTIFICATION_URL, json={
            "student_id": student_id,
            "book_title": book_title,
            "book_id": book_id
        }, timeout=5)
        notify_data = notify_res.json()
    except requests.exceptions.RequestException as e:
        print(f"Notification Connection Error: {e}")
        return jsonify({"error": "Notification System offline."}), 503

    # Step 3: Final Integration Output
    return jsonify({
        "status": "Success",
        "student_id": student_id,
        "book_borrowed": book_title,
        "due_date": notify_data["due_date"]
    }), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)