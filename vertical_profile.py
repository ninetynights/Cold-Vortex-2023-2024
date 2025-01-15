# ---------------------------- 代码文件信息 ---------------------------
# 绘制某一纬度剖面的风场，散度和垂直速度。
# 2024-11-18 修改
# -------------------------------------------------------------------



import os
import netCDF4 as nc
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt


# ------------------------- 配置参数 -------------------------
CONFIG = {
    "file_path": "/Users/momo/Desktop/业务相关/2024高空冷涡降水0827/era5数据+代码/2023.nc",  # 数据路径
    "output_dir": "/Users/momo/Desktop/业务相关/2024高空冷涡降水0827/era5数据+代码/figure/2023_垂直剖面/30N",  # 输出目录
    "time_range": range(0, 64),  # 时间范围
    "lon_range": (117, 123),  # 经度范围
    "target_latitude": 30.0,  # 剖面纬度
    "wind_barb_density": 2,  # 风向杆稀疏密度
}


# ------------------------- 工具函数 -------------------------
def load_nc_file(file_path):
    """加载 NetCDF 文件"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")
    return nc.Dataset(file_path, 'r')


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


# ------------------------- 绘图函数 -------------------------
def plot_vertical_profile_with_barbs(
    longitudes, pressure_levels, data_d, data_w, u_component, v_component, title, output_path, density=2
):
    """绘制垂直速度、散度和风场的经向剖面图"""
    X, Y = np.meshgrid(longitudes, pressure_levels)

    fig, ax = plt.subplots(figsize=(12, 6))

    # 绘制散度场等值线填色图
    cf = ax.contourf(X, Y, data_d, levels=20, cmap="coolwarm", extend="both")
    cbar = plt.colorbar(cf, ax=ax, orientation="vertical", label="Divergence (s⁻¹)")

    # 绘制垂直速度的等值线
    cs = ax.contour(X, Y, data_w, levels=np.arange(-0.5, 0.5, 0.05), colors="k", linewidths=0.8)
    ax.clabel(cs, fmt="%1.2f", inline=True, fontsize=8)

    # 添加风向杆
    for idx, level in enumerate(pressure_levels):
        X_barbs = X[idx, :]
        Y_barbs = Y[idx, :]
        u_barbs = u_component[idx, :]
        v_barbs = v_component[idx, :]

        # 稀疏化风向杆
        skip = slice(None, None, density)
        ax.barbs(
            X_barbs[skip], Y_barbs[skip],
            u_barbs[skip], v_barbs[skip],
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

    # 动态设置纵坐标为实际气压层
    ax.set_yticks(pressure_levels)
    ax.set_yticklabels([f"{int(level)} hPa" for level in pressure_levels])

    # 保存图像
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Saved plot: {output_path}")


# ------------------------- 主程序 -------------------------
def main():
    # 读取配置参数
    file_path = CONFIG["file_path"]
    output_dir = CONFIG["output_dir"]
    time_range = CONFIG["time_range"]
    lon_min, lon_max = CONFIG["lon_range"]
    target_latitude = CONFIG["target_latitude"]
    density = CONFIG["wind_barb_density"]

    # 加载数据
    nc_file = load_nc_file(file_path)

    # 提取经纬度和气压层信息
    lon = nc_file.variables['longitude'][:]
    lat = nc_file.variables['latitude'][:]
    pressure_levels = nc_file.variables['level'][:]

    # 筛选经纬度范围
    lon_mask = (lon >= lon_min) & (lon <= lon_max)
    lat_index = np.where(np.isclose(lat, target_latitude))[0][0]

    # 循环绘制指定时间范围内的图像
    for time_index in time_range:
        actual_time = get_actual_time(nc_file, time_index)

        # 提取变量剖面
        divergence = subset_profile_data(nc_file.variables['d'][time_index], lat_index, lon_mask)
        vertical_velocity = subset_profile_data(nc_file.variables['w'][time_index], lat_index, lon_mask)
        u_component = subset_profile_data(nc_file.variables['u'][time_index], lat_index, lon_mask)
        v_component = subset_profile_data(nc_file.variables['v'][time_index], lat_index, lon_mask)

        # 设置标题和输出路径
        title = f"Vertical Profile at {target_latitude}°N - {actual_time.strftime('%Y-%m-%d %H:%M BJT')}"
        filename = f"Vertical_Profile_{target_latitude}N_{actual_time.strftime('%Y%m%d_%H%M')}.png"
        output_path = os.path.join(output_dir, filename)

        # 绘图
        plot_vertical_profile_with_barbs(
            lon[lon_mask], pressure_levels, divergence, vertical_velocity,
            u_component, v_component, title, output_path, density=density
        )


if __name__ == "__main__":
    main()