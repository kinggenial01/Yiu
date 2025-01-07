import requests
import time
import uuid
from requests.exceptions import ConnectionError, Timeout, RequestException

# Function to send the request with retry logic
def send_request(available_taps, count, token, max_retries=5, retry_delay=10):
    url = 'https://api-gw.geagle.online/tap'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
        'origin': 'https://telegram.geagle.online',
        'priority': 'u=1, i',
        'referer': 'https://telegram.geagle.online/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    timestamp = int(time.time())
    salt = str(uuid.uuid4())

    data = {
        "available_taps": available_taps,
        "count": count,
        "timestamp": timestamp,
        "salt": salt
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)

            # Print the response status and content for debugging
            print(f"Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")

            try:
                return response.json()  # Try to return JSON if possible
            except requests.exceptions.JSONDecodeError:
                return None  # If not JSON, return None or handle it accordingly

        except (ConnectionError, Timeout) as e:
            print(f"Connection error: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)  # Wait before retrying

        except RequestException as e:
            print(f"Request error: {e}. Skipping this token.")
            return None  # Skip this token and move to the next one

    print(f"Failed after {max_retries} retries.")
    return None  # Return None after exceeding max retries

# Read the Bearer tokens from data.txt
with open('data.txt', 'r') as file:
    tokens = [line.strip() for line in file.readlines()]

# Fixed values
available_taps = 1000
count = 200

# Loop to send requests for each token, and repeat the process after completing all accounts
while True:
    for token in tokens:
        response = send_request(available_taps, count, token)
        print(f"Response for token {token}: {response}")

    # Countdown timer for 60 seconds (1 minute)
    print("""#####       ##    ######    ######    ###    ##   ##            ######  #######    ####    ##  ##  
    _____                    _ _         _______        _     
  / ____|                  | (_)       |__   __|      | |    
 | |  __ _ __ ___   ___  __| |_  __ _     | | ___  ___| |__  
 | | |_ | '_ ` _ \ / _ \/ _` | |/ _` |    | |/ _ \/ __| '_ \ 
 | |__| | | | | | |  __/ (_| | | (_| |    | |  __/ (__| | | |
  \_____|_| |_| |_|\___|\__,_|_|\__,_|    |_|\___|\___|_| |_|
                                                             
                                                               
                                                                                                   
📍 WhatsApp:- +2348167893138
Waiting for 2 minutes before repeating...""")
    for remaining in range(120, 0, -1):
        print(f"Time remaining: {remaining} seconds", end="\r")
        time.sleep(1)  # Sleep for 1 second each iteration

    print()  # Just to move to the next line after countdown is done