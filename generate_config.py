#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime
import os

CONFIG_COMMENT = '#'

def print_config(filename_in, prefix, suffix, ignore_regex):
    domain_list = []

    # Read from file
    with open(filename_in, 'r') as f:
        for line in f.read().splitlines():
            line_trimed = line.strip()
            if len(line_trimed) == 0 or line_trimed[0] == CONFIG_COMMENT:
                continue

            if ignore_regex is True and line_trimed[0] == ':' and line_trimed[-1] == ':':
                continue

            domain_list.append(line_trimed)

    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    item_count_str = 'total: '+str(len(domain_list))
    ignore_regex_str = ' (no-regex)' if ignore_regex is True else ''

    print(CONFIG_COMMENT + ' ' + filename_in + ' ' + time_str)
    print(CONFIG_COMMENT + ' ' + item_count_str + ignore_regex_str)

    for domain in domain_list:
        print(prefix + domain + suffix)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                     formatter_class=lambda prog: argparse.HelpFormatter(
                                         prog, max_help_position=120),
                                     description='A simple config file generator for dnsmasq')

    parser.add_argument(
        '-f', '--file', help='file path to input', required=True)
    parser.add_argument(
        '-p', '--prefix', help='prefix to be inserted to each line, for example: "server=/"', required=True)
    parser.add_argument(
        '-s', '--suffix', help='suffix to be appended to each line, for example: "/1.1.1.1"', required=True)
    parser.add_argument('-R', '--no-regex',
                        help='ignore regex domains', action='store_true')

    args = vars(parser.parse_args())

    print_config(args['file'], args['prefix'],
                 args['suffix'], args['no_regex'])
