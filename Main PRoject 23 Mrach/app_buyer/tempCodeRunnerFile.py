import requests
url = "https://api.countrystatecity.in/v1/countries"

headers = {
"X-CSCAPI-KEY": "UXF2OHQ2WjBMT1Y5Q05MQzVhNE1sT3VJSk02Y3BaNzlRNHRVMHRjZA=="
}

mydata =  requests.request("GET", url, headers=headers)
print(mydata.json())