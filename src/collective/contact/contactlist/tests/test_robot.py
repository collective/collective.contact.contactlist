# -*- coding: utf-8 -*-
"""Robot suites of tests/robot, run with the layer of their file name.

ROBOT_PLONE_MAJOR (4 or 6) selects the UI keywords: robotsuite passes the
ROBOT_* environment variables to the suites as robot variables.
"""
from ..testing import ACCEPTANCE
from ..testing import ADDONS_ACCEPTANCE
from ..testing import PLONE_MAJOR
from plone.testing import layered

import os
import robotsuite
import unittest

# suites that need collective.contact.facetednav and collective.excelexport
SUITE_LAYERS = {
    'test_excelexport.robot': ADDONS_ACCEPTANCE,
    'test_facetednav.robot': ADDONS_ACCEPTANCE,
}

# scenarios pinning a bug of the Plone 4 code, fixed by the Plone 6 migration (see MIGRATION.md):
# reported without failing the run on Plone 4 (Robot Framework 3); robotsuite ignores criticality
# on Robot Framework 4+, so they must pass on Plone 6
OPTIONS = {'noncritical': ['plone4-bug']} if PLONE_MAJOR < 5 else {}


def test_suite():
    os.environ.setdefault('ROBOT_PLONE_MAJOR', str(PLONE_MAJOR))
    suite = unittest.TestSuite()
    robot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'robot')
    for name in sorted(os.listdir(robot_dir)):
        if name.startswith('test_') and name.endswith('.robot'):
            tests = robotsuite.RobotTestSuite(os.path.join('robot', name), **OPTIONS)
            if PLONE_MAJOR < 5:
                # behaviour of the Plone 6 code only (robotsuite has no tag filter)
                tests = unittest.TestSuite([test for test in tests if 'plone6-only' not in test._tags])
            suite.addTests([layered(tests, layer=SUITE_LAYERS.get(name, ACCEPTANCE))])
    return suite
