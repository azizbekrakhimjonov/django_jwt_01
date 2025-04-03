import requests

BASE_URL = "http://127.0.0.1:8000/api/"

# 1. Ro‘yxatdan o‘tish
def register(username, email, password):
    url = f"{BASE_URL}register/"
    data = {
        "username": username,
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    return response.json()

# 2. Login qilish va token olish
def login(username, password):
    url = f"{BASE_URL}login/"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=data)
    return response.json()

# 3. JWT token bilan foydalanuvchi ma'lumotlarini olish
def get_user_info(user_id, access_token):
    url = f"{BASE_URL}user/{user_id}/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Test qilish
if __name__ == "__main__":
    # Ro‘yxatdan o‘tish
    reg_response = register("testuser", "test@example.com", "testpassword")
    print("Ro‘yxatdan o‘tish:", reg_response)

    # Login qilish
    login_response = login("testuser", "testpassword")
    print("Login javobi:", login_response)

    if "access" in login_response:
        access_token = login_response["access"]

        # Foydalanuvchi ma'lumotlarini olish
        user_info = get_user_info(1, access_token)
        print("Foydalanuvchi ma'lumotlari:", user_info)
    else:
        print("Login amalga oshmadi.")
