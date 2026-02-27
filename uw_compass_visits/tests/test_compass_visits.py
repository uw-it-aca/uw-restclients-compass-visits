# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from uw_compass_visits import CompassVisits
from restclients_core.exceptions import DataFailureException


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
