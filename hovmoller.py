"""
Produce a Hovmoller diagram (time vs longitudes) from the diagnostics files.
Here we use the vertical velocity at 200 and 500 hPa, for a 15 km global simulation (15 Jan - 04 Feb 2009)
Same methode for the x1.output files: if it's a 3D field, use zgrid to see the altitude of the levels for each cell)
"""

from netCDF4 import *
import numpy as np
from pylab import *
from matplotlib import pyplot, cm
import os

# Load files
f = MFDataset('diagnostics.2009-0*.nc')
g = Dataset('output.nc','r') #either a 3D file like x1.2621442.output.2009-02-01_00.00.00.nc or a netcdf file with 'latCell' and 'lonCell'

# count files and set the number of time steps (ntime):  gives the possibility the load files 
gg=[]
for ff in sorted(os.listdir('.')):
  if (ff.endswith(".nc")) and (ff.startswith("diagnostics.2009-0")):
    gg.append(ff)

ntime=size(gg)

# import latitudes and longitudes of the cells
lonCell=g.variables['lonCell'][:]*180./np.pi
latCell=g.variables['latCell'][:]*180./np.pi
nCells=latCell.shape[0]

# fields to plot
w500  = f.variables['w_500hPa'][:,:]
w200  = f.variables['w_200hPa'][:,:]

# creating mask : the method is to only use the values which are in the area of interest
"""
typical mask made from booleans

NCells=latCell>latitude_minimum
SCells=latCell<latitude_maximum
ECells = lonCell>longitude_minimum
WCells = lonCell<longitude_maximum
cellsNearLon = NCells*SCells*ECells*WCells
"""
# we want to average the fields between 10 South and 10 North
latitude_minimum = -10.
latitude_maximum = 10.

# we need an array with a shape [time, longitudes]. At this point the shape is [time, nCells]
# we brownse/loop the longitudes by an increment of 1 degree, and average over the cells which are in the domaine 10N-10S - 1degree of longitude
incLon=1.
Nw500=np.empty([ntime,len(arange(0,360,incLon))]) # new vertical velocity
LatMask=(latCell < latitude_maximum)&(latCell > latitude_minimum)

for ii in arange(0,360,incLon):
  ECells = lonCell > ii
  WCells = lonCell < ii+incLon
  cellsNearLon = NCells*SCells*ECells*WCells
  Nw500[:,ii]= np.mean(w500[:,cellsNearLon],axis=1)
  print ii


# nice plot latex compatible
rc('font',**{'family':'serif','sans-serif':['Times']})
rcParams['ps.useafm'] = True
rcParams['pdf.use14corefonts'] = True
rcParams['text.usetex'] = False
rcParams.update({'font.size': 18})


# plot
cmap = plt.cm.get_cmap(cm.RdYlBu_r)
lev2=arange(-0.05,0.15,0.01)
lev5=arange(-0.04,0.13,0.01)

fig=figure(figsize=(8,10))
ax = fig.add_subplot(111)
# show only from 45 to 150 degree of longitude
cs=contourf(arange(45,150,incLon),range(ntime),Nw500[::1,int(45./incLon):int(150./incLon)],lev2,cmap=cmap)
cbar  = fig.colorbar(cs, orientation='horizontal', shrink=1., pad=.04, aspect=20)
cbar.ax.tick_params(labelsize=16) 
cbar.set_label('m.s$^{-1}$')
ax.invert_yaxis()
ax.set_yticks(range(0,ntime,4));
ax.set_ylim([ntime,0])
ax.set_yticklabels(["Jan 15","","Jan 17","","Jan 19","","Jan 21","","Jan 23","","Jan 25","","Jan 27","","Jan 29","","Jan 31","","Feb 02","","Feb 04"])

show(block=False)
