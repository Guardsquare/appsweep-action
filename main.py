import os
import sys

import requests


def upload_file(path, url, headers):
    if path is None or path == "":
        # IMO, it is cleaner to handle this in the caller, this makes it a bit
        # implicit that `upload_build`'s arguments can be optional.
        return None

    signed_url_request = {
        "name": os.path.basename(path),
        "size": os.path.getsize(path),
        "type": "application/octet-stream"
    }

    resp = requests.post(
        url=f"{url}/api/v0/files/signed-url",
        json=signed_url_request,
        headers=headers
    )

    if resp.status_code != 200:
        print(f"Error code: {resp.status_code}", file=sys.stderr)
        print(f"Error message: {resp.text}", file=sys.stderr)
        raise Exception("failed to get signed URL")

    signed_url_info = resp.json()

    with open(path, "rb") as data:
        resp = requests.put(
            url=signed_url_info["url"],
            data=data,
            headers={"Content-Type": "application/octet-stream"}
        )

        if resp.status_code != 200:
            print(f"Error code: {resp.status_code}", file=sys.stderr)
            print(f"Error message: {resp.text}", file=sys.stderr)
            raise Exception("failed to upload file")

    return signed_url_info["fileId"]


def upload_build(
    input_file_id,
    mapping_file_id,
    library_file_id,
    commit_hash,
    tags,
    headers,
    url
):
    new_build_request = {
        "inputFileId":   input_file_id,
        "mappingFileId": mapping_file_id,
        "libraryFileId": library_file_id,
        "commitHash":    commit_hash,
        "tags":          tags,
        "source":        "api"
    }

    resp = requests.post(
        url=f"{url}/api/v0/builds",
        json=new_build_request,
        headers=headers
    )

    if resp.status_code != 200:
        print(f"Error code: {resp.status_code}", file=sys.stderr)
        print(f"Error message: {resp.text}", file=sys.stderr)
        raise Exception("failed to create build")

    build_url = resp.json()["details"]["buildUrl"]
    print(f"Created a new build at: {build_url}")


def main():
    # default URL for AppSweep
    url = os.environ["INPUT_URL"]
    # Your AppSweep Project API key (stored as a SECRET)
    api_key = os.environ["INPUT_APPSWEEP_API_KEY"]
    # Path to your APK file to upload and scan
    input_file = os.environ["INPUT_INPUT_FILE"]
    # The commit hash to use for the build
    commit_hash = os.environ["INPUT_COMMIT_HASH"]
    # The obfuscation mapping file of the build [Optional]
    mapping_file = os.environ.get("INPUT_MAPPING_FILE")
    # The library mapping file of the build [Optional]
    library_file = os.environ.get("INPUT_LIBRARY_FILE")
    # The tags to append to the build [Optional]
    tags = os.environ.get("INPUT_TAGS")

    if tags is not None:
        tags = tags.strip("[]").split(",")
        tags = [tag.strip() for tag in tags]

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    input_file_id = upload_file(path=input_file, url=url, headers=headers)
    mapping_file_id = upload_file(path=mapping_file, url=url, headers=headers)
    library_file_id = upload_file(path=library_file, url=url, headers=headers)

    upload_build(
        input_file_id=input_file_id,
        mapping_file_id=mapping_file_id,
        library_file_id=library_file_id,
        commit_hash=commit_hash,
        tags=tags,
        url=url,
        headers=headers
    )


if __name__ == "__main__":
    main()
