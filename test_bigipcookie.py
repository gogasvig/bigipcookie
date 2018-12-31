#!/usr/bin/python
'''
Test cases for bigipcookie.
'''

import unittest

import bigipcookie as bic
import requests

class TestBIC(unittest.TestCase):
    '''bigipcookie test cases.'''

    def test_decode_1(self):
        '''Test case.'''

        ip_list = ['10.1.209.22', 382796042]

        self.assertEqual(ip_list[0], bic.big2ip(ip_list[1]))

    def test_decode_2(self):
        '''Test case.'''

        ip_list = ['10.1.209.2', 47251722]

        self.assertEqual(ip_list[0], bic.big2ip(ip_list[1]))

    def test_decode_3(self):
        '''Test case.'''

        ip_list = ['10.1.209.1', 30474506]

        self.assertEqual(ip_list[0], bic.big2ip(ip_list[1]))

    def test_decode_4(self):
        '''Test case.'''

        ip_list = ['10.1.209.21', 366018826]

        self.assertEqual(ip_list[0], bic.big2ip(ip_list[1]))

    def test_decode_5(self):
        '''Test case.'''

        ip_list = ['192.168.150.6', 110536896]

        self.assertEqual(ip_list[0], bic.big2ip(ip_list[1]))

    def test_encode_1(self):
        '''Test case.'''

        ip_list = [382796042, '10.1.209.22']

        self.assertEqual(ip_list[0], bic.ip2big(ip_list[1]))

    def test_encode_2(self):
        '''Test case.'''

        ip_list = [47251722, '10.1.209.2']

        self.assertEqual(ip_list[0], bic.ip2big(ip_list[1]))

    def test_encode_3(self):
        '''Test case.'''

        ip_list = [30474506, '10.1.209.1']

        self.assertEqual(ip_list[0], bic.ip2big(ip_list[1]))

    def test_encode_4(self):
        '''Test case.'''

        ip_list = [366018826, '10.1.209.21']

        self.assertEqual(ip_list[0], bic.ip2big(ip_list[1]))

    def test_encode_5(self):
        '''Test case.'''

        ip_list = [110536896, '192.168.150.6']

        self.assertEqual(ip_list[0], bic.ip2big(ip_list[1]))

    def test_jar(self):
        '''Test case.'''

        bigip = 'BIGipServeroracle_rlx1v002_http8090'
        jar = requests.cookies.RequestsCookieJar()
        jar.set(bigip, '167880896.39455.000')

        #self.assertEqual('192.168.1.10', stn.return_ip_from_cookie(jar))


def main():
    '''Run the test.
    '''
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBIC)

    unittest.TextTestRunner(verbosity=1).run(suite)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
