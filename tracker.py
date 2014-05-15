import urllib2
import pprint
import json
import os2ll
from os2ll import grid2latlon
from bs4 import BeautifulSoup

def busURL(sid,direction):
  both_sids = ["2","2A","2B","2C","2D", "3", "3B", "8", "9"]
  obc_sids = ["300", "400", "500", "4", "4A", "4B", "4C", "5", "6", "13", "23", "35", "U1", "NU1", "U1X", "U5", "NU5", "U5X"]
  if sid in obc_sids:
    op = "OBC"
  else:
    op = "SOX"
  return "http://www.oxontime.co.uk/MobileNaptan.aspx?t=stoppointsdetails&vc="+sid+"&Direction="+direction+"&Operator="+op+"&format=xhtml"

def trackBuses(sid,direction):
  listurl = busURL(sid,direction)

  buses = {'type':'FeatureCollection', 'features':[]}
  due_buses = [[],[]]
  n=0

  # Iterate over stops on route
  listing = BeautifulSoup(urllib2.urlopen(listurl))
  for stop in listing('table')[2].tbody('tr'):
    tds = stop('td')
    area = tds[4].string
    stopid = tds[1].string
    stopname = stop('a')[1].contents[0]
    # print stop

    n=n+1
    due_buses.append([])

    # Iterate over buses at stop
    stopurl = "http://www.oxontime.co.uk/MobileNaptan.aspx?t=departure&sa="+stopid+"&dc=&ac=96&vc=&x=0&y=0&format=xhtml"
    stop = BeautifulSoup (urllib2.urlopen(stopurl))
    gridref = stop.find("a", { "class" : "DepartureLink" })
    coords = {}
    if gridref:
      xref = gridref['href'].split('&X=')[1].split('&')[0]
      yref = gridref['href'].split('&Y=')[1].split('&')[0]
      ll = grid2latlon(int(xref),int(yref))
      coords={'lat': ll[0], 'lon': ll[1]}
    message = stop('table')[2].find_all('tr')[0].string
    if message !="No current departures for this stop.":
      for bus in stop('table')[2].tbody('tr'):
        busname = bus('td')[0].string
        destination = bus('td')[1].string
        eta = bus('td')[2].string
        if busname == sid:
          if eta == "DUE":
            this_bus = {'type':'Feature','geometry':{'type':'Point', 'coordinates':[ll[1],ll[0]]}, 'properties':{'service': busname, 'destination':destination, 'approaching': {'name':stopname, 'area':area}}}
            if busname not in due_buses[n-1]+due_buses[n-2]:
              due_buses[n].append(busname)
              buses['features'].append(this_bus)
              print busname+" ("+destination+") due at "+stopname+", "+area

  return buses

def createJSON(sid, direction):
  buses = trackBuses(sid,direction)
  with open('static/data/'+sid+'_'+direction+'.json', 'w') as fp:
    json.dump(buses, fp)
  return "JSON created for "+sid
