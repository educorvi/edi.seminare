from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from Products.CMFCore.utils import getToolByName


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'edi.seminare:uninstall',
        ]

def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.

    typesTool = getToolByName(context, 'portal_types')

    typefolder = typesTool['Folder']
    viewlist = typefolder.getProperty('view_methods', d=None)
    if 'seminarliste' not in viewlist:
        viewlist = viewlist + ('seminarliste',)
    if 'terminliste' not in viewlist:
        viewlist = viewlist + ('terminliste',)
    if 'seminarkarten' not in viewlist:
        viewlist = viewlist + ('seminarkarten',)
    typefolder.manage_changeProperties(view_methods = viewlist)

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.