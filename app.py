import requests

url = "https://irctc1.p.rapidapi.com/api/v1/searchStation"

querystring = {"query":"Jaipur"}

headers = {
	"x-rapidapi-key": "cc5c20336amsh1e3e54bce426f0dp18a8bejsn1da808da25bf",
	"x-rapidapi-host": "irctc1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())