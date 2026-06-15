# Example Python code with deprecated API
from old_api import Client

def main():
    client = Client(api_key="secret")
    user = old_api.get_user(user_id=123)
    posts = old_api.fetch_posts(user_id=123)
    return user, posts

if __name__ == "__main__":
    main()
