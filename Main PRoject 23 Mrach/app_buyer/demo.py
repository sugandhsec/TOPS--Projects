import requests

api_key = '' # Generated in your User Profile it shows at the top in a green bar once
team_slug = "" # when you sign up you have a team, its in the URL then use that
email_address = input("Enter Email ") # the test email


response = requests.post(
    "https://app.mailvalidation.io/a/" + team_slug + "/validate/api/validate/",
    json={'email': email_address},
    headers={
            'content-type': 'application/json',
             'accept': 'application/json',
            'Authorization': 'Api-Key ' + api_key,
             },
)

valid = response.json()['is_valid']
print(valid)
if valid:
    print("Valid")
else:
    print("Invalid")