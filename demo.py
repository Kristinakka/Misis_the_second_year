from datetime import datetime
from main import Booking, BookingService, Employee, Workplace
from validate import BookingValidator


def main() -> None:
    workplaces = [
        Workplace(
            "A-01", allowed_department="Разработка", required_permission="тихая зона"
        ),
        Workplace("B-01"),
    ]
    service = BookingService(workplaces, BookingValidator())

    alice = Employee("alice", "Разработка", frozenset({"тихая зона"}))
    bob = Employee("bob", "Продажи")
    start = datetime(2026, 10, 2, 9)
    end = datetime(2026, 10, 2, 12)

    booking = service.create_booking(alice, workplaces[0], start, end)
    print(
        f"Создано бронирование: {booking.workplace.id}, {booking.starts_at:%d.%m %H:%M}–{booking.ends_at:%H:%M}"
    )

    candidate = Booking(
        bob, workplaces[0], datetime(2026, 10, 2, 10), datetime(2026, 10, 2, 11)
    )
    print("Причины отказа:", *service.check_booking(candidate), sep="\n- ")

    available = service.available_workplaces(bob, start, end)
    print("Доступные места для Боба:", ", ".join(place.id for place in available))


if __name__ == "__main__":
    main()
