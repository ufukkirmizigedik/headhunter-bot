import requests
import webbrowser


client_id = "your client ID"
client_secret = "secret key"
redirect_uri = "http://localhost:8000/callback"

# Kullanıcıyı yetki sayfasına yönlendir
auth_url = f"https://hh.ru/oauth/authorize?response_type=code&client_id={client_id}&state=abc123"
print("Tarayıcıda açılıyor:", auth_url)
webbrowser.open(auth_url)

# Kullanıcı giriş yapıp izin verince, URL'den 'code=' parametresini alacağız
authorization_code = input("Tarayıcıdan geri dönen URL'deki code değerini yapıştırın: ")

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
