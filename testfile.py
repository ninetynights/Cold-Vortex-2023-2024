import os
import netCDF4 as nc
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

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

def subset_profile_data(data, lat_index, lon_mask):
    """提取剖面数据，直接返回目标纬度剖面"""
    return data[:, lat_index, lon_mask]

# ------------------------- 绘图模块 -------------------------
def plot_vertical_profile_with_barbs(longitudes, pressure_levels, data_d, data_w, u_component, v_component, title, output_dir, filename):
    """绘制垂直速度、散度和风场的经向剖面图（带风向杆和风羽）"""
    X, Y = np.meshgrid(longitudes, pressure_levels)

    fig, ax = plt.subplots(figsize=(12, 6))

    # 绘制散度场等值线填色图
    cf = ax.contourf(X, Y, data_d, levels=20, cmap="coolwarm", extend="both")
    cbar = plt.colorbar(cf, ax=ax, orientation="vertical", label="Divergence (s⁻¹)")

    # 绘制垂直速度的等值线
    cs = ax.contour(X, Y, data_w, levels=np.arange(-0.5, 0.5, 0.05), colors="k", linewidths=0.8)
    ax.clabel(cs, fmt="%1.2f", inline=True, fontsize=8)

    # 稀疏化风场以避免风向杆过于密集（如每隔2个点绘制一次）
    skip = (slice(None, None, 2), slice(None, None, 2))
    u_sparse = u_component[skip]
    v_sparse = v_component[skip]
    X_sparse = X[skip]
    Y_sparse = Y[skip]

    # 在图上叠加风向杆和风羽
    ax.barbs(
        X_sparse, Y_sparse,
        u_sparse, v_sparse,
        length=6,  # 风向杆的长度
        linewidth=0.7,  # 风向杆线宽
        barb_increments=dict(half=2, full=4, flag=20)  # 风羽对应风速的增量
    )

    # 设置图形属性
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Pressure Level (hPa)")
    ax.set_yscale("log")
    ax.invert_yaxis()  # 倒置y轴，低压在顶部

    # 检查输出目录是否存在
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, bbox_inches="tight")
    print(f"Saved plot: {output_path}")
    plt.close()

# ------------------------- 主程序 -------------------------
def main():
    # 配置参数
    file_path = "/Users/momo/Desktop/业务相关/2024高空冷涡降水0827/era5数据+代码/2024.nc"  # 替换为实际路径
    output_dir = "/Users/momo/Desktop/业务相关/2024高空冷涡降水0827/era5数据+代码/figure"  # 输出目录
    time_index = 61  # 指定时间步
    lon_min, lon_max = 117, 123  # 经度范围
    target_latitude = 30.0  # 剖面纬度

    # 加载数据
    nc_file = load_nc_file(file_path)
    actual_time = get_actual_time(nc_file, time_index)

    # 提取经纬度、气压层和变量数据
    lon = nc_file.variables['longitude'][:]
    lat = nc_file.variables['latitude'][:]
    pressure_levels = nc_file.variables['level'][:]

    lon_mask = (lon >= lon_min) & (lon <= lon_max)
    lat_index = np.where(np.isclose(lat, target_latitude))[0][0]

    # 提取散度和垂直速度剖面
    divergence = subset_profile_data(nc_file.variables['d'][time_index], lat_index, lon_mask)
    vertical_velocity = subset_profile_data(nc_file.variables['w'][time_index], lat_index, lon_mask)

    # 提取水平风速分量 u 和 v
    u_component = subset_profile_data(nc_file.variables['u'][time_index], lat_index, lon_mask)
    v_component = subset_profile_data(nc_file.variables['v'][time_index], lat_index, lon_mask)

    # 设置图标题和输出文件名
    title = f"Vertical Profile at {target_latitude}°N - {actual_time.strftime('%Y-%m-%d %H:%M BJT')}"
    filename = f"Vertical_Profile_{target_latitude}N_{actual_time.strftime('%Y%m%d_%H%M')}.png"

    # 调用绘图函数
    plot_vertical_profile_with_barbs(lon[lon_mask], pressure_levels, divergence, vertical_velocity, u_component, v_component, title, output_dir, filename)

if __name__ == "__main__":
    main()