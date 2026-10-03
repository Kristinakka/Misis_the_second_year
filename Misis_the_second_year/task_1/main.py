from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Employee:
    id: str
    department: str
    permissions: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class Workplace:
    id: str
    allowed_department: str | None = None
    required_permission: str | None = None


@dataclass(frozen=True)
class Booking:
    employee: Employee
    workplace: Workplace
    starts_at: datetime
    ends_at: datetime

    def __post_init__(self) -> None:
        if self.starts_at >= self.ends_at:
            raise ValueError("Время окончания должно быть позже времени начала")


class BookingService:
    def __init__(self, workplaces: Iterable[Workplace], validator) -> None:
        self._workplaces = tuple(workplaces)
        if len({workplace.id for workplace in self._workplaces}) != len(
            self._workplaces
        ):
            raise ValueError("Идентификаторы рабочих мест должны быть уникальными")
        self._validator = validator
        self._bookings: list[Booking] = []

    def check_booking(self, booking: Booking) -> tuple[str, ...]:
        if booking.workplace not in self._workplaces:
            return ("Рабочее место отсутствует в списке компании",)
        return self._validator.validate(booking, self._bookings)

    def can_book(self, booking: Booking) -> bool:
        return not self.check_booking(booking)

    def create_booking(
        self,
        employee: Employee,
        workplace: Workplace,
        starts_at: datetime,
        ends_at: datetime,
    ) -> Booking:
        booking = Booking(employee, workplace, starts_at, ends_at)
        violations = self.check_booking(booking)
        if violations:
            raise ValueError("; ".join(violations))
        self._bookings.append(booking)
        return booking

    def available_workplaces(
        self, employee: Employee, starts_at: datetime, ends_at: datetime
    ) -> list[Workplace]:
        return [
            workplace
            for workplace in self._workplaces
            if self.can_book(Booking(employee, workplace, starts_at, ends_at))
        ]
