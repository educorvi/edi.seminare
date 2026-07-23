# -*- coding: utf-8 -*-
from edi.seminare import _
from edi.seminare.views.seminarangebot import Seminarangebot
from Products.Five.browser import BrowserView


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PureSeminarangebot(Seminarangebot):
    """Ansicht für die Startseite"""
