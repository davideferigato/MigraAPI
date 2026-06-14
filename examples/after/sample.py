# Example Python code with deprecated API
from new_api import Client, fetch_data
import old_api as api

def main():
    client = Client(api_key="secret")
    
    # Direct call
    user = new_api.fetch_user_by_id(user_id=123)
    print(user)
    
    # Call via client instance (if client uses same method names)
    posts = client.fetch_posts(user_id=123)
    
    # Function import call
    data = fetch_data(user_id=123)
    
    # Alias call
    result = api.get_user(user_id=456)
    
    return user, posts, data, result

if __name__ == "__main__":
    main()
