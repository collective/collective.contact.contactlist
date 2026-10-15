"""Installer for the collective.contact.contactlist package."""

from setuptools import setup

long_description = (
    open("README.rst").read() + "\n" + "Contributors\n"
    "============\n"
    + "\n"
    + open("CONTRIBUTORS.rst").read()
    + "\n"
    + open("CHANGES.rst").read()
    + "\n"
)


setup(
    name="collective.contact.contactlist",
    version="3.0.0.dev0",
    description="Manage lists of contacts",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    keywords="crm",
    author="Thomas Desvenain",
    author_email="thomas.desvenain@gmail.com",
    url="http://pypi.python.org/pypi/collective.contact.contactlist",
    license="GPL",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "collective.contact.core",
        "collective.contact.widget",
        "plone.api",
        "plone.app.contenttypes",
        "plone.app.layout",
        "plone.base",
        "plone.dexterity",
        "plone.formwidget.masterselect",
        "plone.protect",
        "plone.supermodel",
        "plone.uuid",
        "plone.z3cform",
        "Products.GenericSetup",
        "Products.statusmessages",
        "z3c.form",
        "z3c.relationfield",
        "zc.relation",
        "Zope",
        "zope.intid",
    ],
    extras_require={
        "test": [
            "collective.contact.facetednav",
            "collective.excelexport",
            "ecreall.helpers.testing",
            "eea.facetednavigation",
            "plone.app.robotframework",
            "plone.app.testing",
            "plone.browserlayer",
            "plone.testing",
            "Products.CMFPlone",
            "robotsuite",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
