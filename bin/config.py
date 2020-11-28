import argparse
import json

from springapi.helpers import encode_json_uri

def create_config_filepath():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config_filepath", help="Path to the JSON configuration file")
    parser.add_argument("--protocol", default="firestore")
    parsed = parser.parse_args()

    with open(parsed.config_filepath, "rb") as fp:
        config = json.loads(fp.read())
        return encode_json_uri(parsed.protocol, config)


if __name__ == "__main__":
    credentials = create_config_filepath()
    print(credentials)
