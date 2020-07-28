REST API for Spring Voice
=========================

REST API for Spring Voice projects. Provides a single endpoint on which to build frontend applications without directly accommodating a specific backend.


System Requirements
-------------------

- Python 3.7+

Using this Application
----------------------

### Setup

1. Optional: Set up and activate virtual environment, or packages will install globally
2. Use example.env as a template to create .env files for environment variables. test.env is required for `make test` and dev.env is required for `make run`.
3. `pip install -r dependencies.py`
4. `pip install -r dependencies-dev.py`

### Starting up the app

`make run` will start the app in production mode.

### Testing

Tests are done in unittest and are initiated by pytest. They can be run using `make test`. `make` will run tests, plus linting and type checking.

User Roles and Authentication
-----------------------------

There are two user roles:

1. Admin user

    These are users who have administrative rights to edit / manage / delete submissions through the [web app](https://gitlab.com/SIVENTH/spring-voice-mobile). They log in throughh the application UI, which generates an `*administrative* <TokenValue>`, which is passed via header `Authorization: Bearer <TokenValue>` to the API.

2. Mobile app / "anonymous" user

    This is anyone other than admin users, who are accessing [the app on mobile devices](https://gitlab.com/SIVENTH/spring-voice-mobile). As of the time of writing (2020-07-16), it was decided that these users would not have a perpetual identity (at least for MVP). They make submissions using the mobile app, but there is nothing linking the user to the submission he just made. Future implementations might involve authentication using a token on user's device.

API Routes
----------

```
GET /api/v1/submissions

POST /api/v1/submissions
Content-type: application/json
{
  "name": str,
  "prefecture": Optional<str>,
  "message": str,
  "image_id": Optional<str>,
}
```

```
GET /api/v1/submissions/[id]

PUT /api/v1/submissions/[id]
Content-type: application/json
{
  "name": str,
  "prefecture": Optional<str>,
  "message": str,
  "image_id": Optional<str>,
  "approved": Optional<bool> @ADMIN-ONLY,
}

DELETE /api/v1/submissions/[id]

... OR ...
GET /api/v1/submissions/[id]/images

DELETE /api/v1/submissions/[id]/images/[id]

POST /api/v1/submissions/[id]/images
-- authentication / authorization --
Content-type: multipart/form-data


POST /api/v1/users
{
    "identifier": "..."
}

... return ...
{
    "token": <TokenValue>,
    "expires": int,
    "expires_in": int
}

```

Internal Resources
------------------

- Database table for Submissions
- Image storage location
- Database table for Users / Devices
- Database table for Tokens
