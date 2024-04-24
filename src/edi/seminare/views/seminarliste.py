# -*- coding: utf-8 -*-
from datetime import datetime
from edi.seminare import _
from Products.Five.browser import BrowserView
from plone import api
from datetime import datetime

def format_plaetze(places):
    """Helper Function to format free places for seminar"""
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
    """Helper Function to make datetime-objects human readable in seminarevent context"""
    formatted_events = []
    for termin in seminartermine:
        event = {}
        event['ort'] = termin['location']
        start = datetime.strptime(termin['start'], '%Y-%m-%dT%H:%M')
        event['start'] = start
        end = datetime.strptime(termin['end'], '%Y-%m-%dT%H:%M')
        event['end'] = end
        if start.day == end.day:
            formatted_day = start.strftime('%d.%m.%Y')
            formatted_time = start.strftime('%H:%M-') + end.strftime('%H:%M')
        else:
            formatted_day = start.strftime('%d.%m.-') + end.strftime('%d.%m.%Y')
            formatted_time = start.strftime('%H:%M-') + start.strftime('%H:%M')
        event['zeit'] = {'day':formatted_day, 'time':formatted_time}
        event['places'] = format_plaetze(termin['places'])
        formatted_events.append(event)
    formatted_events.sort(key=lambda x: x["start"])
    now = datetime.now()
    formatted_events = [termin for termin in formatted_events if termin['end'] > now]
    return formatted_events

def get_monthname(monthnumber):
    monthnames = {1:'Januar',
                   2:'Februar',
                   3:'März',
                   4:'April',
                   5:'Mai',
                   6:'Juni',
                   7:'Juli',
                   8:'August',
                   9:'September',
                   10:'Oktober',
                   11:'November',
                   12:'Dezember'}
    return monthnames.get(monthnumber)

class Seminarliste(BrowserView):

    def __call__(self):
        seminare = [x for x in self.context.getFolderContents() if x.portal_type == 'Seminarangebot']
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
