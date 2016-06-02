# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from eea.meeting.testing import EEA_MEETING_INTEGRATION_TESTING  # noqa
from eea.meeting.interfaces import IEEAMeeting

import unittest2 as unittest


class EEAMeetingIntegrationTest(unittest.TestCase):

    layer = EEA_MEETING_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='EEA Meeting')
        schema = fti.lookupSchema()
        self.assertEqual(IEEAMeeting, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='EEA Meeting')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='EEA Meeting')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IEEAMeeting.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('EEA Meeting', 'EEA Meeting')
        self.assertTrue(
            IEEAMeeting.providedBy(self.portal['EEA Meeting'])
        )
