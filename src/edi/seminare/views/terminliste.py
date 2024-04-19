# -*- coding: utf-8 -*-

from edi.seminare import _
from Products.Five.browser import BrowserView
from edi.seminare.views.seminarliste import format_seminartermine
from plone import api

class Terminliste(BrowserView):

    def __call__(self):
        seminare = api.content.find(context=self.context, portal_type="Seminarangebot")
        formatted_termine = []
        for seminar in seminare:
            seminarobj = seminar.getObject()
            terminliste = format_seminartermine(seminarobj.seminartermine)
            for termin in terminliste:
                termin['title'] = seminarobj.title
                termin['url'] = seminarobj.absolute_url()
                formatted_termine.append(termin)
        self.seminartermine = formatted_termine.sort(key=lambda x: x["start"])
        return self.index()