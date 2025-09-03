import requests
import json

def get_events(save_to_file=False, filename="events.json"):
	"""
	Fetches FIBA 3x3 events for Bosnia and Herzegovina.
	If save_to_file is True, saves the result to filename.
	Returns the events data as a Python object.
	"""
	url = "https://play.fiba3x3.com/api/v2/search/events?countryIso2=BA&name=&input=&when=future&distance=100"
	headers = {
		"accept": "application/json, text/plain, */*",
		"accept-language": "en-US,en;q=0.8",
		"priority": "u=1, i",
		"referer": "https://play.fiba3x3.com/events",
		"sec-ch-ua": '"Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"',
		"sec-ch-ua-mobile": "?0",
		"sec-ch-ua-platform": '"Linux"',
		"sec-fetch-dest": "empty",
		"sec-fetch-mode": "cors",
		"sec-fetch-site": "same-origin",
		"sec-gpc": "1",
		"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
		"x-request-id": "FIBAPLAYCLIENT/2277880c-6c8e-4108-8e2f-02357bc80839"
	}
	response = requests.get(url, headers=headers)
	data = response.json()
	if save_to_file:
		with open(filename, "w", encoding="utf-8") as f:
			json.dump(data, f, ensure_ascii=False, indent=2)
	return data

# Example usage:
if __name__ == "__main__":
	get_events(save_to_file=True)



