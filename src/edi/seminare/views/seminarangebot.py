from edi.seminare.views.seminarliste import format_seminartermine
from plone import api
from Products.Five.browser import BrowserView


class Seminarangebot(BrowserView):
    def __call__(self):
        self.uid = self.context.UID()
        self.list_of_dates = format_seminartermine(self.context)

        self.verweis = None
        verweis = api.relation.get(source=self.context, relationship="verweis")
        if verweis:
            self.verweis = verweis[0].to_object
        return self.index()
