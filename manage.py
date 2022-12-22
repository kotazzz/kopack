#!/usr/bin/env python3
import argparse
import json
import os
import shlex
import shutil
import time
import zipfile

def parse_info(path):
    data = {}
    content = open(path).read()
    for line in content.splitlines():
        if line.startswith('#'):
            continue
        key, val = shlex.split(line)
        data[key] = val
    return data

def log(msg):
    # HH MM SS
    ts = time.strftime('%H:%M:%S')
    print(f'[{ts}]: {msg}')

# add package to list
# 1. get path of new package folder
# 2. get info.meta
def add_package(path, rewrite=False):
    info_file = os.path.join(path, 'info.meta')
    log(f'Path: {path}')
    if not os.path.exists(info_file):
        raise Exception('File info.meta not found')
    else:
        log('Adding package...')
        log(f'Meta: {info_file}')
        meta = parse_info(info_file)
        log(f'Name: {meta["name"]}')
        log(f'Version: {meta["version"]}')
        # package name format is: name-version
        package_filename = os.path.join('packages', meta['id']+'-'+meta['version'])
        # if file exists, raise exception
        if os.path.exists(package_filename+".kpkg") and not rewrite:
            log('Package already exists')
            exit(1)
        else:
            # zip all files in path and put it to packages/package_name.kpkg
            with zipfile.ZipFile(package_filename+".kpkg", 'w') as zip:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        zip.write(os.path.join(root, file), os.path.join(root, file).replace(path, ''))
                        
            # write meta info as packages/package_name.meta
            shutil.copyfile(info_file, package_filename+".meta")
    
def remove_package(id, version):
    # remove package from list
    # 1. get package name
    # 2. remove package file
    # 3. remove meta file
    log(f'Removing package {id} {version}')
    package_filename = os.path.join('packages', id+'-'+version)
    if os.path.exists(package_filename+".kpkg"):
        os.remove(package_filename+".kpkg")
        log('Package removed')
    if os.path.exists(package_filename+".meta"):
        os.remove(package_filename+".meta")
        log('Meta removed')
    

def rebuild():
        # build index
        # for file in packages:
        metas = []
        for filename in os.listdir('packages'):
            if filename.endswith('.meta'):
                meta = parse_info(os.path.join('packages', filename))
                # as json
                metas.append(meta)
        with open('packages/index.json', 'w') as f:
            f.write(json.dumps(metas))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['add', 'remove', 'rebuild'])
    parser.add_argument('-p', '--path')
    parser.add_argument('-i', '--id')
    parser.add_argument('-v', '--version')
    parser.add_argument('-r', '--rewrite', action='store_true')
    args = parser.parse_args()
    if args.action == 'add': # command: manage add -p path
        if not args.path:
            raise Exception('Path not specified')
        add_package(args.path, args.rewrite)
        rebuild()
    elif args.action == 'remove': # command: manage remove -i id -v version
        if not args.id or not args.version:
            raise Exception('ID or version not specified')
        remove_package(args.id, args.version)
        rebuild()
    elif args.action == 'rebuild': # command: manage rebuild
        rebuild()

if __name__ == '__main__':
    main()