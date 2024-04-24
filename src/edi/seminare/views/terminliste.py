# -*- coding: utf-8 -*-

from edi.seminare import _
from Products.Five.browser import BrowserView
from edi.seminare.views.seminarliste import format_seminartermine, get_monthname
from plone import api
from datetime import datetime
from itertools import groupby

class Terminliste(BrowserView):

    def query_seminare(self, obj=None):
        context = self.context
        if obj:
            context=obj
        seminare = api.content.find(context=context, portal_type="Seminarangebot")
        formatted_termine = []
        for seminar in seminare:
            seminarobj = seminar.getObject()
            terminliste = format_seminartermine(seminarobj.seminartermine)
            for termin in terminliste:
                termin['title'] = seminarobj.title
                termin['url'] = seminarobj.absolute_url()
                formatted_termine.append(termin)
        formatted_termine.sort(key=lambda x: x["start"])
        return formatted_termine

    def __call__(self):
        """
        Es wird eine Liste "self.seminartermine" zurückgegeben
        Jedes Element der Terminliste hat folgende Schlüssel oder Attribute:
        
        start - Startdatum (nur für Sortierung)
        end - Enddatum (nur für Sortierung)
        zeit - formatierte Darstellung Datum, Uhrzeit
        ort - Veranstaltungsort
        title - Titel des Seminars (Thema)
        url - Link in die Einzelansicht des Seminars
        places - Anzeige der freien Plätze

        self.seminartermine = [
          'start':'Startdatum (nur für Sortierung)'
          'end':'Enddatum (nur für Sortierung)',
          'zeit':'formatierte Darstellung Datum, Uhrzeit',
          'title':'Titel des Seminars (Thema)',
          'url':'Link in die Einzelansicht des Seminars',
          'places':'Anzeige der freien Plätze'
        ]
        """
        formatted_termine = self.query_seminare()       
        grouped_events = {}
        for key, group in groupby(formatted_termine, key=lambda x: (x["start"].year, x["start"].month)):
            grouped_events[key] = list(group)
        self.seminartermine = grouped_events
        return self.index()

    def get_month(self, number):
        return get_monthname(number)