import requests

# URL of your Flask API endpoint
url = 'http://localhost:5000/process_transactions'

# Path to your image file
image_path = "C:\\Users\\pri\\Downloads\\Screenshot_20240317-180239_GPay.png"  # Specify your image location here

# Open the image file
with open(image_path, 'rb') as image_file:
    # Create a dictionary with the image file
    files = {'file': image_file}
    
    # Send the POST request with the image file
    response = requests.post(url, files=files)
    
    # Print the response
    print(response.json())
