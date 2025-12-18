import os

# Hardcoded secret (Security Risk)
api_key = "sk-1234567890abcdef"

def process_data(data):
    # Inefficient loop (Performance Risk)
    results = []
    for i in range(len(data)):
        # N+1 query simulation
        users = get_users_from_db() 
        for user in users:
            if user.id == data[i]:
                results.append(user)
    return results

def get_users_from_db():
    # Simulate DB call
    return []
