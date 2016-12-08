import requests
import time
from bs4 import BeautifulSoup
import re


def get_tickets(date):
    """
    aim:目的地,
    location:现在的所在地,
    date:车票日期
    """
    Now = time.localtime()
    Date = time.strptime(date, "%Y-%m-%d")
    intervial_year = Date.tm_year - Now.tm_year
    if intervial_year == 0:
        intervial_day = Date.tm_yday - Now.tm_yday
    if intervial_year >= 1:
        intervial_day = 365 * intervial_year - Now.tm_yday + Date.tm_yday + 1
    elif intervial_year < 0:
        return -1
    url = r"http://trains.ctrip.com/TrainBooking/Search.aspx?from=nanchang&to=changzhi&day={0}&number=&fromCn=%C4%CF%B2%FD&toCn=%B3%A4%D6%CE".format(intervial_day)
    result = requests.get(url)
    html = result.text
    bs = BeautifulSoup(html, "lxml")
    trainlist = bs.find_all(re.compile("lisBox"), bs)
    a = re.findall('<strong class="TxtRed">(.*?)</strong>', html)
    return (a)


html = get_tickets("2016-12-12")
print(html)
