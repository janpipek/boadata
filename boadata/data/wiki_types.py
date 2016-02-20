from bs4 import BeautifulSoup
import urllib
from urllib.request import Request
from collections import OrderedDict
import pandas as pd
from boadata.core import DataObject
from boadata.core.data_conversion import IdentityConversion
from .pandas_types import PandasDataFrameBase



@DataObject.register_type()
@IdentityConversion.enable_to("pandas_data_frame")
class WikiTable(PandasDataFrameBase):
    type_name = "wiki_table"

    @classmethod
    def accepts_uri(cls, uri):
        return uri.startswith("wiki://")

    @classmethod
    def from_uri(cls, uri, **kwargs):
        schema, id = uri.split("://", 2)
        page, table_no = id.split(":")
        wiki_uri = "https://en.wikipedia.org/wiki/{0}".format(page)

        header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
        req = Request(wiki_uri, headers=header)

        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page, "lxml")

        tables = soup.findAll("table", { "class" : "wikitable" })
        table = tables[int(table_no)]
        # caption = table.find("caption")
        tr = table.find("tr")

        cols = []
        data = []
        if tr:
            headers = tr.findAll("th")
            for i, col in enumerate(headers):
                name = "".join(col.findAll(text=True, recursive=False)).strip()
                if not name:
                    name = "Column{0}".format(i)
                name.replace("\n", " ")
                cols.append(name)
                # print ("*", name)
            # print(cols)

            trs = table.findAll("tr")[1:]
            for tr in trs:
                tds = tr.findAll("td")
                d = OrderedDict()
                for i, td in enumerate(tds):
                    text  = "".join(td.findAll(text=True, recursive=False)).strip()
                    if not text:
                        for a in td.findAll("a", recursive=False):
                            text += "".join(a.findAll(text=True, recursive=False)).strip()
                    number_candidate = text.replace(",", "")
                    try:
                        number = int(number_candidate)
                        text = number
                    except:
                        try:
                            number = float(number_candidate)
                            text = number
                        except:
                            pass
                    d[cols[i]] = text
                data.append(d)
        df = pd.DataFrame(data)
        # df = df.convert_objects(convert_numeric=True)
        return cls(df, uri=uri)