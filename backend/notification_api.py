import os
import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

@app.route('/send_reminder', methods=['POST'])
def send_reminder():
    data = request.get_json()
    student_id = data.get('student_id')
    book_title = data.get('book_title')
    book_id = data.get('book_id') 

    due_date = (datetime.datetime.now() + datetime.timedelta(days=14)).strftime('%Y-%m-%d')

    # Insert official record via REST API (POST)
    insert_url = f"{SUPABASE_URL}/rest/v1/transactions"
    transaction_data = {
        "student_id": student_id,
        "book_id": book_id,
        "due_date": due_date
    }
    requests.post(insert_url, headers=HEADERS, json=transaction_data)

    print(f"[SYSTEM LOG] Transaction recorded for {student_id}: '{book_title}' is due on {due_date}.")

    return jsonify({
        "status": "sent",
        "due_date": due_date
    }), 200

if __name__ == '__main__':
    app.run(port=5003, debug=True)