"""日期解析与序列化辅助。"""

from datetime import date, datetime, time


def parse_date(value, field_label="日期"):
    """把 YYYY-MM-DD 或 ISO 字符串解析为 date。"""

    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
            try:
                return datetime.strptime(text, fmt).date()
            except ValueError:
                continue
        try:
            return datetime.fromisoformat(text).date()
        except ValueError as exc:
            raise ValueError(f"{field_label}格式应为 YYYY-MM-DD") from exc
    raise ValueError(f"{field_label}格式应为 YYYY-MM-DD")


def format_date(value):
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return None


def format_datetime(value):
    if isinstance(value, datetime):
        return value.replace(microsecond=0).isoformat(sep=" ")
    return None


def today():
    return datetime.now().date()


def day_start(value=None):
    """本地某日的零点（naive datetime），默认今天。

    完成时间等业务日期口径统一使用它，避免与 UTC 当前时刻混用。
    """

    if value is None:
        value = today()
    if isinstance(value, datetime):
        value = value.date()
    return datetime.combine(value, time.min)
