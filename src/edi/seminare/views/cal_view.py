# -*- coding: utf-8 -*-
from io import StringIO
from ics import Calendar, Event
from datetime import datetime, timedelta
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from edi.seminare.views.seminarliste import is_url
import pytz
import datetime

class ICalView(Interface):
    """ Marker Interface for ICalView"""


@implementer(ICalView)
class CalView(BrowserView):
    def __call__(self):
        index = self.request.get('index')
        try:
            index = int(index)
        except:
            print('Error')
        title = self.context.title
        description = self.context.description
        url = self.context.absolute_url()
        termin = self.context.seminartermine[index]
        start = termin['start']
        end = termin['end']
        location = termin['location']
        if is_url(location):
            description += f"\r\nBeitreten: {location}"
            location = 'Online'
        cal = Calendar()

        # Create an event
        event = Event()
        event.name = title
        berlin_timezone = pytz.timezone('Europe/Berlin')
        start = berlin_timezone.localize(start)
        end = berlin_timezone.localize(end)
        event.begin = start
        event.end = end
        event.description = description
        event.location = location
        event.url = url
        
        # Add event to calendar
        cal.events.add(event)

        calendar_string = cal.serialize()
        s = StringIO()

        s.write(calendar_string)
        s.seek(0)
        
        self.request.response.setHeader('Content-Type', 'text/calendar')
        self.request.response.setHeader('Content-Disposition', 'attachment; filename="seminar.ics"') 
        return s.read()
