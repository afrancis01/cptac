from boxsdk import DevelopmentClient
import hashlib
import os
import errno

def concat(arr, delim):
    final = ""
    for x in arr:
        final += x + delim
    return final[:-1]

def ensure_dir(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        if not directory == '':
            os.makedirs(directory)

def parse_file_dict(path):
    dict = open(path, 'r')
    dictlines = dict.readlines()
    dict.close()
    parsedict = {}
    for line in dictlines:
        data = line.split('\t')
        parsedict[data[0]] = data[1]
    return parsedict

def makesum(filename):
    hasher = hashlib.md5()
    with open(filename, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    myhash = hasher.hexdigest()
    return myhash

def retrieve_file(client, fileid, local_path):
    box_file = client.file(fileid).get()
    ensure_dir(local_path)
    file = open(local_path,'wb')
    box_file.download_to(file)
    file.close()
        
def compare_sums(serversum, localfile):
    try:
        md5returned = makesum(localfile) 
        if serversum == md5returned:
            return 1
        else:
            return 0
    except:
        return 0

def get_remote_file(remote_path, local_path, dict_path):
    client = DevelopmentClient()
    dict = parse_file_dict(dict_path)
    print(dict.get(remote_path))
    print(dict.get(remote_path + ".md5hash"))
    retrieve_file(client, dict.get(remote_path + ".md5hash"), "tempsum")
    sumfile = open("tempsum",'r')
    sum = sumfile.readline()
    if not compare_sums(sum, local_path):
        retrieve_file(client, dict.get(remote_path),local_path)
        print("file downloaded")
    else:
        print("file exists and is up to date")


get_remote_file("EndometrialData/clinical.txt","Data/do/notenter/clinical.txt","dictionary.txt")
