#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(
    prog='gendiff',
    usage='gendiff [-h] [-f FORMAT] first_file second_file',
    description='Compares two configuration files and shows a difference.',
)

parser.add_argument('-f', '--format', help='set format of output')

args = parser.parse_args()
print(args.accumulate(args.integers))
