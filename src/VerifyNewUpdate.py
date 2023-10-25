import sys
import requests

def verify_new_update(version, repo_owner, repo_name):
# Connect to github api and check for new release version (tag name)
# Return -1 if error; 0 if there is no update; 1 if there is update.

    print("Starting: verify_new_update()")
    print("Connecting to server")

    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    try:
        request_info_response = requests.get(api_url)

    except requests.exceptions.ConnectionError:
        print("CONNECTION FAIL")
        print("Check network connection, and try again")
        return 0

    except:
        print("UNKNOWN ERROR")
        return 0

    else:
        if request_info_response.status_code == 404:
            print("Server not found or Offline")
            print("Contact Support")
            return 0
        elif request_info_response.status_code == 200:
            print("Connection Successful")

            print("Searching for Updates")
            release_data = request_info_response.json()
            latest_version = release_data["tag_name"]

            if(latest_version != version):
                print(f"New version found: {latest_version}")
                return latest_version

            else:
                print("Already on latest version!")
                return 0


if __name__ == "__main__":
    __version__ = "v0.0.1"
    repo_owner = "MarcosYonamine963"
    repo_name = "python-auto-update"

    verify_new_update(__version__, repo_owner, repo_name)

    # print(f"REPRIIIINTTT {latest_version[0]}")