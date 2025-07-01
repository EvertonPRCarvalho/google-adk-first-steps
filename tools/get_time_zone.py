import requests

async def get_time_zone(country: str):

    url = f'https://Time-Zone-API.proxy-production.allthingsdev.co/v1/timezone.json?q={country}'

    headers = {
        "x-apihub-key": "cJT9AZ0WUFTZR9dYFj6V7ll4VmlyKUiJb5pG-uFmDKXb70KFFk",
        "x-apihub-host": "Time-Zone-API.allthingsdev.co",
        "x-apihub-endpoint": "72572365-f70c-4538-b5ca-4f45c6897f9c"
    }

    response = requests.get(url, headers=headers, allow_redirects=True)
    status_code = response.status_code
    data = response.json()
    if(status_code == 200):

        localtime = data['location']['localtime']
        latitude = data['location']['lat']
        longitude = data['location']['lon']
        hour = localtime.split(" ")[1]
        return {"status": "success", "report":{"hour":hour, "latitude":float(latitude), "longitude":float(longitude)}}
    else:
        return {"status": "fail", "status_code":status_code}
get_time_zone("Brazil")


