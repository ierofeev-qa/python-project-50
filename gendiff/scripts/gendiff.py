#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(
    prog='gendiff',
    usage='gendiff [-h] first_file second_file',
    description='Compares two configuration files and shows a difference.',
)

args = parser.parse_args()
print(args.accumulate(args.integers))
