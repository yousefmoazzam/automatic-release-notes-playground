from typing import Optional

import requests
import sys

FILENAME = "user-announcements.txt"
USER_ANNOUNCEMENT_HEADER = "Notable Changes for Users"


def main(release_body: str, upload_url: str, auth_token: str):
    print(release_body)
    data = extract_user_announcements(release_body)
    print(data)

    if data is not None:
        upload_asset(FILENAME, data, upload_url, auth_token)


def extract_user_announcements(text: str) -> Optional[str]:
    if USER_ANNOUNCEMENT_HEADER not in text:
        return None

    lines = text.splitlines()
    idx = lines.index(f"### {USER_ANNOUNCEMENT_HEADER}")

    notes = []
    for line in lines[idx + 1 :]:
        if line.startswith("*"):
            pr_title = line.split(" by")[0]
            notes.append(pr_title)
            continue
        break

    return str.join("\n", notes)


def upload_asset(filename: str, data: str, url: str, token: str):
    url_split = url.split("{?name,label}")
    url = url_split[0]
    query_params = {"name": filename}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream",
    }
    resp = requests.post(
        url=url, params=query_params, data=data.encode(), headers=headers
    )
    print(resp.json())


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) != 3:
        print(
            "Usage: python extract-user-announcement-changes.py <release-body> <upload-url> <auth-token>"
        )
        sys.exit(1)

    main(args[0], args[1], args[2])
