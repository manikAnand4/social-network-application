Social Network Manager
======================

ReadME
-----------


1. Project Setup:

    * Clone the project in your local machine
    * Run the command to build docker image (Make sure you are in the directory where   you have the docker-compose.yml file)
        ```
        docker compose build --no-cache
        ```
        Make sure you have docker compose installed locally on your machine
    * Run the service
        ```
        docker compose up
        ```
        The server will start locally on your machine's 8000 port and you can login admin using the url ->
        http://127.0.0.1:8000/admin/login/


2.  Postman API Collection Link
    * https://drive.google.com/file/d/1nCVnpghumMEhPC-Enxc7xLVnNBxU5l4u/view

3.  API Config & details
    *   User SignUp API
        * Request Type
        ```
        POST
        ```
        * Endpoint
        ```
        http://localhost:8000/user/sign-up/
        ```
        * Body
        ```
        email: str[required]
        password: str[required]
        first_name: str[optional]
        last_name: str[optional]
        ```
        * Response [200 status code]
        ```
        email: str
        first_name: str
        last_name: str
        ```
    *   User Login API
        * Request Type
        ```
        POST
        ```
        * Endpoint
        ```
        http://localhost:8000/user/login/
        ```
        * Body
        ```
        email: str[required]
        password: str[required]
        ```
        * Response [200 status code]
        ```
        token: str
        ```
    *   User List API
        * Request Type
        ```
        POST
        ```
        * Authorization
        ```
        Token token
        ```
        * Endpoint
        ```
        http://localhost:8000/user/users-list/
        ```
        * Params
        ```
        search: str
        ```
        * Response [200 status code]
        ```
        {
            "count": 2,
            "next": null,
            "previous": null,
            "results": [
                {
                    "email": "dhruv@gmail.com",
                    "first_name": "dhruv",
                    "last_name": "",
                    "id": 2
                },
                {
                    "email": "manish@gmail.com",
                    "first_name": "manish",
                    "last_name": "",
                    "id": 3
                }
            ]
        }
        ```
    *   Send Friend Request API
        * RequestType
        ```
        POST
        ```
        * Authorization
        ```
        Token token
        ```
        * Endpoint
        ```
        http://localhost:8000/user/friend-request/
        ```
        * Body
        ```
        recipient_id: int[required] ((recipient token is the 'id' we get in response from user-list API))
        ```
        * Response [200 status code]
        ```
        request_id: int
        ```
    *   Accept/Reject Friend Request API
        * RequestType
        ```
        PATCH
        ```
        * Authorization
        ```
        Token token
        ```
        * Endpoint
        ```
        http://localhost:8000/user/friend-request/<int:pk>
        
        FOR PK->
        1. pk is the 'request_id' we get when we successfully send a request
        2. pk can also be fetched from pending requests api. key will be 'id' in the api response.
        ```
        * Body
        ```
        status: int[required] (1-> Accept, 2-> Reject)
        ```
        * Response [200 status code]
        ```
        request_id: int
        ```
    *   Pending Requests
        * RequestType
        ```
        GET
        ```
        * Authorization
        ```
        Token token
        ```
        * Endpoint
        ```
        http://localhost:8000/user/pending-requests/
        ```
        * Body
        ```
        status: int[required] (1-> Accept, 2-> Reject)
        ```
        * Response [200 status code]
        ```
        {
            "count": 2,
            "next": null,
            "previous": null,
            "results": [
                {
                    "sender_email": "dhruv@gmail.com",
                    "sender_name": "dhruv",
                    "id": 2
                },
                {
                    "sender_email": "manish@gmail.com",
                    "sender_name": "manish",
                    "id": 2
                }
            ]
        }
        ```
    *   User Friends
        * RequestType
        ```
        GET
        ```
        * Authorization
        ```
        Token token
        ```
        * Endpoint
        ```
        http://localhost:8000/user/user-friends/
        ```
        * Response [200 status code]
        ```
        {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    "id": 1,
                    "friend_email": "dhruv@gmail.com",
                    "friend_name": "dhruv"
                }
            ]
        }
        ```
    