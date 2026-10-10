# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory

import logging

log = logging.getLogger("collective.contact.contactlist")

_ = MessageFactory("collective.contact.contactlist")


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
