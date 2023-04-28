import datetime
import zoneinfo

from app.env import env

TIMEZONE = allow_origins = env.str(
    name="TIMEZONE",
    # For a list, please see the link:
    # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    default="America/Phoenix",
)

# https://docs.python.org/3/library/zoneinfo.html#zoneinfo.ZoneInfo
ZONEINFO = zoneinfo.ZoneInfo(TIMEZONE)


def utc_to_local(utc_dt: datetime.datetime) -> datetime.datetime:
    return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=ZONEINFO)
