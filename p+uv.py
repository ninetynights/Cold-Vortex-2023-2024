# ---------------------------- 代码文件信息 ---------------------------
# 绘制指定气压层的风场和指定高度场。
# 2024-11-16 修改
# -------------------------------------------------------------------
import os
import netCDF4 as nc
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# ------------------------- 数据加载和处理模块 -------------------------
def load_nc_file(file_path):
    """加载 NetCDF 文件"""
    try:
        return nc.Dataset(file_path, 'r')
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit()

def get_actual_time(nc_file, time_index):
    """从 NetCDF 文件中提取实际时间并转换为北京时间"""
    time_values = nc_file.variables['time'][:]
    time_units = nc_file.variables['time'].units
    base_time_str = time_units.split('since')[1].strip().split('.')[0]
    base_time = datetime.strptime(base_time_str, "%Y-%m-%d %H:%M:%S")
    time_offset = timedelta(hours=int(time_values[time_index]))
    actual_time_utc = base_time + time_offset
    return actual_time_utc + timedelta(hours=8)  # 转为北京时间

def subset_data(data, lon_mask, lat_mask):
    """裁剪数据到指定的经纬度范围"""
    return data[lat_mask, :][:, lon_mask]

# ------------------------- 绘图模块 -------------------------
def plot_height_wind(x, y, height_field, u_wind, v_wind,
                        lon_min, lon_max, lat_min, lat_max, wind_pressure,
                        title, output_dir, filename):
    """绘制高度场和风场叠加图"""
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300, subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

    # 添加地理特征
    ax.coastlines(resolution='10m', linewidth=0.5)
    ax.add_feature(cfeature.LAND, color='lightgray')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.NaturalEarthFeature(
        category="cultural", name="admin_1_states_provinces_lines",
        scale="10m", facecolor="none"), edgecolor="gray", linewidth=0.5)

    # 绘制高度场
    contours = ax.contour(x, y, height_field, colors='black', linewidths=0.8)
    ax.clabel(contours, inline=True, fontsize=6, inline_spacing=2)

    # 绘制风场（风向杆）
    skip = 3
    ax.barbs(x[::skip, ::skip], y[::skip, ::skip], u_wind[::skip, ::skip], v_wind[::skip, ::skip],
             length=3, linewidth=0.6, sizes=dict(emptybarb=0.05, spacing=0.2, height=0.5),
             barb_increments=dict(half=2, full=4, flag=20), color='black')

    # 添加网格线和经纬度标注
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.7, linestyle='--')
    gl.xlocator = plt.MultipleLocator(5)
    gl.ylocator = plt.MultipleLocator(5)
    gl.right_labels = False  # 只显示左侧和底部标签
    gl.top_labels = False
    gl.xlabel_style = {'size': 8}
    gl.ylabel_style = {'size': 8}

    # 设置标题
    ax.set_title(title, fontsize=10)

    # 检查输出目录是否存在，不存在则创建
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    # 保存图像
    plt.savefig(output_path, bbox_inches='tight')
    print(f"Saved plot: {output_path}")
    plt.close()

# ------------------------- 主程序入口 -------------------------
def main():
    # 配置参数
    file_path = "/Users/momo/Desktop/业务相关/2024高空冷涡降水0827/era5数据+代码/2024.nc"
    output_dir = "/Users/momo/Desktop/业务相关/2024高空冷涡降水0827/era5数据+代码/figure"
    time_index = 119
    lon_min, lon_max = 110, 140
    lat_min, lat_max = 20, 50

    # 指定高度层 [100, 200, 300, 500, 700, 850, 925, 1000]
    height_pressure_value = 200  # 高度场使用的压力层 (例如200 hPa)
    wind_pressure_value = 200  # 风场使用的压力层 (例如850 hPa)

    # 加载数据
    nc_file = load_nc_file(file_path)
    actual_time = get_actual_time(nc_file, time_index)

    # 提取经纬度数据
    lon = nc_file.variables['longitude'][:]
    lat = nc_file.variables['latitude'][:]
    lon_mask = (lon >= lon_min) & (lon <= lon_max)
    lat_mask = (lat >= lat_min) & (lat <= lat_max)
    lon_subset = lon[lon_mask]
    lat_subset = lat[lat_mask]
    x, y = np.meshgrid(lon_subset, lat_subset)

    # 提取压力层信息
    pressure_levels = nc_file.variables['level'][:]

    # 获取指定高度层的索引
    height_pressure_level_index = np.where(pressure_levels == height_pressure_value)[0][0]
    wind_pressure_level_index = np.where(pressure_levels == wind_pressure_value)[0][0]

    # 提取高度场数据
    height_field = subset_data(nc_file.variables['z'][time_index, height_pressure_level_index, :, :], lon_mask,
                               lat_mask)

    # 提取风场数据
    u_wind = subset_data(nc_file.variables['u'][time_index, wind_pressure_level_index, :, :], lon_mask, lat_mask)
    v_wind = subset_data(nc_file.variables['v'][time_index, wind_pressure_level_index, :, :], lon_mask, lat_mask)

    # 设置图标题和输出文件名
    title = f'{height_pressure_value} hPa Geopotential Height and {wind_pressure_value} hPa Wind - {actual_time.strftime("%Y-%m-%d %H BJT")}'
    filename = f"{height_pressure_value}hPa_Height_{wind_pressure_value}hPa_Wind_{actual_time.strftime('%Y%m%d_%H')}.png"

    # 调用绘图函数
    plot_height_wind(x, y, height_field, u_wind, v_wind,
                        lon_min, lon_max, lat_min, lat_max,
                        wind_pressure_value, title, output_dir, filename)
if __name__ == "__main__":
    main()