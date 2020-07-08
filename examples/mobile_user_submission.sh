#!/bin/sh

TOKEN=$( \
    curl https://api.spring-voice.com/api/v1/users \
        -X POST
        -d '{"identifier": "SOME VALUE"}' \
        -H "Content-Type: application/json" \
    | jq -r .token
);

SUBMISSION_ID=$( \
    curl https://api.spring-voice.com/api/v1/submissions \
        -X POST
        -d '{"name": "Kevin Kee" .. }' \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
    | jq -r .id
);

curl https://api.spring-voice.com/api/v1/submissions/$SUBMISSION_ID \
    -H "Authorization: Bearer $TOKEN" \
    -F image=@local_image.jpg
