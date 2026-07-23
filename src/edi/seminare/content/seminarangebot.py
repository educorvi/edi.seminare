# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.row import DictRow
from plone import api as ploneapi
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.schema import Email

# from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.relationfield.schema import RelationChoice

# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


anmeldeoptionen = SimpleVocabulary([
    SimpleTerm(value="keine", title="keine Anmeldung erforderlich"),
    SimpleTerm(value="email", title="Anmeldung per E-Mail"),
    SimpleTerm(value="telefon", title="Anmeldung per Telefon"),
    SimpleTerm(value="link", title="Anmeldung per Formular"),
    SimpleTerm(value="extlink", title="Anmeldung per externem Link"),
])


class ISeminartermin(model.Schema):
    start = schema.Datetime(title="Beginn der Veranstaltung", required=True)
    end = schema.Datetime(title="Ende der Veranstaltung", required=True)
    location = schema.TextLine(title="Ort der Veranstaltung", required=True)
    places = schema.TextLine(
        title="Verfügbare Plätze",
        description="-1 = ausgebucht, 0 = Warteliste, 1000 = freie Plätze, 1-999 = Anzahl der freien Plätze",
        default="1000",
        required=True,
    )


class ISeminarangebot(model.Schema):
    """Marker interface and Dexterity Python Schema for Seminarangebot"""

    text = RichText(
        title="Haupttext zum Seminarangebot",
        description="Der Text wird oberhalb der Seminardaten angezeigt.",
        required=False,
    )

    kontakt = schema.TextLine(title="Name Ansprechperson", required=True)

    email = Email(title="E-Mail Adresse Ansprechperson", required=True)

    telefon = schema.TextLine(title="Telefonnummer Ansprechperson", required=False)

    verweis = RelationChoice(
        title="Verweis zu einem Artikel im Intranet",
        vocabulary="plone.app.vocabularies.Catalog",
        required=False,
    )

    # directives.widget("verweis",
    #    RelatedItemsFieldWidget,
    #    pattern_options={
    #        "selectableTypes": ["Document", "Event"],
    #    })

    link = schema.URI(title="Link zu einem Artikel im Internet", required=False)

    anmeldung = schema.Choice(
        title="Anmeldeoption auswählen",
        vocabulary=anmeldeoptionen,
        default="keine",
        required=True,
    )

    formular = RelationChoice(
        title="Verweis zu einem Anmeldeformular im Intranet",
        vocabulary="plone.app.vocabularies.Catalog",
        required=False,
    )

    directives.widget(
        "formular",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["EasyForm"],
        },
    )

    extlink = schema.URI(
        title="Verweis auf ein externes Anmeldeformular im Internet", required=False
    )

    seminartermine = schema.List(
        title="Liste der Seminartermine",
        value_type=DictRow(
            title="Seminartermine",
            schema=ISeminartermin,
        ),
        required=False,
    )

    directives.widget("seminartermine", DataGridFieldFactory)

    endtext = RichText(
        title="Schlusstext zum Seminarangebot",
        description="Der Text wird unterhalb der Seminardaten angezeigt.",
        required=False,
    )

    @invariant
    def anmeldung_check(data):
        if data.anmeldung == "telefon":
            if not data.telefon:
                raise Invalid(
                    "Für eine Anmeldung per Telefon muss eine Telefonnummer angegeben werden."
                )
        elif data.anmeldung == "link":
            if not data.formular:
                raise Invalid(
                    "Für eine Anmeldung per Online-Formular muss ein Verweis auf ein Formular gesetzt werden."
                )
        elif data.anmeldung == "extlink":
            if not data.extlink:
                raise Invalid(
                    "Für eine Anmeldung per externem Link muss ein externer Link eingetragen werden."
                )


@implementer(ISeminarangebot)
class Seminarangebot(Container):
    """Content-type class for ISeminarangebot"""

    def get_cluster_content(self, request=None):
        if not request:
            request = getRequest()
        view = ploneapi.content.get_view(
            name="pure-seminarangebot", context=self, request=request
        )
        return view.__call__()
