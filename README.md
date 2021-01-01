REST API for Spring Voice
=========================

REST API for Spring Voice projects. Provides a single endpoint on which to build frontend applications without directly accommodating a specific backend.

Requirements
------------

- Python 3.7+
- Access to the Spring Voice application on Firebase
- Your own Firebase app for development

CI/CD
-----

Continuous integration / continuous delivery is managed by a [Gitlab's CI/CD](https://docs.gitlab.com/ee/ci/). See `.gitlab-ci.yml` for details. 

The following are what happens in CI/CD:

1. A branch is merged into `primary`, triggering the runner. Two pipelines will be run: test and build.

2. Provided all pipelines succeed, the runner will proceed to push built image to AWS ECR. This depends on a number of environment variables, which are [managed by Gitlab](https://docs.gitlab.com/ee/ci/variables/README.html).

3. AWS ECR is the Docker image repository. The image will be stored here with two tags: `latest` (for last pushed image), and `branch-commit_sha-job_id`.

4. (Incomplete) The plan is to deploy on Kubernetes using AWS EKS. As of now (2020-12-31), the Deployment and Service YML files needed have been created and tested locally. They work on minikube.

Using this Application
----------------------

### Configuring external dependencies

The API has three external dependencies: an OAuth provider, a database for submissions, and a database for user tokens. At the time of writing (2020-12-31), the first is Google OAuth; the latter two are both Google Firebase. As such, the following are required:

- Google OAuth client ID *
- Google service account key **

\* See [Using OAuth 2.0 to Access Google APIs](https://developers.google.com/identity/protocols/oauth2) for instructions. Be sure that `redirect_uris` and `javascript_origins` include relevant domains for the API. There is a sample in this repo, `sample-oauth-id.json`.
\** See [Google Cloud documentation](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) for instructions. There is a sample key in this repo, `sample-service-account.json`.

See [environment variables](#environment-variables) on how to implement these.

### Installation

1. Optional, for development: Set up and activate a virtual environment, like venv or pyenv
2. Install dependencies: `pip install -r dependencies.txt`
3. Install dev dependencies: `pip install -r dependencies-dev.txt`
4. Configure [environment variables](#environment-variables)

### Configure environment variables

There are three environment variables which govern how the app runs. The following are mandatory:

1. `AUTH`: Protocol and config file for OAuth provider
2. `KEY`: The secret key for token creation (see [PyJWT](https://pyjwt.readthedocs.io/en/stable/usage.html) for explanation)
3. `SUBMISSION`: Protocol and config file for submissions database
4. `TOKEN`: Protocol and config file for token database

The following are optional, as they have default:

5. `ENV`: Runtime environment - `development`, `production`, or `testing`; defaults to `testing` if not set
6. `DEBUG`: Debug mode - `True` or `False`; defaults to `True` in development, otherwise `False`

### Starting in development mode

`make run AUTH=path-to-oauth-id KEY=abc123 SUBMISSION=path-to-service-account TOKEN=path-to-service-account` will start the app in development mode. `path-to-oauth-id` is location of Google OAuth client ID and `path-to-service-account` location of Google Cloud service account key.

Once started, you can send HTTP requests to `http://localhost:5000/api/v1/<route>` using curl or a client like Postman. Note that if you've set up Firebase correctly, you are making requests to live resources.

Test, lint, type check
----------------------

Tests are done in unittest and are initiated by pytest. `make test` will run tests in quiet mode; otherwise, `pytest <options>` can be used to run your own tests.

Linting is handled by `flake8`. `make lint` will lint the application and tests.

Type checking is handled by `mypy`. `make type-check` will type check the application and tests.

`make` will run tests, linting, and type checking in that order. Do this before pushing a commit to Gitlab, as the Gitlab CI will run these operations.

User Roles and Authentication
-----------------------------

There are two user roles:

1. Admin user

    These are users who have administrative rights to edit / manage / delete submissions through the [web app](https://gitlab.com/SIVENTH/spring-voice-web). They log in throughh the application UI, which generates an `*administrative* <TokenValue>`, which is passed via header `Authorization: Bearer <TokenValue>` to the API.

2. Mobile app / "anonymous" user

    This is anyone other than admin users, who are accessing [the app on mobile devices](https://gitlab.com/SIVENTH/spring-voice-mobile). As of the time of writing (2020-07-16), it was decided that these users would not have a perpetual identity (at least for MVP). They make submissions using the mobile app, but there is nothing linking the user to the submission he just made. Future implementations might involve authentication using a token on user's device.

API Routes
----------

The API uses [REST](https://en.wikipedia.org/wiki/Representational_state_transfer). It accepts [JSON-encoded](https://en.wikipedia.org/wiki/JSON#MIME_type) requests (`Content-Type application/json`) and returns JSON-encoded responses. Responses use standard [HTTP response codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes). Requests use [HTTP verbs / methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods); allowed methods include `GET`, `POST`, and `PUT`.

### Submissions

#### Get all submissions

Request:

```shell script
GET /api/v1/submissions
```

Returns:

```json
"submissions": {
    [id]: {
        "allowSNS": bool,
        "allowSharing": bool,
        "id": str,
        "isApproved": bool,
        "message": str,
        "name": str,
        "prefecture": str
    }
}
```

#### Get single submission

Request:

```shell script
GET /api/v1/submissions/[id]
```

Returns:

```json
{
    [id]: {
        "allowSNS": bool,
        "allowSharing": bool,
        "id": str,
        "isApproved": bool,
        "message": str,
        "name": str,
        "prefecture": str
    }
}
```

#### Create single submission

Request:

```shell script
POST /api/v1/submissions
```

Payload:

```json
{
    "allowSNS": bool,
    "allowSharing": bool,
    "isApproved": bool,
    "message": str,
    "name": str,
    "prefecture": str
}
```

Returns:

```json
{
    [id]: {
        "allowSNS": bool,
        "allowSharing": bool,
        "id": str,
        "isApproved": bool,
        "message": str,
        "name": str,
        "prefecture": str
    }
}
```

#### Update single submission

Request:

```shell script
PUT /api/v1/submissions/[id]
```

Payload:

```json
{
    "allowSNS": bool,
    "allowSharing": bool,
    "isApproved": bool,
    "message": str,
    "name": str,
    "prefecture": str
}
```

Returns:

```json
{
    "success": "[id] updated in submissions"
}
```

### authentication / authorization

Below is yet to be implemented and is (as of 2020-09-07) yet to be fully thought through.

Request:

```shell script
Content-type: multipart/form-data

POST /api/v1/users
```

Payload:

```json
{
    "identifier": str
}
```

Return:

```json
{
    "token": <TokenValue>,
    "expires": int,
    "expires_in": int
}
```
