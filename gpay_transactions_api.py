import pytesseract
from PIL import Image
from io import BytesIO
from flask import Flask, request, jsonify
import re

# Specify the Tesseract executable location if needed
#  pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

app = Flask(__name__)

# Function to process the image and extract transactions
def extract_transactions(image_file):
    transactions = []
    img = Image.open(image_file)
    text = pytesseract.image_to_string(img)

    # Splitting text based on lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Regex patterns for extracting recipient, date/time, and amount
    transaction_pattern = r'([A-Z\s]+)\s+[RV]?\d+\s+(\w{3,4}\s+\d{1,2},\s+\d{4}\s+at\s+\d{1,2}:\d{2}(?:AM|PM))\s+[RV]?(?P<amount>\d+)\s*'
    
    for line in lines:
        # Extracting transaction details using pattern
        match = re.match(transaction_pattern, line)
        if match:
            recipient = match.group(1).strip()
            date_time = match.group(2)
            amount = match.group('amount')
            transactions.append({"recipient": recipient, "date_time": date_time, "amount": amount})

    return transactions

@app.route('/process_transactions', methods=['POST'])
def process_transactions():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file:
        try:
            transactions = extract_transactions(file)
            # Process transactions here...
            # Deduct amounts from existing balance, etc.
            return jsonify({"transactions": transactions})
        except Exception as e:
            return jsonify({"error": str(e)})
    
    return jsonify({"error": "Something went wrong"})

if __name__ == '__main__':
    app.run(debug=True)
