# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0\

from restclients_core import models


class Visit(models.Model):
    id = models.IntegerField()
    student_netid = models.CharField(max_length=255)
    program_area = models.CharField(max_length=255)
    tutoring_option = models.CharField(max_length=255)
    writing_service = models.CharField(max_length=255, null=True, blank=True)
    course = models.CharField(max_length=255, null=True, blank=True)
    check_in_date = models.DateTimeField(auto_now_add=True)
    check_out_date = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def json_data(self):
        return {
            "id": self.id,
            "student_netid": self.student_netid,
            "program_area": self.program_area.name,
            "tutoring_option": self.tutoring_option.name,
            "writing_service": self.writing_service.name if
            self.writing_service else None,
            "course": self.course,
            "check_in_date": self.check_in_date.isoformat(),
            "check_out_date": self.check_out_date.isoformat() if
            self.check_out_date else None,
            "is_verified": self.is_verified,
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            id=data.get("id"),
            student_netid=data.get("student_netid"),
            program_area=data.get("program_area"),
            tutoring_option=data.get("tutoring_option"),
            writing_service=data.get("writing_service"),
            course=data.get("course"),
            check_in_date=data.get("check_in_date"),
            check_out_date=data.get("check_out_date"),
            is_verified=data.get("is_verified", False),
        )
