API_KEY = 'pat-na1-cca50882-e202-465e-830e-1a842308514e'
stripe_api_key = 'sk_test_51OOBFcSJbAzAaGwaC6vI6216XAfJwHA48cZtkkfmu8J4YDFYq5Vk7kc3Z01F4lq71Ix2vlSpsrTQtyg6yQTYGThR00nLzAc294'
import requests
import json

def getRequestHubspot(endpoint_url, body=None):
    # create headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }

    # hit api for get request
    response = requests.get(endpoint_url, data = body, headers=headers)

    if response.status_code == 200:
        # The request was successful
        data = response.json()
        return data
    
    # In case of api failed
    print(f"Error: {response.status_code}, {response.text}")
    return False


def postRequestHubspot(endpoint_url, body):
    # create headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }

    # hit api for get request
    response = requests.post(endpoint_url, data=json.dumps(body), headers=headers)

    if response.status_code in [200, 201]:
        # The request was successful
        data = response.json()
        return data
    
    # In case of api failed
    print(f"Error: {response.status_code}, {response.text}")
    return False

def getRequestStripe(endpoint_url):
    # create headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {stripe_api_key}'
    }

    # hit api for get request
    response = requests.get(endpoint_url, headers=headers)

    if response.status_code == 200:
        # The request was successful
        data = response.json()
        return data
    
    # In case of api failed
    print(f"Error: {response.status_code}, {response.text}")
    return False