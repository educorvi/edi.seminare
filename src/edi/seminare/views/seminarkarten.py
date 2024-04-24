# -*- coding: utf-8 -*-
from nva.kurzfassung.views.erweiterte_kurzfassung import ErweiterteKurzfassung
from edi.seminare.views.seminarliste import format_seminartermine
from plone import api

MAXLEN = 5

class Seminarkarten(ErweiterteKurzfassung):
    """Content-Liste wird von der erweiterten Kurzfassung geerbt und adaptiert"""

    def showdesc(self):
        return getattr(self.context, 'showdesc', True)

    def cardlist(self):
        rowclass = "row-cols-md-3"
        #Abwärtskompatibilität
        if hasattr(self.context, 'columns'):
            if self.context.columns:
                rowclass = f"row-cols-md-{self.context.columns}"
        #Ende Abwärtskompatibilität
        if hasattr(self.context, 'cardscolumns'):
            if self.context.cardscolumns:
                rowclass = f"row-cols-md-{self.context.cardscolumns}"
        self.rowclass = rowclass
        artikelliste = self.contentlist()
        artikel = self.add_seminare(artikelliste)
        return artikel

    def add_seminare(self, artikelliste):
        new_artikelliste = []
        for artikel in artikelliste:
            artikel['seminare'] = []
            artikel['more_seminare'] = False
            seminartermine = []
            obj = api.content.get(UID=artikel['uid'])
            if obj.portal_type == 'Seminarangebot':
                seminartermine = format_seminartermine(obj.seminartermine)
            elif obj.portal_type == 'Folder':
                terminview = api.content.get_view(name='terminliste', context=obj, request=self.request)
                seminartermine = terminview.query_seminare(obj)
            if len(seminartermine) > MAXLEN:
                seminartermine = seminartermine[:MAXLEN]
                artikel['more_seminare'] = True
            artikel['seminare'] = seminartermine
            new_artikelliste.append(artikel)
        return new_artikelliste
