from django.shortcuts import render
import requests

def get_seat_availability(request):
    api_key = "your_api_key"
    bus_id = "bus_id"
    date = "yyyy-mm-dd"
    url = f"https://api.redbus.com/v2/seat?key={api_key}&busid={bus_id}&doj={date}"

    response = requests.get(url)
    data = response.json()
    seat_data = data["seats"]

    return render(request, "available.html", {"seat_data": seat_data})

# Create your views here.
