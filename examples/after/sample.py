# Dopo migrazione: nuova API
from new_api import Client

client = Client(api_key="test")
user = client.fetch_user_by_id(user_id=123)
posts = client.list_posts_by_user(user_id=123)
print(user, posts)
