# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from attrs import define, field
from datetime import datetime
from typing import Any


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
    return datetime.strptime(raw, "%Y-%m-%d")


def conv(data: Any):
    try:
        return int(data)
    except Exception:
        return data


class Alias:
    def __get__(self, obj: object, _objtype=None):
        return getattr(obj, self.name)

    def __init__(self, name: str):
        self.name = name


@define
class LokSabhaQuestion:
    title: str
    type: str
    sessionNo: str
    language: str
    questionType: str
    source: str
    committeeName: str
    debate: str
    handle: str
    keywordsCount: str
    phraseCount: str
    reportNo: str
    members: list[str]
    files: list[str]
    ministry: list[str]
    ministerName: list[str]
    councilOfStateNo: str
    resourceId: str
    assemblyNo: int
    date: datetime = field(converter=date_converter)
    loksabhaNo: int = field(converter=int)
    questionNo: str | int = field(converter=conv)
    year: int = field(converter=int)

    number = Alias("questionNo")
    subject = Alias("title")


@define
class RajyaSabhaQuestion:
    number: int = field(converter=int)
    type: str
    date: datetime = field(converter=date_converter)
    ministry: str
    member: str
    subject: str
    url: str
