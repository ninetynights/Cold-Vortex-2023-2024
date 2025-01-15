# ---------------------------- 代码文件信息 ---------------------------
# 绘制CAPE分布。
# 2024-11-17 修改
# -------------------------------------------------------------------
import os
import netCDF4 as nc
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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
    # 打印所有变量以帮助诊断
    print("NetCDF 文件中的变量：", nc_file.variables.keys())

    # 检查文件中的时间变量
    if 'time' in nc_file.variables:
        time_values = nc_file.variables['time'][:]
        time_units = nc_file.variables['time'].units
    elif 'valid_time' in nc_file.variables:
        time_values = nc_file.variables['valid_time'][:]
        time_units = nc_file.variables['valid_time'].units
    else:
        raise KeyError("未找到时间变量")

    base_time_str = time_units.split('since')[1].strip().split('.')[0]

    # 处理没有时分秒部分的日期时间字符串
    if len(base_time_str) == 10:  # 格式为 '1970-01-01'
        base_time_str += " 00:00:00"  # 添加时分秒
    base_time = datetime.strptime(base_time_str, "%Y-%m-%d %H:%M:%S")

    # 时间偏移量，单位是秒
    time_offset = timedelta(seconds=int(time_values[time_index]))
    actual_time_utc = base_time + time_offset
    return actual_time_utc + timedelta(hours=8)  # 转为北京时间


def subset_data(data, lon_mask, lat_mask):
    """裁剪数据到指定的经纬度范围"""
    return data[lat_mask, :][:, lon_mask]


# ------------------------- 绘图模块 -------------------------
def plot_cape_map(x, y, cape_field, lon_min, lon_max, lat_min, lat_max, title, output_dir, filename):
    """绘制CAPE分布的地图"""
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300, subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

    # 添加地理特征
    ax.coastlines(resolution='10m', linewidth=0.5)
    ax.add_feature(cfeature.LAND, color='lightgray')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.NaturalEarthFeature(
        category="cultural", name="admin_1_states_provinces_lines",
        scale="10m", facecolor="none"), edgecolor="gray", linewidth=0.5)

    # 自定义色标和色阶范围
    cmap_colors = ['#FFFFFF', '#B2D2D9', '#4F9EB6', '#007F7F', '#004C4C']  # 自定义色阶
    cape_bounds = [0, 1000, 1500, 2000, 2500, 3000]  # 色阶区间
    cmap = mcolors.LinearSegmentedColormap.from_list("CAPE", cmap_colors, N=len(cape_bounds) - 1)
    norm = mcolors.BoundaryNorm(cape_bounds, cmap.N)

    # 绘制CAPE分布
    cape_plot = ax.contourf(x, y, cape_field, levels=cape_bounds, cmap=cmap, norm=norm, extend="both")
    cbar = plt.colorbar(cape_plot, ax=ax, orientation="vertical", label="CAPE (J/kg)", shrink=0.8)

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
    file_path = "/Users/momo/Desktop/业务相关/2024高空冷涡降水0827/era5数据+代码/2023_CAPE.nc"
    output_dir = "/Users/momo/Desktop/业务相关/2024高空冷涡降水0827/era5数据+代码/cape/2023_CAPE"
    lon_min, lon_max = 117, 124
    lat_min, lat_max = 25, 35

    # 加载数据
    nc_file = load_nc_file(file_path)

    # 提取经纬度数据
    lon = nc_file.variables['longitude'][:]
    lat = nc_file.variables['latitude'][:]
    lon_mask = (lon >= lon_min) & (lon <= lon_max)
    lat_mask = (lat >= lat_min) & (lat <= lat_max)
    lon_subset = lon[lon_mask]
    lat_subset = lat[lat_mask]
    x, y = np.meshgrid(lon_subset, lat_subset)

    # 循环处理每个 time_index
    for time_index in range(120):  # 从 0 到 119
        actual_time = get_actual_time(nc_file, time_index)

        # 提取CAPE数据
        cape_field = subset_data(nc_file.variables['cape'][time_index, :, :], lon_mask, lat_mask)

        # 绘制CAPE分布
        title = f'CAPE Distribution - {actual_time.strftime("%Y-%m-%d %H:%M:%S")}'
        filename = f"CAPE_{actual_time.strftime('%Y%m%d_%H')}.png"
        plot_cape_map(x, y, cape_field, lon_min, lon_max, lat_min, lat_max, title, output_dir, filename)


if __name__ == "__main__":
    main()
