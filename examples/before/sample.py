# Esempio di codice Python con vecchia API
from old_api import Client

client = Client(api_key="test")
user = client.get_user(user_id=123)
posts = client.fetch_posts(user_id=123)
print(user, posts)
