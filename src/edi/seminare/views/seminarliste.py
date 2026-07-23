from datetime import datetime
from Products.Five.browser import BrowserView

import regex

from edi.seminare import logger


def format_plaetze(seminarobj, location, day, time, places):  # noqa: C901
    """Helper Function to format free places for seminar"""
    link = ""
    erg = "Fehler"
    try:
        int(places)
    except Exception as e:
        logger.error(f"Error parsing places for seminar {seminarobj.title}: {e}")
        return f"<a href={seminarobj.absolute_url()}>zum Seminarangebot</a>"
    verfuegbarkeit = int(places)
    if verfuegbarkeit == -1:
        erg = "ausgebucht"
        erg_class = "danger"
    elif verfuegbarkeit == 0:
        erg = "Warteliste"
        erg_class = "primary"
    elif verfuegbarkeit == 1000:
        erg = "freie Plätze"
        erg_class = "success"
    else:
        erg = f"noch {verfuegbarkeit} Plätze"
        erg_class = "success"

    if seminarobj.anmeldung == "keine":
        link = '<small class="text-success"><strong>nicht erforderlich</strong></small>'
        if is_url(location):
            erg = "beitreten"
            btnclass = "btn btn-success"
            link = f'<a role="button" style="width:140px" class="{btnclass}" href="{location}">{erg}</a>'
    elif verfuegbarkeit == -1:
        link = '<small class="text-danger"><strong>ausgebucht</strong></small>'
    else:
        title = seminarobj.title
        btnclass = f"btn btn-{erg_class}"
        if seminarobj.anmeldung == "email":
            email = seminarobj.email
            url = f"mailto:{email}?subject=Anmeldung: {title} {day}"
            if time:
                url = f"mailto:{email}?subject=Anmeldung: {title} {day} {time}"
            link = f'<a role="button" style="width:140px" class="{btnclass}" href="{url}">{erg}</a>'
        elif seminarobj.anmeldung == "link":
            try:
                url = seminarobj.formular.to_object.absolute_url()
            except Exception as e:
                logger.error(f"Error getting formular URL for seminar {seminarobj.title}: {e}")
                url = ""
            link = f'<a role="button" style="width:140px" class="{btnclass}" href="{url}">{erg}</a>'
        elif seminarobj.anmeldung == "extlink":
            url = seminarobj.extlink
            link = f'<a target="_blank" role="button" style="width:140px" class="{btnclass}" href="{url}">{erg}</a>'
        elif seminarobj.anmeldung == "telefon":
            link = (
                f'<button type="button" style="width:140px" class="{btnclass}" data-toggle="modal" '
                f'data-target="#edi_{seminarobj.UID()}">{erg}</button>'
            )
    return link


def is_url(location):
    """Helper Function to check if it is a Videocall URL"""
    # This regular expression roughly checks for (http/s):// and a domain name with optional path/query.
    url_pattern = regex.compile(r"\bhttps?://[^\s]+?\?.+\b")
    return regex.match(url_pattern, location) is not None


def format_seminartermine(seminarobj):
    """Helper Function to make datetime-objects human readable in seminarevent context"""
    seminartermine = seminarobj.seminartermine
    formatted_events = []
    for termin in seminartermine:
        event = {}
        location = termin["location"]
        if is_url(location):
            location = "Online"
        event["ort"] = location
        try:
            start = datetime.strptime(termin["start"], "%Y-%m-%dT%H:%M")
        except Exception as e:
            logger.error(f"Error parsing start date for seminar {seminarobj.title}: {e}")
            start = termin["start"]
        event["start"] = start
        try:
            end = datetime.strptime(termin["end"], "%Y-%m-%dT%H:%M")
        except Exception as e:
            logger.error(f"Error parsing end date for seminar {seminarobj.title}: {e}")
            end = termin["end"]
        event["end"] = end
        if (start.day, start.month) == (end.day, end.month):
            formatted_day = start.strftime("%d.%m.%Y")
            formatted_time = start.strftime("%H:%M-") + end.strftime("%H:%M")
        else:
            formatted_day = start.strftime("%d.%m.- ") + end.strftime("%d.%m.%Y")
            formatted_time = start.strftime("%H:%M-") + end.strftime("%H:%M")
        if (start.hour, start.minute) == (0, 0) and (start.hour, start.minute) == (
            end.hour,
            end.minute,
        ):
            formatted_time = False
        cal_url = f"{seminarobj.absolute_url()}/@@cal-view?index={seminartermine.index(termin)}"
        event["zeit"] = {
            "day": formatted_day,
            "time": formatted_time,
            "cal_url": cal_url,
        }
        event["places"] = format_plaetze(
            seminarobj,
            termin["location"],
            formatted_day,
            formatted_time,
            termin["places"],
        )
        formatted_events.append(event)
    formatted_events.sort(key=lambda x: x["start"])
    now = datetime.now()
    formatted_events = [termin for termin in formatted_events if termin["end"] > now]
    return formatted_events


def get_monthname(monthnumber):
    monthnames = {
        1: "Januar",
        2: "Februar",
        3: "März",
        4: "April",
        5: "Mai",
        6: "Juni",
        7: "Juli",
        8: "August",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Dezember",
    }
    return monthnames.get(monthnumber)


def format_telefonmodal(seminarobj):
    uid = seminarobj.UID()
    htmlsnippet = (
        f'<div class="modal fade" id="edi_{uid}" tabindex="-1" aria-labelledby="ModalLabel_{uid}" aria-hidden="true">\n'
        f'  <div class="modal-dialog">\n'
        f'    <div class="modal-content">\n'
        f'      <div class="modal-header">\n'
        f'        <h5 class="modal-title" id="ModalLabel_{uid}">Anmeldung für: {seminarobj.title}</h5>\n'
        f'        <button type="button" class="close" data-dismiss="modal" aria-label="Close">\n'
        f'          <span aria-hidden="true">&times;</span>\n'
        f"        </button>\n"
        f"      </div>\n"
        f'      <div class="modal-body">\n'
        f'        <p>Anmeldung via Telefon: <i class="bi bi-telephone"></i> <strong>{seminarobj.telefon}</strong></p>\n'
        f"        <p>Ansprechperson: <strong>{seminarobj.kontakt}</strong></p>\n"
        f'        <p class="small">Bitte halten Sie für die telefonische Anmeldung gegebenenfalls den gewünschten'
        " Veranstaltungsort und die Uhrzeit bereit.</p>\n"
        f"      </div>\n"
        f"    </div>\n"
        f"  </div>\n"
        f"</div>\n"
    )
    return htmlsnippet


class Seminarliste(BrowserView):
    def __call__(self):
        seminare = [x for x in self.context.getFolderContents() if x.portal_type == "Seminarangebot"]
        self.telefonnummern = []
        formatted_seminare = []
        for seminar in seminare:
            seminarevent = {}
            seminarobj = seminar.getObject()
            seminarevent["title"] = seminarobj.title
            seminarevent["url"] = seminarobj.absolute_url()
            seminarevent["list_of_dates"] = format_seminartermine(seminarobj)
            formatted_seminare.append(seminarevent)
            if seminarobj.anmeldung == "telefon":
                self.telefonnummern.append(format_telefonmodal(seminarobj))
        self.seminare = formatted_seminare
        return self.index()
