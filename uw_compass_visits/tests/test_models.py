# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from uw_compass_visits import models
import datetime


class CompassVisitModelTestCase(TestCase):

    def test_compass_visit_model(self):
        visit = models.Visit(
            id=1,
            student_netid="javerage",
            program_area="Program Area 1",
            tutoring_option="Tutoring Option 1",
            writing_service="Writing Service 1",
            check_in_date=datetime.datetime(2024, 1, 1, 10, 0, 0),
            is_verified=False
        )
        self.assertEqual(visit.id, 1)
        self.assertEqual(visit.student_netid, "javerage")
        self.assertEqual(visit.program_area, "Program Area 1")
        self.assertEqual(visit.tutoring_option, "Tutoring Option 1")
        self.assertEqual(visit.writing_service, "Writing Service 1")
        self.assertEqual(visit.check_in_date,
                         datetime.datetime(2024, 1, 1, 10, 0, 0))
        self.assertIsNone(visit.check_out_date)
        self.assertFalse(visit.is_verified)

        json_data = visit.json_data()
        self.assertEqual(json_data["id"], 1)
        self.assertEqual(json_data["student_netid"], "javerage")
        self.assertEqual(json_data["program_area"], "Program Area 1")
        self.assertEqual(json_data["tutoring_option"], "Tutoring Option 1")
        self.assertEqual(json_data["writing_service"], "Writing Service 1")
        self.assertEqual(json_data["check_in_date"], "2024-01-01T10:00:00")
        self.assertIsNone(json_data["check_out_date"])
        self.assertFalse(json_data["is_verified"])

    def test_compass_visit_from_json(self):
        json_data = {
            "id": 2,
            "student_netid": "javerage",
            "program_area": "Program Area 2",
            "tutoring_option": "Tutoring Option 2",
            "writing_service": None,
            "course": "Course 101",
            "check_in_date": "2024-01-02T11:00:00",
            "check_out_date": None,
            "is_verified": True
        }
        visit = models.Visit.from_json(json_data)
        self.assertEqual(visit.id, 2)
        self.assertEqual(visit.student_netid, "javerage")
        self.assertEqual(visit.program_area, "Program Area 2")
        self.assertEqual(visit.tutoring_option, "Tutoring Option 2")
        self.assertIsNone(visit.writing_service)
        self.assertEqual(visit.course, "Course 101")
        self.assertEqual(visit.check_in_date,
                         datetime.datetime(2024, 1, 2, 11, 0, 0))
        self.assertIsNone(visit.check_out_date)
        self.assertTrue(visit.is_verified)
