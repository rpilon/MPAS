"""
Produce a altitude/time plot of the relative humidity at th certain location.
In our simulations, RH is null, so we had to calculate it. (script for a 15 km global simulation (15 Jan - 04 Feb 2009)
"""

from netCDF4 import *
import numpy as np
from pylab import *
from mpl_toolkits.basemap import cm as cmplot
import os

# Load set of files
f = MFDataset('x1.2621442.output.2009-*_00.00.00.nc')

# import latitudes and longitudes of the cells
lon = f.variables['lonCell'][:]
lat = f.variables['latCell'][:]

lonCell=lon*180./np.pi
latCell=lat*180./np.pi
nCells=latCell.shape[0]


# location of the plot (here South Maldives): the trick is to set the coordinates in a -180:180 degrees of longitudes and not 0-360 degrees
longitude_minimum = 72.
longitude_maximum = 74.
latitude_minimum = -.5
latitude_maximum = 1.5

# creating mask : the method is to only use the values which are in the area of interest by multypliyng every value by True or False
# 				  depending on the location of each cell.
NCells=latCell>latitude_minimum
SCells=latCell<latitude_maximum
ECells = lonCell>longitude_minimum
WCells = lonCell<longitude_maximum
cellsNearLon = NCells*SCells*ECells*WCells

#        shape  (Time,Cells,Levels)
pres = f.variables['pressure_base'][:,cellsNearLon,:]   # in hPa
qv = f.variables['qv'][:,cellsNearLon,:]
theta=f.variables['theta'][:,cellsNearLon,:]

# temperature in celsius (we assume that the pressure does not change over time in order to make the calculations faster)
T=theta* (pres[0,0,0]/np.mean(pres,axis=0))**(-287./1004) -273.15

es= 610.8*exp(17.27 * T/ (237.3+T));
ws= (621.97*es/(pres-es))
rh=qv*1000./ws *100

zgrid=f.variables['zgrid'][:,:] # (cells,nvert)

nVertLevels=rh.shape[2]
nTime=rh.shape[0]
time=range(nTime)

rhAvg=np.mean(rh,axis=1)
# we need to swap axes (or use the transpose matrix since it's a n x m matrix) to plot the field
rhAvg=np.swapaxes(rhAvg,0,1)


#nice plot latex compatible
rc('font',**{'family':'serif','sans-serif':['Times']})
rcParams['ps.useafm'] = True
rcParams['pdf.use14corefonts'] = True
rcParams['text.usetex'] = False
rcParams.update({'font.size': 18})

# plot
cmap = plt.cm.get_cmap(cmplot.GMT_no_green)
lev=range(0,125,5)

fig=figure(figsize=(18,6))
cs=contourf(time,zgrid[0,0:-1],Mrh,levels=lev,cmap=cmap,extend='max')#cm.RdYlBu)
cbar=fig.colorbar(cs)
cbar.set_ticks(range(0,130,10))
cbar.set_label('%',rotation=270)
ax=gca()
ylabel("altitude (km)",fontsize=16)
ax.set_ylim([0,20000]) # form 0 to 20km
ax.set_yticks(arange(0,22e3,2e3))
ax.set_yticklabels(arange(0,22,2)) # xlabels im km
ax.set_xticks(time[::4]) # 4 time steps a file/day
ax.set_xticklabels(["Jan 15","","Jan 17","","Jan 19","","Jan 21","","Jan 23","","Jan 25","","Jan 27","","Jan 29","","Jan 31","","Feb 02","","Feb 04"], rotation=0)

show(block=False)
