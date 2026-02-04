from core import GameTime
from models import Realm


def convert_to_realm_time(world_time: GameTime, realm: Realm) -> GameTime:
    """
    Convert World Clock time to realm local time.

    Args:
        world_time: Time in World Clock
        realm: The realm with time_rule offset

    Returns:
        GameTime: Local time in the realm
    """
    total_mins = world_time.to_total_minutes() + realm.time_rule

    days = total_mins // (24 * 60)
    remaining = total_mins % (24 * 60)
    hours = remaining // 60
    minutes = remaining % 60

    return GameTime(days, hours, minutes, 0)
