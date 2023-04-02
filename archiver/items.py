# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from typing import Literal
from attrs import define, field
from datetime import datetime


def date_converter(raw: str):
    """Converts the raw date string to a datetime.datetime object.

    Both Lok Sabha and Rajya Sabha websites currently store the date as `DD.MM.YYYY`
    If that changes in the future, this function will have to be adjusted accordingly.

    Parameters
    ----------
    raw: :class:`str`
        The raw date string.

    Returns
    ----------
    :class:`datetime.datetime`
        The parsed datetime object.

    """
    return datetime.strptime(raw, "%d.%m.%Y")


@define
class Question:
    number: int = field(converter=int)
    type: Literal["STARRED", "UNSTARRED"]
    date: datetime = field(converter=date_converter)
    ministry: str
    member: str
    subject: str
    url: str
