# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This is the interface for interactign with the compass visits web service.
"""

import json
from restclients_core.exceptions import DataFailureException
from uw_compass_visits.dao import COMPASS_VISITS_DAO
from uw_compass_visits.models import Visit


class CompassVisits(object):
    """
    This class provides an interface to the compass visits web service.
    """

    API = '/api/v1'

    def __init__(self):
        self.dao = COMPASS_VISITS_DAO()

    def get_visits_for_student(self, uwnetid):
        """
        Returns a list of visits for the given uw netid.
        """
        url = "{}/studentvisits/{}".format(self.API, uwnetid)
        response = self.dao.getURL(url)
        if response.status != 200:
            raise DataFailureException(url,
                                       response.status,
                                       "Error getting visits for student "
                                       "{}: {}".format(uwnetid,
                                                       response.status))
        visits = [Visit.from_json(v) for v in json.loads(response.data)]
        return visits

    def get_visit_admin_list(self):
        """
        Returns a list of all visits for admin users.
        """
        url = "{}/visitadminlist".format(self.API)
        response = self.dao.getURL(url)
        if response.status != 200:
            raise DataFailureException(url,
                                       response.status,
                                       "Error getting admin visit list: "
                                       "{}".format(response.status))
        visits = [Visit.from_json(v) for v in json.loads(response.data)]
        return visits

    def get_visit_options(self):
        """
        Returns a list of visit options.
        """
        url = "{}/visitoptions".format(self.API)
        response = self.dao.getURL(url)
        if response.status != 200:
            raise DataFailureException(url,
                                       response.status,
                                       "Error getting visit options: "
                                       "{}".format(response.status))
        options = json.loads(response.data)
        return options

    def admin_create_visit(self, visit):
        """
        Creates a new visit as an admin user.
        """
        url = "{}/managevisit/".format(self.API)
        response = self.dao.postURL(url,
                                    data=json.dumps(visit.json_data())
                                    )
        if response.status != 200:
            raise DataFailureException(url,
                                       response.status,
                                       "Error creating visit: "
                                       "{}".format(response.status))
        return Visit.from_json(json.loads(response.data))

    def admin_update_visit(self, visit_id, verify=None, checkout=None):
        """
        Allows an admin user to update an existing visit.
        """
        url = "{}/managevisit/{}".format(self.API, visit_id)
        request_body = {}
        if verify is not None:
            request_body["verify"] = verify
        if checkout is not None:
            request_body["checkout"] = checkout

        response = self.dao.patchURL(url,
                                     data=json.dumps(request_body)
                                     )
        if response.status != 200:
            raise DataFailureException(url,
                                       response.status,
                                       "Error updating visit {}: "
                                       "{}".format(visit_id, response.status))
        return Visit.from_json(json.loads(response.data))

    def admin_delete_visit(self, visit_id):
        """
        Allows an admin user to delete an existing visit.
        """
        url = "{}/managevisit/{}".format(self.API, visit_id)
        response = self.dao.deleteURL(url)
        if response.status != 200:
            raise DataFailureException(url,
                                       response.status,
                                       "Error deleting visit {}: "
                                       "{}".format(visit_id,
                                                   response.status))
        return response
