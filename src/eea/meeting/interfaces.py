# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from eea.meeting import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid
from plone.app.textfield import RichText

from plone.schema import Email
from plone.autoform import directives
from z3c.form.browser.text import TextFieldWidget

from zope.interface import Invalid
import re


meeting_types = SimpleVocabulary(
    [SimpleTerm(value=u'meeting', title=_(u'Meeting')),
     SimpleTerm(value=u'conference', title=_(u'Conference')),
     SimpleTerm(value=u'workshop', title=_(u'Workshop'))]
    )


def validate_email(email):
    try:
        checkEmailAddress(email)
    except EmailAddressInvalid:
        raise EmailAddressInvalid(email)
    return True

def cc_constraint(value):
    data_lines = value.split('\r\n')

    for idx, email in enumerate(data_lines):
        idx += 1
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise Invalid(_(u"Invalid email address on line %d" % idx))

    return True


class IMeetingLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IMeeting(Interface):
    """ Meeting """
    text = RichText(
        title=_(u"Body text"),
        required=True,
    )

    meeting_type = schema.Choice(
        title=_(u"Meeting type"),
        vocabulary=meeting_types,
        required=True,
    )

    allow_register = schema.Bool(
        title=_(u"Allow users to register to the meeting"),
        required=True,
    )

    restrict_content_access = schema.Bool(
        title=(u"Restrict user access to the contents in the meeting"),
        required=True
    )

    auto_approve = schema.Bool(
        title=_(u"Automatically approve registrations"),
        required=True,
    )

    max_participants = schema.Int(
        title=_(u"Maximum number of participants"),
        required=True,
    )

    contact_name = schema.TextLine(
        title=_(u"Contact person"),
        required=True,
    )

    contact_email = schema.TextLine(
        title=_(u"Contact email"),
        required=True,
        constraint=validate_email
    )

    location =  schema.TextLine(
        title=_(
            u'label_event_location',
            default=u'Location'
        ),
        description=_(
            u'help_event_location',
            default=u'Location of the event.'
        ),
        required=True,
        default=None
    )


class ISubscriber(Interface):
    """ Meeting subscriber """
    userid = schema.TextLine(
        title=_("User id"),
        required=True
    )

    email = schema.TextLine(
        title=_(u"Email"),
        required=True,
        constraint=validate_email
    )


class ISubscribers(Interface):
    """ Meeting subscribers """


class IEmails(Interface):
    """ Meeting emails """


class ISearchUser(Interface):
    """ Search user """
    containing = schema.TextLine(
        title=_(u"Add users to E-mail CC"),
        required=True,
    )

    results = schema.Set(
        required=False,
        value_type=schema.Choice(vocabulary='eea.meeting.vocabularies.LDAPListingVocabulary')
    )


class IEmail(Interface):
    """ Email """
    sender = Email(
        title=_(u"From"),
        required=True,
    )

    receiver = schema.Set(
        title=u'Recipients',
        value_type=schema.Choice(vocabulary='eea.meeting.vocabularies.RecipientsVocabulary')
    )

    cc = schema.Text(
        title=_(u"CC"),
        description=_(u'Add CC addresses one per line, no separator'),
        constraint = cc_constraint,
        required=False,
    )

    subject = schema.TextLine(
        title=_(u"Subject"),
        required=True,
    )

    body = RichText(
        title=_(u"Body"),
        required=True,
        output_mime_type='text/plain',
        allowed_mime_types=('text/html', 'text/structured', 'text/plain'),
    )

    directives.widget(
        'sender',
        TextFieldWidget,
        klass=u'mail_widget'
    )
