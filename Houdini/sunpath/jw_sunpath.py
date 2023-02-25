node = hou.pwd()
geo = node.geometry()

# Add code to modify contents of geo.
# Use drop down menu to select examples.

import math
import pandas as pd
import numpy as np
import pvlib
from pvlib.location import Location, solarposition

# Definition of Location oject. Coordinates and elevation of Madrid Ciemat Headquarters (Spain)
lat = node.parm("lat").eval()
lon = node.parm("lon").eval()
tz = f'Etc/GMT{node.parm("tz").eval()}' # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
site = Location(lat, lon, tz)
times = pd.date_range('2022-01-01 00:00:00', '2023-01-01 ', freq='H', tz=tz)
solpos = solarposition.get_solarposition(times, lat, lon)
solpos = solpos.loc[solpos['apparent_elevation'] > 0, :] # remove nighttime
scale = node.parm("scale").eval()

if node.parm("analemma").eval() == 1:
    # draw analemma loops
    analemmagroup = geo.createPointGroup("analemma")
    for hour in range(24):
        poly = geo.createPolygon(is_closed=False)
        
    for timestamp, row in solpos.iterrows():  
        pt = geo.createPoint()
        x = scale * math.cos(math.radians(row["azimuth"]-90)) * math.sin(math.radians(row["zenith"]))
        z = scale * math.sin(math.radians(row["azimuth"]-90)) * math.sin(math.radians(row["zenith"]))
        y = scale * math.cos(math.radians(row["zenith"]))
        pt.setPosition((x,y,z))
        geo.prim(timestamp.hour).addVertex(pt)  
        analemmagroup.add(pt)

if node.parm("dates").eval() == 1:        
    # draw solstices and equinox
    dategroup = geo.createPointGroup("major_dates")
    for date in pd.to_datetime(['2022-03-21', '2022-06-21', '2022-12-21']):
        times = pd.date_range(date, date+pd.Timedelta('24h'), freq='10min', tz=tz)
        solpos = solarposition.get_solarposition(times, lat, lon)
        solpos = solpos.loc[solpos['apparent_elevation'] > 0, :] # remove nighttime
        poly = geo.createPolygon(is_closed=False)
        for index, row in solpos.iterrows():
            pt = geo.createPoint()
            x = scale * math.cos(math.radians(row["azimuth"]-90)) * math.sin(math.radians(row["zenith"]))
            z = scale * math.sin(math.radians(row["azimuth"]-90)) * math.sin(math.radians(row["zenith"]))
            y = scale * math.cos(math.radians(row["zenith"]))
            pt.setPosition((x,y,z))
            poly.addVertex(pt)
            dategroup.add(pt)
        
# draw current time
analysis_year = node.parm("year").eval()
analysis_month = node.parm("month").eval()
analysis_day = node.parm("day").eval()
analysis_hour = node.parm("hour").eval()
analysis_min = node.parm("min").eval()
if analysis_min > 59:
    divmod = np.divmod(analysis_min, 59)
    analysis_min = divmod[1]
    analysis_hour = analysis_hour + divmod[0]
date = f"{analysis_year}-{analysis_month}-{analysis_day}"
analysis_date = pd.date_range(f"{date} {analysis_hour}:{analysis_min}", "2000", periods=1, tz=tz)
analysis_solpos = solarposition.get_solarposition(analysis_date, lat, lon)
if node.parm("sun").eval() == 1:
    sunpt = geo.createPoint()
    x = scale * math.cos(math.radians(analysis_solpos.iloc[0]["azimuth"]-90)) * math.sin(math.radians(analysis_solpos.iloc[0]["zenith"]))
    z = scale * math.sin(math.radians(analysis_solpos.iloc[0]["azimuth"]-90)) * math.sin(math.radians(analysis_solpos.iloc[0]["zenith"]))
    y = scale * math.cos(math.radians(analysis_solpos.iloc[0]["zenith"]))
    sunpt.setPosition((x,y,z))
    geo.createPointGroup("sun").add(sunpt)

if node.parm("analysisarc").eval() == 1:
    # analysis day arc
    analysis_day = pd.date_range(f"{date} 00:00:00", f"{date} 23:59:00", freq="10min", tz=tz)
    analysis_day_solpos = solarposition.get_solarposition(analysis_day, lat, lon)
    analysis_day_solpos = analysis_day_solpos.loc[analysis_day_solpos['apparent_elevation'] > 0, :] # remove nighttime
    dayarc_poly = geo.createPolygon(is_closed=False)
    arcgroup = geo.createPointGroup("analysis_arc")
    for index, row in analysis_day_solpos.iterrows():
        pt = geo.createPoint()
        x = scale * math.cos(math.radians(row["azimuth"]-90)) * math.sin(math.radians(row["zenith"]))
        z = scale * math.sin(math.radians(row["azimuth"]-90)) * math.sin(math.radians(row["zenith"]))
        y = scale * math.cos(math.radians(row["zenith"]))
        pt.setPosition((x,y,z))
        dayarc_poly.addVertex(pt)
        arcgroup.add(pt)
        
if node.parm("sunline").eval() == 1:    
    sunline = geo.createPolygon(is_closed=False)
    origpt = geo.createPoint()
    origpt.setPosition((0,0,0))
    sunline.addVertex(sunpt)
    sunline.addVertex(origpt)
    geo.createPrimGroup("sunline").add(sunline)
    
if node.parm("base").eval() == 1:    
    #create base
    basepoly = geo.createPolygon()
    geo.createPrimGroup("base").add(basepoly) 
    for degree in range(0, 360, 10):
        pt = geo.createPoint()
        x = scale * math.cos(math.radians(degree-90))
        z = scale * math.sin(math.radians(degree-90))
        pt.setPosition((x,0,z))
        basepoly.addVertex(pt)  
    