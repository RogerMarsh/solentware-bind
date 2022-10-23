# __init__.py
# Copyright 2022 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Define bind and try methods for tkinter callbacks.

The gridbindings module provides standard bindings used by applications
available on www.solentware.co.uk.  The gridbindings.GridBindings class
expects to be a superclass alongside the solentware_grid.datagrid.DataGrid
class, but the setup module for solentware_misc does not declare the
dependency.
It is assumed the solentware_grid package will be present if gridbindings is
used.

The exceptionhandler module provides a widget for displaying an exception
report for an exception which is causing the application to stop.
"""
