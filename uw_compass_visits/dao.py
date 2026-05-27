# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core.dao import DAO
from os.path import abspath, dirname
import os


class COMPASS_VISITS_DAO(DAO):
    def service_name(self):
        return 'compass_visits'

    def service_mock_paths(self):
        path = [abspath(os.path.join(dirname(__file__), "resources"))]
        return path

    def _custom_headers(self):
        custom_headers = {}
        token = self.get_service_setting('AUTH_TOKEN')
        if token:
            custom_headers['Authorization'] = "Token {}".format(token)
        return custom_headers
