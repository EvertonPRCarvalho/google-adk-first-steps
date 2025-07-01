import requests

async def post_weather(latitude: float, longitude: float):
    url = f'https://Weather-API.proxy-production.allthingsdev.co/weather/getForecast?latitude={latitude}&longitude={longitude}&unit=celsius'

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://edition.cnn.com",
        "priority": "u=1, i",
        "referer": "https://edition.cnn.com/",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "x-apihub-key": "cJT9AZ0WUFTZR9dYFj6V7ll4VmlyKUiJb5pG-uFmDKXb70KFFk",
        "x-apihub-host": "Weather-API.allthingsdev.co",
        "x-apihub-endpoint": "f5ba59cd-7870-46b6-8f91-3053fcd66349"
    }

    response = requests.post(url, headers=headers, allow_redirects=True)

    status_code = response.status_code
    data = response.text
    if(status_code == 200):
        return {"status": "success", "data":data}
    else:
        return {"status": "fail", "status_code":status_code}
