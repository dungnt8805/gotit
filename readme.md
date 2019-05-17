# Got It Test

## Getting started

### Prerequisites

```
install mysql, python, pip, pipenv
```


### Installation

clone project to local

```
git clone https://github.com/spiritwild/gotit.git
```

#### Create data table and run sql command in gotit/database.sql

move to gotit app folder
create pipenv enviroment
```
pipenv --three
```
enter pipenv shell
```
pipenv shell
```

prepare configuration
```
cp env.example .env
```

edit configuration in .env file
```
DATABASE_URL={YOUR_MYSQL_URL}
FACEBOOK_APP_ID={YOUR_FB_APP_ID}
FACEBOOK_APP_SECRET={YOUR_FB_APP_SECRET}
FACEBOOK_APP_REDIRECT={YOUR_FB_CLIENT_CALLBACK}
GOOGLE_CLIENT_ID={YOUR_GG_CLIENT_ID}
GOOGLE_CLIENT_SECRET={YOUR_GG_CLIENT_SECRET}
GOOGLE_CLIENT_REDIRECT={YOUR_GG_CLIENT_CALLBACK}
```

run app
```
python run.py
```

your app running in localhost:8080

# App API

get facebook login url
```
/api/auth/get-facebook-login-url

method: 'GET'
```

use that url to redirect client to facebook login
after facebook return to your callback url get hash #access_token then send to
```
/api/auth/facebook/authorized?access_token={access_token}

method: 'GET'
```
if access_token valid it will return jwt token

get google login url

```
/api/auth/get-google-login-url

method: 'GET'
```

use that url to redirect client to google login
after google return to your callback url get query string code then send to
```
/api/auth/google/authorized?cod={cod}

method: 'GET'
```
if access_token valid it will return jwt token

## Authorization
App authorization with Bearer Token

get token from login url then set to header with formar

```
Authorization: "Bearer {YOUR_TOKEN}"
```

### Required authenticate API

#### update information

```
/api/users/me

method: POST
required: authenticate
with payload: {full_name, phone_number, occupations}

example
{
  "full_name": "John Harry",
  "phone_number": "0934995522"
}
```

#### create blog
```
/api/blogs

method: 'POST'
required: authenticate, fill information

example payload:
{
  "title": "This is title",
  "content": "this is content"
}
```

#### list blogs

```
/api/blogs

method: 'POST'
required: authenticate, fill information

example response:
[
  {
    "title": "This is title",
    "content": "this is content"
  }
]
```

#### list user blogs
```
/api/users/{user_id}/blogs

method: 'GET'
required: authenticate, fill information

example response:
[
  {
    "title": "This is title",
    "content": "this is content"
  }
]
```

#### blog details

```
/api/blogs/{blog_id}/likes


method: GET
required: authenticate, fill information

example response:
{
  "title": "This is title",
  "content": "this is content"
}
```

#### users who liked blog
```
/api/blogs/{blog_id}


method: GET
required: authenticate, fill information

example response:
[
  {
    "id": 1,
    "email": "test@gmail.com",
    "full_name": "John Harry",
    "phone_number": "098342423"
  }
]
```
