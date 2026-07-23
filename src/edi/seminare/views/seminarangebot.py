from edi.seminare.views.seminarliste import format_seminartermine
from Products.Five.browser import BrowserView


class Seminarangebot(BrowserView):
    def __call__(self):
        self.uid = self.context.UID()
        self.list_of_dates = format_seminartermine(self.context)
        return self.index()
