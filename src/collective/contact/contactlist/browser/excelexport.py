from collective.contact.contactlist import _
from collective.contact.contactlist.interfaces import ICollectiveContactContactlistLayer
from collective.contact.contactlist.interfaces import IContactList
from collective.excelexport.datasources.base import BaseContentsDataSource
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.i18n import translate


class ContactListDataSource(BaseContentsDataSource):
    adapts(IContactList, ICollectiveContactContactlistLayer)

    def get_filename(self):
        return "%s.xls" % (self.context.getId())

    def get_objects(self):
        return [r.to_object for r in self.context.contacts if r.to_object]


class ExportLinkViewlet(ViewletBase):

    def render(self):
        url = "%s/@@collective.excelexport" % self.context.absolute_url()
        title = translate(_(u"Excel export list of contacts"),
                          context=self.request)
        icon_url = getMultiAdapter((self.context, self.request), name='iconresolver').url(
            'mimetype-application/vnd.ms-excel')
        return """<a title="%(title)s" href="%(url)s">
                     <img src="%(icon_url)s" />
                     %(title)s
                  </a>""" % {'url': url,
                             'title': title,
                             'icon_url': icon_url}
