import urllib2
import pprint
from bs4 import BeautifulSoup

#Define route
sid = "S1"
direction = "2"
listurl = "http://www.oxontime.co.uk/MobileNaptan.aspx?t=stoppointsdetails&vc="+sid+"&Direction="+direction+"&Operator=SOX&format=xhtml"

buses = []
already_due = []

# Iterate over stops on route
listing = BeautifulSoup (urllib2.urlopen(listurl))
for stop in listing('table')[2].tbody('tr'):
  tds = stop('td')
  area = tds[4].string
  stopid = tds[1].string
  stopname = stop('a')[1].contents[0]

  # Iterate over buses at stop
  stopurl = "http://www.oxontime.co.uk/MobileNaptan.aspx?t=departure&sa="+stopid+"&dc=&ac=96&vc=&x=0&y=0&format=xhtml"
  stop = BeautifulSoup (urllib2.urlopen(stopurl))
  message = stop('table')[2].find_all('tr')[0].string
  if message !="No current departures for this stop.":
    for bus in stop('table')[2].tbody('tr'):
      busname = bus('td')[0].string
      destination = bus('td')[1].string
      eta = bus('td')[2].string
      if eta == "DUE":
        this_bus = {'service': busname, 'destination':destination, 'approaching': {'name':stopname, 'area':area}}
        print already_due
        if busname in already_due:
          print busname+" is already due at prior stop"
        else:
          already_due.append(busname)
          print already_due
          buses.append(this_bus)
          print busname+" ("+destination+") due at "+stopname+", "+area
      else:
        if busname in already_due:
          already_due.remove(busname)

print "\nFinal list:"
pprint.pprint(buses)
