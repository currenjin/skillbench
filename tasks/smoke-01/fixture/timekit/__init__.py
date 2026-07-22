"""timekit — tiny duration parsing helpers."""
import re

_PATTERN = re.compile(r"^(?:(\d+)h)?(?:(\d+)m)?$")


def parse_duration(text):
    """Parse durations like '2h', '45m', '1h30m' into total minutes."""
    text = text.strip()
    m = _PATTERN.match(text)
    if not m or not any(m.groups()):
        raise ValueError(f"invalid duration: {text!r}")
    hours, minutes = m.groups()
    if hours:
        return int(hours) * 60
    return int(minutes)
