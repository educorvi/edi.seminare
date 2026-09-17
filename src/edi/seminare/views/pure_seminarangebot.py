from edi.seminare.views.seminarangebot import Seminarangebot

from plone import api


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PureSeminarangebot(Seminarangebot):
    """Ansicht für die Startseite"""

    def __call__(self):
        return super().__call__()
