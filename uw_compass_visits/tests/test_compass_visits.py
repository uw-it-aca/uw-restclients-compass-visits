# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase, mock
from uw_compass_visits import CompassVisits
from uw_compass_visits.models import Visit
from restclients_core.exceptions import DataFailureException
import datetime
import json


class CompassVisitsTestCase(TestCase):

    def test_get_visits_for_student(self):
        visits = CompassVisits().get_visits_for_student("javerage")
        self.assertIsNotNone(visits)
        self.assertIsInstance(visits, list)
        self.assertGreater(len(visits), 0)

    def test_get_visits_for_student_empty(self):
        with self.assertRaises(DataFailureException):
            CompassVisits().get_visits_for_student("123456789")

    def test_get_visit_admin_list(self):
        visits = CompassVisits().get_visit_admin_list()
        self.assertIsNotNone(visits)
        self.assertIsInstance(visits, list)
        self.assertEqual(len(visits), 2)
        self.assertEqual(visits[0].id, 1)
        self.assertTrue(visits[0].is_verified is False)
        self.assertEqual(visits[1].id, 2)
        self.assertTrue(visits[1].is_verified is True)

    def test_visitadmin_failure(self):
        with (mock.patch('uw_compass_visits.dao.COMPASS_VISITS_DAO.getURL')
              as mock_getURL):
            mock_getURL.return_value.status = 500
            with self.assertRaises(DataFailureException):
                CompassVisits().get_visit_admin_list()

    def test_get_visit_options(self):
        options = CompassVisits().get_visit_options()
        self.assertIsNotNone(options)
        self.assertIsInstance(options, dict)
        self.assertIn("program_areas", options)
        self.assertIn("tutoring_options", options)
        self.assertIn("writing_services", options)
        self.assertIsInstance(options["program_areas"], list)
        self.assertIsInstance(options["tutoring_options"], list)
        self.assertIsInstance(options["writing_services"], list)
        self.assertEqual(len(options["program_areas"]), 4)
        self.assertEqual(len(options["tutoring_options"]), 3)
        self.assertEqual(len(options["writing_services"]), 2)

        for area in options["program_areas"]:
            self.assertIn("id", area)
            self.assertIn("name", area)
        for option in options["tutoring_options"]:
            self.assertIn("id", option)
            self.assertIn("name", option)
        for service in options["writing_services"]:
            self.assertIn("id", service)
            self.assertIn("name", service)

        self.assertEqual(options["program_areas"][0]["id"], 1)
        self.assertEqual(options["program_areas"][0]["name"],
                         "Program Area 1")
        self.assertEqual(options["tutoring_options"][0]["id"], 1)
        self.assertEqual(options["tutoring_options"][0]["name"],
                         "Tutoring Option 1")
        self.assertEqual(options["writing_services"][0]["id"], 1)
        self.assertEqual(options["writing_services"][0]["name"],
                         "Writing Service 1")

    def test_get_visit_options_failure(self):
        with (mock.patch('uw_compass_visits.dao.COMPASS_VISITS_DAO.getURL')
              as mock_getURL):
            mock_getURL.return_value.status = 500
            with self.assertRaises(DataFailureException):
                CompassVisits().get_visit_options()

    def test_admin_create_visit_failure(self):
        visit = Visit(
            id=None,
            student_netid="javerage",
            program_area="Program Area 1",
            tutoring_option="Tutoring Option 1",
            writing_service="Writing Service 1",
            course="Course 101",
            check_in_date=datetime.datetime(2024, 1, 1, 10, 0, 0),
            check_out_date=None,
            is_verified=False
        )
        with (mock.patch('uw_compass_visits.dao.COMPASS_VISITS_DAO.postURL')
              as mock_postURL):
            mock_postURL.return_value.status = 500
            with self.assertRaises(DataFailureException):
                CompassVisits().admin_create_visit(visit)

    def test_admin_create_visit_success(self):
        visit = Visit(
            id=None,
            student_netid="javerage",
            program_area="Program Area 1",
            tutoring_option="Tutoring Option 1",
            writing_service="Writing Service 1",
            course="Course 101",
            check_in_date=datetime.datetime(2024, 1, 1, 10, 0, 0),
            check_out_date=None,
            is_verified=False
        )
        with (mock.patch('uw_compass_visits.dao.COMPASS_VISITS_DAO.postURL')
              as mock_postURL):
            mock_postURL.return_value.status = 200
            mock_postURL.return_value.data = json.dumps(visit.json_data())
            CompassVisits().admin_create_visit(visit)
            mock_postURL.assert_called_once_with(
                "/api/v1/managevisit/",
                data=json.dumps(visit.json_data())
            )

    def test_admin_update_visit_success(self):
        visit = Visit(
            id=1,
            student_netid="javerage",
            program_area="Program Area 1",
            tutoring_option="Tutoring Option 1",
            writing_service="Writing Service 1",
            course="Course 101",
            check_in_date=datetime.datetime(2024, 1, 1, 10, 0, 0),
            check_out_date=None,
            is_verified=False
        )
        with (mock.patch('uw_compass_visits.dao.COMPASS_VISITS_DAO.patchURL')
              as mock_patchURL):
            mock_patchURL.return_value.status = 200
            mock_patchURL.return_value.data = json.dumps(visit.json_data())
            CompassVisits().admin_update_visit(visit.id,
                                               verify=True,
                                               checkout=True)
            mock_patchURL.assert_called_once_with(
                "/api/v1/managevisit/1",
                data=json.dumps({'verify': True,
                                 'checkout': True})
            )

    def test_admin_update_visit_failure(self):
        visit = Visit(
            id=1,
            student_netid="javerage",
            program_area="Program Area 1",
            tutoring_option="Tutoring Option 1",
            writing_service="Writing Service 1",
            course="Course 101",
            check_in_date=datetime.datetime(2024, 1, 1, 10, 0, 0),
            check_out_date=None,
            is_verified=False
        )
        with (mock.patch('uw_compass_visits.dao.COMPASS_VISITS_DAO.patchURL')
              as mock_patchURL):
            mock_patchURL.return_value.status = 500
            with self.assertRaises(DataFailureException):
                CompassVisits().admin_update_visit(visit.id,
                                                   verify=True,
                                                   checkout=True)

    def test_admin_delete_visit_success(self):
        with (mock.patch('uw_compass_visits.dao.COMPASS_VISITS_DAO.deleteURL')
              as mock_deleteURL):
            mock_deleteURL.return_value.status = 200
            CompassVisits().admin_delete_visit(1)
            mock_deleteURL.assert_called_once_with("/api/v1/managevisit/1")

    def test_admin_delete_visit_failure(self):
        with (mock.patch('uw_compass_visits.dao.COMPASS_VISITS_DAO.deleteURL')
              as mock_deleteURL):
            mock_deleteURL.return_value.status = 500
            with self.assertRaises(DataFailureException):
                CompassVisits().admin_delete_visit(1)
