# Project Capstone A sample blogpost for final NanoDegree Project 

## Overview

Capstone (a sample blogpost) is a full stack application for final Full Stack Nano degree submission. We've Post and Comment.
Depend on user profile, some permissions are apply to him:
 
 1. Anonymous (Unauthenticate User) : 
    - List all posts
    - Read an post 
    - Read all comment for a specific post
 2. Reader (Authenticate user): 
    - All Permissions from Anonymous 
    - Create a comment
    - Vote a comment
 3. Editor: 
    - All permissions from Reader
    - Create post
    - update post
    - delete post
    - update comment
    - delete comment

## Installation & Configuration

### Set up the Database

With Postgres running, create a `capstone` database:

```bash
createdb capstone
psql capstone < capstone.psql
```


### Run the Server

- Activate virtualEnv
On the root of the project run :

```bash
python3 -m venv venv
source venv/bin/activate
```

- Install requirements

```bash
pip install -r requirements.txt
```

- Export environment variable

```bash
source setup.sh
```

- Upgrade your application schema

```bash
python migrate db upgrade
```

- Run the server, execute:

```bash
python app.py
```

or 

```bash
flask run
```

### Generate a token

> On Postman collect token is already configure \
If you change it adapt the information on postman collection variable

You can generate a token from this link : 
 - https://dev-6c7upuk3.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=R0FdN3l1B1EDkEJ5Z6BgvgZjGIOiXbCM&redirect_uri=https://eo6nlbgy2ozay8f.m.pipedream.net

 - Test user is : 
   - Reader 
   ```
      username : reader@mmkmou.me 
      password : Passer@12
   ``` 

   - Editor
   ```
      username : editor@mmkmou.me 
      password : Passer@12
   ``` 



### Test API

 - Follow step will help you have data for test on local 
```
dropdb capstone
createdb capstone
psql capstone < capstone.psql
```

You can test all endpoint by used the postman. For That, 
 - Import the collection Capstone.postman_collection.json
 - Change Token on collectin variable for Reader and Editor
 - Run test in the predefine order 

 > To test success you need to add the prepopulate data on preview and also run once, \
you need to adapt value if you want to run it again or just remove and recreate on DB.

 - You can test one by one any endpoint by adapted  payload and/or get parameter

>  To test the online application with postman just change on the collection variable the host value with this one : \
https://capstone-blogpost.herokuapp.com 


## API Documentation

### Getting Started
- __Host__  : https://capstone-blogpost.herokuapp.com
- __Base URL__ : The base URL for the backend is  __/api/v1__. 
- ___Authentication__ : This application use __Bearer__ with Auth0 token 

> All necessary token is already provide on postman security tab for Reader and editor

### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "error": 400,
    "message": "bad request",
    "success": false
}
```
The API will return four(4) error types when requests fail:

- 400: Bad Request
- 401: Unauthorized
- 401: Forbidden
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable


### Endpoints 

#### GET /posts
- General:
    - Fetches An arrays of posts with a short body (first 100 chars) - title - id
    - Request Arguments: None
    - Returns: 
       - An object with an arrays of posts.
       - The number of posts

- Sample: `curl http://127.0.0.1:5000/api/v1/posts`

``` json
{
    "posts": [
        {
            "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam vitae augue vel massa commodo bland...",
            "id": 2,
            "image": "https://ihdemu.com/images/blog/que-es-lorem-ipsum.jpg",
            "title": "Ceci est mon second article"
        },
        {
            "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam vitae augue vel massa commodo bland...",
            "id": 3,
            "image": "https://ihdemu.com/images/blog/que-es-lorem-ipsum.jpg",
            "title": "Ceci est mon second article"
        }
    ],
    "success": true,
    "total_posts": 2
}
```

#### GET /posts/${id}
- General:
    - Get an specific post information.
    - Request Arguments: `id` - integer
    - Returns: An object with post information

- `curl 'http://localhost:5000/api/v1/posts/1'`
```json
{
    "posts": {
        "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam vitae augue vel massa commodo blandit sed non mauris. Phasellus condimentum urna eget porttitor vestibulum. Integer vitae cursus arcu. Aliquam metus eros, consequat quis laoreet in, pharetra vel massa. Praesent finibus augue lacus, sit amet accumsan magna mollis eu. Quisque metus tortor, feugiat eget maximus quis, faucibus ut nibh. In vel elit quis tellus aliquam rutrum a vel leo. Pellentesque a justo at est convallis volutpat vitae eu arcu. Nulla a tellus nulla.",
        "id": 2,
        "image": "https://ihdemu.com/images/blog/que-es-lorem-ipsum.jpg",
        "title": "Ceci est mon second article"
    },
    "success": true
}
```

#### GET /posts/${id}/comments
- General:
    - Fetches the list of comments for a specific posts.
    - Request Arguments: `id` - integer, post_id.
    - Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
- `curl 'http://localhost:5000/api/v1/posts/1/comments'`

```json
{
    "comments": [
        {
            "id": 5,
            "message": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...",
            "title": "to delete",
            "vote": 0
        }
    ],
    "success": true
}
```
#### POST /posts
- General:
    - Create a new post
- Request Body:
```json
{
    "title": "Lorem ipsum dolor sit ame",
    "message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam vitae augue vel massa commodo blandit sed non mauris. Phasellus condimentum urna eget porttitor vestibulum. Integer vitae cursus arcu. Aliquam metus eros, consequat quis laoreet in, pharetra vel massa. Praesent finibus augue lacus, sit amet accumsan magna mollis eu. Quisque metus tortor, feugiat eget maximus quis, faucibus ut nibh. In vel elit quis tellus aliquam rutrum a vel leo. Pellentesque a justo at est convallis volutpat vitae eu arcu. Nulla a tellus nulla.",
    "image_url": "https://ihdemu.com/images/blog/que-es-lorem-ipsum.jpg"
}
```
`curl --request POST 'http://localhost:5000/api/v1/posts' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Lorem ipsum dolor sit ame",
    "message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam vitae augue vel massa commodo blandit sed non mauris. Phasellus condimentum urna eget porttitor vestibulum. Integer vitae cursus arcu. Aliquam metus eros, consequat quis laoreet in, pharetra vel massa. Praesent finibus augue lacus, sit amet accumsan magna mollis eu. Quisque metus tortor, feugiat eget maximus quis, faucibus ut nibh. In vel elit quis tellus aliquam rutrum a vel leo. Pellentesque a justo at est convallis volutpat vitae eu arcu. Nulla a tellus nulla.",
    "image_url": "https://ihdemu.com/images/blog/que-es-lorem-ipsum.jpg"
}'`
- Response :
```json
{
    "posts": {
        "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam vitae augue vel massa commodo bland...",
        "id": 4,
        "image": "https://ihdemu.com/images/blog/que-es-lorem-ipsum.jpg",
        "title": "Lorem ipsum dolor sit ame"
    },
    "success": true
}
```

#### PATCH /posts/${id}
- General:
    - Update a post 
- Request Body:
```json
{
  "title": "updated posts title"
}
```
`curl --request PATCH 'http://localhost:5000/api/v1/posts/1' \
--header 'Content-Type: application/json' \
--data-raw '{
  "title": "updated posts title"
}'`
- Response :
```json
{
    "success": true,
    "updated": 1
}
```

#### DELETE /api/v1/posts/${id}
- General:
    - Delete a specific posts by id 

`curl --request DELETE 'http://localhost:5000/api/v1/posts/25'`
- Response :
```json
{
    "deleted": 25,
    "success": true
}
```

#### POST /api/v1/comments
- General:
    -  Create a new comment.
- Request Body:
```json
{
    "message": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...",
    "post_id": 2,
    "title": "a new comment"
}
```
`curl --request POST 'http://localhost:5000/api/v1/comments' \
--header 'content-type: application/json' \
--data-raw '{
    "message": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...",
    "post_id": 2,
    "title": "a new comment"
}'`
- Response :
```json
{
    "comments": {
        "id": 5,
        "message": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...",
        "title": "to delete",
        "vote": 0
    },
    "success": true
}
```

#### PATCH /api/v1/comments/${id}
- General:
    -  Update a comment.
- Request Body:
```json
{
    "message": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...",
    "title": "a updated comment"
}
```
`curl --request PATCH 'http://localhost:5000/api/v1/comments/5' \
--header 'content-type: application/json' \
--data-raw '{
    "message": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...",
    "title": "a updated comment"
}'`
- Response :
```json
{
    "comments": {
        "id": 5,
        "message": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...",
        "title": "a updated comment",
        "vote": 0
    },
    "success": true
}
```

#### PATCH /api/v1/comments/${id}/vote
- General:
    -  Vote for a comment
- Request Body:
```json
```
`curl --request PATCH 'http://localhost:5000/api/v1/comments/5/vote' \
--header 'content-type: application/json' \
--data-raw ''`
- Response :
```json
{
    "score": 1,
    "success": true
}
```

#### DELETE /api/v1/comments/${id}
- General:
    -  Delete a comment

`curl --request DELETE 'http://localhost:5000/api/v1/comments/5' \
--header 'content-type: application/json' \
`
- Response :
```json
{
    "deleted": 5,
    "success": true
}
```