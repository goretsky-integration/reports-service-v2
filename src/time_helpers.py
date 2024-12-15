from dataclasses import dataclass
from datetime import datetime, timedelta

__all__ = (
    "get_moscow_now",
    "round_to_upper_hour",
    "Period",
)


def get_moscow_now() -> datetime:
    return datetime.utcnow() + timedelta(hours=3)


def round_to_upper_hour(dt: datetime) -> datetime:
    if dt.minute != 0:
        dt = dt + timedelta(hours=1)
    return dt.replace(minute=0, second=0, microsecond=0)


@dataclass(frozen=True, slots=True)
class Period:
    from_datetime: datetime
    to_datetime: datetime

    @classmethod
    def today_to_this_time(cls) -> "Period":
        now = get_moscow_now()
        return cls(
            from_datetime=datetime(
                year=now.year,
                month=now.month,
                day=now.day,
            ),
            to_datetime=now,
        )

    @classmethod
    def week_before_today_to_this_time(cls) -> "Period":
        now = get_moscow_now()
        week_before = now - timedelta(weeks=1)
        return cls(
            from_datetime=datetime(
                year=week_before.year,
                month=week_before.month,
                day=week_before.day,
            ),
            to_datetime=datetime(
                year=week_before.year,
                month=week_before.month,
                day=week_before.day,
                hour=now.hour,
                minute=now.minute,
                second=now.second,
                microsecond=now.microsecond,
            ),
        )

    def rounded_to_upper_hour(self) -> "Period":
        return Period(
            from_datetime=round_to_upper_hour(self.from_datetime),
            to_datetime=round_to_upper_hour(self.to_datetime),
        )
