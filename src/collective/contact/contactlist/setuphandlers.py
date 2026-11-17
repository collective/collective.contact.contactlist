from plone import api
from plone.app.contenttypes.setuphandlers import configure_members_folder


def post_install(context):
    """Lists are stored in member folders: Plone 6 only creates the Members folder with the example content"""
    configure_members_folder(api.portal.get(), api.portal.get_default_language())
