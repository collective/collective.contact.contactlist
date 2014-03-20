from zope.component import adapts
from zope.i18n import translate

from plone.app.layout.viewlets.common import ViewletBase

from collective.excelexport.datasources.base import BaseContentsDataSource
from collective.contact.contactlist.interfaces import IContactList,\
    ICollectiveContactContactlistLayer
from collective.contact.contactlist import _


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
        portal_url = self.site_url
        return """<a title="%(title)s" href="%(url)s">
                     <img src="%(portal_url)s/xls.png" />
                     %(title)s
                  </a>""" % {'url': url,
                             'title': title,
                             'portal_url': portal_url}