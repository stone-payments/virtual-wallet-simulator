"""
BaseController

this module contains the BaseController class. This class
is a base wrapper of Flask Blueprint, making it easier to
modularize endpoints and avoiding repeating configurations
"""

from flask import Blueprint


class BaseController(Blueprint):

    def __init__(self, name=__name__, **kwargs):
        """
        Simple Blueprint with some configurations
        """

        super().__init__(name, name, **kwargs)

        self.register_error_handler(404, self.handle_404)

    def handle_404(self, _):
        return dict(message='Requested page not found'), 404
