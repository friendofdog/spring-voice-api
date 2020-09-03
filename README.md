REST API for Spring Voice
=========================

REST API for Spring Voice projects. Provides a single endpoint on which to build frontend applications without directly accommodating a specific backend.

Requirements
------------

- Python 3.7+
- Access to the Spring Voice application on Firebase
- Your own Firebase app for development

Using this Application
----------------------

Setup
=====

1. Optional: Set up and activate a virtual environment, like venv or pyenv.
2. Install dependencies: `pip install -r dependencies.py`.
3. Install dev dependencies: `pip install -r dependencies-dev.py`.
4. Acquire service account keys from Google and put it somewhere that can be accessed by this app.*
5. Configure environment variables (see below).

\* See [Google Cloud documentation](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) for instructions. There is a sample key in this repo, `sample-config.json`.

### Environment variables

There are three environment variables which govern how the app runs:

1. `ENV`: `development`, `production`, `testing`. Defaults to `testing` if not set.
2. `DEBUG`: `True` or `False`. Defaults to `True` in development, otherwise `False`.
3. `DATABASE_URI`: Determines the scheme and configuration for the database. The value should be the path to the aforementioned Google Cloud service account key.

Starting up the app
===================

`make run CONFIG=path-to-config` will start the app in development mode. `path-to-config` is wherever you put the Google Cloud service account key.

Once started, you can send HTTP requests to `http://localhost:5000/api/v1/<route>` using curl or a client like Postman. Note that if you've set up Firebase correctly, you are making requests to live resources.

Testing
=======

Tests are done in unittest and are initiated by pytest. They can be run using `make test`. `make` will run tests, plus linting and type checking.

User Roles and Authentication
-----------------------------

There are two user roles:

1. Admin user

    These are users who have administrative rights to edit / manage / delete submissions through the [web app](https://gitlab.com/SIVENTH/spring-voice-web). They log in throughh the application UI, which generates an `*administrative* <TokenValue>`, which is passed via header `Authorization: Bearer <TokenValue>` to the API.

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
