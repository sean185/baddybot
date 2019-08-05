import requests as re
from bs4 import BeautifulSoup
from datetime import date, timedelta
from baddybot.constants import STATUSMAP

def getAvailability(CCcode, bookingdate):
    res = re.get('https://www.onepa.sg/facilities/{}?date={}'.format(CCcode, bookingdate))
    soup = BeautifulSoup(res.text, 'html.parser')

    timeslotElems = soup.find(id='facTable1').select('.timeslotsContainer .slots')
    timeslots = [elem.text.split(' - ')[0].replace(' ','') for elem in timeslotElems]

    courtElems = soup.find(id='facTable1').select('.facilitiesType')
    courtNumbers = [court.select_one('.slotsTitle').text.strip() for court in courtElems]

    availability = []
    for court in courtElems:
        slotElems = court.select('.slots')
        slots = [list(elem.attrs['class'])[-1] for elem in slotElems]
        slots = [STATUSMAP[s] for s in slots]
        availability.append(slots)

    rows = list(zip(*[timeslots]+availability))

    output = ['|'.join(['Timings']+[n.ljust(2) for n in courtNumbers])]
    for r in rows:
        output.append('|'.join([r[0].rjust(7)]+[i.ljust(2) for i in r[1:]]))

    return '\n'.join(output)

def testGetAvailability():
    output = getAvailability('4330ccmcpa-bm', date.today()+timedelta(days=1))
    print(output)