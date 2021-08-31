# pylint: disable=no-name-in-module

from pydantic import BaseModel
from pydantic.types import constr

from .options import Options
from .window import Window


class Symbol(BaseModel):
    """Holds all data related to a symbol, such as `BTCUSDT`."""

    name:    constr(strip_whitespace=True, to_lower=True, min_length=3, max_length=6)
    windows: dict[Options.Interval, Window] = dict()