import requests

bot_token = "8028509482:AAH7gWYtzPigJt7cK--QDipyG1mBg-LFYiw"
chat_id = "@huracanescaribe"  # or -100xxxx if private
message = "✅ Prueba desde el bot de Huracanes Caribe."

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
response = requests.get(url, params={"chat_id": chat_id, "text": message})

print(response.status_code)
print(response.text)
