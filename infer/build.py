#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import shutil
import os
from builder import Builder, CMakeAndroidBuilder, CMakeBuilder


def get_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build and install the project")
    parser.add_argument("--platform", help="Build the project", default="Linux", choices=["Android", "Linux"])
    parser.add_argument("--clean", action="store_true", help="Clean the build directory")
    args = parser.parse_args()
    return args


def get_builder(args) -> Builder:
    if args.platform == "Android":
        return CMakeAndroidBuilder("build", "output")
    elif args.platform == "Linux":
        return CMakeBuilder("build", "output")
    else:
        return None

def package():
    current_path = os.path.dirname(os.path.realpath(__file__))
    if args.platform == "Android":
        shutil.copy2(os.path.join(current_path, "..", "MNN", "libs", "android", "libMNN.so"), 
                     os.path.join(current_path, "output", "libMNN.so"))
        shutil.copy2(os.path.join(current_path, "..", "MNN", "libs", "android", "libMNN_Express.so"), 
                     os.path.join(current_path, "output", "libMNN_Express.so"))
        shutil.copy2(os.path.join(current_path, "..", "MNN", "libs", "android", "libMNN_CL.so"), 
                     os.path.join(current_path, "output", "libMNN_CL.so"))
        shutil.copy2(os.path.join(current_path, "..", "MNN", "libs", "android", "libMNNConvertDeps.so"), 
                     os.path.join(current_path, "output", "libMNNConvertDeps.so"))
    elif args.platform == "Linux":
        shutil.copy2(os.path.join(current_path, "..", "MNN", "libs", "linux", "libMNN.so"), 
                     os.path.join(current_path, "output", "libMNN.so"))
    shutil.copy2(os.path.join(current_path, "..", "train", "linear.mnn"), 
                 os.path.join(current_path, "output", "linear.mnn"))


if __name__ == "__main__":
    args = get_args()
    builder = get_builder(args)
    if builder is None:
        print("Unsupported platform")
        exit(1)
    if args.clean:
        builder.clean()
        exit(0)
    builder.build()
    package()
