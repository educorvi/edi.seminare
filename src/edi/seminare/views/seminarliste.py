# -*- coding: utf-8 -*-
from datetime import datetime
from edi.seminare import _
from Products.Five.browser import BrowserView
from plone import api

def format_plaetze(places):
    erg = 'Fehler'
    try:
        int(places)
    except:
        return erg
    verfuegbarkeit = int(places)
    if verfuegbarkeit == -1:
        erg = 'ausgebucht'
        erg_class = 'danger'
    elif verfuegbarkeit == 0:
        erg = 'Warteliste'
        erg_class = 'warning'
    elif verfuegbarkeit == 1000:
        erg = 'freie Plätze'
        erg_class = 'success'
    else:
        erg = f'freie Plätze: {verfuegbarkeit}'
        erg_class = 'success'
    return {'number':erg, 'class': erg_class}

def format_seminartermine(seminartermine):
    formatted_events = []
    for termin in seminartermine:
        event = {}
        event['ort'] = termin['location']
        start = datetime.strptime(termin['start'], '%Y-%m-%dT%H:%M')
        end = datetime.strptime(termin['end'], '%Y-%m-%dT%H:%M')
        if start.day == end.day:
            formatted_day = start.strftime('%d.%m.%Y')
            formatted_time = start.strftime('%H:%M-') + end.strftime('%H:%M Uhr')
        else:
            formatted_day = start.strftime('%d.%m.-') + end.strftime('%d.%m.%Y')
            formatted_time = start.strftime('%H:%M-') + start.strftime('%H:%M Uhr')
        event['zeit'] = {'day':formatted_day, 'time':formatted_time}
        event['places'] = format_plaetze(termin['places'])
        formatted_events.append(event)
    return formatted_events


class Seminarliste(BrowserView):

    def __call__(self):
        seminare = api.content.find(context=self.context, portal_type="Seminarangebot")
        formatted_seminare = []
        for seminar in seminare:
            seminarevent = {}
            seminarobj = seminar.getObject()
            seminarevent['title'] = seminarobj.title
            seminarevent['url'] = seminarobj.absolute_url()
            seminarevent['list_of_dates'] = format_seminartermine(seminarobj.seminartermine)
            formatted_seminare.append(seminarevent)
        self.seminare = formatted_seminare
        return self.index()
