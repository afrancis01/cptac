#   Copyright 2018 Samuel Payne sam_payne@byu.edu
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import requests
from .utilities import *

def sync(dataset, version="latest"):
    """Sync the specified version of the specified dataset.

    Parameters:
    dataset (str): The name of the dataset to sync
    version (str, optional): Which version of the dataset to sync. Defaults to latest.

    Returns:
    bool: Indicates whether sync was successful.
    """
    # Get our dataset path
    dataset = dataset.lower()
    dataset_path = get_dataset_path(dataset)
    if dataset_path is None: # Invalid dataset. get_dataset_path already printed an error message.
        return False

    # Update the index
    updated = update_index(dataset_path)
    if not updated:
        print("Insufficient internet to sync. Check your internet connection.")
        return False

    # Load the index
    index = get_index(dataset_path)

    # Validate the version number, including parsing if it's "latest"
    version = validate_version(version, dataset_path, index)
    if version is None: # Invalid version, or latest version installed did not match latest in index. get_latest_version_number already printed error message.
        return False

    # Construct the path to the directory for this version
    version_path = os.path.join(dataset_path, f"{dataset}_v{version}")

    # If they haven't downloaded this version before, create its directory
    if not os.path.isdir(version_path):
        os.mkdir(version_path)

    # Check the files in that version of the dataset. Download if don't exist, and update if have been changed.
    version_index = index.get(version)
    for data_file in version_index.keys():
        file_index = version_index.get(data_file)
        file_path = os.path.join(version_path, data_file)
        local_hash = hash_file(file_path) # Returns None if file doesn't exist, which will also fail the hash comparison later and lead to an update
        server_hash = file_index.get("hash")

        if local_hash != server_hash:
            file_url = file_index.get("url")
            downloaded_path = download_file(file_url, file_path, server_hash)
            if downloaded_path is None:
                print("Insufficient internet to sync. Check your internet connection.")
                return False
    return True

def update_index(dataset_path):
    """Check if the index of the given dataset is up to date with server version, and update it if needed.

    Parameters:
    dataset_path (str): The path to the dataset to check the index of.

    Returns:
    bool: Indicates if we were able to check the index and update if needed (i.e. we had internet)
    """
    # Define our file names we'll need
    index_urls_file = "index_urls.tsv"
    index_hash_file = "index_hash.txt"
    index_file = "index.txt"

    # Get, from the server, what the md5 hash of our index file should be
    index_urls_path = os.path.join(dataset_path, index_urls_file)
    urls_dict = parse_tsv_dict(index_urls_path)
    index_hash_url = urls_dict.get(index_hash_file)

    print(f"Checking that index is up-to-date...", end='\r')
    server_index_hash = download_text(index_hash_url)
    print("\033[K", end='\r') # Erase the status message

    if server_index_hash is None: # I.e., we have no internet
        return False
    else:
        index_path = os.path.join(dataset_path, index_file)
        local_index_hash = hash_file(index_path)
        if local_index_hash == server_index_hash:
            return True
        else:
            index_url = urls_dict.get(index_file)
            index_downloaded_path = download_file(index_url, index_path, server_index_hash)
            if index_downloaded_path is None:
                return False
            else:
                return True

def download_text(url):
    """Download text from a direct download url for a text file.

    Parameters:
    url (str): The direct download url for the text.

    Returns:
    str: The downloaded text.
    """
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status() # Raises a requests HTTPError if the response code was unsuccessful
    except requests.RequestException: # Parent class for all exceptions in the requests module
        return None

    text = response.text.strip()
    return text

def download_file(url, path, server_hash): 
    """Download a file from a given url to the specified location.

    Parameters:
    url (str): The direct download url for the file.
    path (str): The path to the file (not just the directory) to save the file to on the local machine.
    server_hash (str): The hash for the file, to check it against. If check fails, try download one more time, then throw an exception.

    Returns:
    str: The path the file was downloaded to.
    """
    file_name = path.split(os.sep)[-1]
    if os.path.isfile(path):
        action = "Updating"
    else:
        action = "Downloading"
    print(f"{action} {file_name}...", end='\r')

    for i in range(2):
        try:
            response = requests.get(url, allow_redirects=True)
            response.raise_for_status() # Raises a requests HTTPError if the response code was unsuccessful
        except requests.RequestException: # Parent class for all exceptions in the requests module
            return None
            
        local_hash = hash_bytes(response.content)
        if local_hash == server_hash: # Only replace the old file if the new one downloaded successfully.
            with open(path, 'wb') as dest:
                dest.write(response.content)
            print("\033[K", end='\r') # Erase the downloading message
            return path

def get_version_path(dataset, version):
    """Check that a version is valid and installed, then return the path to the version's directory.

    Parameters:
    dataset (str): The name of the dataset to perform the chores for.
    version (sr): The version of the dataset to perform the chores for.

    Returns:
    str: The path to the data files for specified version of the dataset.
    """
    # Get the path to the dataset's main directory
    dataset_path = get_dataset_path("endometrial")

    # Update the index, if possible
    update_index(dataset_path) # If there's no internet, this will return False, but we don't care
    index = get_index(dataset_path)

    # Validate the version, which includes parsing if it's "latest"
    version = validate_version(version, dataset_path, index)
    if version is None: # Validation error
        return None

    # Check that they've installed the version they requested
    version_path = os.path.join(dataset_path, f"endometrial_v{version}")
    if os.path.isdir(version_path):
        return version_path
    else:
        print(f"{version} not installed. To install, run 'cptac.sync(dataset='endometrial', version='{version}')'.")
        return None
