import requests
import webbrowser


client_id = "your client ID"
client_secret = "secret key"
redirect_uri = "http://localhost:8000/callback"


auth_url = f"https://hh.ru/oauth/authorize?response_type=code&client_id={client_id}&state=abc123"
print("Tarayıcıda açılıyor:", auth_url)
webbrowser.open(auth_url)


authorization_code = input("Paste the 'code' parameter from the URL after authorization in your browser: ")

# Token alma isteği
data = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "client_id": client_id,
    "client_secret": client_secret,
    "redirect_uri": redirect_uri
}

response = requests.post("https://hh.ru/oauth/token", data=data)
print("Token answer:")
print(response.json())
