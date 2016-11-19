#!/usr/bin/python3.4

from os import listdir, mkdir, getcwd
from os.path import isfile, isdir, join, realpath, getsize
import umt_rar
import click
import sys


@click.group()
def umt():
    """ Unpacking management tool """
    pass


@umt.command()
@click.option('--path',
              default=None,
              help='specific path to scan',
              nargs=1)
@click.option('--recursive/--non-recursive',
              default=True,
              help='if scan should be recursive (default) or not')
def ls(path, recursive):
    """ List existing rar files. """
    if path is None:
        path = getcwd()

    if isdir(path):
        rlist = rar_list(path, recursive)
        print(rlist)
    else:
        print('"' + path + '"', " is not a valid directory!")


@umt.command()
@click.option('--rar-path',
              default=None,
              help='path to rar file',
              nargs=1)
@click.option('--unpack-path',
              default=None,
              help='path where rar file was unpacked',
              nargs=1)
def check(rar_path, unpack_path):
    """ Check if rar file has already been unpacked correctly """
    if rar_path is None or unpack_path is None:
        print('Provide rar and unpack path.')
        sys.exit()

    rar_file = realpath(rar_path)
    if isfile(rar_file) and rar_file.endswith('.rar'):
        rar_info = umt_rar.get_details(rar_file)
        if check_if_fully_unpacked(unpack_path, rar_info):
            print('Rar fully unpacked to',
                  join(realpath(unpack_path), rar_info['filename']))
        else:
            print('Rar not unpacked')


@umt.command('mass-unpack')
@click.option('--rar-path',
              default=None,
              help='path to rar files',
              required=True,
              nargs=1)
@click.option('--unpack-path',
              default='unpack',
              required=True,
              help='path where to unpack files',
              nargs=1)
@click.option('--recursive/--non-recursive',
              default=True,
              help='if scan should be recursive (default) or not')
def mass_unpack(rar_path, unpack_path, recursive):
    """ Unpack all rar files found in a directory to a destination path """
    rpath = realpath(rar_path)
    upath = realpath(unpack_path)

    if isdir(rpath) and isdir(upath):
        rlist = rar_list(rpath, recursive)
#        print(rlist)
        for rar_file in rlist:
#            print(rar_file)
            rar_info = umt_rar.get_details(rar_file)
#            print(rar_info)
            if rar_info is None:
                pass
            elif check_if_fully_unpacked(upath, rar_info):
                print(rar_file, 'unpacked to', rar_info['filename'])
            else:
                print(rar_file, 'needs to be unpacked.')
                umt_rar.unpack_rar(rar_file, upath)
    else:
        print('One of the provided paths is invalid:')
        sys.exit()


# Returns True if it finds a file in unpack path with the same name and size as the one in the rar file
# upath - path where to look for the unpacked files (not recursive)
# rar_info - dict with file information extracted from the rar file
def check_if_fully_unpacked(upath, rar_info):
    unpack_path = realpath(upath)
    file_path = join(unpack_path, rar_info['filename'])
    try:
        fsize = getsize(file_path)
        if fsize == int(rar_info['size']):
            return True
        else:
            return False
    except FileNotFoundError:
        return False


# returns a list of *.rar files in a path
# if 'recursive' is set to true then it will call it self for any new directory that it finds
# path - path to scan for rar files
# recursive - if any discovered directories should also be scanned
def rar_list(path, recursive):
#    print(path, recursive)
    rlist = []
    filelist = listdir(path)
    for file in filelist:
        file = join(path, file)
        if isdir(file):
            if recursive:
                new_path = join(getcwd(), file)
                rlist = rlist + rar_list(new_path, recursive)
        elif isfile(file):
            if file.endswith('.rar'):
                rlist.append(file)
        else:
            print('\'' + file + '\'', 'is neither a file or a directory.')

    return rlist


# returns info of files in the provided rar file
def get_rar_info(rar):
    #tprint(rar)
    umt_rar.get_details(rar)


if __name__ == '__main__':
    umt()


#    # Create dir to unpack files if it doesn't exist yet
#    try:
#        mkdir(unpack_root)
#    except OSError:
#        pass


#    dirs = get_dirs(dir_to_scan)
#    for dir_ in dirs:
#        rars = get_rars_on_dir(dir_)
#        if len(rars) > 1:
#            print(dir_)
#            print(len(rars))
#            pass
#        elif len(rars) == 1:
#            #print(rars)
#            unpack_path = join(unpack_root, dir_)
#            try:
#                mkdir(unpack_path)
#                print("Creating dir", unpack_path)
#            except OSError:
#                pass
#            get_rar_info(rars[0])
#
#            # patoolib.extract_archive(rars[0], outdir=unpack_path)

