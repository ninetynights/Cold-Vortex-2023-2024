
'''
# 查找所有变量
import netCDF4 as nc

# 打开netCDF文件
file_path = "/Users/momo/Desktop/业务相关/2024高空冷涡降水0827/era5数据+代码/2024.nc"
f = nc.Dataset(file_path, 'r')

# 遍历所有变量
for var_name in f.variables:
    var = f.variables[var_name]
    var_info = {
        'name': var.name,
        'dimensions': var.dimensions,
        'shape': var.shape,
        'units': var.units if 'units' in var.ncattrs() else 'unknown',
        'long_name': var.long_name if 'long_name' in var.ncattrs() else 'unknown'
    }

    # 打印变量的基本信息
    print(f"Variable Name: {var_info['name']}")
    print(f"Dimensions: {var_info['dimensions']}")
    print(f"Shape: {var_info['shape']}")
    print(f"Units: {var_info['units']}")
    print(f"Long Name: {var_info['long_name']}")
    print("-" * 50)
'''


'''
Variable Name: longitude
Dimensions: ('longitude',)
Shape: (281,)
Units: degrees_east
Long Name: longitude
--------------------------------------------------
Variable Name: latitude
Dimensions: ('latitude',)
Shape: (201,)
Units: degrees_north
Long Name: latitude
--------------------------------------------------
Variable Name: level
Dimensions: ('level',)
Shape: (8,)
Units: millibars
Long Name: pressure_level
--------------------------------------------------
Variable Name: time
Dimensions: ('time',)
Shape: (120,)
Units: hours since 1900-01-01 00:00:00.0
Long Name: time
--------------------------------------------------
Variable Name: d
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: s**-1
Long Name: Divergence
--------------------------------------------------
Variable Name: cc
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: (0 - 1)
Long Name: Fraction of cloud cover
--------------------------------------------------
Variable Name: z
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: m**2 s**-2
Long Name: Geopotential
--------------------------------------------------
Variable Name: o3
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: kg kg**-1
Long Name: Ozone mass mixing ratio
--------------------------------------------------
Variable Name: pv
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: K m**2 kg**-1 s**-1
Long Name: Potential vorticity
--------------------------------------------------
Variable Name: r
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: %
Long Name: Relative humidity
--------------------------------------------------
Variable Name: ciwc
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: kg kg**-1
Long Name: Specific cloud ice water content
--------------------------------------------------
Variable Name: clwc
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: kg kg**-1
Long Name: Specific cloud liquid water content
--------------------------------------------------
Variable Name: q
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: kg kg**-1
Long Name: Specific humidity
--------------------------------------------------
Variable Name: crwc
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: kg kg**-1
Long Name: Specific rain water content
--------------------------------------------------
Variable Name: cswc
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: kg kg**-1
Long Name: Specific snow water content
--------------------------------------------------
Variable Name: t
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: K
Long Name: Temperature
--------------------------------------------------
Variable Name: u
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: m s**-1
Long Name: U component of wind
--------------------------------------------------
Variable Name: v
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: m s**-1
Long Name: V component of wind
--------------------------------------------------
Variable Name: w
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: Pa s**-1
Long Name: Vertical velocity
--------------------------------------------------
Variable Name: vo
Dimensions: ('time', 'level', 'latitude', 'longitude')
Shape: (120, 8, 201, 281)
Units: s**-1
Long Name: Vorticity (relative)
--------------------------------------------------
'''


'''
时间索引

*******2024******
48 - 2024_08_27_08
60 - 2024_08_27_20
72 - 2024_08_28_08
84 - 2024_08_28_20

'''


import netCDF4 as nc

# 打开netCDF文件
file_path = "/Users/momo/Desktop/业务相关/2024高空冷涡降水0827/era5数据+代码/2024.nc"
f = nc.Dataset(file_path, 'r')

# 指定要查找的变量名称
var_name = 'level'  # 替换为你想查找的变量名称

# 检查变量是否存在并打印其信息
if var_name in f.variables:
    var = f.variables[var_name]
    var_info = {
        'name': var.name,
        'dimensions': var.dimensions,
        'shape': var.shape,
        'units': var.units if 'units' in var.ncattrs() else 'unknown',
        'long_name': var.long_name if 'long_name' in var.ncattrs() else 'unknown'
    }

    # 打印指定变量的基本信息
    print(f"Variable Name: {var_info['name']}")
    print(f"Dimensions: {var_info['dimensions']}")
    print(f"Shape: {var_info['shape']}")
    print(f"Units: {var_info['units']}")
    print(f"Long Name: {var_info['long_name']}")

    # 打印前10个值
    data_values = var[:10].data if hasattr(var[:10], 'data') else var[:10]
    print("First 10 values:", data_values)
else:
    print(f"The variable '{var_name}' is not present in the dataset.")