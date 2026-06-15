# Example Python code with deprecated API
from new_api import Client

def main():
    client = Client(api_key="secret")
    user = new_api.fetch_user_by_id(user_id=123)
    posts = new_api.list_posts_by_user(user_id=123)
    return user, posts

if __name__ == "__main__":
    main()
