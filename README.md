REST API for Spring Voice
=========================

REST API for Spring Voice projects. Provides a single endpoint on which to build frontend applications without directly accommodating a specific backend.


System Requirements
-------------------

- Python 3.7

User Roles
----------

Mobile App / "Anonymous" User (Device)
Admin User

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

Authentication
--------------

- Mobile App User
  - Generate a random key / token at the device level?
  - Request a random key / token from the API
  - Passes token via header `Authorization: Bearer <TokenValue>`
- Admin App User
  - Login via an application UI
  - The API generates an *administrative* <TokenValue>
  - Passes token via header `Authorization: Bearer <TokenValue>`

Internal Resources
------------------

- Database table for Submissions
- Image storage location
- Database table for Users / Devices
- Database table for Tokens
