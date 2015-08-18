#!/usr/bin/env python
# -*- coding: utf-8 -*-

import doctest
import unittest
import jsonpatch
import random_json
import sys

class RandomTests(unittest.TestCase):

    @classmethod
    def generate_tests(cls, number=100):

        for i in xrange(0, number):
            exec """
def test_rand_json(self):
    # random_json seems to raise an OverflowError once in a while. If that happens, retry.
    # Will look into that eventually...
    while True:
        try:
            src = random_json.obj()
            dst = random_json.obj()
        except OverflowError:
            continue
        else:
            break
    patch = jsonpatch.make_patch(src, dst)
    self.assertEqual(dst, patch.apply(src))

cls.test_rand_json{number} = test_rand_json
""".format(number=i)


def get_suite():
    suite = unittest.TestSuite()
    RandomTests.generate_tests()
    suite.addTest(unittest.makeSuite(RandomTests))
    return suite


suite = get_suite()

runner = unittest.TextTestRunner(verbosity=2)

result = runner.run(suite)

if not result.wasSuccessful():
    sys.exit(1)