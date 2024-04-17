# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE
    PloneSandboxLayer,
)
from plone.testing import z2

import edi.seminare


class EdiSeminareLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=edi.seminare)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'edi.seminare:default')


EDI_SEMINARE_FIXTURE = EdiSeminareLayer()


EDI_SEMINARE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EDI_SEMINARE_FIXTURE,),
    name='EdiSeminareLayer:IntegrationTesting',
)


EDI_SEMINARE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EDI_SEMINARE_FIXTURE,),
    name='EdiSeminareLayer:FunctionalTesting',
)


EDI_SEMINARE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EDI_SEMINARE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='EdiSeminareLayer:AcceptanceTesting',
)
