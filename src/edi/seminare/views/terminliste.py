# -*- coding: utf-8 -*-

from edi.seminare import _
from Products.Five.browser import BrowserView
from edi.seminare.views.seminarliste import format_seminartermine
from plone import api

class Terminliste(BrowserView):

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