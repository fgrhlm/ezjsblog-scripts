#!/usr/bin/env python3

import json
import sys
import argparse
import requests

arg_parser = argparse.ArgumentParser(
    prog="blog-publish",
    usage='%(prog)s key url file',
    description="publishes posts to blog-engine"
)

arg_parser.add_argument("key",type=str,help="path to key file")
arg_parser.add_argument("url",type=str,help="blog-engine url")
arg_parser.add_argument("post_id",type=str,help="id of the post you wish to delete")

if __name__=="__main__":
    args = arg_parser.parse_args()

    # API urls
    post_url = f"{args.url}/posts/{args.post_id}"
    auth_url = f"{args.url}/auth"

    # Read key file
    with open(args.key) as f:
        key = f.read()

    # Authorize @ /auth endpoint
    print("Authorizing..")
    token_request_body = {"key": key}

    token_response = requests.post(auth_url, json=token_request_body)
    token_response = json.loads(token_response.text)

    # JWT token
    token = token_response["token"]

    # Publish markdown file @ /posts endpoint
    print(f"Deleting post {args.post_id}..")

    # Headers
    delete_request_headers = {
        "content-Type": "application/json",
        "authorization": f"Bearer {token}"
    }
    
    # Publish file
    delete_response = requests.delete(
        post_url,
        headers=delete_request_headers
    )

    print(delete_response)