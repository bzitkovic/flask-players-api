# flask-players-api
Flask API with the use of JWT token 

## POST /register
To use the API you first need to register with username and password

## POST /login
For using the API you first need to login, if you don't have an account you need to register first. After you logged in, you get a JWS token for authentication
which need to be in a header of every call as 'x-access-tokens'

JSON object returned:
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZXhwIjoxNjMwMzIwMjM5fQ.FJNqfWEMe_GBs1HbpjP-6TIJGSTY0NVU6t2ie3jhDlk"
}
```

##  GET /players
Returns all the players in the database as JSON object

```json
[
    {
        "players": [
            {
                "age": 27,
                "club": "F.C. Juventus",
                "id": 2,
                "name": "Pavel",
                "nationality": "Czech",
                "surname": "Nedved"
            },
            {
                "age": 26,
                "club": "F.C. Juventus",
                "id": 3,
                "name": "Alessandro",
                "nationality": "Italian",
                "surname": "Del Piero"
            }
         ]
    },
    200
]
```

## GET /players/<id>
Returns single player with specific <id> as JSON object
  
```json
/players/2 returns: 

[
    {
        "player": {
            "age": 27,
            "club": "F.C. Juventus",
            "id": 2,
            "name": "Pavel",
            "nationality": "Czech",
            "surname": "Nedved"
        }
    },
    200
]
```
  
## POST /players
Adds new player to the database if the request is POST call in JSON format
Example:
```json
{
	"name": "Alessandro",
	"surname": "Del Piero",
	"age": 26,
	"nationality": "Italian",     
	"club": "F.C. Juventus",                                          
}
```
  
If the request is successful the API return the newly inserted object

## PUT /players/<id>

Updated existing player with requested <id> in the database 

Example:
```json
{
	"name": "Updated Alessandro",
	"surname": "Del Piero",
	"age": 26,
	"nationality": "Italian",     
	"club": "F.C. Juventus",                                          
}
```
  
If the requst is successful the API returns updated object in JSON format

## DELETE /players/<id>

Deletes the player with requested <id> from the database


