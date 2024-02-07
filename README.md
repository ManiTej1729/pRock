# Lab - 3
## Flask 
### find
My find function will find the data (username, email and password) of the user by its user name.
In other words we can do /user/\<username\> to get the details
```python
    def find(user_id):
    with open('users.txt', 'r') as file:
        for line in file:
            stri = json.loads(line)
            if stri["name"] == user_id:
                return line
    return "User doesn't exists"
```
Rest everything is obvious.