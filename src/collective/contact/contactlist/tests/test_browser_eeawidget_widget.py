# -*- coding: utf-8 -*-
from collective.contact.contactlist.api import create_list
from collective.contact.contactlist.browser.eeawidget.widget import Widget
from collective.contact.contactlist.testing import IntegrationTestCase
from eea.facetednavigation.widgets.storage import Criterion
from plone import api
from plone.app.testing import login
from plone.uuid.interfaces import IUUID


class FakeData(object):
    """Faceted criterion"""
    hidden = False

    def __init__(self, data):
        self.data = data

    def getId(self):
        return 'contact_lists'

    def get(self, val, default=None):
        return self.data.get(val, default)


class FakeRequest(object):
    debug = False


class TestWidget(IntegrationTestCase):

    def setUp(self):
        super(TestWidget, self).setUp()
        login(self.portal, 'testuser')
        self.army = self.portal.mydirectory.armeedeterre
        self.list_1 = create_list("Corpses", "Description of my list", [self.army.corpsa, self.army.corpsb])
        self.list_2 = create_list("Corpses", "Description of my list", [self.army, self.army.corpsb])

    def test_updateWidgets(self):
        # edit form of the criterion: a vocabulary of lists, the UID index
        widget = Widget(self.portal, self.layer['request'], data=Criterion(widget='contactlist', _cid_=u'lists'))
        widget.update()
        group = [g for g in widget.groups if g.label == u'default'][0]
        self.assertEqual(group.fields['vocabulary'].field.vocabularyName,
                         u'collective.contact.contactlist.vocabularies')
        self.assertTrue(group.fields['index'].field.readonly)

    def test_update(self):
        widget = Widget(self.portal, self.layer['request'], data=Criterion(widget='contactlist', _cid_=u'lists'))
        widget.update()
        group = [g for g in widget.groups if g.label == u'default'][0]
        self.assertEqual(group.widgets['vocabulary'].value, ['collective.contact.contactlist.lists'])
        self.assertEqual(group.widgets['index'].value, ['UID'])

    def test_query(self):
        army = self.army
        widget = Widget(self.portal, FakeRequest(), data=FakeData({'index': 'UID'}))
        query = widget.query(form={'contact_lists': [IUUID(self.list_1)]})
        self.assertEqual(sorted(query['UID']), sorted([IUUID(army.corpsa), IUUID(army.corpsb)]))

        # empty cases
        self.assertEqual(widget.query(form={'contact_lists': []}), {})
        self.assertEqual(widget.query(form={'contact_lists': None}), {})
        self.assertEqual(widget.query(form={}), {})

        # or operator
        query = widget.query(form={'contact_lists': [IUUID(self.list_1), IUUID(self.list_2)]})
        self.assertEqual(sorted(query['UID']),
                         sorted([IUUID(army), IUUID(army.corpsa), IUUID(army.corpsb)]))

        # and operator
        widget = Widget(self.portal, FakeRequest(), data=FakeData({'index': 'UID', 'operator': 'and'}))
        query = widget.query(form={'contact_lists': [IUUID(self.list_1), IUUID(self.list_2)]})
        self.assertEqual(sorted(query['UID']), [IUUID(army.corpsb)])
        query = widget.query(form={'contact_lists': [IUUID(self.list_1)]})
        self.assertEqual(sorted(query['UID']), sorted([IUUID(army.corpsa), IUUID(army.corpsb)]))

    def test_count(self):
        widget = Widget(self.portal, FakeRequest(),
                        data=FakeData({'index': 'UID', 'vocabulary': 'collective.contact.contactlist.lists'}))
        count = widget.count(api.content.find(portal_type='organization'))
        self.assertEqual(count, {IUUID(self.list_1): 2, IUUID(self.list_2): 2, '': 7, 'all': 7})
