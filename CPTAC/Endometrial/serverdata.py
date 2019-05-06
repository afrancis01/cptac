import hashlib
import os
import wget
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

def retrieve_file(fileurl, local_path):
    ensure_dir(local_path)
    data_file_name = wget.download(fileurl, local_path)
    
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
    dict = parse_file_dict(dict_path)
    retrieve_file(dict.get(remote_path + ".md5hash"), "tempsum.md5hash")
    sumfile = open("tempsum.md5hash",'r')
    sum = sumfile.readline()
    if not compare_sums(sum, local_path):
        retrieve_file(dict.get(remote_path),local_path)
        print("\nfile downloaded")
    else:
        print("\nfile exists and is up to date")
    os.remove("tempsum.md5hash")
