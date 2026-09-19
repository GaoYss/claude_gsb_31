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
    """完成时间的统一口径：日期粒度，返回指定日期（默认今天）当天零点。

    completed_at 只精确到日：有养护记录的任务以最新养护日期为准，
    无记录的任务以操作当天为准，不再写入具体时分秒，保证同一任务
    无论走哪条路径、在当天哪个时刻操作，归属月份都唯一确定。
    """

    if value is None:
        value = today()
    if isinstance(value, datetime):
        value = value.date()
    return datetime.combine(value, time.min)
