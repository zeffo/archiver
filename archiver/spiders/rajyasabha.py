from scrapy.http import Request, TextResponse
from archiver.items import Question
from archiver.spider import BaseSpider

from urllib.parse import urlencode
from attrs import fields


class RajyaSabhaSpider(BaseSpider):
    BASE_URL = "http://rajyasabha.nic.in"
    URL = "https://rajyasabha.nic.in/Questions/IntegratedSearchFormResult"

    HEADERS = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    name = "rajyasabha"

    # //*[@id="txtTitle"]
    # //*[@id="show"]

    def form_data(self, search_term: str):
        """Returns URL Encoded form data for the given search term.

        Parameters
        ----------

        search_term: :class:`str`
           The term to search for.

        Returns
        ----------

        :class:`str`
            The encoded URL string.

        """
        raw = {
            "session": "",
            "sessionto": "",
            "mpCode": "",
            "minCode": "",
            "sesType": "ANYTYPE",
            "QesNumber": "",
            "Title": search_term,
            "SessionDate_from": "Select",
            "SessionDate_to": "Select",
            "Match_on": "AllWord",
            "Sort_by": "Any+Word",
            "SearchOn": "Title",
        }
        return urlencode(raw)

    def start_requests(self):
        for term in self.search_terms:
            yield Request(
                self.URL, method="POST", body=self.form_data(term), headers=self.HEADERS
            )

    def parse(self, response: TextResponse):
        table = response.xpath('//*[@id="Member_Tables"]')

        headers = fields(Question)

        for row in table.xpath("./tbody//tr"):
            data = {}
            for i, col in enumerate(row.xpath("./td")):
                if i == 6:
                    elem = col.xpath(".//a[text()='English']/@href").get()
                    value = f"{self.BASE_URL}{elem}"
                else:
                    value = col.xpath(".//text()").get()

                header = headers[i].name
                data[header] = value

            try:
                yield Question(**data)
            except ValueError:
                self.log_error(data)
