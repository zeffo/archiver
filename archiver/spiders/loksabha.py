from scrapy.http import FormRequest, TextResponse, Request
from archiver.items import Question
from archiver.spider import BaseSpider


class LokSabhaSpider(BaseSpider):

    URL = "https://loksabha.nic.in/Questions/Qtextsearch.aspx"

    name = "loksabha"

    @staticmethod
    def form_data(search_term: str, page_no: int = 1):
        return {
            "ctl00$txtSearchGlobal": "",
            "ctl00$ContentPlaceHolder1$ddlfile": ".pdf",
            "ctl00$ContentPlaceHolder1$TextBox1": search_term,
            "ctl00$ContentPlaceHolder1$btn": "allwordbtn",
            "ctl00$ContentPlaceHolder1$btn1": "titlebtn",
            "ctl00$ContentPlaceHolder1$txtpage": str(page_no),
            "ctl00$ContentPlaceHolder1$btngo": "Go",
        }

    def get_total_pages(self, response: TextResponse):
        TARGET_XPATH = '//*[@id="ContentPlaceHolder1_lblfrom"]//text()'
        target = response.xpath(TARGET_XPATH).get()
        if target:
            return int(target.split()[1])

    def get_data(self, response: TextResponse) -> list[Question]:
        """Parses the data table and returns a list of `Question`"""
        TARGET_XPATH = '//*[@id="ContentPlaceHolder1_tblMember"]/tr/td/table'
        table = response.xpath(TARGET_XPATH)

        raw_headers = table.xpath("//thead/tr/td//text()").getall()
        headers = list(map(str.strip, raw_headers))
        questions: list[Question] = []

        for row in table.xpath("./tr"):
            data = {}
            for h, col in enumerate(row.xpath(".//td")):
                header = headers[h].lower()

                if h == 0:  # Q.No. --> number
                    header = "number"
                if (
                    h == 1
                ):  # This tag gives both the Question Type and PDF url, so we'll parse it seperately
                    data["url"] = col.xpath(".//a[text()='PDF/WORD']/@href").get()
                    raw_type = col.xpath("./a[2]/text()").get()
                    data["type"] = raw_type.strip() if raw_type else "UNKNOWN"
                    continue

                # the rest are plaintext
                data[header] = "".join(col.xpath("./a//text()").getall()).strip()

            try:
                questions.append(Question(**data))
            except ValueError:
                self.logger.error(f"Error adding question: {data}")
        return questions

    def parse(self, response: TextResponse):
        for term in self.search_terms:
            yield FormRequest.from_response(
                response, formdata=self.form_data(term), callback=self.parse_pages(term)
            )

    def add_data(self, response: TextResponse):
        return self.get_data(response)

    def parse_pages(self, term: str):
        def callback(response: TextResponse):
            pages = self.get_total_pages(response) or 0
            for i in range(1, pages + 1):
                yield FormRequest.from_response(
                    response, formdata=self.form_data(term, i), callback=self.add_data
                )

        return callback

    def start_requests(self):
        req = Request(self.URL)
        yield req
