from zope.component import adapts

from collective.excelexport.datasources.base import BaseContentsDataSource
from collective.contact.contactlist.interfaces import IContactList,\
    ICollectiveContactContactlistLayer


class ContactListDataSource(BaseContentsDataSource):
    adapts(IContactList, ICollectiveContactContactlistLayer)

    def get_filename(self):
        return "%s.xls" % (self.context.getId())

    def get_objects(self):
        return [r.to_object for r in self.context.contacts if r.to_object]
