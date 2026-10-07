from ..testing import ACCEPTANCE
from ..testing import ADDONS_ACCEPTANCE
from plone.testing import layered

import os
import robotsuite
import unittest

# suites that need collective.contact.facetednav and collective.excelexport
ADDONS_SUITES = ('test_facetednav.robot', 'test_excelexport.robot')


def test_suite():
    suite = unittest.TestSuite()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    robot_dir = os.path.join(current_dir, 'robot')
    robot_tests = [
        doc for doc in os.listdir(robot_dir)
        if doc.endswith('.robot') and doc.startswith('test_')
    ]
    for test in robot_tests:
        suite.addTests([
            layered(
                robotsuite.RobotTestSuite(os.path.join('robot', test)),
                layer=ADDONS_ACCEPTANCE if test in ADDONS_SUITES else ACCEPTANCE
            ),
        ])
    return suite
