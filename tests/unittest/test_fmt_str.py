#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

import os
import sys
import unittest

bindir = os.path.dirname(os.path.realpath(__file__))
damo_dir = os.path.join(bindir, '..', '..')
sys.path.append(damo_dir)

import _damo_fmt_str

def test_input_expects(testcase, function, input_expects):
    for input_ in input_expects:
        testcase.assertEqual(function(input_), input_expects[input_])

def test_input_expects_funcs(testcase, functions, input_expects):
    for input_ in input_expects:
        for idx, expect in enumerate(input_expects[input_]):
            test_input_expects(testcase, functions[idx], {input_: expect})

class TestDamoFmtStr(unittest.TestCase):
    def test_format_nr(self):
        self.assertEqual(_damo_fmt_str.format_nr(123, False), '123')
        self.assertEqual(_damo_fmt_str.format_nr(1234, False), '1,234')
        self.assertEqual(_damo_fmt_str.format_nr(1234567, False), '1,234,567')

    def test_text_to_nr(self):
        test_input_expects(self,
                _damo_fmt_str.text_to_nr,
                {
                    '12': 12,
                    '1,234': 1234,
                    '1,234.567': 1234.567,
                    '1,234,567': 1234567})

    def test_format_time(self):
        usec_ns = 1000
        msec_ns = 1000 * usec_ns
        sec_ns = 1000 * msec_ns
        minute_ns = 60 * sec_ns
        hour_ns = 60 * minute_ns
        day_ns = 24 * hour_ns
        test_input_expects_funcs(self,
                [lambda x: _damo_fmt_str.format_time_ns_exact(x, False),
                    lambda x: _damo_fmt_str.format_time_ns(x, False)],
                {
                    123: ['123 ns', '123 ns'],
                    123456: ['123 us 456 ns', '123.456 us'],
                    123000: ['123 us', '123 us'],
                    123456789: ['123 ms 456 us 789 ns', '123.457 ms'],
                    123000000: ['123 ms', '123 ms'],
                    123456789123:
                    ['2 m 3 s 456 ms 789 us 123 ns', '2 m 3.457 s'],
                    123000000000: ['2 m 3 s', '2 m 3 s'],
                    1 * minute_ns: ['1 m', '1 m'],
                    1 * minute_ns + 59 * sec_ns: ['1 m 59 s', '1 m 59 s'],
                    1 * minute_ns + 59 * sec_ns + 123 * msec_ns:
                    ['1 m 59 s 123 ms', '1 m 59.123 s'],
                    2 * hour_ns + 1 * minute_ns + 59 * sec_ns + 123 * msec_ns:
                    ['2 h 1 m 59 s 123 ms', '2 h 1 m 59.123 s'],
                    2 * hour_ns: ['2 h', '2 h'],
                    3 * day_ns + 2 * hour_ns + 1 * minute_ns +
                    59 * sec_ns + 123 * msec_ns:
                    ['3 d 2 h 1 m 59 s 123 ms', '74 h 1 m 59.123 s'],
                    3 * day_ns + 2 * hour_ns: ['3 d 2 h', '74 h'],
                    1234 * day_ns + 2 * hour_ns: ['1,234 d 2 h', '29618 h']})

    def test_text_to_time(self):
        test_input_expects(self,
                _damo_fmt_str.text_to_ns,
                {
                    '1': 1,
                    '1 ns': 1,
                    'max': _damo_fmt_str.ulong_max})
        test_input_expects(self,
                _damo_fmt_str.text_to_us,
                {
                    '1 us': 1,
                    '1234 us': 1234,
                    '1,234 us': 1234,
                    '1234us': 1234,
                    '1 ms': 1000,
                    '1 m 2 s': 62 * 1000 * 1000,
                    '2 h 1 m 2 s': 7262 * 1000 * 1000,
                    '3 d 2 h 1 m 2 s':
                    3 * 24 * 60 * 60 * 1000 * 1000 + 7262 * 1000 * 1000,
                    '134': 134,
                    'max': _damo_fmt_str.ulong_max})
        test_input_expects(self,
                _damo_fmt_str.text_to_ms,
                {
                    '134': 134,
                    'max': _damo_fmt_str.ulong_max})

    def test_text_to_percent(self):
        test_input_expects(self, _damo_fmt_str.text_to_percent,
                {'10%': 10.0,
                    '12.34%': 12.34,
                    '12.34 %': 12.34,
                    '1,234.567 %': 1234.567,
                    '1,234.567,89 %': 1234.56789})

    def test_text_to_bytes(self):
        test_input_expects(self, _damo_fmt_str.text_to_bytes,
                {
                    '123': 123,
                    '123 B': 123,
                    '2 K': 2048,
                    '2 KiB': 2048,
                    '2 M': 2 * 1 << 20,
                    '2 MiB': 2 * 1 << 20,
                    '2 G': 2 * 1 << 30,
                    '1,234.457 G': int(1234.457 * (1 << 30)),
                    '1,234.457 GiB': int(1234.457 * (1 << 30)),
                    '1,234.457': 1234,
                    '2 GiB': 2 * 1 << 30,
                    '2 T': 2 * 1 << 40,
                    '2 TiB': 2 * 1 << 40,
                    '2 P': 2 * 1 << 50,
                    '2 PiB': 2 * 1 << 50,
                    '2.0 PiB': 2 * 1 << 50,
                    '16384.000 PiB': (1 << 64) - 1,
                    '2.0 EiB': 2 * 1 << 60})

if __name__ == '__main__':
    unittest.main()
