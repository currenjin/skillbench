# timekit

Tiny duration parsing helpers.

```python
from timekit import parse_duration

parse_duration("2h")     # 120
parse_duration("45m")    # 45
parse_duration("1h30m")  # 90
```

Run tests: `python3 -m pytest tests -q`
