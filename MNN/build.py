#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
from typing import List
from builder import Builder, CMakeAndroidBuilder, CMakeBuilder


def get_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build and install the project")
    parser.add_argument("--platform", help="Build the project", default="Linux", choices=["Android", "Linux"])
    parser.add_argument("--clean", action="store_true", help="Clean the build directory")
    parser.add_argument("--benchmark", action="store_true", help="Build benchmark")
    parser.add_argument("--converter", action="store_true", help="Build converter")
    parser.add_argument("--demo", action="store_true", help="Build demo")
    parser.add_argument("--quantools", action="store_true", help="Build quantools")
    args = parser.parse_args()
    return args

def get_builder(args) -> Builder:
    if args.platform == "Android":
        return CMakeAndroidBuilder("build", "output")
    elif args.platform == "Linux":
        return CMakeBuilder("build", "output")
    else:
        return None

def get_build_options() -> List[str]:
    build_options = []
    if args.benchmark:
        build_options.append('-DMNN_BUILD_BENCHMARK=on')
    if args.converter:
        build_options.append('-DMNN_BUILD_CONVERTER=on')
    if args.demo:
        build_options.append('-DMNN_BUILD_DEMO=on')
    if args.quantools:
        build_options.append('-DMNN_BUILD_QUANTOOLS=on')
    if args.platform == "Android":
        build_options.append('-DMNN_OPENCL=on')
        build_options.append('-DMNN_ARM82=on')
    return build_options

if __name__ == "__main__":
    args = get_args()
    builder = get_builder(args)
    if builder is None:
        print("Unsupported platform")
        exit(1)
    if args.clean:
        builder.clean()
        exit(0)
    build_options = get_build_options()
    builder.build(build_options)
