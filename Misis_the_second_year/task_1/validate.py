from collections.abc import Iterable
from typing import Protocol

from Misis_the_second_year.task_1.main import Booking


class BookingRule(Protocol):
    def check(
        self, booking: Booking, existing_bookings: tuple[Booking, ...]
    ) -> str | None: ...


class NoOverlapRule:
    def check(
        self, booking: Booking, existing_bookings: tuple[Booking, ...]
    ) -> str | None:
        for existing in existing_bookings:
            if (
                existing.workplace.id == booking.workplace.id
                and booking.starts_at < existing.ends_at
                and existing.starts_at < booking.ends_at
            ):
                return "Место уже забронировано на это время"
        return None


class DepartmentRule:
    def check(
        self, booking: Booking, existing_bookings: tuple[Booking, ...]
    ) -> str | None:
        department = booking.workplace.allowed_department
        if department is not None and booking.employee.department != department:
            return f"Место доступно только отделу «{department}»"
        return None


class PermissionRule:
    def check(
        self, booking: Booking, existing_bookings: tuple[Booking, ...]
    ) -> str | None:
        permission = booking.workplace.required_permission
        if permission is not None and permission not in booking.employee.permissions:
            return f"Требуется разрешение «{permission}»"
        return None


class BookingValidator:
    def __init__(self, extra_rules: Iterable[BookingRule] = ()) -> None:
        self._rules = (
            NoOverlapRule(),
            DepartmentRule(),
            PermissionRule(),
            *extra_rules,
        )

    def validate(
        self, booking: Booking, existing_bookings: Iterable[Booking]
    ) -> tuple[str, ...]:
        bookings = tuple(existing_bookings)
        violations = []
        for rule in self._rules:
            violation = rule.check(booking, bookings)
            if violation is not None:
                violations.append(violation)
        return tuple(violations)
