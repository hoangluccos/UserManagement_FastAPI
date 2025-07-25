from fastapi import FastAPI, HTTPException
import os
import json
import schemas

app = FastAPI()

USERS_FILE = "users.json"
USER_DATABASE = []


if os.path.exists(USERS_FILE):
    try:
        with open(USERS_FILE, "r") as f:
            USER_DATABASE = json.load(f)
    except json.JSONDecodeError:
        USER_DATABASE = []  

@app.get("/")
def read_root():
    return {"result": "Hello world"}

@app.get("/users")
def get_all_users():
    return {
        "result": {
            "listUser": USER_DATABASE
        }
    }


@app.post("/user")
def add_update_user(newUser: schemas.User):
    user_dict = newUser.dict()

    for idx, user in enumerate(USER_DATABASE):
        #update user
        if(user['name'].lower() == newUser.name.lower()):
            USER_DATABASE[idx] = user_dict
            with open(USERS_FILE, "w") as f:
                json.dump(USER_DATABASE, f, indent=2)
            return {
                "result": {
                    "message": f"User {newUser.name} was updated."
                }
            }
    #add user
    USER_DATABASE.append(user_dict)
    with open(USERS_FILE, "w") as f:
        json.dump(USER_DATABASE, f, indent=2)
    return {
        "result": {
            "message": f"User {newUser.name} was added."
        }
    }
    
    

@app.get("/user/{name}")
def find_user_by_name(username: str):
    for user in USER_DATABASE:
        if(user["name"].lower() == username.lower()):
            return {"result": user}
    return {
        "error" : f"User with {username} wasn't found"
    }

@app.delete("/user/{name}")
def delete_user_by_username(username: str):
    for user in USER_DATABASE:
        if(user["name"].lower() == username.lower()):
            USER_DATABASE.remove(user)
            with open(USERS_FILE, "w") as f:
                json.dump(USER_DATABASE, f)
            return {"result": {
                "message" : f"Delete user by username {username} successfully"
            }}
    return {
        "error" : f"User with {username} wasn't found"
    }
