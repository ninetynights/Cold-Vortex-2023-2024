
import netCDF4 as nc
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 打开文件
f = nc.Dataset("/Users/momo/Desktop/20240827/era5/2023.nc", 'r')

# 提取时间变量
time_values = f.variables['time'][:]
time_units = f.variables['time'].units
base_time_str = time_units.split('since')[1].strip().split('.')[0]
base_time = datetime.strptime(base_time_str, "%Y-%m-%d %H:%M:%S")

# 定义要绘制的时间索引（例如：第24小时）
# 第24小时表示 2023-08-18-00时  即北京时间2023-08-18-08时
time_index = 24
time_offset = timedelta(hours=int(time_values[time_index]))
actual_time_utc = base_time + time_offset
actual_time_cst = actual_time_utc + timedelta(hours=8)


# 提取经纬度数据
lon = f.variables['longitude'][:]
lat = f.variables['latitude'][:]

# 查找东经90度到140度的经度索引范围
lon_min, lon_max = 90, 140
lon_mask = (lon >= lon_min) & (lon <= lon_max)
lon_subset = lon[lon_mask]

# 提取对应经度范围的变量数据
var_name = 'z' # 高度场
var = f.variables[var_name][time_index, 0, :, :]  # 提取指定时间点和气压层的数据
var_subset = var[:, lon_mask]  # 只选择东经90°到140°之间的数据


# 网格化经纬度
lat_subset = lat  # 维持原有纬度
x, y = np.meshgrid(lon_subset, lat_subset)

# 绘制图像
fig = plt.figure(dpi=120)
proj = ccrs.PlateCarree()
ax = plt.axes(projection=proj)
extents = [lon_min, lon_max, 10, 60]  # 设置绘图的经纬度范围
ax.set_extent(extents, crs=proj)

ax.coastlines(lw=0.25)
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.BORDERS, lw=0.2)

# 等高线和填充图
MIN = np.min(var_subset)
MAX = np.max(var_subset)
levels = np.arange(MIN-1, MAX+20, (MAX-MIN)/100)
cs = ax.contourf(x, y, var_subset, levels, cmap='rainbow')
contours = plt.contour(x, y, var_subset, colors='black', linewidths=0.5)
plt.clabel(contours, inline=True, fontsize=4, inline_spacing=2)

# 动态设置标题，包含自动生成的北京时间信息
ax.set_title(f'Geopotential at 500 hPa (m²/s²) - {actual_time_cst.strftime("%Y-%m-%d %H BJT")}', fontsize=10)

# 设置经纬度刻度
plt.xticks(range(90, 141, 10), ['90°E', '100°E', '110°E', '120°E', '130°E', '140°E'], fontsize=8)
plt.yticks(range(10, 61, 10), ['10°N', '20°N', '30°N', '40°N', '50°N', '60°N'], fontsize=8)

# 添加颜色条
cb = plt.colorbar(cs)
plt.show()
