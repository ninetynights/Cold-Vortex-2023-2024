import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


from netCDF4 import Dataset
rootgrp = Dataset("D:/HKUST_RA/SAMPLE_ERA5/2022.8.1to7.nc", "r")
print(rootgrp.data_model)

f = nc.Dataset('D:/HKUST_RA/SAMPLE_ERA5/2022.8.1to7.nc','r' ) 
f = nc.Dataset('D:/HKUST_RA/SAMPLE_ERA5/2023.JF.nc','r' ) 

all_vars = f.variables.keys() 
print(all_vars) 

all_vars_info = f.variables.items()    
print(all_vars_info)

lat = f.variables['latitude'][:]  #-40到80 res. 0.25  
lon = f.variables['longitude'][:] #50到170 res. 0.25
level = f.variables['level'][:] #200,300,500,700,850,925 
time = f.variables['time'][:]


#%%
#变量
#有的变量：z,q,t,u,v
var_name ='z'#(时间，气压层0-5，经，纬)
var_range = f.variables[var_name][0,:,:,:]

zuida=np.max(var_range)
zuixiao=np.min(var_range)
print(zuixiao,zuida)

var = f.variables[var_name][0,0,:,:]
var = np.array(var)

lon = np.array(lon)
lat = np.array(lat)

x, y = np.meshgrid(lon, lat)

fig = plt.figure(dpi=1000)
proj = ccrs.PlateCarree()
ax = plt.axes(projection=proj)
extents = [50, 170, 0, 80]
ax.set_extent(extents, crs=proj)


ax.coastlines(lw=0.25)
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.BORDERS,lw=0.2)

MIN=np.min(var)
MAX=np.max(var)

levels=np.arange(MIN-1,MAX+20,(MAX-MIN)/100)
cs = ax.contourf(x, y, var, levels,cmap='rainbow')

contours = plt.contour(x, y, var, colors = 'black',linewidths=0.5)
plt.clabel(contours, inline = True, fontsize = 4, inline_spacing = 2)

ax.set_title('Geopotential at 200 hPa  (m2/s2)',fontsize=10) 

plt.xticks(range(50, 171, 20), ['50°E', '70°E', '90°E', '110°E', '130°E', '150°E', '170°E'],fontsize=8)
plt.yticks(range(0, 81, 20), ['0', '20°N', '40°N', '60°N', '80°N'],fontsize=8)

cb=plt.colorbar(cs)
#cb.ax.set_yticklabels(np.arange(MIN,MAX,(MAX-MIN)/10))  # vertically oriented colorbar
'''
cb.ax.set_yticklabels(cbtick)
#cb.set_ticks(np.linspace(MIN,MAX,12))
cb.set_ticks(cbtlog,cbtick)
#cb.ax.yaxis.set_major_locator(MultipleLocator(0.5))
cb.update_ticks()
'''

plt.show()

#%%
var_name ='z'#(时间，气压层0-5，经，纬)
var_range = f.variables[var_name][0,:,:,:]

zuida=np.max(var_range)
zuixiao=np.min(var_range)
print(zuixiao,zuida)

var = f.variables[var_name][0,0,:,:]
var = np.array(var)
#画位势高度时候需要转化m
import metpy.calc
from metpy.units import units

var = var * units.m ** 2 / units.s ** 2
var = metpy.calc.geopotential_to_height(var)
var = np.array(var)

#%%
#画图
lon = np.array(lon)
lat = np.array(lat)

x, y = np.meshgrid(lon, lat)

fig = plt.figure(dpi=1000)
proj = ccrs.PlateCarree()
ax = plt.axes(projection=proj)
extents = [50, 170, -40, 80]
ax.set_extent(extents, crs=proj)


ax.coastlines(lw=0.25)
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.BORDERS,lw=0.2)

MIN=np.min(var)
MAX=np.max(var)

levels=np.arange(MIN-1,MAX+20,(MAX-MIN)/100)
cs = ax.contourf(x, y, var, levels,cmap='rainbow')

contours = plt.contour(x, y, var, colors = 'black',linewidths=0.5)
plt.clabel(contours, inline = True, fontsize = 4, inline_spacing = 2)

ax.set_title('Geopotential height at 200 hPa  (m)',fontsize=10) 

plt.xticks(range(50, 171, 20), ['50°E', '70°E', '90°E', '110°E', '130°E', '150°E', '170°E'],fontsize=8)
plt.yticks(range(-40, 81, 20), ['40°S', '20°S', '0', '20°N', '40°N', '60°N', '80°N'],fontsize=8)

cb=plt.colorbar(cs)
#cb.ax.set_yticklabels(np.arange(MIN,MAX,(MAX-MIN)/10))  # vertically oriented colorbar
'''
cb.ax.set_yticklabels(cbtick)
#cb.set_ticks(np.linspace(MIN,MAX,12))
cb.set_ticks(cbtlog,cbtick)
#cb.ax.yaxis.set_major_locator(MultipleLocator(0.5))
cb.update_ticks()
'''

plt.show()

#%%
#气温变量
#有的变量：z,q,t,u,v
var_name ='t'#(时间，气压层0-5，经，纬)
var_range = f.variables[var_name][0,:,:,:]

zuida=np.max(var_range)
zuixiao=np.min(var_range)
print(zuixiao,zuida)

var = f.variables[var_name][0,0,:,:]
var = np.array(var)

lon = np.array(lon)
lat = np.array(lat)

x, y = np.meshgrid(lon, lat)

fig = plt.figure(dpi=1000)
proj = ccrs.PlateCarree()
ax = plt.axes(projection=proj)
extents = [50, 170, 0, 80]
ax.set_extent(extents, crs=proj)


ax.coastlines(lw=0.25)
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.BORDERS,lw=0.2)

MIN=np.min(var)
MAX=np.max(var)

levels=np.arange(MIN,MAX,(MAX-MIN)/100)
cs = ax.contourf(x, y, var, levels,cmap='rainbow')

#contours = plt.contour(x, y, var, colors = 'black',linewidths=0.5)
#plt.clabel(contours, inline = True, fontsize = 4, inline_spacing = 2)

ax.set_title('Temperature at 200 hPa  (K)',fontsize=10) 

plt.xticks(range(50, 171, 20), ['50°E', '70°E', '90°E', '110°E', '130°E', '150°E', '170°E'],fontsize=8)
plt.yticks(range(0, 81, 20), ['0', '20°N', '40°N', '60°N', '80°N'],fontsize=8)

cb=plt.colorbar(cs)

'''
cb.ax.set_yticklabels(cbtick)
#cb.set_ticks(np.linspace(MIN,MAX,12))
cb.set_ticks(cbtlog,cbtick)
#cb.ax.yaxis.set_major_locator(MultipleLocator(0.5))
cb.update_ticks()
'''

plt.show()
#%%
var_name ='q'#(时间，气压层0-5，经，纬)
var_range = f.variables[var_name][0,:,:,:]

zuida=np.max(var_range)
zuixiao=np.min(var_range)
print(zuixiao,zuida)

var = f.variables[var_name][0,0,:,:]
var = 1000000*np.array(var)

cbmax=np.max(var)
cbmin=np.min(var)

var = np.log(var)

lon = np.array(lon)
lat = np.array(lat)

x, y = np.meshgrid(lon, lat)

fig = plt.figure(dpi=1000)
proj = ccrs.PlateCarree()
ax = plt.axes(projection=proj)
extents = [50, 170, 0, 80]
ax.set_extent(extents, crs=proj)


ax.coastlines(lw=0.25)
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.BORDERS,lw=0.2)

MIN=np.min(var)
MAX=np.max(var)

levels=np.arange(MIN,MAX,(MAX-MIN)/100)
cs = ax.contourf(x, y, var, levels,cmap='rainbow')

#contours = plt.contour(x, y, var, colors = 'black',linewidths=0.5)
#plt.clabel(contours, inline = True, fontsize = 4, inline_spacing = 2)

ax.set_title('Specific humidity at 200 hPa  (mg/kg)',fontsize=10) 

plt.xticks(range(50, 171, 20), ['50°E', '70°E', '90°E', '110°E', '130°E', '150°E', '170°E'],fontsize=8)
plt.yticks(range(0, 81, 20), ['0', '20°N', '40°N', '60°N', '80°N'],fontsize=8)

#cb=plt.colorbar(cs)

'''
cb.ax.set_yticklabels(cbtick)
#cb.set_ticks(np.linspace(MIN,MAX,12))
cb.set_ticks(cbtlog,cbtick)
#cb.ax.yaxis.set_major_locator(MultipleLocator(0.5))
cb.update_ticks()
'''

plt.show()

import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
fig, axes = plt.subplots(1, 1, figsize=(5, 10),dpi=1000)
cmap3 = copy.copy(cm.viridis)
norm3 = mcolors.LogNorm(vmin=cbmin, vmax=cbmax)
im3 = cm.ScalarMappable(norm=norm3, cmap='rainbow')
# 使用LogNorm时,colorbar会自动选取合适的Locator和Formatter.
cbar3 = fig.colorbar(
    im3, orientation='vertical',ticks=np.arange(cbmin,cbmax,(cbmax-cbmin)/10))
# Add colorbar, make sure to specify tick locations to match desired ticklabels
cbar3.ax.set_yticklabels(np.arange(cbmin,cbmax,(cbmax-cbmin)/10))  # vertically oriented colorbar

plt.show()

import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
fig, axes = plt.subplots(1, 1, figsize=(5, 10),dpi=1000)
cmap3 = copy.copy(cm.viridis)
norm3 = mcolors.LogNorm(vmin=cbmin, vmax=cbmax)
im3 = cm.ScalarMappable(norm=norm3, cmap='rainbow')
# 使用LogNorm时,colorbar会自动选取合适的Locator和Formatter.
cbar3 = fig.colorbar(
    im3, orientation='vertical',ticks=[cbmin,cbmax])
# Add colorbar, make sure to specify tick locations to match desired ticklabels
cbar3.ax.set_yticklabels([cbmin,cbmax])  # vertically oriented colorbar

plt.show()
#%%
#风速
p_level=5
lon = np.array(lon)
lat = np.array(lat)

u = f.variables['u'][0,p_level,:,:]
u = np.array(u)

v = f.variables['v'][0,p_level,:,:]
v = np.array(v)

WS=(u**2+v**2)**0.5

#位势高度
g ='z'#(时间，气压层0-5，经，纬)
g = f.variables[g][0,p_level,:,:]
g = np.array(g)

#画位势高度时候需要转化m
import metpy.calc
from metpy.units import units

g = g * units.m ** 2 / units.s ** 2
gh = metpy.calc.geopotential_to_height(g)
gh = np.array(gh)

#
x_d=lon[::10]
y_d=lat[::10]
u_d=u[::10,::10]
v_d=v[::10,::10]

#画图
lon = np.array(lon)
lat = np.array(lat)

x, y = np.meshgrid(lon, lat)
x_d,y_d=np.meshgrid(x_d, y_d)

fig = plt.figure(dpi=1000)
proj = ccrs.PlateCarree()
ax = plt.axes(projection=proj)
extents = [50, 170,0, 80]
ax.set_extent(extents, crs=proj)


ax.coastlines(lw=0.25)
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.BORDERS,lw=0.2)


MIN=np.min(WS)
MAX=np.max(WS)

levels=np.arange(MIN,MAX,(MAX-MIN)/100)
cs = ax.contourf(x, y, WS, levels,cmap='rainbow')

contours = plt.contour(x, y, gh, colors = 'black',linewidths=1)
plt.clabel(contours, inline = True, fontsize = 7, inline_spacing = 2)

ax.set_title('Windfield at 925 hPa  (m/s)',fontsize=10) 

plt.xticks(range(50, 171, 20), ['50°E', '70°E', '90°E', '110°E', '130°E', '150°E', '170°E'],fontsize=8)
plt.yticks(range(0, 81, 20), ['0', '20°N', '40°N', '60°N', '80°N'],fontsize=8)

cb=plt.colorbar(cs)
##cb.ax.set_yticklabels(np.arange(MIN,MAX,(MAX-MIN)/10))  # vertically oriented colorbar
Q = plt.quiver(lon[::10], lat[::10], u[::10,::10], v[::10,::10], edgecolors=('k'), width = 0.002,headwidth = 3, headlength=4.5, minshaft=1)
plt.quiverkey(Q, X=0.015, Y=1.1, U=20, label='', labelpos='E')


ticks=np.arange(np.min(WS), np.max(WS),5)
ticks=np.around(ticks,0)
cb.set_ticks(ticks)
cb.update_ticks()

plt.show()


#%%
#平均风速
p_level=1
lon = np.array(lon)
lat = np.array(lat)

u = f.variables['u'][:,p_level,:,:]
u = np.average(u,axis=0)
u = np.array(u)

v = f.variables['v'][:,p_level,:,:]
v = np.average(v,axis=0)
v = np.array(v)

WS=(u**2+v**2)**0.5

#位势高度
g ='z'#(时间，气压层0-5，经，纬)
g = f.variables[g][:,p_level,:,:]
g = np.average(g,axis=0)
g = np.array(g)

#画位势高度时候需要转化m
import metpy.calc
from metpy.units import units

g = g * units.m ** 2 / units.s ** 2
gh = metpy.calc.geopotential_to_height(g)
gh = np.array(gh)

#
x_d=lon[::10]
y_d=lat[::10]
u_d=u[::10,::10]
v_d=v[::10,::10]

#画图
lon = np.array(lon)
lat = np.array(lat)

x, y = np.meshgrid(lon, lat)
x_d,y_d=np.meshgrid(x_d, y_d)

fig = plt.figure(dpi=1000)
proj = ccrs.PlateCarree()
ax = plt.axes(projection=proj)
extents = [50, 170, 0, 80]
ax.set_extent(extents, crs=proj)


ax.coastlines(lw=0.25)
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.BORDERS,lw=0.2)


MIN=np.min(WS)
MAX=np.max(WS)

levels=np.arange(MIN,MAX+1,(MAX-MIN)/100)
cs = ax.contourf(x, y, WS, levels,cmap='rainbow')

contours = plt.contour(x, y, gh, colors = 'black',linewidths=1)
plt.clabel(contours, inline = True, fontsize = 7, inline_spacing = 2)

ax.set_title('Windfield at 300 hPa  (m/s)',fontsize=10) 

plt.xticks(range(50, 171, 20), ['50°E', '70°E', '90°E', '110°E', '130°E', '150°E', '170°E'],fontsize=8)
plt.yticks(range(0, 81, 20), ['0', '20°N', '40°N', '60°N', '80°N'],fontsize=8)

cb=plt.colorbar(cs)
##cb.ax.set_yticklabels(np.arange(MIN,MAX,(MAX-MIN)/10))  # vertically oriented colorbar
Q = plt.quiver(lon[::10], lat[::10], u[::10,::10], v[::10,::10], edgecolors=('k'), width = 0.002,headwidth = 3, headlength=4.5, minshaft=1)
plt.quiverkey(Q, X=0.015, Y=1.1, U=20, label='', labelpos='E')


ticks=np.arange(np.min(WS), np.max(WS),10)
ticks=np.around(ticks,0)
cb.set_ticks(ticks)
cb.update_ticks()

plt.show()
