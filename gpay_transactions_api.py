import pytesseract
from PIL import Image
import re, io

import numpy as np
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile
from typing import Annotated

import cv2

# Specify the Tesseract executable location if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

router = APIRouter(prefix="/ocr")

def get_last_integer(string: str):
    right = len(string)-1
    num = ''
    if "+" in string:
        return None
    while right != 0:
        if string[right].isdigit():
            num = string[right] + num
        else:
            break
        right -= 1
    if num: 
        return int(num)
    return None


# Function to process the image and extract transactions
def extract_transactions(image_file):
    nparr = np.fromstring(image_file, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_not(img)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite('temp.png', img)
    text = pytesseract.image_to_string(img)

    # Splitting text based on lines
    print(text)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    transactions = []
    for line in lines:
        amount = get_last_integer(line)
        if amount:
            transactions.append(amount)
    return transactions
    # todo: check if it ends in a number. if so, we know that it can be read
    
@router.post('/process_transactions')
def process_transactions(file: Annotated[bytes, File()]):
    if file:
        try:
            transactions = extract_transactions(file)
            # Process transactions here...
            # Deduct amounts from existing balance, etc.
            return JSONResponse({"transactions": transactions})
        except Exception as e:
            return JSONResponse({"error": str(e)})
    
    return JSONResponse({"error": "Something went wrong"})