# Install this - python -m pip install requests, python -m pip install Pillow 
import requests 
from PIL import Image 
from io import BytesIO 
import time

api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImNjZGY5YzA0NmMzMzM5NWYxZDcxMjUwMWEzNzhlMzRkIiwiY3JlYXRlZF9hdCI6IjIwMjUtMDQtMjRUMjE6Mjg6NTIuOTM0MDk3In0.6M9zCfBwz7pHhyAMCbTsQmiGdchy8oWi7nMPPKEDHuc"
user_input = input("Enter the description of your image...... ")

# Let's add a function to try different model names/formats
def try_generate_image(model_name):
    print(f"\nTrying with model: {model_name}")
    
    # Option 1: Model in URL path
    url = f"https://api.monsterapi.ai/v1/generate/{model_name}"
    
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {
        "prompt": user_input,
        "safe_fillers": True
    }
    
    print(f"Sending request to: {url}")
    print(f"Payload: {payload}")
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"API Response Status: {response.status_code}")
    print(f"Response Content: {response.text}")
    
    return response

# Let's try a few common model names for text-to-image generation
models_to_try = [
    "stable-diffusion", 
    "dall-e", 
    "midjourney",
    "text-to-image",
    "txt2img"
]

success = False
for model in models_to_try:
    response = try_generate_image(model)
    if response.status_code == 200:
        success = True
        print("Loading.... The image may take few seconds")
        process_id = response.json().get("process_id")
        
        while True:
            status_response = requests.get(f"https://api.monsterapi.ai/v1/status/{process_id}", headers={"Authorization": f"Bearer {api_token}"})
            status_data = status_response.json()
            print(f"Status check: {status_data}")
            
            if status_data.get("status") == "COMPLETED":
                img_url = status_data["result"]["output"][0]  # extracting image url
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    img = Image.open(BytesIO(img_response.content)).show()
                    print("Image generated successfully!")
                else:
                    print(f"Failed to download image: {img_response.status_code}")
                break
            elif status_data.get("status") == "FAILED":
                print("Image Generation failed")
                break
            else:
                print(f"Current status: {status_data.get('status')}. Waiting...")
                time.sleep(2)  # Add a delay to avoid frequent API calls
        break

if not success:
    print("\nAll model attempts failed.")
    print("Please check the MonsterAPI documentation for the correct model names and endpoint structure.")
    print("You might also want to verify that your API token has permissions to use the text-to-image service.")