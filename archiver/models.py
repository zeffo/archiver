# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from attrs import define, field
from datetime import datetime
from typing import Any, TypeVar, Type


def int_or_str(data: Any):
    try:
        return int(data)
    except Exception:
        return data

T = TypeVar("T")

class Alias:
    def __get__(self, obj: T, _objtype: Type[T] | None = None):
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
    date: datetime = field(converter=lambda r: datetime.strptime(r, "%Y-%m-%d"))
    loksabhaNo: int = field(converter=int)
    questionNo: str | int = field(converter=int_or_str)
    year: int = field(converter=int)

    number = Alias("questionNo")
    subject = Alias("title")


@define
class RajyaSabhaQuestion:
    mp_code: int
    qslno: int
    qtitle: str
    qtype: str
    ans_date: datetime = field(converter=lambda r: datetime.strptime(r, "%d-%m-%Y"))
    adate: datetime = field(converter=datetime.fromisoformat)   # Same as ans_date but sent as an ISO-8601 string.
    shri: str # Yes, this is a real key. I promise.
    qno: float  # Yes, the question numbers are sent as floats.
    name: str
    min_name: str
    qn_text: str
    ans_text: str | None
    ses_no: int
    depc: int
    status: str
    P_flag: str
    files: str
    hindifiles: str
    min_code: int
    supp: None

    number = Alias("qno")
    subject = Alias("qtitle")
    date = Alias("ans_date")
    

