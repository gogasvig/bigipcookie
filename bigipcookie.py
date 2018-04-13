#!/usr/bin/env python2
'''
Utilities related to BigIP's cookie format.
'''

from __future__ import print_function


from argparse import ArgumentParser
import logging
import re
import socket
import struct
import sys


__all__ = ['big2ip',
           'big2port',
           'ip2big',
           'port2big',
           'swap16']


def big2ip(addr):
    '''addr: int; Integer that is treated like an unsigned long (32 bits).

    Convert BigIP integer to IP address.

    See also int2ip().

    '''
    if isinstance(addr, str):
        addr = int(addr)

    if addr < 0 or addr > 4294967295:
        logging.error("big2ip: requires 0 <= encoded IP address <= 4294967295")
        return None

    return socket.inet_ntoa(struct.pack("!I", addr)[::-1])


def big2port(port):
    '''port: str; Port number in BigIP port number.

    Convert BigIP port number to integer.

    '''
    return swap16(port)


def cmd_args():
    '''Process command line arguments.

    '''
    parser = ArgumentParser(
        description='Utilities for BigIP cookie format.')

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--ip',
        action="store_true",
        help="Encode an IP address")

    group.add_argument(
        '--port',
        action="store_true",
        help="Encode an port")

    parser.add_argument(
        'value',
        help="Input value could be a BigIP cookie (e.g. '16885952.39455.000')," +
        " IP address or port number (see '--ip' and '--port').")

    return parser.parse_args()


def ip2big(addr):
    '''addr: str; IP address.

    Convert IP address to BigIP integer.

    See also ip2int().

    '''
    result = None
    try:
        result = struct.unpack("!I", socket.inet_aton(addr)[::-1])[0]
    except socket.error, err:
        logging.error("%s", err)

    return result


def ip2int(addr):
    '''addr: str; IP address

    Credit: https://stackoverflow.com/questions/5619685/conversion-from-ip-string-to-integer-and-backward-in-python#13294427

    '''
    return struct.unpack("!I", socket.inet_aton(addr))[0]


def int2ip(addr):
    '''addr: int; IP address represented as an integer.

    Credit: https://stackoverflow.com/questions/5619685/conversion-from-ip-string-to-integer-and-backward-in-python#13294427

    '''
    return socket.inet_ntoa(struct.pack("!I", addr))


def port2big(port):
    '''port: int; Port number.

    Convert integer to BigIP port number.

    '''
    return swap16(port)


def swap16(unsigned_short):
    '''unsigned_short: int; Integer that is treated like an unsigned short
    (16 bits).

    This function will swap 2 bytes from big endian to little endian.

    E.g. If the input was an unsigned_short of 0x1234, then the result
    would be 0x3412.

    '''

    if isinstance(unsigned_short, str):
        try:
            unsigned_short = int(unsigned_short)
        except ValueError:
            logging.error("Could not convert '%s' to integer.", unsigned_short)

    if unsigned_short < 0 or unsigned_short > 65535:
        logging.error("swap16: requires 0 <= port number <= 65535")
        return None

    return struct.unpack("<H", struct.pack(">H", unsigned_short))[0]


def main():
    '''Main entry.

    '''
    args = cmd_args()

    # == 3 cases ==
    # 1) User wants IP address converted.
    # 2) User wants port number converted.
    # 3) User wants cookie crumbled.

    if args.ip:
        ip_pat = (r'^(\d+\.\d+\.\d+\.\d+)$')
        match = re.search(ip_pat, args.value)

        if not match:
            logging.error('Could not parse IP address.')
            sys.exit(1)

        print("Encoded IP address: {}".format(ip2big(args.value)))
    elif args.port:
        print("Encoded port: {}".format(port2big(args.value)))
    else:
        cookie_pat = (r'^(\d+)\.(\d+)\.\d+$')
        match = re.search(cookie_pat, args.value)

        if not match:
            logging.error('Could not parse BigIP cookie.')
            sys.exit(1)

        (addr, port) = match.groups()

        print("IP address: {}; Port: {}".format(big2ip(addr), big2port(port)))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
