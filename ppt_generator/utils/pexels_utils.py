import io
import requests
import config


def search_pexels_best_match_url(description):
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": config.PEXEL_API_KEY}
    params = {"query": description, "per_page": 1}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("photos"):
            return data["photos"][0]["src"]["original"]
        else:
            return f"No images found for description: {description}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


def get_image_stream_from_url(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_stream = io.BytesIO(response.content)
        return image_stream
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from URL: {e}")
        return None
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def get_image_from_promt(prompt):
    image_url = search_pexels_best_match_url(prompt)
    if image_url:
        return get_image_stream_from_url(image_url)
    return None
