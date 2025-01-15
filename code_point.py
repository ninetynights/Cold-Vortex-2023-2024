'''
对流有效位能是天气诊断中，日常使用的大气能量条件的诊断条件，一般micaps中各探空站的站点数据可以通过内置的按钮直接展示。
不过这些探空站的分布比较不均匀，下面我们使用metpy来计算ERA5再分析资料中的格点对流有效位能，并将其实现可视化。
由于cape值较大的时候往往在下雨前，所以我们选取一个已经知道发生了大暴雨的过程之前的一次数据，用以求出一个比较大的cape值。
当然，对流有效位能只是一个潜势，其与降水强度没有绝对关系。
要求取对流有效位能，主要依靠MetPy这个库包。其中calc模块，支持我们对格点数据实现带单位的物理量计算。
ERA5再分析资料中，我们能直接得到的物理量有气温t、比湿q、相对湿度r。所以我们就只能从这些基本物理量来计算出对流有效位能。
Metpy直接计算对流有效位能的函数只是计算了具体的cape值，而对流有效位能本质是包裹面积大小，所以需要另外计算状态曲线和层结曲线的面积。计算状态曲线的函数为parcel_profile。该函数的输入参数为：
1、pressure (pint.Quantity) – 气压层，大小降序
2、temperature (pint.Quantity) – 温度
3、dewpoint (pint.Quantity) – 露点温度
那么又引出露点的求取，Metpy也提供了从温度和比湿计算露点的函数dewpoint_from_specific_humidity。该函数的输入参数为：
1、pressure (pint.Quantity) – 气压层，大小降序
2、temperature (pint.Quantity) – 温度
3、specific_humidity (pint.Quantity) –比湿
'''

import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import metpy
import metpy.calc as mcalc
from metpy.units import units
from metpy.plots import SkewT
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

#导入再分析文件
file=r'/Users/momo/Desktop/业务相关/2024高空冷涡降水0827/era5数据+代码/2024.nc'
ds=xr.open_dataset(file)

#我们只求取世界时7-13 12:00的数据,具体地点为108.5°E、30°N
ds=ds.sel(time='2024-08-27T14:00:00.000000000',longitude=120.5,latitude=30.5,level=slice(1000,100))
#print(ds)
print(ds['level'])
print(ds['time'])

#读取温度数据，并将开氏度转换为摄氏度
T=(ds['t']*units('K')).metpy.convert_units(units('degC'))
#读取比湿数据，将单位转化为常用比湿单位
Q=ds['q']*1000*units('g/kg')
#读取气压层数据，将单位设置为百帕
level=ds['level']*units('hPa')
#计算露点温度，计算结果为摄氏度
Td=mcalc.dewpoint_from_specific_humidity(level,T,Q)
#计算状态曲线温度，单位为摄氏度
State_Curve=mcalc.parcel_profile(level,T[0],Td[0]).metpy.convert_units(units('degC'))

print(mcalc.cape_cin(level,T,Td,State_Curve))

# 开始绘制图像，调用metpy提供的专门温度对数压力图方法
fig = plt.figure(figsize=(5,5),dpi=500)
skew = SkewT(fig, rotation=45)
# 绘制层结曲线
skew.plot(level, T, 'r',lw=1)
# 绘制露点曲线
skew.plot(level, Td, 'g',lw=1)
# 绘制状态曲线
skew.plot(level,State_Curve,'k', linewidth=1)
# 绘制cape阴影
skew.shade_cape(level,T,State_Curve)
skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-40, 60)
# 绘制底图上的干绝热线
skew.plot_dry_adiabats(lw=0.5)
# 绘制底图上的湿绝热线
skew.plot_moist_adiabats(lw=0.5)
# 绘制底图上的等比湿线
skew.plot_mixing_lines(lw=0.5)
cape_text=fig.text(0.2,0.7,'Cape:'+str(mcalc.cape_cin(level,T,Td,State_Curve)[0].magnitude.round(1)))
cape_text.set_bbox({'fc':'w','ec':'gray'})