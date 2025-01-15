# ---------------------------- 代码文件信息 ---------------------------
# 输出2024_CAPE.nc和2023_CAPE.nc文件中的时间相关信息。
# 2024-11-17 修改
# -------------------------------------------------------------------

import netCDF4 as nc
from datetime import datetime, timedelta

def load_nc_file(file_path):
    """加载 NetCDF 文件"""
    try:
        return nc.Dataset(file_path, 'r')
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit()

def extract_time_table(nc_file):
    """提取时间索引、世界时间和北京时间"""
    if 'valid_time' in nc_file.variables:
        time_values = nc_file.variables['valid_time'][:]
        time_units = nc_file.variables['valid_time'].units
    else:
        raise KeyError("未找到时间变量")

    base_time_str = time_units.split('since')[1].strip()

    # 如果 base_time_str 中没有时分秒，补充 ":00:00:00"
    if len(base_time_str) == 10:  # 格式为 'YYYY-MM-DD'
        base_time_str += " 00:00:00"

    base_time = datetime.strptime(base_time_str, "%Y-%m-%d %H:%M:%S")

    print(f"{'Time Index':<12}{'UTC Time':<25}{'Beijing Time':<25}")
    print("-" * 60)

    for idx, offset in enumerate(time_values, start=0):
        try:
            actual_time_utc = base_time + timedelta(seconds=int(offset))
            actual_time_bj = actual_time_utc + timedelta(hours=8)

            # 格式化时间为字符串
            utc_str = actual_time_utc.strftime('%Y-%m-%d %H:%M:%S')
            bj_str = actual_time_bj.strftime('%Y-%m-%d %H:%M:%S')

            print(f"{idx:<12}{utc_str:<25}{bj_str:<25}")
        except Exception as e:
            print(f"Error processing time index {idx}: {e}")

# 主程序
file_path = "/Users/momo/Desktop/业务相关/2024高空冷涡降水0827/era5数据+代码/2024_CAPE.nc"
nc_file = load_nc_file(file_path)
extract_time_table(nc_file)