from models.options import Options


def get_interval(open_time: str, close_time: str):
    """Returns Interval enum object."""

    delta = {
        2000: Options.Interval.second_2,
        60000: Options.Interval.minute_1,
        180000: Options.Interval.minute_3,
        300000: Options.Interval.minute_5,
        900000: Options.Interval.minute_15,
        1800000: Options.Interval.minute_30,
        3600000: Options.Interval.hour_1,
        7200000: Options.Interval.hour_2,
        14400000: Options.Interval.hour_4,
        21600000: Options.Interval.hour_6,
        28800000: Options.Interval.hour_8,
        43200000: Options.Interval.hour_12,
        86400000: Options.Interval.day_1,
        259200000: Options.Interval.day_3,
        604800000: Options.Interval.week_1,
    }

    try:
        ms = close_time - open_time
    except KeyError:
        raise Exception("Candle has incorrect time interval")
    return delta[ms]
