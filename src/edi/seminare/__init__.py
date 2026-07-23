"""Init and utils."""

from zope.i18nmessageid import MessageFactory

import logging


__version__ = "1.4.dev0"

PACKAGE_NAME = "edi.seminare"

_ = MessageFactory(PACKAGE_NAME)

logger = logging.getLogger(PACKAGE_NAME)
