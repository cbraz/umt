#!/usr/bin/python3.4

import subprocess
from shutil import which
import sys


# read the details of the rar file, equivalent to 'rar lt filename'
# receives the full path to the rar file
# returns a dict with the attribute list
# TODO check possible error conditions from stderr
def get_details(filepath):
    cmd = 'rar'
    if which(cmd) is None:
        print(cmd, 'not found in $PATH')
        sys.exit()
    output = subprocess.Popen(cmd + ' lt ' + filepath, shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = output.stdout.read().decode("utf-8").split('\n')
#    stdout = [str_.strip() for str_ in stdout]

#    print(">>>>FILEPATH: ", filepath)
#    print("stdout: ", output.stdout)
#    print("stderr: ", output.stderr)

    details = {}
    if 'is not RAR archive' in stdout[4]:
        return None
    else:
#        i = 0
#        for element in stdout:
#            print(i, "==", element)
#            i = i + 1
#        print(">>>>STDOUT: ", stdout)
        if 'Recovery record is present' in stdout[6]:
            data = stdout[11].split()
        else:
            data = stdout[9].split()
#        print(">>>>DATA: ", data)
#        i = 0
#        for element in data:
#            print(i, '==', data[i])
#            i = i + 1
        details['filename'] = data[0]
        details['size'] = data[1]
        details['packed'] = data[2]
        details['ratio'] = data[3]
        details['date'] = data[4]
        details['time'] = data[5]
        details['attr'] = data[6]
        details['crc'] = data[7]
        details['meth'] = data[8]
        details['ver'] = data[9]
#    print(details)
    return details


# Unpacks rar file to destination directory
# filepath - rar file that will be unpacked
# unpack_path - path where to unpack rar file
# TODO check possible error conditions from stderr
def unpack_rar(filepath, unpack_path):
    cmd = 'rar'
    if which(cmd) is None:
        print(cmd, 'not found in $PATH')
        sys.exit()
#    print(cmd + ' e -o+' + filepath + ' ' + unpack_path)
#    output = subprocess.Popen(cmd + ' e -o+ ' + filepath + ' ' + unpack_path,
#                              shell=True,
#                              stdout=subprocess.PIPE,
#                              stderr=subprocess.PIPE)
    output = subprocess.call(cmd + ' e -o+ ' + filepath + ' ' + unpack_path,
                              shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
#    print("stdout: ", output.stdout.read())
#    print("stderr: ", output.stderr.read())

