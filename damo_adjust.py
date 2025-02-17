#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

"Adjust a damon monitoring result with new attributes"

import argparse

import _damon_result

def set_argparser(parser):
    parser.add_argument('--aggregate_interval', type=int, default=None,
            metavar='<microseconds>', help='new aggregation interval')
    parser.add_argument('--input', '-i', type=str, metavar='<file>',
            default='damon.data', help='input file name')
    parser.add_argument('--output', '-o', type=str, metavar='<file>',
            default='damon.adjusted.data', help='output file name')
    parser.add_argument('--output_type', choices=['record', 'perf_script'],
            default='record', help='output file\'s type')
    parser.add_argument('--output_permission', type=str, default='600',
            help='permission of the output file')
    parser.add_argument('--skip', type=int, metavar='<int>', default=20,
            help='number of first snapshots to skip')

def main(args=None):
    if not args:
        parser = argparse.ArgumentParser()
        set_argparser(parser)
        args = parser.parse_args()

    file_path = args.input

    output_permission, err = _damon_result.parse_file_permission_str(
            args.output_permission)
    if err != None:
        print('wrong --output_permission (%s) (%s)' %
                (args.output_permission, err))
        exit(1)

    result, err = _damon_result.parse_damon_result(file_path)
    if err:
        print('monitoring result file (%s) parsing failed (%s)' %
                (file_path, err))
        exit(1)

    if args.aggregate_interval != None:
        _damon_result.adjust_result(result, args.aggregate_interval, args.skip)
    _damon_result.write_damon_result(result, args.output, args.output_type,
            output_permission)

if __name__ == '__main__':
    main()
