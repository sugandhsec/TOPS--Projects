import requests

url = "https://api.countrystatecity.in/v1/countries"

headers = {
    'X-CSCAPI-KEY': 'UVY0VEFQZE45dm8xNGtaYTZudTNmYUtHSW9TN1hvZENHSUd3YURSdg=='
}

response = requests.request("GET", url, headers=headers)
return render(request, "demo.html", {'response': response.json})
print(response.text)
