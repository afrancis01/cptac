import os
import sys
import hashlib
import glob

mylist = glob.glob("**/*",recursive=True)
print(mylist)
for path in mylist:
    pathlist = path.split("/")
    print(pathlist)
    mypath = ""
    for item in pathlist[:-1]:
        mypath = mypath + item + "/"
    if os.path.isfile(pathlist[-1]):
        hasher = hashlib.md5()
        with open(path, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        myhash = hasher.hexdigest()
        file = open(mypath + pathlist[-1] + ".md5hash","w")
        file.write(myhash)
        file.close()
