#!/usr/bin/env python3
import argparse
import os
import platform
import zipfile
import requests

packages = "https://raw.githubusercontent.com/kotazzz/kopack/master/packages/"
index = packages + "index.json"

def get_index():
    return requests.get(index).json()

def get_package(id, version):
    link = packages + id + "-" + version + ".kpkg"
    # download package
    r = requests.get(link)
    # write package to file
    with open(id + "-" + version + ".kpkg", 'wb') as f:
        f.write(r.content)
    # unpack it to installed folder
    # path: installed/id-version
    # unpack package

    os.mkdir("installed/" + id + "-" + version)
    with zipfile.ZipFile(id + "-" + version + ".kpkg", 'r') as zip:
        zip.extractall("installed/" + id + "-" + version)

def run_package(id, version):
    # run package
    # path: installed/id-version/main.py
    # bin - py310/python.exe
    # get full path of bin
    # change dir to package
    # if windows
    install_path = "installed/" + id + "-" + version
    if platform.system() == "Windows":
        pybin = os.path.abspath("py310/python.exe")
        os.chdir(install_path)
        # run main.py
        os.system(f"{pybin!r} main.py")
    else:
        print("run_package() is not implemented for this platform")
        print(f"Please, run it manually: {install_path}/main.py")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="install package", nargs=2)
    parser.add_argument("-r", "--run", help="run package", nargs=2)
    args = parser.parse_args()
    if args.install:
        get_package(args.install[0], args.install[1])
    if args.run:
        run_package(args.run[0], args.run[1])