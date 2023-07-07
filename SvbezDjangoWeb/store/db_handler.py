import os
import hashlib


def hash_upload(instance, filename):
    instance.my_file.open()  # make sure we're at the beginning of the file
    contents = instance.my_file.read()  # get the contents
    fname, ext = os.path.splitext(filename)
    return "{0}_{1}{2}".format(fname, hashlib.sha256().update(contents), ext)  # assemble the filename
