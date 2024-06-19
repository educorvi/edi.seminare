# -*- coding: utf-8 -*-
from edi.seminare.testing import EDI_SEMINARE_FUNCTIONAL_TESTING
from edi.seminare.testing import EDI_SEMINARE_INTEGRATION_TESTING
from edi.seminare.views.cal_view import ICalView
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = EDI_SEMINARE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Folder', 'other-folder')
        api.content.create(self.portal, 'Document', 'front-page')

    def test_cal_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='cal-view'
        )
        self.assertTrue(ICalView.providedBy(view))

    def test_cal_view_not_matching_interface(self):
        view_found = True
        try:
            view = getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='cal-view'
            )
        except ComponentLookupError:
            view_found = False
        else:
            view_found = ICalView.providedBy(view)
        self.assertFalse(view_found)


class ViewsFunctionalTest(unittest.TestCase):

    layer = EDI_SEMINARE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
