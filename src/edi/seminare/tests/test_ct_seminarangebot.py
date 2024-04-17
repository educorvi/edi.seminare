# -*- coding: utf-8 -*-
from edi.seminare.content.seminarangebot import ISeminarangebot  # NOQA E501
from edi.seminare.testing import EDI_SEMINARE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class SeminarangebotIntegrationTest(unittest.TestCase):

    layer = EDI_SEMINARE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_seminarangebot_schema(self):
        fti = queryUtility(IDexterityFTI, name='Seminarangebot')
        schema = fti.lookupSchema()
        self.assertEqual(ISeminarangebot, schema)

    def test_ct_seminarangebot_fti(self):
        fti = queryUtility(IDexterityFTI, name='Seminarangebot')
        self.assertTrue(fti)

    def test_ct_seminarangebot_factory(self):
        fti = queryUtility(IDexterityFTI, name='Seminarangebot')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ISeminarangebot.providedBy(obj),
            u'ISeminarangebot not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_seminarangebot_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Seminarangebot',
            id='seminarangebot',
        )

        self.assertTrue(
            ISeminarangebot.providedBy(obj),
            u'ISeminarangebot not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('seminarangebot', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('seminarangebot', parent.objectIds())

    def test_ct_seminarangebot_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Seminarangebot')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_seminarangebot_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Seminarangebot')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'seminarangebot_id',
            title='Seminarangebot container',
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
