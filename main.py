import os
import requests
import sys

# default URL for AppSweep
url = "https://appsweep.guardsquare.com"
# Your AppSweep Project API key (stored as a SECRET)
apiKey = os.environ["APPSWEEP_API_KEY"]
# Path to your APK file to upload and scan
inputFile = os.environ["INPUT_FILE"]
# The commit hash to use for the build
commit_hash = os.environ["COMMIT_HASH"]
# The obfuscation mapping file of the build [Optional]
mappingFile = os.environ.get('MAPPING_FILE', None)
# The library mapping file of the build [Optional]
libraryFile = os.environ.get('LIBRARY_FILE', None)
# The tags to append to the build [Optional]
tags = os.environ.get('TAGS', None)

HEADERS = {
    'Authorization': f'Bearer {apiKey}',
}

def upload_file(path):
    if path is None:
        # IMO, it is cleaner to handle this in the caller, this makes it a bit
        # implicit that `upload_build`'s arguments can be optional.
        return None

    filename = os.path.basename(path)
    signed_url_request = {
        'name': os.path.basename(path),
        'size': os.path.getsize(path),
        'type': 'application/octet-stream'
    }
    resp = requests.post(f"{url}/api/v0/files/signed-url", json=signed_url_request, headers=HEADERS)
    if resp.status_code != 200:
        print(f"{resp.text} {resp.status_code}")
        raise Exception('failed to get signed url')

    signed_url_info = resp.json()
    with open(path, 'rb') as data:
        resp = requests.put(signed_url_info['url'], data=data, headers={'Content-Type': 'application/octet-stream'})
        if resp.status_code != 200:
            print(f"{resp.text} {resp.status_code}")
            raise Exception('failed to upload file')
    return signed_url_info['fileId']

def upload_build(
    input_file_id, # required
    mapping_file_id, # optional
    library_file_id, # optional
    build_commit_hash, #optional
    build_tags, # optional
    ):
    new_build_request = {
        'inputFileId': input_file_id,
        'mappingFileId': mapping_file_id,
        'libraryFileId': library_file_id,
        'commitHash': build_commit_hash,
        'tags': build_tags,
        'source': 'api'
    }
    resp = requests.post(f"{url}/api/v0/builds", json=new_build_request, headers=HEADERS)
    if resp.status_code != 200:
        print(f"{resp.text} {resp.status_code}")
        raise Exception('failed to create build')

    build_url = resp.json()['details']['buildUrl']
    print(f"Created a new build at: {build_url}")

if __name__ == "__main__":
    input_file_id = upload_file(inputFile)
    mapping_file_id = upload_file(mappingFile)
    library_file_id = upload_file(libraryFile)

    upload_build(
        input_file_id,
        mapping_file_id,
        library_file_id,
        commit_hash,
        tags,
    )
