# -*- coding: utf-8 -*-

from edi.seminare import _
from Products.Five.browser import BrowserView
from edi.seminare.views.seminarliste import format_seminartermine

class Seminarangebot(BrowserView):

    def __call__(self):
        self.uid = self.context.UID()
        self.list_of_dates = format_seminartermine(self.context)
        return self.index()
