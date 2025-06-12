#!/usr/bin/env python
# coding: utf-8

# In[393]:


import xarray as xr
import math
import metpy.plots as mpplots
import numpy as np
import pygrib
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.gridspec as gridspec
from metpy.units import units
import matplotlib.colors
import scipy.ndimage as ndimage
import geopandas as gpd
from datetime import datetime
import matplotlib.offsetbox as offsetbox
from cartopy.feature import ShapelyFeature
import shapefile
import matplotlib.patches as patches
from metpy.plots import colortables
from shapely.geometry import shape
from metpy.interpolate import (interpolate_to_grid, remove_nan_observations,
                               remove_repeat_coordinates)
from datetime import datetime, timedelta

logo_path = '/Users/tejedawx/Documents/TSRD Fondo Negro-Blanco.png'
save_path = '/Users/tejedawx/IMAGES'


# In[394]:


prob_file_1 = 'Model_Data/18Z/href.t18z.pr.prob.f10.grib2'
prob_file_2 = 'Model_Data/18Z/href.t18z.pr.prob.f11.grib2'
prob_file_3 = 'Model_Data/18Z/href.t18z.pr.prob.f12.grib2'
prob_file_4 = 'Model_Data/18Z/href.t18z.pr.prob.f13.grib2'
prob_file_5 = 'Model_Data/18Z/href.t18z.pr.prob.f14.grib2'
prob_file_6 = 'Model_Data/18Z/href.t18z.pr.prob.f15.grib2'
prob_file1 = 'Model_Data/18Z/href.t18z.pr.prob.f16.grib2'
prob_file2 = 'Model_Data/18Z/href.t18z.pr.prob.f17.grib2'
prob_file3 = 'Model_Data/18Z/href.t18z.pr.prob.f18.grib2'
prob_file4 = 'Model_Data/18Z/href.t18z.pr.prob.f19.grib2'
prob_file5 = 'Model_Data/18Z/href.t18z.pr.prob.f20.grib2'
prob_file6 = 'Model_Data/18Z/href.t18z.pr.prob.f21.grib2'
prob_file7 = 'Model_Data/18Z/href.t18z.pr.prob.f22.grib2'
prob_file8 = 'Model_Data/18Z/href.t18z.pr.prob.f23.grib2'
prob_file9 = 'Model_Data/18Z/href.t18z.pr.prob.f24.grib2'
prob_file10 = 'Model_Data/18Z/href.t18z.pr.prob.f25.grib2'
prob_file11 = 'Model_Data/18Z/href.t18z.pr.prob.f26.grib2'
prob_file12 = 'Model_Data/18Z/href.t18z.pr.prob.f27.grib2'
prob_file13 = 'Model_Data/18Z/href.t18z.pr.prob.f28.grib2'
prob_file14 = 'Model_Data/18Z/href.t18z.pr.prob.f29.grib2'
prob_file15 = 'Model_Data/18Z/href.t18z.pr.prob.f30.grib2'
prob_file16 = 'Model_Data/18Z/href.t18z.pr.prob.f31.grib2'
prob_file17 = 'Model_Data/18Z/href.t18z.pr.prob.f32.grib2'
prob_file18 = 'Model_Data/18Z/href.t18z.pr.prob.f33.grib2'


prob_1  = pygrib.open(prob_file_1)
prob_2  = pygrib.open(prob_file_2)
prob_3  = pygrib.open(prob_file_3)
prob_4  = pygrib.open(prob_file_4)
prob_5  = pygrib.open(prob_file_5)
prob_6  = pygrib.open(prob_file_6)

prob1  = pygrib.open(prob_file1)
prob2  = pygrib.open(prob_file2)
prob3  = pygrib.open(prob_file3)
prob4  = pygrib.open(prob_file4)
prob5  = pygrib.open(prob_file5)
prob6  = pygrib.open(prob_file6)
prob7  = pygrib.open(prob_file7)
prob8  = pygrib.open(prob_file8)
prob9  = pygrib.open(prob_file9)
prob10 = pygrib.open(prob_file10)
prob11 = pygrib.open(prob_file11)
prob12 = pygrib.open(prob_file12)
prob13 = pygrib.open(prob_file13)
prob14 = pygrib.open(prob_file14)
prob15 = pygrib.open(prob_file15)
prob16 = pygrib.open(prob_file16)
prob17 = pygrib.open(prob_file17)
prob18 = pygrib.open(prob_file18)


lprob_1 = prob_1.select(name="Lightning")[0]
lprob_2 = prob_2.select(name="Lightning")[0]
lprob_3 = prob_3.select(name="Lightning")[0]
lprob_4 = prob_4.select(name="Lightning")[0]
lprob_5 = prob_5.select(name="Lightning")[0]
lprob_6 = prob_6.select(name="Lightning")[0]

lprob1 = prob1.select(name="Lightning")[0]
lprob2 = prob2.select(name="Lightning")[0]
lprob3 = prob3.select(name="Lightning")[0]
lprob4 = prob4.select(name="Lightning")[0]
lprob5 = prob5.select(name="Lightning")[0]
lprob6 = prob6.select(name="Lightning")[0]
lprob7 = prob7.select(name="Lightning")[0]
lprob8 = prob8.select(name="Lightning")[0]
lprob9 = prob9.select(name="Lightning")[0]
lprob10 = prob10.select(name="Lightning")[0]
lprob11 = prob11.select(name="Lightning")[0]
lprob12 = prob12.select(name="Lightning")[0]
lprob13 = prob13.select(name="Lightning")[0]
lprob14 = prob14.select(name="Lightning")[0]
lprob15 = prob15.select(name="Lightning")[0]
lprob16 = prob16.select(name="Lightning")[0]
lprob17 = prob17.select(name="Lightning")[0]
lprob18 = prob18.select(name="Lightning")[0]

light_value_1 = lprob_1.values
light_value_2 = lprob_2.values
light_value_3 = lprob_3.values
light_value_4 = lprob_4.values
light_value_5 = lprob_5.values
light_value_6 = lprob_6.values

light_value1 = lprob1.values
light_value2 = lprob2.values
light_value3 = lprob3.values
light_value4 = lprob4.values
light_value5 = lprob5.values
light_value6 = lprob6.values
light_value7 = lprob7.values
light_value8 = lprob8.values
light_value9 = lprob9.values
light_value10 = lprob10.values
light_value11 = lprob11.values
light_value12 = lprob12.values
light_value13 = lprob13.values
light_value14 = lprob14.values
light_value15 = lprob15.values
light_value16 = lprob16.values
light_value17 = lprob17.values
light_value18 = lprob18.values

light_value1_v = ndimage.gaussian_filter(light_value_1, sigma=1.5, order=0)
light_value2_v = ndimage.gaussian_filter(light_value_2, sigma=1.5, order=0)
light_value3_v = ndimage.gaussian_filter(light_value_3, sigma=1.5, order=0)
light_value4_v = ndimage.gaussian_filter(light_value_4, sigma=1.5, order=0)
light_value5_v = ndimage.gaussian_filter(light_value_5, sigma=1.5, order=0)
light_value6_v = ndimage.gaussian_filter(light_value_6, sigma=1.5, order=0)

light_value1v = ndimage.gaussian_filter(light_value1, sigma=1.5, order=0)
light_value2v = ndimage.gaussian_filter(light_value2, sigma=1.5, order=0)
light_value3v = ndimage.gaussian_filter(light_value3, sigma=1.5, order=0)
light_value4v = ndimage.gaussian_filter(light_value4, sigma=1.5, order=0)
light_value5v = ndimage.gaussian_filter(light_value5, sigma=1.5, order=0)
light_value6v = ndimage.gaussian_filter(light_value6, sigma=1.5, order=0)
light_value7v = ndimage.gaussian_filter(light_value7, sigma=1.5, order=0)
light_value8v = ndimage.gaussian_filter(light_value8, sigma=1.5, order=0)
light_value9v = ndimage.gaussian_filter(light_value9, sigma=1.5, order=0)
light_value10v = ndimage.gaussian_filter(light_value10, sigma=1.5, order=0)
light_value11v = ndimage.gaussian_filter(light_value11, sigma=1.5, order=0)
light_value12v = ndimage.gaussian_filter(light_value12, sigma=1.5, order=0)
light_value13v = ndimage.gaussian_filter(light_value13, sigma=1.5, order=0)
light_value14v = ndimage.gaussian_filter(light_value14, sigma=1.5, order=0)
light_value15v = ndimage.gaussian_filter(light_value15, sigma=1.5, order=0)
light_value16v = ndimage.gaussian_filter(light_value16, sigma=1.5, order=0)
light_value17v = ndimage.gaussian_filter(light_value17, sigma=1.5, order=0)
light_value18v = ndimage.gaussian_filter(light_value18, sigma=1.5, order=0)


print('-----------------------------------------------------------------------------------')
print(lprob1)
print('-----------------------------------------------------------------------------------')

max_lightning = np.maximum.reduce([
light_value1_v,
light_value2_v,
light_value3_v,
light_value4_v,
light_value5_v,
light_value6_v,
light_value1v , 
light_value2v , 
light_value3v , 
light_value4v , 
light_value5v , 
light_value6v , 
light_value7v , 
light_value8v , 
light_value9v , 
light_value10v, 
light_value11v, 
light_value12v,
light_value13v, 
light_value14v, 
light_value15v, 
light_value16v, 
light_value17v, 
light_value18v])

max_light_int = ndimage.gaussian_filter(max_lightning, sigma=1.5, order=0)
light_L = (max_light_int/40)
light_L_P = ((light_L-1)/1.5)*100


# In[395]:


EAS_file_1 = 'Model_Data/18Z/href.t18z.pr.eas.f10.grib2'
EAS_file_2 = 'Model_Data/18Z/href.t18z.pr.eas.f11.grib2'
EAS_file_3 = 'Model_Data/18Z/href.t18z.pr.eas.f12.grib2'
EAS_file_4 = 'Model_Data/18Z/href.t18z.pr.eas.f13.grib2'
EAS_file_5 = 'Model_Data/18Z/href.t18z.pr.eas.f14.grib2'
EAS_file_6 = 'Model_Data/18Z/href.t18z.pr.eas.f15.grib2'

EAS_file1 = 'Model_Data/18Z/href.t18z.pr.eas.f16.grib2'
EAS_file2 = 'Model_Data/18Z/href.t18z.pr.eas.f17.grib2'
EAS_file3 = 'Model_Data/18Z/href.t18z.pr.eas.f18.grib2'
EAS_file4 = 'Model_Data/18Z/href.t18z.pr.eas.f19.grib2'
EAS_file5 = 'Model_Data/18Z/href.t18z.pr.eas.f20.grib2'
EAS_file6 = 'Model_Data/18Z/href.t18z.pr.eas.f21.grib2'
EAS_file7 = 'Model_Data/18Z/href.t18z.pr.eas.f22.grib2'
EAS_file8 = 'Model_Data/18Z/href.t18z.pr.eas.f23.grib2'
EAS_file9 = 'Model_Data/18Z/href.t18z.pr.eas.f24.grib2'
EAS_file10 = 'Model_Data/18Z/href.t18z.pr.eas.f25.grib2'
EAS_file11 = 'Model_Data/18Z/href.t18z.pr.eas.f26.grib2'
EAS_file12 = 'Model_Data/18Z/href.t18z.pr.eas.f27.grib2'
EAS_file13 = 'Model_Data/18Z/href.t18z.pr.eas.f28.grib2'
EAS_file14 = 'Model_Data/18Z/href.t18z.pr.eas.f29.grib2'
EAS_file15 = 'Model_Data/18Z/href.t18z.pr.eas.f30.grib2'
EAS_file16 = 'Model_Data/18Z/href.t18z.pr.eas.f31.grib2'
EAS_file17 = 'Model_Data/18Z/href.t18z.pr.eas.f32.grib2'
EAS_file18 = 'Model_Data/18Z/href.t18z.pr.eas.f33.grib2'

EAS_1 = pygrib.open(EAS_file_1)
EAS_2 = pygrib.open(EAS_file_2)
EAS_3 = pygrib.open(EAS_file_3)
EAS_4 = pygrib.open(EAS_file_4)
EAS_5 = pygrib.open(EAS_file_5)
EAS_6 = pygrib.open(EAS_file_6)
EAS1 = pygrib.open(EAS_file1)
EAS2 = pygrib.open(EAS_file2)
EAS3 = pygrib.open(EAS_file3)
EAS4 = pygrib.open(EAS_file4)
EAS5 = pygrib.open(EAS_file5)
EAS6 = pygrib.open(EAS_file6)
EAS7 = pygrib.open(EAS_file7)
EAS8 = pygrib.open(EAS_file8)
EAS9 = pygrib.open(EAS_file9)
EAS10 = pygrib.open(EAS_file10)
EAS11 = pygrib.open(EAS_file11)
EAS12 = pygrib.open(EAS_file12)
EAS13 = pygrib.open(EAS_file13)
EAS14 = pygrib.open(EAS_file14)
EAS15 = pygrib.open(EAS_file15)
EAS16 = pygrib.open(EAS_file16)
EAS17 = pygrib.open(EAS_file17)
EAS18 = pygrib.open(EAS_file18)

EAS2p5__1 = EAS_1.select(name='Total Precipitation')[0]
EAS2p5__2 = EAS_2.select(name='Total Precipitation')[0]
EAS2p5__3 = EAS_3.select(name='Total Precipitation')[0]
EAS2p5__4 = EAS_4.select(name='Total Precipitation')[0]
EAS2p5__5 = EAS_5.select(name='Total Precipitation')[0]
EAS2p5__6 = EAS_6.select(name='Total Precipitation')[0]
EAS2p5_1 = EAS1.select(name='Total Precipitation')[0]
EAS2p5_2 = EAS2.select(name='Total Precipitation')[0]
EAS2p5_3 = EAS3.select(name='Total Precipitation')[0]
EAS2p5_4 = EAS4.select(name='Total Precipitation')[0]
EAS2p5_5 = EAS5.select(name='Total Precipitation')[0]
EAS2p5_6 = EAS6.select(name='Total Precipitation')[0]
EAS2p5_7 = EAS7.select(name='Total Precipitation')[0]
EAS2p5_8 = EAS8.select(name='Total Precipitation')[0]
EAS2p5_9 = EAS9.select(name='Total Precipitation')[0]
EAS2p5_10 = EAS10.select(name='Total Precipitation')[0]
EAS2p5_11 = EAS11.select(name='Total Precipitation')[0]
EAS2p5_12 = EAS12.select(name='Total Precipitation')[0]                                                        
EAS2p5_13 = EAS13.select(name='Total Precipitation')[0]
EAS2p5_14 = EAS14.select(name='Total Precipitation')[0]
EAS2p5_15 = EAS15.select(name='Total Precipitation')[0]                                                         
EAS2p5_16 = EAS16.select(name='Total Precipitation')[0]
EAS2p5_17 = EAS17.select(name='Total Precipitation')[0]
EAS2p5_18 = EAS18.select(name='Total Precipitation')[0]

EAS__1v =  EAS2p5__1.values
EAS__2v =  EAS2p5__2.values
EAS__3v =  EAS2p5__3.values
EAS__4v  = EAS2p5__4.values
EAS__5v  = EAS2p5__5.values
EAS__6v  = EAS2p5__6.values
EAS_1v =  EAS2p5_1.values
EAS_2v =  EAS2p5_2.values
EAS_3v =  EAS2p5_3.values
EAS_4v  = EAS2p5_4.values
EAS_5v  = EAS2p5_5.values
EAS_6v  = EAS2p5_6.values
EAS_7v  = EAS2p5_7.values
EAS_8v  = EAS2p5_8.values
EAS_9v  = EAS2p5_9.values
EAS_10v = EAS2p5_10.values
EAS_11v = EAS2p5_11.values
EAS_12v = EAS2p5_12.values
EAS_13v = EAS2p5_13.values
EAS_14v = EAS2p5_14.values
EAS_15v = EAS2p5_15.values
EAS_16v = EAS2p5_16.values
EAS_17v = EAS2p5_17.values
EAS_18v = EAS2p5_18.values

print(EAS2p5_18)

max_EASrain = np.maximum.reduce([
EAS__1v,
EAS__2v,
EAS__3v,
EAS__4v,
EAS__5v,
EAS__6v,
EAS_1v , 
EAS_2v , 
EAS_3v , 
EAS_4v , 
EAS_5v , 
EAS_6v , 
EAS_7v , 
EAS_8v , 
EAS_9v , 
EAS_10v, 
EAS_11v, 
EAS_12v,
EAS_13v, 
EAS_14v, 
EAS_15v, 
EAS_16v, 
EAS_17v, 
EAS_18v])


# In[396]:


#EAS12__1 = EAS_1.select(name='Total Precipitation')[2]
#EAS12__2 = EAS_2.select(name='Total Precipitation')[2]
EAS12__3 = EAS_3.select(name='Total Precipitation')[5]
#EAS12__4 = EAS_4.select(name='Total Precipitation')[5]
#EAS12__5 = EAS_5.select(name='Total Precipitation')[5]
EAS12__6 = EAS_6.select(name='Total Precipitation')[5]
#EAS12_1 = EAS1.select(name='Total Precipitation')[5]
#EAS12_2 = EAS2.select(name='Total Precipitation')[5]
EAS12_3 = EAS3.select(name='Total Precipitation')[5]
#EAS12_4 = EAS4.select(name='Total Precipitation')[5]
#EAS12_5 = EAS5.select(name='Total Precipitation')[5]
EAS12_6 = EAS6.select(name='Total Precipitation')[5]
#EAS12_7 = EAS7.select(name='Total Precipitation')[5]
#EAS12_8 = EAS8.select(name='Total Precipitation')[5]
EAS12_9 = EAS9.select(name='Total Precipitation')[5]
#EAS12_10 = EAS10.select(name='Total Precipitation')[5]
#EAS12_11 = EAS11.select(name='Total Precipitation')[5]
EAS12_12 = EAS12.select(name='Total Precipitation')[5]                                                        
#EAS12_13 = EAS13.select(name='Total Precipitation')[5]
#EAS12_14 = EAS14.select(name='Total Precipitation')[5]
EAS12_15 = EAS15.select(name='Total Precipitation')[5]                                                         
#EAS12_16 = EAS16.select(name='Total Precipitation')[5]
#EAS12_17 = EAS17.select(name='Total Precipitation')[5]
EAS12_18 = EAS18.select(name='Total Precipitation')[5]

#EAS12__1v =  EAS12__1.values
#EAS12__2v =  EAS12__2.values
EAS12__3v =  EAS12__3.values
#EAS12__4v  = EAS12__4.values
#EAS12__5v  = EAS12__5.values
EAS12__6v  = EAS12__6.values
#EAS12_1v =  EAS12_1.values
#EAS12_2v =  EAS12_2.values
EAS12_3v =  EAS12_3.values
#EAS12_4v  = EAS12_4.values
#EAS12_5v  = EAS12_5.values
EAS12_6v  = EAS12_6.values
#EAS12_7v  = EAS12_7.values
#EAS12_8v  = EAS12_8.values
EAS12_9v  = EAS12_9.values
#EAS12_10v = EAS12_10.values
#EAS12_11v = EAS12_11.values
EAS12_12v = EAS12_12.values
#EAS12_13v = EAS12_13.values
#EAS12_14v = EAS12_14.values
EAS12_15v = EAS12_15.values
#EAS12_16v = EAS12_16.values
#EAS12_17v = EAS12_17.values
EAS12_18v = EAS12_18.values

print(EAS12_18)

#EAS12__1 = EAS_1.select(name='Total Precipitation')[2]
#EAS12__2 = EAS_2.select(name='Total Precipitation')[2]
#EAS12__3 = EAS_3.select(name='Total Precipitation')[5]
#EAS12__4 = EAS_4.select(name='Total Precipitation')[5]
#EAS12__5 = EAS_5.select(name='Total Precipitation')[5]
EAS25__6 = EAS_6.select(name='Total Precipitation')[9]
#EAS12_1 = EAS1.select(name='Total Precipitation')[5]
#EAS12_2 = EAS2.select(name='Total Precipitation')[5]
#EAS12_3 = EAS3.select(name='Total Precipitation')[5]
#EAS12_4 = EAS4.select(name='Total Precipitation')[5]
#EAS12_5 = EAS5.select(name='Total Precipitation')[5]
EAS25_6 = EAS6.select(name='Total Precipitation')[9]
#EAS12_7 = EAS7.select(name='Total Precipitation')[5]
#EAS12_8 = EAS8.select(name='Total Precipitation')[5]
#EAS12_9 = EAS9.select(name='Total Precipitation')[5]
#EAS12_10 = EAS10.select(name='Total Precipitation')[5]
#EAS12_11 = EAS11.select(name='Total Precipitation')[5]
EAS25_12 = EAS12.select(name='Total Precipitation')[9]                                                        
#EAS12_13 = EAS13.select(name='Total Precipitation')[5]
#EAS12_14 = EAS14.select(name='Total Precipitation')[5]
#EAS12_15 = EAS15.select(name='Total Precipitation')[5]                                                         
#EAS12_16 = EAS16.select(name='Total Precipitation')[5]
#EAS12_17 = EAS17.select(name='Total Precipitation')[5]
EAS25_18 = EAS18.select(name='Total Precipitation')[9]

#EAS12__1v =  EAS12__1.values
#EAS12__2v =  EAS12__2.values
#EAS25__3v =  EAS25__3.values
#EAS12__4v  = EAS12__4.values
#EAS12__5v  = EAS12__5.values
EAS25__6v  = EAS25__6.values
#EAS12_1v =  EAS12_1.values
#EAS12_2v =  EAS12_2.values
#EAS25_3v =  EAS25_3.values
#EAS12_4v  = EAS12_4.values
#EAS12_5v  = EAS12_5.values
EAS25_6v  = EAS25_6.values
#EAS12_7v  = EAS12_7.values
#EAS12_8v  = EAS12_8.values
#EAS25_9v  = EAS25_9.values
#EAS12_10v = EAS12_10.values
#EAS12_11v = EAS12_11.values
EAS25_12v = EAS25_12.values
#EAS12_13v = EAS12_13.values
#EAS12_14v = EAS12_14.values
#EAS25_15v = EAS25_15.values
#EAS12_16v = EAS12_16.values
#EAS12_17v = EAS12_17.values
EAS25_18v = EAS25_18.values

print(EAS25_18)

max_EAS12rain = np.maximum.reduce([

EAS12__3v,
EAS12__6v,
EAS12_3v , 
EAS12_6v , 
EAS12_9v , 
EAS12_12v,
EAS12_15v, 
EAS12_18v])

max_EAS25rain = np.maximum.reduce([

EAS25__6v,
EAS25_6v ,  
EAS25_12v, 
EAS25_18v])


# In[397]:


lats, lons = lprob_1.latlons()
lats.shape, lats.min(), lats.max(), lons.shape, lons.min(), lons.max()

cLat = (lats.min() + lats.max()) / 2
cLon = (lons.min() + lons.max()) / 2

map_crs = ccrs.LambertConformal(central_longitude=cLon, central_latitude=cLat, standard_parallels=(30,60))

data_crs= ccrs.PlateCarree()


# In[398]:


import pygrib
from datetime import datetime, timedelta

# Suponiendo que EAS_file_1 es la ruta del primer archivo
EAS_file_1 = 'Model_Data/18Z/href.t18z.pr.prob.f10.grib2'
EAS_1 = pygrib.open(EAS_file_1)

# Obtener el primer mensaje (campo) en el archivo
primer_mensaje = EAS_1.read(1)[0]

# Extraer información de la fecha y la hora
fecha_info = primer_mensaje.validityDate
hora_info = primer_mensaje.dataTime  # Usar dataTime en lugar de dateTime

# Crear objetos datetime para formatear la fecha y la hora
fecha_datetime = datetime.strptime(str(fecha_info), '%Y%m%d')
hora_datetime = datetime.strptime(f'{hora_info:04d}', '%H%M')

# Obtener la fecha del día anterior
fecha_dia_anterior = fecha_datetime - timedelta(days=1)

# Obtener la fecha del día siguente
fecha_dia_siguiente = fecha_datetime - timedelta(days=-1)

# Definir nombres de días y meses en español
dias_semana_espanol = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
meses_espanol = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# Formatear la fecha en español para el día anterior
fecha_formateada_dia_anterior = fecha_dia_anterior.strftime(f"{dias_semana_espanol[fecha_dia_anterior.weekday()]} %d de {meses_espanol[fecha_dia_anterior.month - 1]} del %Y")

# Formatear la fecha en español para el día anterior
fecha_formateada_dia_siguiente = fecha_dia_siguiente.strftime(f"{dias_semana_espanol[fecha_dia_siguiente.weekday()]} %d de {meses_espanol[fecha_dia_siguiente.month - 1]} del %Y")

# Formatear la fecha en español
fecha_formateada = fecha_datetime.strftime(f"{dias_semana_espanol[fecha_datetime.weekday()]} %d de {meses_espanol[fecha_datetime.month - 1]} del %Y")
# Formatear la hora en formato "18z"
hora_formateada = f"{hora_datetime.hour:02d}Z"

# Imprimir los resultados
print(f"Fecha del día anterior: {fecha_formateada_dia_anterior}")
print(f"Fecha: {fecha_formateada}, Hora: {hora_formateada}")
print(f"Fecha del dia siguente: {fecha_formateada_dia_siguiente}")

# Cerrar el archivo
EAS_1.close()


# In[399]:


fig = plt.figure (1,figsize=(20,22))
ax=plt.subplot(1,1,1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space
ax.set_extent ([-67.5, -74.5, 17.25, 20.5], data_crs)
ax.add_feature(cfeature.COASTLINE, linewidth=2)
ax.add_feature(cfeature.BORDERS, linewidth=2)


colormap = matplotlib.colors.ListedColormap(['#00c700','#ffff00','#ff8f00','#cc3300'])

clev = [15, 20, 40, 60, 80, 100]

cf = ax.contourf(lons,lats, max_EAS25rain, clev, extend='neither', cmap='viridis', transform=data_crs, 
                 norm=plt.Normalize(1, 100))

cb = plt.colorbar(cf, ax=ax, orientation='horizontal',pad=0.05, extendrect='true', ticks=clev)
cb.set_label(r'PORCIENTO', size='xx-large')

cs1 = ax.contour(lons, lats, max_EAS25rain, clev, colors='black',
              linestyles='solid', transform=data_crs)
ax.set_title(f'PROBABILIDAD DE AGUACEROS TARDE & NOCHE | 12PM - 12AM \n{fecha_formateada} | DATA: {hora_formateada}', fontsize=22)
ax.clabel(cs1, fmt='%d', fontsize=20)

# PR COUNTIES SHAPEFILES
shapefile1_path = 'shp/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp'
gdf1 = gpd.read_file(shapefile1_path)
county_PR = ShapelyFeature(gdf1['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_PR)

shapefile2_path = 'shp/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_RD)

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

plt.show()
plt.show()

fig.savefig(f'{save_path}/D1n_TSRD_PROB-AGUAC_TN_RD.png', bbox_inches='tight', dpi=300)


# In[400]:


fig = plt.figure (1,figsize=(20,22))
ax=plt.subplot(1,1,1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space
ax.set_extent ([-67.5, -74.5, 17.25, 20.5], data_crs)
ax.add_feature(cfeature.COASTLINE, linewidth=2)
ax.add_feature(cfeature.BORDERS, linewidth=2)


colormap = matplotlib.colors.ListedColormap(['#00c700','#ffff00','#ff8f00','#cc3300'])

clev = [15, 20, 40, 60, 80, 100]

cf = ax.contourf(lons,lats, max_EAS12rain, clev, extend='neither', cmap='viridis', transform=data_crs, 
                 norm=plt.Normalize(1, 100))

cb = plt.colorbar(cf, ax=ax, orientation='horizontal',pad=0.05, extendrect='true', ticks=clev)
cb.set_label(r'PORCIENTO', size='xx-large')

cs1 = ax.contour(lons, lats, max_EAS12rain, clev, colors='black',
              linestyles='solid', transform=data_crs)
ax.set_title(f'PROBABILIDAD DE AGUACEROS TARDE & NOCHE | 12PM - 12AM \n{fecha_formateada} | DATA: {hora_formateada}', fontsize=22)
ax.clabel(cs1, fmt='%d', fontsize=20)

# PR COUNTIES SHAPEFILES
shapefile1_path = 'shp/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp'
gdf1 = gpd.read_file(shapefile1_path)
county_PR = ShapelyFeature(gdf1['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_PR)

shapefile2_path = 'shp/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_RD)

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

plt.show()
plt.show()

fig.savefig(f'{save_path}/D1n_TSRD_PROB-AGUAC_TN_RD.png', bbox_inches='tight', dpi=300)


# In[ ]:





# In[ ]:





# In[401]:


rprob_1 = prob_1.message(11)
rprob_2 = prob_2.message(11)
rprob_3 = prob_3.message(5)
rprob_4 = prob_4.message(11)
rprob_5 = prob_5.message(11)
rprob_6 = prob_6.message(5)

rprob1 = prob1.message(11)
rprob2 = prob2.message(11)
rprob3 = prob3.message(5)
rprob4 = prob4.message(11)
rprob5 = prob5.message(11)
rprob6 = prob6.message(5)
rprob7 = prob7.message(11)
rprob8 = prob8.message(11)
rprob9 = prob9.message(5)
rprob10 = prob10.message(11)
rprob11 = prob11.message(11)
rprob12 = prob12.message(5)
rprob13 = prob13.message(11)
rprob14 = prob14.message(11)
rprob15 = prob15.message(5)
rprob16 = prob16.message(11)
rprob17 = prob17.message(11)
rprob18 = prob18.message(5)

REFD_value_1 = rprob_1.values
REFD_value_2 = rprob_2.values
REFD_value_3 = rprob_3.values
REFD_value_4 = rprob_4.values
REFD_value_5 = rprob_5.values
REFD_value_6 = rprob_6.values

REFD_value1 = rprob1.values
REFD_value2 = rprob2.values
REFD_value3 = rprob3.values
REFD_value4 = rprob4.values
REFD_value5 = rprob5.values
REFD_value6 = rprob6.values
REFD_value7 = rprob7.values
REFD_value8 = rprob8.values
REFD_value9 = rprob9.values
REFD_value10 = rprob10.values
REFD_value11 = rprob11.values
REFD_value12 = rprob12.values
REFD_value13 = rprob13.values
REFD_value14 = rprob14.values
REFD_value15 = rprob15.values
REFD_value16 = rprob16.values
REFD_value17 = rprob17.values
REFD_value18 = rprob18.values


print('-----------------------------------------------------------------------------------')
print(rprob1)
print('-----------------------------------------------------------------------------------')

max_refd = np.maximum.reduce([
REFD_value_1,
REFD_value_2,
REFD_value_3,
REFD_value_4,
REFD_value_5,
REFD_value_6,
REFD_value1 , 
REFD_value2 , 
REFD_value3 , 
REFD_value4 , 
REFD_value5 , 
REFD_value6 , 
REFD_value7 , 
REFD_value8 , 
REFD_value9 , 
REFD_value10, 
REFD_value11, 
REFD_value12,
REFD_value13, 
REFD_value14, 
REFD_value15, 
REFD_value16, 
REFD_value17, 
REFD_value18])

REFC_max = ndimage.gaussian_filter(max_refd, sigma=1.5, order=0)
refd_L = REFC_max/25
refd_L_P = ((refd_L-1)/3)*100

print(refd_L)




# In[402]:


etop_p_1 = prob_1.message(17)
etop_p_2 = prob_2.message(17)
etop_p_3 = prob_3.message(11)
etop_p_4 = prob_4.message(17)
etop_p_5 = prob_5.message(17)
etop_p_6 = prob_6.message(11)

etop_p1 = prob1.message(17)
etop_p2 = prob2.message(17)
etop_p3 = prob3.message(11)
etop_p4 = prob4.message(17)
etop_p5 = prob5.message(17)
etop_p6 = prob6.message(11)
etop_p7 = prob7.message(17) 
etop_p8 = prob8.message(17)
etop_p9 = prob9.message(11)
etop_p10 = prob10.message(17)
etop_p11 = prob11.message(17)
etop_p12 = prob12.message(11)
etop_p13 = prob13.message(17)
etop_p14 = prob14.message(17)
etop_p15 = prob15.message(11)
etop_p16 = prob16.message(17)
etop_p17 = prob17.message(17)
etop_p18 = prob18.message(11)

etop_value_1 =  etop_p_1.values
etop_value_2 =  etop_p_2.values
etop_value_3 =  etop_p_3.values
etop_value_4 =  etop_p_4.values
etop_value_5 =  etop_p_5.values
etop_value_6 =  etop_p_6.values

etop_value1 =  etop_p1.values
etop_value2 =  etop_p2.values
etop_value3 =  etop_p3.values
etop_value4 =  etop_p4.values
etop_value5 =  etop_p5.values
etop_value6 =  etop_p6.values
etop_value7 =  etop_p7.values
etop_value8 =  etop_p8.values
etop_value9 =  etop_p9.values
etop_value10 = etop_p10.values
etop_value11 = etop_p11.values
etop_value12 = etop_p12.values
etop_value13 = etop_p13.values
etop_value14 = etop_p14.values
etop_value15 = etop_p15.values
etop_value16 = etop_p16.values
etop_value17 = etop_p17.values
etop_value18 = etop_p18.values


print('4-----------------------------------------------------------------------------------')
print(etop_p3)
print('4-----------------------------------------------------------------------------------')

etop_values = np.maximum.reduce([

etop_value_1,
etop_value_2,
etop_value_3,
etop_value_4,
etop_value_5,
etop_value_6,    
etop_value1, 
etop_value2, 
etop_value3, 
etop_value4, 
etop_value5, 
etop_value6, 
etop_value7, 
etop_value8, 
etop_value9, 
etop_value10, 
etop_value11, 
etop_value12,
etop_value13, 
etop_value14, 
etop_value15, 
etop_value16, 
etop_value17, 
etop_value18])

Interp4 = ndimage.gaussian_filter(etop_values, sigma=1.5, order=0)
etop_L = (Interp4/90)
etop_L_P = ((etop_L-1)/0.112)*100


# In[403]:


rain_prob_1 = prob_1.select(name="Total Precipitation")[0]
rain_prob_2 = prob_2.select(name="Total Precipitation")[0]
rain_prob_3 = prob_3.select(name="Total Precipitation")[0]
rain_prob_4 = prob_4.select(name="Total Precipitation")[0]
rain_prob_5 = prob_5.select(name="Total Precipitation")[0]
rain_prob_6 = prob_6.select(name="Total Precipitation")[0]
rain_prob1 = prob1.select(name="Total Precipitation")[0]
rain_prob2 = prob2.select(name="Total Precipitation")[0]
rain_prob3 = prob3.select(name="Total Precipitation")[0]
rain_prob4 = prob4.select(name="Total Precipitation")[0]
rain_prob5 = prob5.select(name="Total Precipitation")[0]
rain_prob6 = prob6.select(name="Total Precipitation")[0]
rain_prob7 = prob7.select(name="Total Precipitation")[0]
rain_prob8 = prob8.select(name="Total Precipitation")[0]
rain_prob9 = prob9.select(name="Total Precipitation")[0]
rain_prob10 = prob10.select(name="Total Precipitation")[0]
rain_prob11 = prob11.select(name="Total Precipitation")[0]
rain_prob12 = prob12.select(name="Total Precipitation")[0]
rain_prob13 = prob13.select(name="Total Precipitation")[0]
rain_prob14 = prob14.select(name="Total Precipitation")[0]
rain_prob15 = prob15.select(name="Total Precipitation")[0]
rain_prob16 = prob16.select(name="Total Precipitation")[0]
rain_prob17 = prob17.select(name="Total Precipitation")[0]
rain_prob18 = prob18.select(name="Total Precipitation")[0]

rainprob_value_1 = rain_prob_1.values
rainprob_value_2 = rain_prob_2.values
rainprob_value_3 = rain_prob_3.values
rainprob_value_4 = rain_prob_4.values
rainprob_value_5 = rain_prob_5.values
rainprob_value_6 = rain_prob_6.values
rainprob_value1 = rain_prob1.values
rainprob_value2 = rain_prob2.values
rainprob_value3 = rain_prob3.values
rainprob_value4 = rain_prob4.values
rainprob_value5 = rain_prob5.values
rainprob_value6 = rain_prob6.values
rainprob_value7 = rain_prob7.values
rainprob_value8 = rain_prob8.values
rainprob_value9 = rain_prob9.values
rainprob_value10 = rain_prob10.values
rainprob_value11 = rain_prob11.values
rainprob_value12 = rain_prob12.values
rainprob_value13 = rain_prob13.values
rainprob_value14 = rain_prob14.values
rainprob_value15 = rain_prob15.values
rainprob_value16 = rain_prob16.values
rainprob_value17 = rain_prob17.values
rainprob_value18 = rain_prob18.values

rainmax_value = np.maximum.reduce([
rainprob_value_1,
rainprob_value_2,
rainprob_value_3,
rainprob_value_4,
rainprob_value_5,
rainprob_value_6,
rainprob_value1, 
rainprob_value2, 
rainprob_value3, 
rainprob_value4, 
rainprob_value5, 
rainprob_value6, 
rainprob_value7, 
rainprob_value8, 
rainprob_value9, 
rainprob_value10, 
rainprob_value11, 
rainprob_value12, 
rainprob_value13, 
rainprob_value14, 
rainprob_value15, 
rainprob_value16, 
rainprob_value17, 
rainprob_value18])

print('-----------------------------------------------------------------------------------')
print(rain_prob_1)
print('-----------------------------------------------------------------------------------')


# In[404]:


crain_1 = prob_1.select(name="Categorical rain")[0]
crain_2 = prob_2.select(name="Categorical rain")[0]
crain_3 = prob_3.select(name="Categorical rain")[0]
crain_4 = prob_4.select(name="Categorical rain")[0]
crain_5 = prob_5.select(name="Categorical rain")[0]
crain_6 = prob_6.select(name="Categorical rain")[0]
crain1 = prob1.select(name="Categorical rain")[0]
crain2 = prob2.select(name="Categorical rain")[0]
crain3 = prob3.select(name="Categorical rain")[0]
crain4 = prob4.select(name="Categorical rain")[0]
crain5 = prob5.select(name="Categorical rain")[0]
crain6 = prob6.select(name="Categorical rain")[0]
crain7 = prob7.select(name="Categorical rain")[0]
crain8 = prob8.select(name="Categorical rain")[0]
crain9 = prob9.select(name="Categorical rain")[0]
crain10 = prob10.select(name="Categorical rain")[0]
crain11 = prob11.select(name="Categorical rain")[0]
crain12 = prob12.select(name="Categorical rain")[0]
crain13 = prob13.select(name="Categorical rain")[0]
crain14 = prob14.select(name="Categorical rain")[0]
crain15 = prob15.select(name="Categorical rain")[0]
crain16 = prob16.select(name="Categorical rain")[0]
crain17 = prob17.select(name="Categorical rain")[0]
crain18 = prob18.select(name="Categorical rain")[0]

crain_value_1 = crain_1.values
crain_value_2 = crain_2.values
crain_value_3 = crain_3.values
crain_value_4 = crain_4.values
crain_value_5 = crain_5.values
crain_value_6 = crain_6.values
crain_value1 =  crain1.values
crain_value2 =  crain2.values
crain_value3 =  crain3.values
crain_value4 =  crain4.values
crain_value5 =  crain5.values
crain_value6 =  crain6.values
crain_value7 =  crain7.values
crain_value8 =  crain8.values
crain_value9 =  crain9.values
crain_value10 = crain10.values
crain_value11 = crain11.values
crain_value12 = crain12.values
crain_value13 = crain13.values
crain_value14 = crain14.values
crain_value15 = crain15.values
crain_value16 = crain16.values
crain_value17 = crain17.values
crain_value18 = crain18.values

crain_value1_v = ndimage.gaussian_filter(crain_value_1, sigma=1.5, order=0)
crain_value2_v = ndimage.gaussian_filter(crain_value_2, sigma=1.5, order=0)
crain_value3_v = ndimage.gaussian_filter(crain_value_3, sigma=1.5, order=0)
crain_value4_v = ndimage.gaussian_filter(crain_value_4, sigma=1.5, order=0)
crain_value5_v = ndimage.gaussian_filter(crain_value_5, sigma=1.5, order=0)
crain_value6_v = ndimage.gaussian_filter(crain_value_6, sigma=1.5, order=0)
crain_value1v = ndimage.gaussian_filter(crain_value1, sigma=1.5, order=0)
crain_value2v = ndimage.gaussian_filter(crain_value2, sigma=1.5, order=0)
crain_value3v = ndimage.gaussian_filter(crain_value3, sigma=1.5, order=0)
crain_value4v = ndimage.gaussian_filter(crain_value4, sigma=1.5, order=0)
crain_value5v = ndimage.gaussian_filter(crain_value5, sigma=1.5, order=0)
crain_value6v = ndimage.gaussian_filter(crain_value6, sigma=1.5, order=0)
crain_value7v = ndimage.gaussian_filter(crain_value7, sigma=1.5, order=0)
crain_value8v = ndimage.gaussian_filter(crain_value8, sigma=1.5, order=0)
crain_value9v = ndimage.gaussian_filter(crain_value9, sigma=1.5, order=0)
crain_value10v = ndimage.gaussian_filter(crain_value10, sigma=1.5, order=0)
crain_value11v = ndimage.gaussian_filter(crain_value11, sigma=1.5, order=0)
crain_value12v = ndimage.gaussian_filter(crain_value12, sigma=1.5, order=0)
crain_value13v = ndimage.gaussian_filter(crain_value13, sigma=1.5, order=0)
crain_value14v = ndimage.gaussian_filter(crain_value14, sigma=1.5, order=0)
crain_value15v = ndimage.gaussian_filter(crain_value15, sigma=1.5, order=0)
crain_value16v = ndimage.gaussian_filter(crain_value16, sigma=1.5, order=0)
crain_value17v = ndimage.gaussian_filter(crain_value17, sigma=1.5, order=0)
crain_value18v = ndimage.gaussian_filter(crain_value18, sigma=1.5, order=0)


print('-----------------------------------------------------------------------------------')
print(crain1)
print('-----------------------------------------------------------------------------------')

max_crain = np.maximum.reduce([
crain_value1_v,
crain_value2_v,
crain_value3_v,
crain_value4_v,
crain_value5_v,
crain_value6_v,
crain_value1v , 
crain_value2v , 
crain_value3v , 
crain_value4v , 
crain_value5v , 
crain_value6v , 
crain_value7v , 
crain_value8v , 
crain_value9v , 
crain_value10v, 
crain_value11v, 
crain_value12v,
crain_value13v, 
crain_value14v, 
crain_value15v, 
crain_value16v, 
crain_value17v, 
crain_value18v])

max_crain_int = ndimage.gaussian_filter(max_crain, sigma=4, order=0)


final_rain1 =  np.power((crain_value1_v ) * (rainprob_value_1)*(EAS__1v), (1/3))
final_rain2 =  np.power((crain_value2_v ) * (rainprob_value_2)*(EAS__2v), (1/3))
final_rain3 =  np.power((crain_value3_v ) * (rainprob_value_3)*(EAS__3v), (1/3))
final_rain4 =  np.power((crain_value4_v ) * (rainprob_value_4)*(EAS__4v), (1/3))
final_rain5 =  np.power((crain_value5_v ) * (rainprob_value_5)*(EAS__5v), (1/3))
final_rain6 =  np.power((crain_value6_v ) * (rainprob_value_6)*(EAS__6v), (1/3))
final_rain7 = np.power((crain_value1v ) * (rainprob_value1 )  *(EAS_1v ), (1/3))
final_rain8 = np.power((crain_value2v ) * (rainprob_value2 )  *(EAS_2v ), (1/3))
final_rain9 = np.power((crain_value3v ) * (rainprob_value3 )  *(EAS_3v ), (1/3))
final_rain10 = np.power((crain_value4v ) * (rainprob_value4 ) *(EAS_4v ), (1/3))
final_rain11 = np.power((crain_value5v ) * (rainprob_value5 ) *(EAS_5v ), (1/3))
final_rain12 = np.power((crain_value6v ) * (rainprob_value6 ) *(EAS_6v ), (1/3))
final_rain13 = np.power((crain_value7v ) * (rainprob_value7 ) *(EAS_7v ), (1/3))
final_rain14 = np.power((crain_value8v ) * (rainprob_value8 ) *(EAS_8v ), (1/3))
final_rain15 = np.power((crain_value9v ) * (rainprob_value9 ) *(EAS_9v ), (1/3))
final_rain16 = np.power((crain_value10v) * (rainprob_value10) *(EAS_10v), (1/3))
final_rain17 = np.power((crain_value11v) * (rainprob_value11) *(EAS_11v), (1/3))
final_rain18 = np.power((crain_value12v) * (rainprob_value12) *(EAS_12v), (1/3))
final_rain19 = np.power((crain_value13v) * (rainprob_value13) *(EAS_13v), (1/3))
final_rain20 = np.power((crain_value14v) * (rainprob_value14) *(EAS_14v), (1/3))
final_rain21 = np.power((crain_value15v) * (rainprob_value15) *(EAS_15v), (1/3))
final_rain22 = np.power((crain_value16v) * (rainprob_value16) *(EAS_16v), (1/3))
final_rain23 = np.power((crain_value17v) * (rainprob_value17) *(EAS_17v), (1/3))
final_rain24 = np.power((crain_value18v) * (rainprob_value18) *(EAS_18v), (1/3))


max_final_rain = np.maximum.reduce([
final_rain1 ,
final_rain2 ,
final_rain3 ,
final_rain4 ,
final_rain5 ,
final_rain6 ,
final_rain7 , 
final_rain8 , 
final_rain9 , 
final_rain10, 
final_rain11, 
final_rain12, 
final_rain13, 
final_rain14, 
final_rain15, 
final_rain16, 
final_rain17, 
final_rain18,
final_rain19, 
final_rain20, 
final_rain21, 
final_rain22, 
final_rain23, 
final_rain24])

max_final_rain_int = ndimage.gaussian_filter(max_final_rain, sigma=1.5, order=0)


# In[405]:


fig = plt.figure (1,figsize=(20,22))
ax=plt.subplot(1,1,1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space
ax.set_extent ([-67.5, -74.5, 17.25, 20.5], data_crs)
ax.add_feature(cfeature.COASTLINE, linewidth=2)
ax.add_feature(cfeature.BORDERS, linewidth=2)


colormap = matplotlib.colors.ListedColormap(['#00c700','#ffff00','#ff8f00','#cc3300'])

clev = [15, 20, 40, 60, 80, 100]

cf = ax.contourf(lons,lats, max_EASrain, clev, extend='neither', cmap='viridis', transform=data_crs, 
                 norm=plt.Normalize(1, 100))

cb = plt.colorbar(cf, ax=ax, orientation='horizontal',pad=0.05, extendrect='true', ticks=clev)
cb.set_label(r'PORCIENTO', size='xx-large')

cs1 = ax.contour(lons, lats, max_EASrain, clev, colors='black',
              linestyles='solid', transform=data_crs)
ax.set_title(f'PROBABILIDAD DE AGUACEROS TARDE & NOCHE | 12PM - 12AM \n{fecha_formateada} | DATA: {hora_formateada}', fontsize=22)
ax.clabel(cs1, fmt='%d', fontsize=20)

# PR COUNTIES SHAPEFILES
shapefile1_path = 'shp/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp'
gdf1 = gpd.read_file(shapefile1_path)
county_PR = ShapelyFeature(gdf1['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_PR)

shapefile2_path = 'shp/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_RD)

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

plt.show()
plt.show()

fig.savefig(f'{save_path}/D1n_TSRD_PROB-AGUAC_TN_RD.png', bbox_inches='tight', dpi=300)


# In[406]:


fig = plt.figure (1,figsize=(20,22))
ax=plt.subplot(1,1,1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space
ax.set_extent ([-67.5, -74.5, 17.25, 20.5], data_crs)
ax.add_feature(cfeature.COASTLINE, linewidth=2)
ax.add_feature(cfeature.BORDERS, linewidth=2)


colormap = matplotlib.colors.ListedColormap(['#00c700','#ffff00','#ff8f00','#cc3300'])

clev = [20, 40, 60, 80, 100]

cf = ax.contourf(lons,lats, max_crain, clev, extend='neither', cmap='viridis', transform=data_crs, 
                 norm=plt.Normalize(1, 100))

cb = plt.colorbar(cf, ax=ax, orientation='horizontal',pad=0.05, extendrect='true', ticks=clev)
cb.set_label(r'PORCIENTO', size='xx-large')

cs1 = ax.contour(lons, lats, max_crain, clev, colors='black',
              linestyles='solid', transform=data_crs)
ax.set_title(f'PROBABILIDAD DE AGUACEROS TARDE & NOCHE | 12PM - 12AM \n{fecha_formateada} | DATA: {hora_formateada}', fontsize=22)
ax.clabel(cs1, fmt='%d', fontsize=20)

# PR COUNTIES SHAPEFILES
shapefile1_path = 'shp/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp'
gdf1 = gpd.read_file(shapefile1_path)
county_PR = ShapelyFeature(gdf1['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_PR)

shapefile2_path = 'shp/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_RD)

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

plt.show()
plt.show()

fig.savefig(f'{save_path}/D1n_TSRD_PROB-AGUAC_TN_RD.png', bbox_inches='tight', dpi=300)


# In[407]:


fig = plt.figure (1,figsize=(20,22))
ax=plt.subplot(1,1,1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space
ax.set_extent ([-67.5, -74.5, 17.25, 20.5], data_crs)
ax.add_feature(cfeature.COASTLINE, linewidth=2)
ax.add_feature(cfeature.BORDERS, linewidth=2)


colormap = matplotlib.colors.ListedColormap(['#00c700','#ffff00','#ff8f00','#cc3300'])

clev = [15, 20, 40, 60, 80, 100]

cf = ax.contourf(lons,lats, rainmax_value, clev, extend='neither', cmap='viridis', transform=data_crs, 
                 norm=plt.Normalize(1, 100))

cb = plt.colorbar(cf, ax=ax, orientation='horizontal',pad=0.05, extendrect='true', ticks=clev)
cb.set_label(r'PORCIENTO', size='xx-large')

cs1 = ax.contour(lons, lats, rainmax_value, clev, colors='black',
              linestyles='solid', transform=data_crs)
ax.set_title(f'PROBABILIDAD DE AGUACEROS 24 HORAS | 12AM - 12AM \n{fecha_formateada} | DATA: {hora_formateada}', fontsize=22)

ax.clabel(cs1, fmt='%d', fontsize=20)

# PR COUNTIES SHAPEFILES
shapefile1_path = 'shp/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp'
gdf1 = gpd.read_file(shapefile1_path)
county_PR = ShapelyFeature(gdf1['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_PR)

shapefile2_path = 'shp/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_RD)

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

plt.show()
plt.show()

fig.savefig(f'{save_path}/D1_TSRD_PROB-AGUAC_24_RD.png', bbox_inches='tight', dpi=300)


# In[408]:


fig = plt.figure (1,figsize=(20,22))
ax=plt.subplot(1,1,1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space
ax.set_extent ([-67.5, -74.5, 17.25, 20.5], data_crs)
ax.add_feature(cfeature.COASTLINE, linewidth=2)
ax.add_feature(cfeature.BORDERS, linewidth=2)


colormap = matplotlib.colors.ListedColormap(['#00c700','#ffff00','#ff8f00','#cc3300'])

clev = [15, 20, 40, 60, 80, 100]

cf = ax.contourf(lons,lats, max_final_rain_int, clev, extend='neither', cmap='viridis', transform=data_crs, 
                 norm=plt.Normalize(0, 100))

cb = plt.colorbar(cf, ax=ax, orientation='horizontal',pad=0.05, extendrect='true', ticks=clev)
cb.set_label(r'PORCIENTO', size='xx-large')

cs1 = ax.contour(lons, lats, max_final_rain_int, clev, colors='black',
              linestyles='solid', transform=data_crs)
ax.set_title(f'PROBABILIDAD DE AGUACEROS TARDE & NOCHE | 12PM - 12AM \n{fecha_formateada} | DATA: {hora_formateada}', fontsize=22)
ax.clabel(cs1, fmt='%d', fontsize=20)

# PR COUNTIES SHAPEFILES
shapefile1_path = 'shp/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp'
gdf1 = gpd.read_file(shapefile1_path)
county_PR = ShapelyFeature(gdf1['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_PR)

shapefile2_path = 'shp/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_RD)

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

plt.show()
plt.show()

fig.savefig(f'{save_path}/D1n_TSRD_PROB-AGUAC_TN_RD.png', bbox_inches='tight', dpi=300)


# In[409]:


import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from cartopy.feature import ShapelyFeature
from matplotlib import offsetbox
import matplotlib.patheffects as path_effects
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap

# Define the coordinate reference systems
map_crs = ccrs.PlateCarree()
data_crs = ccrs.PlateCarree()

# Create the figure and axis
fig = plt.figure(1, figsize=(20, 22))
ax = plt.subplot(1, 1, 1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space

# Set the extent of the map
ax.set_extent([-67.5, -72.5, 17.25, 20.25], crs=data_crs)

# Add features to the map
ax.add_feature(cfeature.COASTLINE, linewidth=3.5)
ax.add_feature(cfeature.BORDERS, linewidth=3.5, zorder=3)
ax.add_feature(cfeature.OCEAN, facecolor='#00374d', zorder=3)
ax.add_feature(cfeature.LAND, facecolor='#b3b4b3')
ax.add_feature(cfeature.LAKES, linewidth=2, zorder=3, edgecolor='black', alpha=1)

# Add Dominican lakes (if the default lakes feature does not include them, create a custom one)
canada_lakes = cfeature.NaturalEarthFeature(
    category='physical',
    name='lakes',
    scale='10m',
    facecolor='none'
)
ax.add_feature(canada_lakes, edgecolor='black', linewidth=1)

# Define the second colormap and contour levels
clev = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# Define the second colormap and contour levels
clev2 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# Plot the second set of filled contours
cf = ax.contourf(lons, lats, max_final_rain_int, clev, extend='neither', transform=data_crs, norm=plt.Normalize(10, 80), cmap='BuGn', alpha=1)


# Position and customize the second color bar
cax = fig.add_axes([0.1, 0.245, 0.8, 0.04], zorder=0)  # Adjust the position as needed
cb = plt.colorbar(cf, cax=cax, orientation='horizontal', extendrect='true', drawedges=True)
cb.set_ticks([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])  # Hide the ticks
cb.ax.xaxis.set_tick_params(color='white')
plt.setp(plt.getp(cb.ax, 'xticklabels'), color='white', fontsize=20, fontweight='bold')
cb.outline.set_edgecolor('k')  # Set color of the outline
cb.outline.set_linewidth(3)  # Set the width of the outline
cb.dividers.set_color('k')  # Set color of the dividers
cb.dividers.set_linewidth(3)  # Set the width of the dividers

# Plot the second set of line contours
cs1 = ax.contour(lons, lats, max_final_rain_int, clev2, colors='k', linestyles='solid', transform=data_crs, linewidths=2, fontsize=40)
labels = ax.clabel(cs1, fmt='%d', fontsize=25, zorder=2)
# Set the font weight to bold for each label
for label in labels:
    label.set_fontweight('bold')

# Set titles for the plot
#ax.set_title(f'EVALUACIÓN DE PROBABILIDADES DE TRONADAS - 24 HORAS (12AM - 12AM) \nVálido para este {fecha_formateada}', loc='left', fontsize=22, fontweight='bold')
#ax.set_title(f'INIT: {hora_formateada} de este {fecha_formateada_dia_anterior}', loc='right', fontsize=16, fontweight='bold', style='italic')

# Add shapefile data
shapefile2_path = 'shp/rd/geoBoundaries-DOM-ADM1_simplified.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=1.5)
ax.add_feature(county_RD)

# Add shapefile data
shapefile3_path = 'shp/haiti/ne_10m_admin_0_countries.shp'
gdf3 = gpd.read_file(shapefile3_path)
county_HTI = ShapelyFeature(gdf3['geometry'], ccrs.PlateCarree(), facecolor='grey', edgecolor='black', lw=1, zorder=2)
ax.add_feature(county_HTI)

# Dictionary of important cities with their coordinates
cities = {
    "Santo Domingo": {"lat": 18.4861, "lon": -69.9312},
    "Santiago": {"lat": 19.4792, "lon": -70.6931},
    "La Romana": {"lat": 18.4333, "lon": -68.9667},
    "Punta Cana": {"lat": 18.582, "lon": -68.4055},
    "Puerto Plata": {"lat": 19.7975, "lon": -70.6884},
    "La Vega": {"lat": 19.2232, "lon": -70.5294},
    "Bonao": {"lat": 18.9356, "lon": -70.4094},
    "Baní": {"lat": 18.2796, "lon": -70.3319},
    "Azua": {"lat": 18.4532, "lon": -70.7349},
    "Barahona": {"lat": 18.2085, "lon": -71.1008},
    "Montecristi": {"lat": 19.8489, "lon": -71.6464},
    "Dajabón": {"lat": 19.5483, "lon": -71.7083},
    "Samaná": {"lat": 19.2057, "lon": -69.3367},
    "V. Altagracia": {"lat": 18.6700, "lon": -70.1700},
    "El Seibo": {"lat": 18.7650, "lon": -69.0383},
    "Nagua": {"lat": 19.3833, "lon": -69.8500},
    "San Juan": {"lat": 18.8050, "lon": -71.2300},
    "Pedernales": {"lat": 18.0370, "lon": -71.7440},
    "Ocoa": {"lat": 18.5500, "lon": -70.5000},
    "Oviedo": {"lat": 17.8007, "lon": -71.4008},
    "S. de la Mar": {"lat": 19.0579, "lon": -69.3892},
    "Monte Plata": {"lat": 18.8073, "lon": -69.7850},
    "Pimentel": {"lat": 19.1832, "lon": -70.1085},
    "Mao": {"lat": 19.5511, "lon": -71.0781},
    "Neyba": {"lat": 18.4847, "lon": -71.4194},
    "Pedro Santana": {"lat": 19.1050, "lon": -71.6959},
    "Elías Piña": {"lat": 18.8770, "lon": -71.7048},
    "Restauración": {"lat": 19.3159, "lon": -71.6947},
    "SAJOMA": {"lat": 19.3405, "lon": -70.9376}
}

# Add city names and dots to the plot
for city, coords in cities.items():
    ax.plot(coords["lon"], coords["lat"], 'o', color='k', markersize=10, transform=data_crs, path_effects=[path_effects.withStroke(linewidth=5, foreground='white')])  # Add a red dot
    ax.text(coords["lon"], coords["lat"], city, transform=data_crs, fontsize=22, fontweight='bold',
            ha='left', color='white', path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])

# Dictionary of important cities with their coordinates
cities2 = {
    "Higuey": {"lat": 18.6150, "lon": -68.7070},
    "Constanza": {"lat": 18.9094, "lon": -70.7208},

}

# Add city names and dots to the plot
for city, coords in cities2.items():
    ax.plot(coords["lon"], coords["lat"], 'o', color='k', markersize=10, transform=data_crs, path_effects=[path_effects.withStroke(linewidth=5, foreground='white')])  # Add a red dot
    ax.text(coords["lon"], coords["lat"], city, transform=data_crs, fontsize=22, fontweight='bold',
            ha='right', color='white', path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])

# Add text annotations
text1 = ax.text(0.5, 0.125, 'PROBABILIDADES', ha='center', va='center', fontsize=40, transform=ax.transAxes, fontweight='bold', color='white')
text1.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

text2 = ax.text(0.84, 0.75, f'Válidez del Mapa: \n 12:00 AM - 12:00 AM del \n {fecha_formateada}', ha='center', va='center', fontsize=25, transform=ax.transAxes, fontweight='bold', color='white')
text2.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

text4 = ax.text(0.84, 0.985, f'INIT: {hora_formateada} de este {fecha_formateada_dia_anterior}', ha='center', va='center', fontsize=16, transform=ax.transAxes, fontweight='bold', color='white')
text4.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

text3 = ax.text(0.32, 0.95, 'MAPA DE PROBABILIDADES DE AGUACEROS', ha='center', va='center', fontsize=35, transform=ax.transAxes, fontweight='bold', color='white', zorder=5)
text3.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

def add_rounded_rect_with_shadow(ax, xy, width, height, rounding_size=0.1, shadow_offset=(0.02, -0.02)):
    # Add shadow
    shadow = FancyBboxPatch(
        (xy[0] + shadow_offset[0], xy[1] + shadow_offset[1]), width, height,
        boxstyle=f"round,pad=0.05,rounding_size={rounding_size}",
        edgecolor='none', facecolor='black', alpha=0.3,
        transform=data_crs, zorder=3
    )
    ax.add_patch(shadow)

    # Add rectangle
    rect = FancyBboxPatch(
        xy, width, height,
        boxstyle=f"round,pad=0.05,rounding_size={rounding_size}",
        edgecolor='k', facecolor='#4c955a', alpha=1,
        transform=data_crs, linewidth=2, zorder=4
    )
    ax.add_patch(rect)

# Define the position and size of the rectangle
rect_xy = (-72.4, 20.05)
rect_width = 3
rect_height = 0.1

# Add the rectangle with shadow to the plot
add_rounded_rect_with_shadow(ax, rect_xy, rect_width, rect_height)

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

# Save the figure
fig.savefig(f'{save_path}/D1_TSRD_PROB-TRON_24_RD.png', bbox_inches='tight', dpi=300)


# In[410]:


vvel_p_1 = prob_1.message(22)
vvel_p_2 = prob_2.message(22)
vvel_p_3 = prob_3.message(19)
vvel_p_4 = prob_4.message(22)
vvel_p_5 = prob_5.message(22)
vvel_p_6 = prob_6.message(19)

vvel_p1 = prob1.message(22)
vvel_p2 = prob2.message(22)
vvel_p3 = prob3.message(19)
vvel_p4 = prob4.message(22)
vvel_p5 = prob5.message(22)
vvel_p6 = prob6.message(19)
vvel_p7 = prob7.message(22) 
vvel_p8 = prob8.message(22)
vvel_p9 = prob9.message(19)
vvel_p10 = prob10.message(22)
vvel_p11 = prob11.message(22)
vvel_p12 = prob12.message(19)
vvel_p13 = prob13.message(22)
vvel_p14 = prob14.message(22)
vvel_p15 = prob15.message(19)
vvel_p16 = prob16.message(22)
vvel_p17 = prob17.message(22)
vvel_p18 = prob18.message(19)

vvelp_value_1 = vvel_p_1.values
vvelp_value_2 = vvel_p_2.values
vvelp_value_3 = vvel_p_3.values
vvelp_value_4 = vvel_p_4.values
vvelp_value_5 = vvel_p_5.values
vvelp_value_6 = vvel_p_6.values
vvelp_value1 =  vvel_p1.values
vvelp_value2 =  vvel_p2.values
vvelp_value3 =  vvel_p3.values
vvelp_value4 =  vvel_p4.values
vvelp_value5 =  vvel_p5.values
vvelp_value6 =  vvel_p6.values
vvelp_value7 =  vvel_p7.values
vvelp_value8 =  vvel_p8.values
vvelp_value9 =  vvel_p9.values
vvelp_value10 = vvel_p10.values
vvelp_value11 = vvel_p11.values
vvelp_value12 = vvel_p12.values
vvelp_value13 = vvel_p13.values
vvelp_value14 = vvel_p14.values
vvelp_value15 = vvel_p15.values
vvelp_value16 = vvel_p16.values
vvelp_value17 = vvel_p17.values
vvelp_value18 = vvel_p18.values


print('4-----------------------------------------------------------------------------------')
print(vvel_p3)
print('4-----------------------------------------------------------------------------------')

vvel_values = np.maximum.reduce([

vvelp_value_1,
vvelp_value_2,
vvelp_value_3,
vvelp_value_4,
vvelp_value_5,
vvelp_value_6,    
vvelp_value1, 
vvelp_value2, 
vvelp_value3, 
vvelp_value4, 
vvelp_value5, 
vvelp_value6, 
vvelp_value7, 
vvelp_value8, 
vvelp_value9, 
vvelp_value10, 
vvelp_value11, 
vvelp_value12,
vvelp_value13, 
vvelp_value14, 
vvelp_value15, 
vvelp_value16, 
vvelp_value17, 
vvelp_value18])

vvelp_int = ndimage.gaussian_filter(vvel_values, sigma=1.5, order=0)


# In[411]:


pmmn_file_1  = 'Model_Data/18Z/href.t18z.pr.pmmn.f10.grib2'
pmmn_file_2  = 'Model_Data/18Z/href.t18z.pr.pmmn.f11.grib2'
pmmn_file_3  = 'Model_Data/18Z/href.t18z.pr.pmmn.f12.grib2'
pmmn_file_4  = 'Model_Data/18Z/href.t18z.pr.pmmn.f13.grib2'
pmmn_file_5  = 'Model_Data/18Z/href.t18z.pr.pmmn.f14.grib2'
pmmn_file_6  = 'Model_Data/18Z/href.t18z.pr.pmmn.f15.grib2'

pmmn_file1  = 'Model_Data/18Z/href.t18z.pr.pmmn.f16.grib2'
pmmn_file2  = 'Model_Data/18Z/href.t18z.pr.pmmn.f17.grib2'
pmmn_file3  = 'Model_Data/18Z/href.t18z.pr.pmmn.f18.grib2'
pmmn_file4  = 'Model_Data/18Z/href.t18z.pr.pmmn.f19.grib2'
pmmn_file5  = 'Model_Data/18Z/href.t18z.pr.pmmn.f20.grib2'
pmmn_file6  = 'Model_Data/18Z/href.t18z.pr.pmmn.f21.grib2'
pmmn_file7  = 'Model_Data/18Z/href.t18z.pr.pmmn.f22.grib2'
pmmn_file8  = 'Model_Data/18Z/href.t18z.pr.pmmn.f23.grib2'
pmmn_file9  = 'Model_Data/18Z/href.t18z.pr.pmmn.f24.grib2'
pmmn_file10 = 'Model_Data/18Z/href.t18z.pr.pmmn.f25.grib2'
pmmn_file11 = 'Model_Data/18Z/href.t18z.pr.pmmn.f26.grib2'
pmmn_file12 = 'Model_Data/18Z/href.t18z.pr.pmmn.f27.grib2'
pmmn_file13 = 'Model_Data/18Z/href.t18z.pr.pmmn.f28.grib2'
pmmn_file14 = 'Model_Data/18Z/href.t18z.pr.pmmn.f29.grib2'
pmmn_file15 = 'Model_Data/18Z/href.t18z.pr.pmmn.f30.grib2'
pmmn_file16 = 'Model_Data/18Z/href.t18z.pr.pmmn.f31.grib2'
pmmn_file17 = 'Model_Data/18Z/href.t18z.pr.pmmn.f32.grib2'
pmmn_file18 = 'Model_Data/18Z/href.t18z.pr.pmmn.f33.grib2'

pmmn_1  = pygrib.open(pmmn_file_1)
pmmn_2  = pygrib.open(pmmn_file_2)
pmmn_3  = pygrib.open(pmmn_file_3)
pmmn_4  = pygrib.open(pmmn_file_4)
pmmn_5  = pygrib.open(pmmn_file_5)
pmmn_6  = pygrib.open(pmmn_file_6)

pmmn1  = pygrib.open(pmmn_file1)
pmmn2  = pygrib.open(pmmn_file2)
pmmn3  = pygrib.open(pmmn_file3)
pmmn4  = pygrib.open(pmmn_file4)
pmmn5  = pygrib.open(pmmn_file5)
pmmn6  = pygrib.open(pmmn_file6)
pmmn7  = pygrib.open(pmmn_file7)
pmmn8  = pygrib.open(pmmn_file8)
pmmn9  = pygrib.open(pmmn_file9)
pmmn10 = pygrib.open(pmmn_file10)
pmmn11 = pygrib.open(pmmn_file11)
pmmn12 = pygrib.open(pmmn_file12)
pmmn13 = pygrib.open(pmmn_file13)
pmmn14 = pygrib.open(pmmn_file14)
pmmn15 = pygrib.open(pmmn_file15)
pmmn16 = pygrib.open(pmmn_file16)
pmmn17 = pygrib.open(pmmn_file17)
pmmn18 = pygrib.open(pmmn_file18)

reflect_1  = pmmn_1.message(3)
reflect_2  = pmmn_2.message(3)
reflect_3  = pmmn_3.message(2)
reflect_4  = pmmn_4.message(3)
reflect_5  = pmmn_5.message(3)
reflect_6  = pmmn_6.message(2)

reflect1  = pmmn1.message(3)
reflect2  = pmmn2.message(3)
reflect3  = pmmn3.message(2)
reflect4  = pmmn4.message(3)
reflect5  = pmmn5.message(3)
reflect6  = pmmn6.message(2)
reflect7  = pmmn7.message(3)
reflect8  = pmmn8.message(3)
reflect9  = pmmn9.message(2)
reflect10 = pmmn10.message(3)
reflect11 = pmmn11.message(3)
reflect12 = pmmn12.message(2)
reflect13 = pmmn13.message(3)
reflect14 = pmmn14.message(3)
reflect15 = pmmn15.message(2)
reflect16 = pmmn16.message(3)
reflect17 = pmmn17.message(3)
reflect18 = pmmn18.message(2)

REFD_1  = reflect_1.values
REFD_2  = reflect_2.values
REFD_3  = reflect_3.values
REFD_4 = reflect_4.values
REFD_5 = reflect_5.values
REFD_6 = reflect_6.values

REFD1  = reflect1.values
REFD2  = reflect2.values
REFD3  = reflect3.values
REFD4 = reflect4.values
REFD5 = reflect5.values
REFD6 = reflect6.values
REFD7 = reflect7.values
REFD8 = reflect8.values
REFD9 = reflect9.values
REFD10 = reflect10.values
REFD11 = reflect11.values
REFD12 = reflect12.values
REFD13 = reflect13.values
REFD14 = reflect14.values
REFD15 = reflect15.values
REFD16 = reflect16.values
REFD17 = reflect17.values
REFD18 = reflect18.values

REFD_max_value = np.maximum.reduce([
REFD_1,
REFD_2,
REFD_3,
REFD_4,
REFD_5,
REFD_6,
REFD1, 
REFD2, 
REFD3, 
REFD4, 
REFD5, 
REFD6, 
REFD7, 
REFD8, 
REFD9, 
REFD10, 
REFD11, 
REFD12, 
REFD13, 
REFD14, 
REFD15, 
REFD16, 
REFD17, 
REFD18])

REFD_max_value_int = ndimage.gaussian_filter(REFD_max_value, sigma=1.5, order=0)

print('-----------------------------------------------------------------------------------')
print(reflect_1)
print('-----------------------------------------------------------------------------------')


pmmn_1  = pygrib.open(pmmn_file_1)
pmmn_2  = pygrib.open(pmmn_file_2)
pmmn_3  = pygrib.open(pmmn_file_3)
pmmn_4  = pygrib.open(pmmn_file_4)
pmmn_5  = pygrib.open(pmmn_file_5)
pmmn_6  = pygrib.open(pmmn_file_6)
pmmn1  = pygrib.open(pmmn_file1)
pmmn2  = pygrib.open(pmmn_file2)
pmmn3  = pygrib.open(pmmn_file3)
pmmn4  = pygrib.open(pmmn_file4)
pmmn5  = pygrib.open(pmmn_file5)
pmmn6  = pygrib.open(pmmn_file6)
pmmn7  = pygrib.open(pmmn_file7)
pmmn8  = pygrib.open(pmmn_file8)
pmmn9  = pygrib.open(pmmn_file9)
pmmn10 = pygrib.open(pmmn_file10)
pmmn11 = pygrib.open(pmmn_file11)
pmmn12 = pygrib.open(pmmn_file12)
pmmn13 = pygrib.open(pmmn_file13)
pmmn14 = pygrib.open(pmmn_file14)
pmmn15 = pygrib.open(pmmn_file15)
pmmn16 = pygrib.open(pmmn_file16)
pmmn17 = pygrib.open(pmmn_file17)
pmmn18 = pygrib.open(pmmn_file18)

reflectc_1  = pmmn_1.message(4)
reflectc_2  = pmmn_2.message(4)
reflectc_3  = pmmn_3.message(3)
reflectc_4  = pmmn_4.message(4)
reflectc_5  = pmmn_5.message(4)
reflectc_6  = pmmn_6.message(3)
reflectc1  = pmmn1.message(4)
reflectc2  = pmmn2.message(4)
reflectc3  = pmmn3.message(3)
reflectc4  = pmmn4.message(4)
reflectc5  = pmmn5.message(4)
reflectc6  = pmmn6.message(3)
reflectc7  = pmmn7.message(4)
reflectc8  = pmmn8.message(4)
reflectc9  = pmmn9.message(3)
reflectc10 = pmmn10.message(4)
reflectc11 = pmmn11.message(4)
reflectc12 = pmmn12.message(3)
reflectc13 = pmmn13.message(4)
reflectc14 = pmmn14.message(4)
reflectc15 = pmmn15.message(3)
reflectc16 = pmmn16.message(4)
reflectc17 = pmmn17.message(4)
reflectc18 = pmmn18.message(3)

REFC_1  = reflectc_1.values
REFC_2  = reflectc_2.values
REFC_3  = reflectc_3.values
REFC_4 = reflectc_4.values
REFC_5 = reflectc_5.values
REFC_6 = reflectc_6.values

REFC1  = reflectc1.values
REFC2  = reflectc2.values
REFC3  = reflectc3.values
REFC4 = reflectc4.values
REFC5 = reflectc5.values
REFC6 = reflectc6.values
REFC7 = reflectc7.values
REFC8 = reflectc8.values
REFC9 = reflectc9.values
REFC10 = reflectc10.values
REFC11 = reflectc11.values
REFC12 = reflectc12.values
REFC13 = reflectc13.values
REFC14 = reflectc14.values
REFC15 = reflectc15.values
REFC16 = reflectc16.values
REFC17 = reflectc17.values
REFC18 = reflectc18.values

REFC_max_value = np.maximum.reduce([
REFC_1,
REFC_2,
REFC_3,
REFC_4,
REFC_5,
REFC_6,
REFC1, 
REFC2, 
REFC3, 
REFC4, 
REFC5, 
REFC6, 
REFC7, 
REFC8, 
REFC9, 
REFC10, 
REFC11, 
REFC12, 
REFC13, 
REFC14, 
REFC15, 
REFC16, 
REFC17, 
REFC18])

REFC_max_value_int = ndimage.gaussian_filter(REFC_max_value, sigma=1.5, order=0)

print('-----------------------------------------------------------------------------------')
print(reflectc_1)
print('-----------------------------------------------------------------------------------')


# In[ ]:





# In[412]:


#root = 3
#FINAL = (np.power((EAS_L*light_L_P*refd_L_P), (1/root)))
#FINAL_PERC = (FINAL/230)*100


# In[413]:


root = 3

p_1  = np.power((final_rain1/10 ) * (etop_value_1/80 ), (1/2))
p_2  = np.power((final_rain2/10 ) * (etop_value_2/80 ), (1/2))
p_3  = np.power((final_rain3/10 ) * (etop_value_3/80 ), (1/2))
p_4  = np.power((final_rain4/10 ) * (etop_value_4/80 ), (1/2))
p_5  = np.power((final_rain5/10 ) * (etop_value_5/80 ), (1/2))
p_6  = np.power((final_rain6/10 ) * (etop_value_6/80 ), (1/2))
p1  = np.power((final_rain7/10 ) * (etop_value1/80 ), (1/2))
p2  = np.power((final_rain8/10 ) * (etop_value2/80 ), (1/2))
p3  = np.power((final_rain9/10 ) * (etop_value3/80 ), (1/2))
p4  = np.power((final_rain10/10 ) * (etop_value4/80 ), (1/2))
p5  = np.power((final_rain11/10 ) * (etop_value5/80 ), (1/2))
p6  = np.power((final_rain12/10 ) * (etop_value6/80 ), (1/2))
p7  = np.power((final_rain13/10 ) * (etop_value7/80 ), (1/2))
p8  = np.power((final_rain14/10 ) * (etop_value8/80 ), (1/2))
p9  = np.power((final_rain15/10 ) * (etop_value9/80 ), (1/2))
p10 = np.power((final_rain16/10) * (etop_value10/80), (1/2))
p11 = np.power((final_rain17/10) * (etop_value11/80), (1/2))
p12 = np.power((final_rain18/10) * (etop_value12/80), (1/2))
p13 = np.power((final_rain19/10) * (etop_value13/80), (1/2))
p14 = np.power((final_rain20/10) * (etop_value14/80), (1/2))
p15 = np.power((final_rain21/10) * (etop_value15/80), (1/2))
p16 = np.power((final_rain22/10) * (etop_value16/80), (1/2))
p17 = np.power((final_rain23/10) * (etop_value17/80), (1/2))
p18 = np.power((final_rain24/10) * (etop_value18/80), (1/2))

q_1 = np.power(light_value1_v  * REFD_value_1 *vvelp_value_1, (1/root))
q_2 = np.power(light_value2_v  * REFD_value_2 *vvelp_value_2, (1/root))
q_3 = np.power(light_value3_v  * REFD_value_3 *vvelp_value_3, (1/root))
q_4 = np.power(light_value4_v  * REFD_value_4 *vvelp_value_4, (1/root))
q_5 = np.power(light_value5_v  * REFD_value_5 *vvelp_value_5, (1/root))
q_6 = np.power(light_value6_v  * REFD_value_6 *vvelp_value_6, (1/root))
q1 = np.power(light_value1v  * REFD_value1 *   vvelp_value1,(1/root))
q2 = np.power(light_value2v  * REFD_value2 *   vvelp_value2,(1/root))
q3 = np.power(light_value3v  * REFD_value3 *   vvelp_value3,(1/root))
q4 = np.power(light_value4v  * REFD_value4 *   vvelp_value4,(1/root))
q5 = np.power(light_value5v  * REFD_value5 *   vvelp_value5,(1/root))
q6 = np.power(light_value6v  * REFD_value6 *   vvelp_value6,(1/root))
q7 = np.power(light_value7v  * REFD_value7 *   vvelp_value7,(1/root))
q8 = np.power(light_value8v  * REFD_value8 *   vvelp_value8,(1/root))
q9 = np.power(light_value9v  * REFD_value9 *   vvelp_value9,(1/root))
q10 = np.power(light_value10v * REFD_value10 * vvelp_value10, (1/root))
q11 = np.power(light_value11v * REFD_value11 * vvelp_value11, (1/root))
q12 = np.power(light_value12v * REFD_value12 * vvelp_value12, (1/root))
q13 = np.power(light_value13v * REFD_value13 * vvelp_value13, (1/root))
q14 = np.power(light_value14v * REFD_value14 * vvelp_value14, (1/root))
q15 = np.power(light_value15v * REFD_value15 * vvelp_value15, (1/root))
q16 = np.power(light_value16v * REFD_value16 * vvelp_value16, (1/root))
q17 = np.power(light_value17v * REFD_value17 * vvelp_value17, (1/root))
q18 = np.power(light_value18v * REFD_value18 * vvelp_value18, (1/root))


t_1  = np.where(p_1  >= 1, q_1 , 0)
t_2  = np.where(p_2  >= 1, q_2 , 0)
t_3  = np.where(p_3  >= 1, q_3 , 0)
t_4  = np.where(p_4  >= 1, q_4 , 0)
t_5  = np.where(p_5  >= 1, q_5 , 0)
t_6  = np.where(p_6  >= 1, q_6 , 0)

t1  = np.where(p1  >= 1, q1 , 0)
t2  = np.where(p2  >= 1, q2 , 0)
t3  = np.where(p3  >= 1, q3 , 0)
t4  = np.where(p4  >= 1, q4 , 0)
t5  = np.where(p5  >= 1, q5 , 0)
t6  = np.where(p6  >= 1, q6 , 0)
t7  = np.where(p7  >= 1, q7 , 0)
t8  = np.where(p8  >= 1, q8 , 0)
t9  = np.where(p9  >= 1, q9 , 0)
t10 = np.where(p10 >= 1, q10, 0)
t11 = np.where(p11 >= 1, q11, 0)
t12 = np.where(p12 >= 1, q12, 0)
t13 = np.where(p13 >= 1, q13, 0)
t14 = np.where(p14 >= 1, q14, 0)
t15 = np.where(p15 >= 1, q15, 0)
t16 = np.where(p16 >= 1, q16, 0)
t17 = np.where(p17 >= 1, q17, 0)
t18 = np.where(p18 >= 1, q18, 0)

Thunder_max = np.maximum.reduce([
t_1, 
t_2, 
t_3, 
t_4, 
t_5, 
t_6, 
t1, 
t2, 
t3, 
t4, 
t5, 
t6, 
t7, 
t8, 
t9, 
t10, 
t11, 
t12, 
t13, 
t13, 
t14, 
t15, 
t16, 
t17, 
t18])

Thunder = ndimage.gaussian_filter(Thunder_max, sigma=2, order=0)

Ts1 = ndimage.gaussian_filter(t_1, sigma=1.5, order=0)
Ts2 = ndimage.gaussian_filter(t_2, sigma=1.5, order=0)
Ts3 = ndimage.gaussian_filter(t_3, sigma=1.5, order=0)
Ts4 = ndimage.gaussian_filter(t_4, sigma=1.5, order=0)
Ts5 = ndimage.gaussian_filter(t_5, sigma=1.5, order=0)
Ts6 = ndimage.gaussian_filter(t_6, sigma=1.5, order=0)
Ts7 = ndimage.gaussian_filter(t1, sigma=1.5, order=0)
Ts8 = ndimage.gaussian_filter(t2, sigma=1.5, order=0)
Ts9 = ndimage.gaussian_filter(t3, sigma=1.5, order=0)
Ts10 = ndimage.gaussian_filter(t4, sigma=1.5, order=0)
Ts11 = ndimage.gaussian_filter(t5, sigma=1.5, order=0)
Ts12 = ndimage.gaussian_filter(t6, sigma=1.5, order=0)
Ts13 = ndimage.gaussian_filter(t7, sigma=1.5, order=0)
Ts14 = ndimage.gaussian_filter(t8, sigma=1.5, order=0)
Ts15 = ndimage.gaussian_filter(t9, sigma=1.5, order=0)
Ts16 = ndimage.gaussian_filter(t10, sigma=1.5, order=0)
Ts17 = ndimage.gaussian_filter(t11, sigma=1.5, order=0)
Ts18 = ndimage.gaussian_filter(t12, sigma=1.5, order=0)
Ts19 = ndimage.gaussian_filter(t13, sigma=1.5, order=0)
Ts20 = ndimage.gaussian_filter(t14, sigma=1.5, order=0)
Ts21 = ndimage.gaussian_filter(t15, sigma=1.5, order=0)
Ts22 = ndimage.gaussian_filter(t16, sigma=1.5, order=0)
Ts23 = ndimage.gaussian_filter(t17, sigma=1.5, order=0)
Ts24 = ndimage.gaussian_filter(t18, sigma=1.5, order=0)


# In[414]:


fig = plt.figure (1,figsize=(20,22))
ax=plt.subplot(1,1,1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space
ax.set_extent ([-67.5, -74.5, 16.5, 20.5], data_crs)
ax.add_feature(cfeature.COASTLINE, linewidth=2.5)
ax.add_feature(cfeature.BORDERS, linewidth=3.5)
ax.add_feature(cfeature.OCEAN, facecolor='#00374d', zorder=1)
ax.add_feature(cfeature.LAND, facecolor='#b3b4b3')


#Filter2 = np.where(Thunder <= 20, max_crain_int == Thunder, max_EAS2p5)


colormap2 = matplotlib.colors.ListedColormap(['#b9eac3','#79c789','#478f55','#02757f', '#015057'])

clev = [15, 20, 60, 80, 100]

cf1 = ax.contourf(lons,lats, max_final_rain_int, clev, extend='neither', cmap=colormap2, transform=data_crs, 
                 norm=plt.Normalize(10, 100))

# Position color bar inside the image
cax = fig.add_axes([0.515, 0.28, 0.48, 0.04])  # Adjust the position as needed
cb = plt.colorbar(cf1, cax=cax, orientation='horizontal', extendrect='true', drawedges=True)
cb.set_ticks([])  # Hide the ticks

cb.outline.set_edgecolor('k')  # Set color of the outline
cb.outline.set_linewidth(3)  # Set the width of the outline
cb.dividers.set_color('k')  # Set color of the dividers
cb.dividers.set_linewidth(3)  # Set the width of the dividers

#cb = plt.colorbar(cf, ax=ax, orientation='horizontal',pad=0.01, extendrect='true', ticks=clev)
#cb.set_label(r'PORCIENTO', size='xx-large')

cs1 = ax.contour(lons, lats, max_final_rain_int, clev, colors='black',
              linestyles='solid', transform=data_crs, zorder=1,linewidths=2)
#ax.clabel(cs1, fmt='%d', fontsize=20)

#------------------------------------------------------------------------------------------------------
Filter = np.where(max_final_rain_int <= 5, 0, Thunder) 

colormap = matplotlib.colors.ListedColormap(['#fefea6','#ffff00','#ff8f00','#cc3300','#9f0101'])

clev = [20, 30, 40, 60, 80, 100]

cf = ax.contourf(lons,lats, Filter, clev, extend='neither', transform=data_crs, 
                norm=plt.Normalize(10, 100), cmap=colormap, alpha=1)

# Position color bar inside the image
cax = fig.add_axes([0.195, 0.23, 0.8, 0.04])  # Adjust the position as needed
cb = plt.colorbar(cf, cax=cax, orientation='horizontal', extendrect='true', drawedges=True)
cb.set_ticks([])  # Hide the ticks

cb.outline.set_edgecolor('k')  # Set color of the outline
cb.outline.set_linewidth(3)  # Set the width of the outline
cb.dividers.set_color('k')  # Set color of the dividers
cb.dividers.set_linewidth(3)  # Set the width of the dividers

#cb = plt.colorbar(cf, ax=ax, orientation='horizontal',pad=0.05, extendrect='true', ticks=clev)
#cb.set_label(r'PORCIENTO', size=16)
#cb.ax.tick_params(labelsize=16)

cs1 = ax.contour(lons, lats, Filter, clev, colors='black',
                linestyles='solid', transform=data_crs, linewidths=2, fontsize=40)
#ax.clabel(cs1, fmt='%d', fontsize=20)
ax.set_title(f'EVALUACIÓN DE PROBABILIDADES DE AGUACEROS Y TRONADAS (Experimental) - 24 HORAS (12AM - 12AM) \nVálido para este {fecha_formateada}',loc='left', fontsize=22, fontweight='bold')
ax.set_title(f'INIT: {hora_formateada} de este {fecha_formateada_dia_anterior}', loc='right', fontsize=16, fontweight='bold', style='italic')

shapefile2_path = 'shp/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=1)
ax.add_feature(county_RD)

text1 = ax.text(0.77, 0.215, 'PROBABILIDADES', ha='center', va='center', fontsize=40, transform=ax.transAxes, fontweight='bold', color='white')
text1.set_path_effects([matplotlib.patheffects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

text2 = ax.text(0.42, 0.14, 'Aguaceros', ha='center', va='center', fontsize=40, transform=ax.transAxes, fontweight='bold', color='white')
text2.set_path_effects([matplotlib.patheffects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

text3 = ax.text(0.11, 0.05, 'Tronadas', ha='center', va='center', fontsize=40, transform=ax.transAxes, fontweight='bold', color='white')
text3.set_path_effects([matplotlib.patheffects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

#text4 = ax.text(0.15, 0.05, 'Muy Baja', ha='center', va='center', fontsize=40, transform=ax.transAxes, fontweight='bold', color='white', zorder = 10)
#text4.set_path_effects([matplotlib.patheffects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

#text5 = ax.text(0.77, 0.22, 'PROBABILIDADES', ha='center', va='center', fontsize=40, transform=ax.transAxes, fontweight='bold', color='white')
#text5.set_path_effects([matplotlib.patheffects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect
#
#text6 = ax.text(0.77, 0.22, 'PROBABILIDADES', ha='center', va='center', fontsize=40, transform=ax.transAxes, fontweight='bold', color='white')
#text6.set_path_effects([matplotlib.patheffects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect
#
#text7 = ax.text(0.77, 0.22, 'PROBABILIDADES', ha='center', va='center', fontsize=40, transform=ax.transAxes, fontweight='bold', color='white')
#text7.set_path_effects([matplotlib.patheffects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect
#
#text8 = ax.text(0.77, 0.22, 'PROBABILIDADES', ha='center', va='center', fontsize=40, transform=ax.transAxes, fontweight='bold', color='white')
#text8.set_path_effects([matplotlib.patheffects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect
#
#text9 = ax.text(0.77, 0.22, 'PROBABILIDADES', ha='center', va='center', fontsize=40, transform=ax.transAxes, fontweight='bold', color='white')
#text9.set_path_effects([matplotlib.patheffects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect
#
#text10 = ax.text(0.77, 0.22, 'PROBABILIDADES', ha='center', va='center', fontsize=40, transform=ax.transAxes, fontweight='bold', color='white')
#text10.set_path_effects([matplotlib.patheffects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

fig.savefig(f'{save_path}/D1_TSRD_PROB-TRON_24_RD.png', bbox_inches='tight', dpi=300)


# In[415]:


import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from cartopy.feature import ShapelyFeature
from matplotlib import offsetbox
import matplotlib.patheffects as path_effects
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap

# Define the coordinate reference systems
map_crs = ccrs.PlateCarree()
data_crs = ccrs.PlateCarree()

# Create the figure and axis
fig = plt.figure(1, figsize=(20, 22))
ax = plt.subplot(1, 1, 1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space

# Set the extent of the map
ax.set_extent([-67.5, -72.5, 17.25, 20.25], crs=data_crs)

# Add features to the map
ax.add_feature(cfeature.COASTLINE, linewidth=3.5)
ax.add_feature(cfeature.BORDERS, linewidth=3.5, zorder=3)
ax.add_feature(cfeature.OCEAN, facecolor='#00374d', zorder=3)
ax.add_feature(cfeature.LAND, facecolor='#b3b4b3')
ax.add_feature(cfeature.LAKES, linewidth=2, zorder=3, edgecolor='black', alpha=1)

# Define colormap and contour levels for the first data set
colormap2 = matplotlib.colors.ListedColormap(['#b9eac3', '#79c789', '#478f55', '#02757f', '#015057'])
clev = [20, 60, 80, 100]

# Assuming lons, lats, max_final_rain_int, and Thunder are already defined
# If not, you need to define these variables
# lons = ...
# lats = ...
# max_final_rain_int = ...
# Thunder = ...

# Plot the filled contours
#cf1 = ax.contourf(lons, lats, max_final_rain_int, clev, extend='neither', cmap=colormap2, transform=data_crs, 
                 # norm=plt.Normalize(10, 100))

# Position and customize the color bar
#cax = fig.add_axes([0.515, 0.28, 0.48, 0.04])  # Adjust the position as needed
#cb = plt.colorbar(cf1, cax=cax, orientation='horizontal', extendrect='true', drawedges=True)
#cb.set_ticks([])  # Hide the ticks
#cb.outline.set_edgecolor('k')  # Set color of the outline
#cb.outline.set_linewidth(3)  # Set the width of the outline
#cb.dividers.set_color('k')  # Set color of the dividers
#cb.dividers.set_linewidth(3)  # Set the width of the dividers

# Add Dominican lakes (if the default lakes feature does not include them, create a custom one)
canada_lakes = cfeature.NaturalEarthFeature(
    category='physical',
    name='lakes',
    scale='10m',
    facecolor='none'
)
ax.add_feature(canada_lakes, edgecolor='black', linewidth=1)


# Plot the line contours
#cs1 = ax.contour(lons, lats, max_final_rain_int, clev, colors='black', linestyles='solid', transform=data_crs, zorder=1, linewidths=2)

# Further data filtering
Filter = np.where(max_final_rain_int <= 5, 0, Thunder)

# Define the second colormap and contour levels
colormap = matplotlib.colors.ListedColormap(['#fefea6', '#ffff00', '#ff8f00', '#cc3300', '#9f0101'])
clev = [20, 30, 40, 60, 80, 100]

# Plot the second set of filled contours
cf = ax.contourf(lons, lats, Filter, clev, extend='neither', transform=data_crs, norm=plt.Normalize(10, 100), cmap=colormap, alpha=1)

# Position and customize the second color bar
cax = fig.add_axes([0.1, 0.245, 0.8, 0.04], zorder=0)  # Adjust the position as needed
cb = plt.colorbar(cf, cax=cax, orientation='horizontal', extendrect='true', drawedges=True)
cb.set_ticks([20, 30, 40, 60, 80, 100])  # Hide the ticks
cb.ax.xaxis.set_tick_params(color='white')
plt.setp(plt.getp(cb.ax, 'xticklabels'), color='white', fontsize=20, fontweight='bold')
cb.outline.set_edgecolor('k')  # Set color of the outline
cb.outline.set_linewidth(3)  # Set the width of the outline
cb.dividers.set_color('k')  # Set color of the dividers
cb.dividers.set_linewidth(3)  # Set the width of the dividers

# Plot the second set of line contours
cs1 = ax.contour(lons, lats, Filter, clev, colors='black', linestyles='solid', transform=data_crs, linewidths=2, fontsize=40)

# Set titles for the plot
#ax.set_title(f'EVALUACIÓN DE PROBABILIDADES DE TRONADAS - 24 HORAS (12AM - 12AM) \nVálido para este {fecha_formateada}', loc='left', fontsize=22, fontweight='bold')
#ax.set_title(f'INIT: {hora_formateada} de este {fecha_formateada_dia_anterior}', loc='right', fontsize=16, fontweight='bold', style='italic')

# Add shapefile data
shapefile2_path = 'shp/rd/geoBoundaries-DOM-ADM1_simplified.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=1.5)
ax.add_feature(county_RD)

# Add shapefile data
shapefile3_path = 'shp/haiti/ne_10m_admin_0_countries.shp'
gdf3 = gpd.read_file(shapefile3_path)
county_HTI = ShapelyFeature(gdf3['geometry'], ccrs.PlateCarree(), facecolor='grey', edgecolor='black', lw=1, zorder=2)
ax.add_feature(county_HTI)

# Dictionary of important cities with their coordinates
cities = {
    "Santo Domingo": {"lat": 18.4861, "lon": -69.9312},
    "Santiago": {"lat": 19.4792, "lon": -70.6931},
    "La Romana": {"lat": 18.4333, "lon": -68.9667},
    "Punta Cana": {"lat": 18.582, "lon": -68.4055},
    "Puerto Plata": {"lat": 19.7975, "lon": -70.6884},
    "La Vega": {"lat": 19.2232, "lon": -70.5294},
    "Bonao": {"lat": 18.9356, "lon": -70.4094},
    "Baní": {"lat": 18.2796, "lon": -70.3319},
    "Azua": {"lat": 18.4532, "lon": -70.7349},
    "Barahona": {"lat": 18.2085, "lon": -71.1008},
    "Montecristi": {"lat": 19.8489, "lon": -71.6464},
    "Dajabón": {"lat": 19.5483, "lon": -71.7083},
    "Samaná": {"lat": 19.2057, "lon": -69.3367},
    "V. Altagracia": {"lat": 18.6700, "lon": -70.1700},
    "El Seibo": {"lat": 18.7650, "lon": -69.0383},
    "Nagua": {"lat": 19.3833, "lon": -69.8500},
    "San Juan": {"lat": 18.8050, "lon": -71.2300},
    "Pedernales": {"lat": 18.0370, "lon": -71.7440},
    "Ocoa": {"lat": 18.5500, "lon": -70.5000},
    "Oviedo": {"lat": 17.8007, "lon": -71.4008},
    "S. de la Mar": {"lat": 19.0579, "lon": -69.3892},
    "Monte Plata": {"lat": 18.8073, "lon": -69.7850},
    "Pimentel": {"lat": 19.1832, "lon": -70.1085},
    "Mao": {"lat": 19.5511, "lon": -71.0781},
    "Neyba": {"lat": 18.4847, "lon": -71.4194},
    "Pedro Santana": {"lat": 19.1050, "lon": -71.6959},
    "Elías Piña": {"lat": 18.8770, "lon": -71.7048},
    "Restauración": {"lat": 19.3159, "lon": -71.6947},
    "SAJOMA": {"lat": 19.3405, "lon": -70.9376}
}

# Add city names and dots to the plot
for city, coords in cities.items():
    ax.plot(coords["lon"], coords["lat"], 'o', color='k', markersize=10, transform=data_crs, path_effects=[path_effects.withStroke(linewidth=5, foreground='white')])  # Add a red dot
    ax.text(coords["lon"], coords["lat"], city, transform=data_crs, fontsize=22, fontweight='bold',
            ha='left', color='white', path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])

# Dictionary of important cities with their coordinates
cities2 = {
    "Higuey": {"lat": 18.6150, "lon": -68.7070},
    "Constanza": {"lat": 18.9094, "lon": -70.7208},

}

# Add city names and dots to the plot
for city, coords in cities2.items():
    ax.plot(coords["lon"], coords["lat"], 'o', color='k', markersize=10, transform=data_crs, path_effects=[path_effects.withStroke(linewidth=5, foreground='white')])  # Add a red dot
    ax.text(coords["lon"], coords["lat"], city, transform=data_crs, fontsize=22, fontweight='bold',
            ha='right', color='white', path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])

# Add text annotations
text1 = ax.text(0.5, 0.125, 'PROBABILIDADES', ha='center', va='center', fontsize=40, transform=ax.transAxes, fontweight='bold', color='white')
text1.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

text2 = ax.text(0.84, 0.75, f'Válidez del Mapa: \n 12:00 AM - 12:00 AM del \n {fecha_formateada}', ha='center', va='center', fontsize=25, transform=ax.transAxes, fontweight='bold', color='white')
text2.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

text4 = ax.text(0.84, 0.985, f'INIT: {hora_formateada} de este {fecha_formateada_dia_anterior}', ha='center', va='center', fontsize=16, transform=ax.transAxes, fontweight='bold', color='white')
text4.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

text3 = ax.text(0.32, 0.95, 'MAPA DE PROBABILIDADES DE TRONADAS', ha='center', va='center', fontsize=35, transform=ax.transAxes, fontweight='bold', color='white', zorder=5)
text3.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

def add_rounded_rect_with_shadow(ax, xy, width, height, rounding_size=0.1, shadow_offset=(0.02, -0.02)):
    # Add shadow
    shadow = FancyBboxPatch(
        (xy[0] + shadow_offset[0], xy[1] + shadow_offset[1]), width, height,
        boxstyle=f"round,pad=0.05,rounding_size={rounding_size}",
        edgecolor='none', facecolor='black', alpha=0.3,
        transform=data_crs, zorder=3
    )
    ax.add_patch(shadow)

    # Add rectangle
    rect = FancyBboxPatch(
        xy, width, height,
        boxstyle=f"round,pad=0.05,rounding_size={rounding_size}",
        edgecolor='k', facecolor='#ff8f00', alpha=1,
        transform=data_crs, linewidth=2, zorder=4
    )
    ax.add_patch(rect)

# Define the position and size of the rectangle
rect_xy = (-72.4, 20.05)
rect_width = 3
rect_height = 0.1

# Add the rectangle with shadow to the plot
add_rounded_rect_with_shadow(ax, rect_xy, rect_width, rect_height)

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

# Save the figure
fig.savefig(f'{save_path}/D1_TSRD_PROB-TRON_24_RD.png', bbox_inches='tight', dpi=300)


# In[416]:


import matplotlib.colors as mcolors

fig = plt.figure (1,figsize=(20,20))
ax=plt.subplot(1,1,1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space
ax.set_extent ([-67.5, -74.5, 17.25, 20.5], data_crs)
ax.add_feature(cfeature.STATES, linewidth=2)
ax.add_feature(cfeature.BORDERS, linewidth=2)
#ax.set_aspect("equal", "datalim")

colormap = matplotlib.colors.ListedColormap(['#00eded','#00a1f5','#0000f5','#00ff00','#00c700','#008f00','#ffff00',
                                             '#e8bf00','#ff8f00','#ff0000','#cc3300','#990000','#ff00ff','#9933cc'])

# Read RGB values from file, skipping the first line
#with open("BkBlAqGrYeOrReViWh200.rgb") as f:
#    rgb_values = np.genfromtxt(f, skip_header=1)

# Normalize RGB values to range [0, 1]
#rgb_values_normalized = rgb_values / 255.0

# Create colormap
#colormap = mcolors.LinearSegmentedColormap.from_list("custom_colormap", rgb_values_normalized)

#clev = [20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 
        #60, 62, 64, 66, 68, 70, 72]

clev2 = [30, 40, 60, 80, 100]

clev3 = range(20, 80, 5)

cf = ax.contourf(lons,lats,REFD_max_value, clev3, extend='neither', cmap=colormap, 
                 norm=plt.Normalize(5, 75), transform=data_crs)


cb = plt.colorbar(cf, ax=ax,  orientation='horizontal', pad=0.05, extendrect='True', ticks=clev3)
cb.set_label(r'Milimetros', size='20')
cb.ax.tick_params(labelsize='20')

cs1 = ax.contour(lons, lats, Filter, clev2, colors='black',
                 linestyles='solid', transform=data_crs, linewidths=2.5)
ax.set_title(f'REFD & THUNDER 24 HORAS | 12AM - 12AM \n{fecha_formateada} | DATA: {hora_formateada}', fontsize=22)
ax.clabel(cs1, fmt='%d', fontsize=25)

# PR COUNTIES SHAPEFILES
shapefile1_path = 'shp/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp'
gdf1 = gpd.read_file(shapefile1_path)
county_PR = ShapelyFeature(gdf1['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_PR)

shapefile2_path = 'shp/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_RD)

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

plt.show()
plt.show()

fig.savefig(f'{save_path}/D1_TSRD_REFD_PROB-TRON_24_RD.png', bbox_inches='tight', dpi=300)


# In[417]:


import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from cartopy.feature import ShapelyFeature
from matplotlib import offsetbox
import matplotlib.patheffects as path_effects

# Define the coordinate reference systems
map_crs = ccrs.PlateCarree()
data_crs = ccrs.PlateCarree()

# Create the figure and axis
fig = plt.figure(1, figsize=(20, 22))
ax = plt.subplot(1, 1, 1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space

# Set the extent of the map
ax.set_extent([-67.5, -72.5, 17.25, 20.25], crs=data_crs)

# Add features to the map
ax.add_feature(cfeature.COASTLINE, linewidth=3.5)
ax.add_feature(cfeature.BORDERS, linewidth=3.5, zorder=3)
ax.add_feature(cfeature.OCEAN, facecolor='#00374d', zorder=3)
ax.add_feature(cfeature.LAND, facecolor='#b3b4b3')
ax.add_feature(cfeature.LAKES, linewidth=2, zorder=3, edgecolor='black', alpha=1)

# Define colormap and contour levels for the first data set
colormap = matplotlib.colors.ListedColormap(['#00eded','#00a1f5','#0000f5','#00ff00','#00c700','#008f00','#ffff00',
                                             '#e8bf00','#ff8f00','#ff0000','#cc3300','#990000','#ff00ff','#9933cc'])

# Assuming lons, lats, max_final_rain_int, and Thunder are already defined
# If not, you need to define these variables
# lons = ...
# lats = ...
# max_final_rain_int = ...
# Thunder = ...

# Plot the filled contours
#cf1 = ax.contourf(lons, lats, max_final_rain_int, clev, extend='neither', cmap=colormap2, transform=data_crs, 
                 # norm=plt.Normalize(10, 100))

# Position and customize the color bar
#cax = fig.add_axes([0.515, 0.28, 0.48, 0.04])  # Adjust the position as needed
#cb = plt.colorbar(cf1, cax=cax, orientation='horizontal', extendrect='true', drawedges=True)
#cb.set_ticks([])  # Hide the ticks
#cb.outline.set_edgecolor('k')  # Set color of the outline
#cb.outline.set_linewidth(3)  # Set the width of the outline
#cb.dividers.set_color('k')  # Set color of the dividers
#cb.dividers.set_linewidth(3)  # Set the width of the dividers

# Add Dominican lakes (if the default lakes feature does not include them, create a custom one)
canada_lakes = cfeature.NaturalEarthFeature(
    category='physical',
    name='lakes',
    scale='10m',
    facecolor='none'
)
ax.add_feature(canada_lakes, edgecolor='black', linewidth=1)


clev2 = [20, 40, 60, 80, 100]

clev3 = range(20, 80, 5)

cf = ax.contourf(lons,lats,REFD_max_value, clev3, extend='neither', cmap=colormap, 
                 norm=plt.Normalize(5, 75), transform=data_crs)

cs1 = ax.contour(lons, lats, Filter, clev2, colors='black',
                 linestyles='solid', transform=data_crs, linewidths=3.5)
ax.clabel(cs1, fmt='%d', fontsize=25)

# Position and customize the second color bar
cax = fig.add_axes([0.1, 0.23, 0.8, 0.04], zorder=0)  # Adjust the position as needed
cb = plt.colorbar(cf, cax=cax, orientation='horizontal', extendrect='true', drawedges=True)
cb.set_ticks([])  # Hide the ticks
cb.outline.set_edgecolor('k')  # Set color of the outline
cb.outline.set_linewidth(3)  # Set the width of the outline
cb.dividers.set_color('k')  # Set color of the dividers
cb.dividers.set_linewidth(3)  # Set the width of the dividers

# Plot the second set of line contours
#cs1 = ax.contour(lons, lats, SS_maxSMT, clev, colors='black', linestyles='solid', transform=data_crs, linewidths=2, fontsize=40)

# Set titles for the plot
ax.set_title(f'REFLECTIVIDAD 1KM MÁXIMA DE LOS MIEMBROS DEL CONJUNTO & PROBS. DE TRONADAS 24 HORAS (12AM - 12AM) \nVálido para este {fecha_formateada}', loc='left', fontsize=22, fontweight='bold')
ax.set_title(f'INIT: {hora_formateada} de este {fecha_formateada_dia_anterior}', loc='right', fontsize=16, fontweight='bold', style='italic')

# Add shapefile data
shapefile2_path = 'shp/rd/geoBoundaries-DOM-ADM1_simplified.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=1.5)
ax.add_feature(county_RD)

# Add shapefile data
shapefile3_path = 'shp/haiti/ne_10m_admin_0_countries.shp'
gdf3 = gpd.read_file(shapefile3_path)
county_HTI = ShapelyFeature(gdf3['geometry'], ccrs.PlateCarree(), facecolor='grey', edgecolor='black', lw=1, zorder=2)
ax.add_feature(county_HTI)

# Dictionary of important cities with their coordinates
cities = {
    "Santo Domingo": {"lat": 18.4861, "lon": -69.9312},
    "Santiago": {"lat": 19.4792, "lon": -70.6931},
    "La Romana": {"lat": 18.4333, "lon": -68.9667},
    "Punta Cana": {"lat": 18.582, "lon": -68.4055},
    "Puerto Plata": {"lat": 19.7975, "lon": -70.6884},
    "La Vega": {"lat": 19.2232, "lon": -70.5294},
    "Bonao": {"lat": 18.9356, "lon": -70.4094},
    "Baní": {"lat": 18.2796, "lon": -70.3319},
    "Azua": {"lat": 18.4532, "lon": -70.7349},
    "Barahona": {"lat": 18.2085, "lon": -71.1008},
    "Montecristi": {"lat": 19.8489, "lon": -71.6464},
    "Dajabón": {"lat": 19.5483, "lon": -71.7083},
    "Samaná": {"lat": 19.2057, "lon": -69.3367},
    "V. Altagracia": {"lat": 18.6700, "lon": -70.1700},
    "El Seibo": {"lat": 18.7650, "lon": -69.0383},
    "Nagua": {"lat": 19.3833, "lon": -69.8500},
    "San Juan": {"lat": 18.8050, "lon": -71.2300},
    "Pedernales": {"lat": 18.0370, "lon": -71.7440},
    "Ocoa": {"lat": 18.5500, "lon": -70.5000},
    "Oviedo": {"lat": 17.8007, "lon": -71.4008},
    "S. de la Mar": {"lat": 19.0579, "lon": -69.3892},
    "Monte Plata": {"lat": 18.8073, "lon": -69.7850},
    "Pimentel": {"lat": 19.1832, "lon": -70.1085},
    "Mao": {"lat": 19.5511, "lon": -71.0781},
    "Neyba": {"lat": 18.4847, "lon": -71.4194},
    "Pedro Santana": {"lat": 19.1050, "lon": -71.6959},
    "Elías Piña": {"lat": 18.8770, "lon": -71.7048},
    "Restauración": {"lat": 19.3159, "lon": -71.6947},
    "SAJOMA": {"lat": 19.3405, "lon": -70.9376}
}

# Add city names and dots to the plot
for city, coords in cities.items():
    ax.plot(coords["lon"], coords["lat"], 'o', color='k', markersize=10, transform=data_crs, path_effects=[path_effects.withStroke(linewidth=5, foreground='white')])  # Add a red dot
    ax.text(coords["lon"], coords["lat"], city, transform=data_crs, fontsize=22, fontweight='bold',
            ha='left', color='white', path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])

# Dictionary of important cities with their coordinates
cities2 = {
    "Higuey": {"lat": 18.6150, "lon": -68.7070},
    "Constanza": {"lat": 18.9094, "lon": -70.7208},

}

# Add city names and dots to the plot
for city, coords in cities2.items():
    ax.plot(coords["lon"], coords["lat"], 'o', color='k', markersize=10, transform=data_crs, path_effects=[path_effects.withStroke(linewidth=5, foreground='white')])  # Add a red dot
    ax.text(coords["lon"], coords["lat"], city, transform=data_crs, fontsize=22, fontweight='bold',
            ha='right', color='white', path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])

# Add text annotations
text1 = ax.text(0.5, 0.11, 'ECOS DE REFLECTIVIDAD MÁXIMOS SIMULADOS A 1KM', ha='center', va='center', fontsize=30, transform=ax.transAxes, fontweight='bold', color='white')
text1.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

#text3 = ax.text(0.11, 0.05, 'Tronadas', ha='center', va='center', fontsize=40, transform=ax.transAxes, fontweight='bold', color='white')
#text3.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

# Save the figure
fig.savefig(f'{save_path}/D1_TSRD_PROB-TRON_24_RD.png', bbox_inches='tight', dpi=300)


# In[418]:


def plot_background(ax):
    ax.set_extent([-67.5, -72.5, 17.25, 20.25])
    ax.add_feature(cfeature.COASTLINE, linewidth=1.5)
    ax.add_feature(cfeature.BORDERS, linewidth=2, zorder=3)
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(cfeature.OCEAN, facecolor='#00374d', zorder=1)
    ax.add_feature(cfeature.LAND, facecolor='#b3b4b3')
    ax.add_feature(cfeature.LAKES, linewidth=2, zorder=3, edgecolor='black', alpha=1)

    return ax


fig, axarr = plt.subplots(nrows=4, ncols=3, figsize=(18, 22), constrained_layout=True,
                          subplot_kw={'projection': map_crs})
axlist = axarr.flatten()
for ax in axlist:
    plot_background(ax)

colormap = matplotlib.colors.ListedColormap(['#00eded','#00a1f5','#0000f5','#00ff00','#00c700','#008f00','#ffff00','#e8bf00','#ff8f00','#ff0000','#cc3300','#990000','#ff00ff','#9933cc'])
clev = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
clev2 = [20, 40, 80, 100] #20%,40%,60%,80%,100%

# 1
cf1 = axlist[0].contourf(lons, lats, REFD_1, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                         norm=plt.Normalize(5, 75))
c1 = axlist[0].contour(lons, lats, Ts1, clev2,  colors='black', linewidths=1.8,transform=ccrs.PlateCarree())
axlist[0].clabel(c1, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[0].set_title('REFD 12AM', fontsize=16)
cb1 = fig.colorbar(cf1, ax=axlist[0], orientation='horizontal', shrink=0.74, pad=0)
cb1.set_label('dBZ', size='x-large')

# 2
cf2 = axlist[1].contourf(lons, lats, REFD_2, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c2 = axlist[1].contour(lons, lats, Ts2, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c2, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[1].set_title('REFD 01AM', fontsize=16)
cb2 = fig.colorbar(cf2, ax=axlist[1], orientation='horizontal', shrink=0.74, pad=0)
cb2.set_label('dBZ', size='x-large')

# 3
cf3 = axlist[2].contourf(lons, lats, REFD_3, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c3 = axlist[2].contour(lons, lats, Ts3, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[2].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[2].set_title('REFD 02AM', fontsize=16)
cb3 = fig.colorbar(cf3, ax=axlist[2], orientation='horizontal', shrink=0.74, pad=0)
cb3.set_label('dBZ', size='x-large')

# 4
cf4 = axlist[3].contourf(lons, lats, REFD_4, clev, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
axlist[3].set_title('REFD 03AM', fontsize=16)
c4 = axlist[3].contour(lons, lats, Ts4, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb4 = fig.colorbar(cf4, ax=axlist[3], orientation='horizontal', shrink=0.74, pad=0)
cb4.set_label('dBZ', size='x-large')

# 5
cf5 = axlist[4].contourf(lons, lats, REFD_5, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c5 = axlist[4].contour(lons, lats, Ts5, clev2,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[4].clabel(c5, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[4].set_title('REFD 04AM', fontsize=16)
cb5 = fig.colorbar(cf5, ax=axlist[4], orientation='horizontal', shrink=0.74, pad=0)
cb5.set_label('dBZ', size='x-large')

# 6
cf6 = axlist[5].contourf(lons, lats, REFD_6, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c6 = axlist[5].contour(lons, lats, Ts6, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[5].clabel(c6, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[5].set_title('REFD 05AM', fontsize=16)
cb6 = fig.colorbar(cf6, ax=axlist[5], orientation='horizontal', shrink=0.74, pad=0)
cb6.set_label('dBZ', size='x-large')

# 7
cf7 = axlist[6].contourf(lons, lats, REFD1, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
axlist[6].set_title('REFD 06AM', fontsize=16)
c7 = axlist[6].contour(lons, lats, Ts7, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[6].clabel(c7, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb7 = fig.colorbar(cf7, ax=axlist[6], orientation='horizontal', shrink=0.74, pad=0)
cb7.set_label('dBZ', size='x-large')

# 8
cf8 = axlist[7].contourf(lons, lats, REFD2, clev, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
axlist[7].set_title('REFD 07AM', fontsize=16)
c8 = axlist[7].contour(lons, lats, Ts8, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[7].clabel(c8, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb8 = fig.colorbar(cf8, ax=axlist[7], orientation='horizontal', shrink=0.74, pad=0)
cb8.set_label('dBZ', size='x-large')

# 9
cf9 = axlist[8].contourf(lons, lats, REFD3, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c9 = axlist[8].contour(lons, lats, Ts9, clev2,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[8].clabel(c9, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[8].set_title('REFD 08AM', fontsize=16)
cb9 = fig.colorbar(cf9, ax=axlist[8], orientation='horizontal', shrink=0.74, pad=0)
cb9.set_label('dBZ', size='x-large')

# 10
cf10 = axlist[9].contourf(lons, lats, REFD4, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c10 = axlist[9].contour(lons, lats, Ts10, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[9].clabel(c10, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[9].set_title('REFD 09AM', fontsize=16)
cb10 = fig.colorbar(cf10, ax=axlist[9], orientation='horizontal', shrink=0.74, pad=0)
cb10.set_label('dBZ', size='x-large')

# 11
cf11 = axlist[10].contourf(lons, lats, REFD5, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
axlist[10].set_title('REFD 10AM', fontsize=16)
c11 = axlist[10].contour(lons, lats, Ts11, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[10].clabel(c11, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb11 = fig.colorbar(cf11, ax=axlist[10], orientation='horizontal', shrink=0.74, pad=0)
cb11.set_label('dBZ', size='x-large')

# 12
cf12 = axlist[11].contourf(lons, lats, REFD6, clev, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
axlist[11].set_title('REFD 11AM', fontsize=16)
c12 = axlist[11].contour(lons, lats, Ts12, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[11].clabel(c12, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb12 = fig.colorbar(cf12, ax=axlist[11], orientation='horizontal', shrink=0.74, pad=0)
cb12.set_label('dBZ', size='x-large')

fig.suptitle(f'REFLECTIVIDAD DERIVADA 1KM & PROBABILIDAD DE TRONADAS (Madrugada-Mañana)\nVálido para este {fecha_formateada} \n\nINIT: {hora_formateada} de este {fecha_formateada_dia_anterior}\n', fontsize=20)

fig.savefig(f'{save_path}/D1_TSRD_REFD_12_PERIOD_MM_RD.png', bbox_inches='tight', dpi=600)


# In[419]:


def plot_background(ax):
    ax.set_extent([-67.5, -72.5, 17.25, 20.25])
    ax.add_feature(cfeature.COASTLINE, linewidth=1.5)
    ax.add_feature(cfeature.BORDERS, linewidth=2, zorder=3)
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(cfeature.OCEAN, facecolor='#00374d', zorder=1)
    ax.add_feature(cfeature.LAND, facecolor='#b3b4b3')
    ax.add_feature(cfeature.LAKES, linewidth=2, zorder=3, edgecolor='black', alpha=1)

    return ax


fig, axarr = plt.subplots(nrows=4, ncols=3, figsize=(18, 22), constrained_layout=True,
                          subplot_kw={'projection': map_crs})
axlist = axarr.flatten()
for ax in axlist:
    plot_background(ax)

colormap = matplotlib.colors.ListedColormap(['#00eded','#00a1f5','#0000f5','#00ff00','#00c700','#008f00','#ffff00','#e8bf00','#ff8f00','#ff0000','#cc3300','#990000','#ff00ff','#9933cc'])
clev = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
clev2 = [20, 40, 80, 100] #20%,40%,60%,80%,100%

# 1
cf1 = axlist[0].contourf(lons, lats, REFD7, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                         norm=plt.Normalize(5, 75))
c1 = axlist[0].contour(lons, lats, Ts13, clev2,  colors='black', linewidths=1.8,transform=ccrs.PlateCarree())
axlist[0].clabel(c1, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[0].set_title('REFD 12PM', fontsize=16)
cb1 = fig.colorbar(cf1, ax=axlist[0], orientation='horizontal', shrink=0.74, pad=0)
cb1.set_label('dBZ', size='x-large')

# 2
cf2 = axlist[1].contourf(lons, lats, REFD8, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c2 = axlist[1].contour(lons, lats, Ts14, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c2, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[1].set_title('REFD 01PM', fontsize=16)
cb2 = fig.colorbar(cf2, ax=axlist[1], orientation='horizontal', shrink=0.74, pad=0)
cb2.set_label('dBZ', size='x-large')

# 3
cf3 = axlist[2].contourf(lons, lats, REFD9, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c3 = axlist[2].contour(lons, lats, Ts15, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[2].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[2].set_title('REFD 02PM', fontsize=16)
cb3 = fig.colorbar(cf3, ax=axlist[2], orientation='horizontal', shrink=0.74, pad=0)
cb3.set_label('dBZ', size='x-large')

# 4
cf4 = axlist[3].contourf(lons, lats, REFD10, clev, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
axlist[3].set_title('REFD 03PM', fontsize=16)
c4 = axlist[3].contour(lons, lats, Ts16, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb4 = fig.colorbar(cf4, ax=axlist[3], orientation='horizontal', shrink=0.74, pad=0)
cb4.set_label('dBZ', size='x-large')

# 5
cf5 = axlist[4].contourf(lons, lats, REFD11, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c5 = axlist[4].contour(lons, lats, Ts17, clev2,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[4].clabel(c5, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[4].set_title('REFD 04PM', fontsize=16)
cb5 = fig.colorbar(cf5, ax=axlist[4], orientation='horizontal', shrink=0.74, pad=0)
cb5.set_label('dBZ', size='x-large')

# 6
cf6 = axlist[5].contourf(lons, lats, REFD12, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c6 = axlist[5].contour(lons, lats, Ts18, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[5].clabel(c6, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[5].set_title('REFD 05PM', fontsize=16)
cb6 = fig.colorbar(cf6, ax=axlist[5], orientation='horizontal', shrink=0.74, pad=0)
cb6.set_label('dBZ', size='x-large')

# 7
cf7 = axlist[6].contourf(lons, lats, REFD13, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
axlist[6].set_title('REFD 06PM', fontsize=16)
c7 = axlist[6].contour(lons, lats, Ts19, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[6].clabel(c7, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb7 = fig.colorbar(cf7, ax=axlist[6], orientation='horizontal', shrink=0.74, pad=0)
cb7.set_label('dBZ', size='x-large')

# 8
cf8 = axlist[7].contourf(lons, lats, REFD14, clev, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
axlist[7].set_title('REFD 07PM', fontsize=16)
c8 = axlist[7].contour(lons, lats, Ts20, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[7].clabel(c8, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb8 = fig.colorbar(cf8, ax=axlist[7], orientation='horizontal', shrink=0.74, pad=0)
cb8.set_label('dBZ', size='x-large')

# 9
cf9 = axlist[8].contourf(lons, lats, REFD15, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c9 = axlist[8].contour(lons, lats, Ts21, clev2,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[8].clabel(c9, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[8].set_title('REFD 08PM', fontsize=16)
cb9 = fig.colorbar(cf9, ax=axlist[8], orientation='horizontal', shrink=0.74, pad=0)
cb9.set_label('dBZ', size='x-large')

# 10
cf10 = axlist[9].contourf(lons, lats, REFD16, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c10 = axlist[9].contour(lons, lats, Ts22, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[9].clabel(c10, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[9].set_title('REFD 09PM', fontsize=16)
cb10 = fig.colorbar(cf10, ax=axlist[9], orientation='horizontal', shrink=0.74, pad=0)
cb10.set_label('dBZ', size='x-large')

# 11
cf11 = axlist[10].contourf(lons, lats, REFD17, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
axlist[10].set_title('REFD 10PM', fontsize=16)
c11 = axlist[10].contour(lons, lats, Ts23, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[10].clabel(c11, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb11 = fig.colorbar(cf11, ax=axlist[10], orientation='horizontal', shrink=0.74, pad=0)
cb11.set_label('dBZ', size='x-large')

# 12
cf12 = axlist[11].contourf(lons, lats, REFD18, clev, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
axlist[11].set_title('REFD 11PM', fontsize=16)
c12 = axlist[11].contour(lons, lats, Ts24, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[11].clabel(c12, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb12 = fig.colorbar(cf12, ax=axlist[11], orientation='horizontal', shrink=0.74, pad=0)
cb12.set_label('dBZ', size='x-large')

fig.suptitle(f'REFLECTIVIDAD DERIVADA 1KM & PROBABILIDAD DE TRONADAS (Tarde-Noche)\nVálido para este {fecha_formateada} \n\nINIT: {hora_formateada} de este {fecha_formateada_dia_anterior}\n', fontsize=20)

fig.savefig(f'{save_path}/D1_TSRD_REFD_12_PERIOD_TN_RD.png', bbox_inches='tight', dpi=300)


# In[420]:


#--------------------------------------- SUB-SEVERE WEATHER PROBS ---------------------------------------


# In[421]:


tenmw20_prob_1 = prob_1.select(name="10 metre wind speed")[0]
tenmw20_prob_2 = prob_2.select(name="10 metre wind speed")[0]
tenmw20_prob_3 = prob_3.select(name="10 metre wind speed")[0]
tenmw20_prob_4 = prob_4.select(name="10 metre wind speed")[0]
tenmw20_prob_5 = prob_5.select(name="10 metre wind speed")[0]
tenmw20_prob_6 = prob_6.select(name="10 metre wind speed")[0]
tenmw20_prob1 = prob1.select(name="10 metre wind speed")[0]
tenmw20_prob2 = prob2.select(name="10 metre wind speed")[0]
tenmw20_prob3 = prob3.select(name="10 metre wind speed")[0]
tenmw20_prob4 = prob4.select(name="10 metre wind speed")[0]
tenmw20_prob5 = prob5.select(name="10 metre wind speed")[0]
tenmw20_prob6 = prob6.select(name="10 metre wind speed")[0]
tenmw20_prob7 = prob7.select(name="10 metre wind speed")[0]
tenmw20_prob8 = prob8.select(name="10 metre wind speed")[0]
tenmw20_prob9 = prob9.select(name="10 metre wind speed")[0]
tenmw20_prob10 = prob10.select(name="10 metre wind speed")[0]
tenmw20_prob11 = prob11.select(name="10 metre wind speed")[0]
tenmw20_prob12 = prob12.select(name="10 metre wind speed")[0]
tenmw20_prob13 = prob13.select(name="10 metre wind speed")[0]
tenmw20_prob14 = prob14.select(name="10 metre wind speed")[0]
tenmw20_prob15 = prob15.select(name="10 metre wind speed")[0]
tenmw20_prob16 = prob16.select(name="10 metre wind speed")[0]
tenmw20_prob17 = prob17.select(name="10 metre wind speed")[0]
tenmw20_prob18 = prob18.select(name="10 metre wind speed")[0]

tenmw20_value_1 = tenmw20_prob_1.values
tenmw20_value_2 = tenmw20_prob_2.values
tenmw20_value_3 = tenmw20_prob_3.values
tenmw20_value_4 = tenmw20_prob_4.values
tenmw20_value_5 = tenmw20_prob_5.values
tenmw20_value_6 = tenmw20_prob_6.values
tenmw20_value1 = tenmw20_prob1.values
tenmw20_value2 = tenmw20_prob2.values
tenmw20_value3 = tenmw20_prob3.values
tenmw20_value4 = tenmw20_prob4.values
tenmw20_value5 = tenmw20_prob5.values
tenmw20_value6 = tenmw20_prob6.values
tenmw20_value7 = tenmw20_prob7.values
tenmw20_value8 = tenmw20_prob8.values
tenmw20_value9 = tenmw20_prob9.values
tenmw20_value10 = tenmw20_prob10.values
tenmw20_value11 = tenmw20_prob11.values
tenmw20_value12 = tenmw20_prob12.values
tenmw20_value13 = tenmw20_prob13.values
tenmw20_value14 = tenmw20_prob14.values
tenmw20_value15 = tenmw20_prob15.values
tenmw20_value16 = tenmw20_prob16.values
tenmw20_value17 = tenmw20_prob17.values
tenmw20_value18 = tenmw20_prob18.values

tenmw30_prob_1 = prob_1.select(name="10 metre wind speed")[1]
tenmw30_prob_2 = prob_2.select(name="10 metre wind speed")[1]
tenmw30_prob_3 = prob_3.select(name="10 metre wind speed")[1]
tenmw30_prob_4 = prob_4.select(name="10 metre wind speed")[1]
tenmw30_prob_5 = prob_5.select(name="10 metre wind speed")[1]
tenmw30_prob_6 = prob_6.select(name="10 metre wind speed")[1]
tenmw30_prob1 = prob1.select(name="10 metre wind speed")[1]
tenmw30_prob2 = prob2.select(name="10 metre wind speed")[1]
tenmw30_prob3 = prob3.select(name="10 metre wind speed")[1]
tenmw30_prob4 = prob4.select(name="10 metre wind speed")[1]
tenmw30_prob5 = prob5.select(name="10 metre wind speed")[1]
tenmw30_prob6 = prob6.select(name="10 metre wind speed")[1]
tenmw30_prob7 = prob7.select(name="10 metre wind speed")[1]
tenmw30_prob8 = prob8.select(name="10 metre wind speed")[1]
tenmw30_prob9 = prob9.select(name="10 metre wind speed")[1]
tenmw30_prob10 = prob10.select(name="10 metre wind speed")[1]
tenmw30_prob11 = prob11.select(name="10 metre wind speed")[1]
tenmw30_prob12 = prob12.select(name="10 metre wind speed")[1]
tenmw30_prob13 = prob13.select(name="10 metre wind speed")[1]
tenmw30_prob14 = prob14.select(name="10 metre wind speed")[1]
tenmw30_prob15 = prob15.select(name="10 metre wind speed")[1]
tenmw30_prob16 = prob16.select(name="10 metre wind speed")[1]
tenmw30_prob17 = prob17.select(name="10 metre wind speed")[1]
tenmw30_prob18 = prob18.select(name="10 metre wind speed")[1]

tenmw30_value_1 = tenmw30_prob_1.values
tenmw30_value_2 = tenmw30_prob_2.values
tenmw30_value_3 = tenmw30_prob_3.values
tenmw30_value_4 = tenmw30_prob_4.values
tenmw30_value_5 = tenmw30_prob_5.values
tenmw30_value_6 = tenmw30_prob_6.values
tenmw30_value1 = tenmw30_prob1.values
tenmw30_value2 = tenmw30_prob2.values
tenmw30_value3 = tenmw30_prob3.values
tenmw30_value4 = tenmw30_prob4.values
tenmw30_value5 = tenmw30_prob5.values
tenmw30_value6 = tenmw30_prob6.values
tenmw30_value7 = tenmw30_prob7.values
tenmw30_value8 = tenmw30_prob8.values
tenmw30_value9 = tenmw30_prob9.values
tenmw30_value10 = tenmw30_prob10.values
tenmw30_value11 = tenmw30_prob11.values
tenmw30_value12 = tenmw30_prob12.values
tenmw30_value13 = tenmw30_prob13.values
tenmw30_value14 = tenmw30_prob14.values
tenmw30_value15 = tenmw30_prob15.values
tenmw30_value16 = tenmw30_prob16.values
tenmw30_value17 = tenmw30_prob17.values
tenmw30_value18 = tenmw30_prob18.values

Shear20_prob_1 = prob_1.select(name="Vertical speed shear")[1]
Shear20_prob_2 = prob_2.select(name="Vertical speed shear")[1]
Shear20_prob_3 = prob_3.select(name="Vertical speed shear")[1]
Shear20_prob_4 = prob_4.select(name="Vertical speed shear")[1]
Shear20_prob_5 = prob_5.select(name="Vertical speed shear")[1]
Shear20_prob_6 = prob_6.select(name="Vertical speed shear")[1]
Shear20_prob1 = prob1.select(name="Vertical speed shear")[1]
Shear20_prob2 = prob2.select(name="Vertical speed shear")[1]
Shear20_prob3 = prob3.select(name="Vertical speed shear")[1]
Shear20_prob4 = prob4.select(name="Vertical speed shear")[1]
Shear20_prob5 = prob5.select(name="Vertical speed shear")[1]
Shear20_prob6 = prob6.select(name="Vertical speed shear")[1]
Shear20_prob7 = prob7.select(name="Vertical speed shear")[1]
Shear20_prob8 = prob8.select(name="Vertical speed shear")[1]
Shear20_prob9 = prob9.select(name="Vertical speed shear")[1]
Shear20_prob10 = prob10.select(name="Vertical speed shear")[1]
Shear20_prob11 = prob11.select(name="Vertical speed shear")[1]
Shear20_prob12 = prob12.select(name="Vertical speed shear")[1]
Shear20_prob13 = prob13.select(name="Vertical speed shear")[1]
Shear20_prob14 = prob14.select(name="Vertical speed shear")[1]
Shear20_prob15 = prob15.select(name="Vertical speed shear")[1]
Shear20_prob16 = prob16.select(name="Vertical speed shear")[1]
Shear20_prob17 = prob17.select(name="Vertical speed shear")[1]
Shear20_prob18 = prob18.select(name="Vertical speed shear")[1]

Shear20_value_1 = Shear20_prob_1.values
Shear20_value_2 = Shear20_prob_2.values
Shear20_value_3 = Shear20_prob_3.values
Shear20_value_4 = Shear20_prob_4.values
Shear20_value_5 = Shear20_prob_5.values
Shear20_value_6 = Shear20_prob_6.values
Shear20_value1 = Shear20_prob1.values
Shear20_value2 = Shear20_prob2.values
Shear20_value3 = Shear20_prob3.values
Shear20_value4 = Shear20_prob4.values
Shear20_value5 = Shear20_prob5.values
Shear20_value6 = Shear20_prob6.values
Shear20_value7 = Shear20_prob7.values
Shear20_value8 = Shear20_prob8.values
Shear20_value9 = Shear20_prob9.values
Shear20_value10 = Shear20_prob10.values
Shear20_value11 = Shear20_prob11.values
Shear20_value12 = Shear20_prob12.values
Shear20_value13 = Shear20_prob13.values
Shear20_value14 = Shear20_prob14.values
Shear20_value15 = Shear20_prob15.values
Shear20_value16 = Shear20_prob16.values
Shear20_value17 = Shear20_prob17.values
Shear20_value18 = Shear20_prob18.values

cape500_prob_1 = prob_1.select(name="Convective available potential energy")[0]
cape500_prob_2 = prob_2.select(name="Convective available potential energy")[0]
cape500_prob_3 = prob_3.select(name="Convective available potential energy")[0]
cape500_prob_4 = prob_4.select(name="Convective available potential energy")[0]
cape500_prob_5 = prob_5.select(name="Convective available potential energy")[0]
cape500_prob_6 = prob_6.select(name="Convective available potential energy")[0]
cape500_prob1 = prob1.select(name="Convective available potential energy")[0]
cape500_prob2 = prob2.select(name="Convective available potential energy")[0]
cape500_prob3 = prob3.select(name="Convective available potential energy")[0]
cape500_prob4 = prob4.select(name="Convective available potential energy")[0]
cape500_prob5 = prob5.select(name="Convective available potential energy")[0]
cape500_prob6 = prob6.select(name="Convective available potential energy")[0]
cape500_prob7 = prob7.select(name="Convective available potential energy")[0]
cape500_prob8 = prob8.select(name="Convective available potential energy")[0]
cape500_prob9 = prob9.select(name="Convective available potential energy")[0]
cape500_prob10 = prob10.select(name="Convective available potential energy")[0]
cape500_prob11 = prob11.select(name="Convective available potential energy")[0]
cape500_prob12 = prob12.select(name="Convective available potential energy")[0]
cape500_prob13 = prob13.select(name="Convective available potential energy")[0]
cape500_prob14 = prob14.select(name="Convective available potential energy")[0]
cape500_prob15 = prob15.select(name="Convective available potential energy")[0]
cape500_prob16 = prob16.select(name="Convective available potential energy")[0]
cape500_prob17 = prob17.select(name="Convective available potential energy")[0]
cape500_prob18 = prob18.select(name="Convective available potential energy")[0]

cape500_value_1 = cape500_prob_1.values
cape500_value_2 = cape500_prob_2.values
cape500_value_3 = cape500_prob_3.values
cape500_value_4 = cape500_prob_4.values
cape500_value_5 = cape500_prob_5.values
cape500_value_6 = cape500_prob_6.values
cape500_value1 = cape500_prob1.values
cape500_value2 = cape500_prob2.values
cape500_value3 = cape500_prob3.values
cape500_value4 = cape500_prob4.values
cape500_value5 = cape500_prob5.values
cape500_value6 = cape500_prob6.values
cape500_value7 = cape500_prob7.values
cape500_value8 = cape500_prob8.values
cape500_value9 = cape500_prob9.values
cape500_value10 = cape500_prob10.values
cape500_value11 = cape500_prob11.values
cape500_value12 = cape500_prob12.values
cape500_value13 = cape500_prob13.values
cape500_value14 = cape500_prob14.values
cape500_value15 = cape500_prob15.values
cape500_value16 = cape500_prob16.values
cape500_value17 = cape500_prob17.values
cape500_value18 = cape500_prob18.values

cape5_SMT1 = ndimage.gaussian_filter(cape500_value_1, sigma=1.5, order=0)
cape5_SMT2 = ndimage.gaussian_filter(cape500_value_2, sigma=1.5, order=0)
cape5_SMT3 = ndimage.gaussian_filter(cape500_value_3, sigma=1.5, order=0)
cape5_SMT4 = ndimage.gaussian_filter(cape500_value_4, sigma=1.5, order=0)
cape5_SMT5 = ndimage.gaussian_filter(cape500_value_5, sigma=1.5, order=0)
cape5_SMT6 = ndimage.gaussian_filter(cape500_value_6, sigma=1.5, order=0)
cape5_SMT7 = ndimage.gaussian_filter(cape500_value1, sigma=1.5, order=0)
cape5_SMT8 = ndimage.gaussian_filter(cape500_value2, sigma=1.5, order=0)
cape5_SMT9 = ndimage.gaussian_filter(cape500_value3, sigma=1.5, order=0)
cape5_SMT10 = ndimage.gaussian_filter(cape500_value4, sigma=1.5, order=0)
cape5_SMT11 = ndimage.gaussian_filter(cape500_value5, sigma=1.5, order=0)
cape5_SMT12 = ndimage.gaussian_filter(cape500_value6, sigma=1.5, order=0)
cape5_SMT13 = ndimage.gaussian_filter(cape500_value7, sigma=1.5, order=0)
cape5_SMT14 = ndimage.gaussian_filter(cape500_value8, sigma=1.5, order=0)
cape5_SMT15 = ndimage.gaussian_filter(cape500_value9, sigma=1.5, order=0)
cape5_SMT16 = ndimage.gaussian_filter(cape500_value10,  sigma=1.5, order=0)
cape5_SMT17 = ndimage.gaussian_filter(cape500_value11,  sigma=1.5, order=0)
cape5_SMT18 = ndimage.gaussian_filter(cape500_value12,  sigma=1.5, order=0)
cape5_SMT19 = ndimage.gaussian_filter(cape500_value13,  sigma=1.5, order=0)
cape5_SMT20 = ndimage.gaussian_filter(cape500_value14,  sigma=1.5, order=0)
cape5_SMT21 = ndimage.gaussian_filter(cape500_value15,  sigma=1.5, order=0)
cape5_SMT22 = ndimage.gaussian_filter(cape500_value16,  sigma=1.5, order=0)
cape5_SMT23 = ndimage.gaussian_filter(cape500_value17,  sigma=1.5, order=0)
cape5_SMT24 = ndimage.gaussian_filter(cape500_value18,  sigma=1.5, order=0)

helic25_prob_1 = prob_1.message(25)
helic25_prob_2 = prob_2.message(25)
helic25_prob_3 = prob_3.message(16)
helic25_prob_4 = prob_4.message(25)
helic25_prob_5 = prob_5.message(25)
helic25_prob_6 = prob_6.message(16)
helic25_prob1 =  prob1.message(25)
helic25_prob2 =  prob2.message(25)
helic25_prob3 =  prob3.message(16)
helic25_prob4 =  prob4.message(25)
helic25_prob5 =  prob5.message(25)
helic25_prob6 =  prob6.message(16)
helic25_prob7 =  prob7.message(25)
helic25_prob8 =  prob8.message(25)
helic25_prob9 =  prob9.message(16)
helic25_prob10 = prob10.message(25)
helic25_prob11 = prob11.message(25)
helic25_prob12 = prob12.message(16)
helic25_prob13 = prob13.message(25)
helic25_prob14 = prob14.message(25)
helic25_prob15 = prob15.message(16)
helic25_prob16 = prob16.message(25)
helic25_prob17 = prob17.message(25)
helic25_prob18 = prob18.message(16)

helic25_value_1 = helic25_prob_1.values
helic25_value_2 = helic25_prob_2.values
helic25_value_3 = helic25_prob_3.values
helic25_value_4 = helic25_prob_4.values
helic25_value_5 = helic25_prob_5.values
helic25_value_6 = helic25_prob_6.values
helic25_value1 = helic25_prob1.values
helic25_value2 = helic25_prob2.values
helic25_value3 = helic25_prob3.values
helic25_value4 = helic25_prob4.values
helic25_value5 = helic25_prob5.values
helic25_value6 = helic25_prob6.values
helic25_value7 = helic25_prob7.values
helic25_value8 = helic25_prob8.values
helic25_value9 = helic25_prob9.values
helic25_value10 = helic25_prob10.values
helic25_value11 = helic25_prob11.values
helic25_value12 = helic25_prob12.values
helic25_value13 = helic25_prob13.values
helic25_value14 = helic25_prob14.values
helic25_value15 = helic25_prob15.values
helic25_value16 = helic25_prob16.values
helic25_value17 = helic25_prob17.values
helic25_value18 = helic25_prob18.values

print('3-----------------------------------------------------------------------------------')
print(helic25_prob_1)
print('3-----------------------------------------------------------------------------------')
print(helic25_prob_2)
print('3-----------------------------------------------------------------------------------')
print(helic25_prob_3)
print('3-----------------------------------------------------------------------------------')
print(helic25_prob_4)

root2 = 3

ssvr1  = np.power(Shear20_value_1*  cape5_SMT1 *    helic25_value_1,  (1/root2))
ssvr2  = np.power(Shear20_value_2*  cape5_SMT2 *    helic25_value_2,  (1/root2))
ssvr3  = np.power(Shear20_value_3*  cape5_SMT3 *    helic25_value_3,  (1/root2))
ssvr4  = np.power(Shear20_value_4*  cape5_SMT4 *    helic25_value_4,  (1/root2))
ssvr5  = np.power(Shear20_value_5*  cape5_SMT5 *    helic25_value_5,  (1/root2))
ssvr6  = np.power(Shear20_value_6*  cape5_SMT6 *    helic25_value_6,  (1/root2))
ssvr7  = np.power(Shear20_value1 *  cape5_SMT7 *    helic25_value1,   (1/root2))
ssvr8  = np.power(Shear20_value2 *  cape5_SMT8 *    helic25_value2,   (1/root2))
ssvr9  = np.power(Shear20_value3 *  cape5_SMT9 *    helic25_value3,   (1/root2))
ssvr10 = np.power(Shear20_value4  * cape5_SMT10 * helic25_value4 ,  (1/root2))
ssvr11 = np.power(Shear20_value5  * cape5_SMT11 * helic25_value5 ,  (1/root2))
ssvr12 = np.power(Shear20_value6  * cape5_SMT12 * helic25_value6 ,  (1/root2))
ssvr13 = np.power(Shear20_value7  * cape5_SMT13 * helic25_value7 ,  (1/root2))
ssvr14 = np.power(Shear20_value8  * cape5_SMT14 * helic25_value8 ,  (1/root2))
ssvr15 = np.power(Shear20_value9  * cape5_SMT15 * helic25_value9 ,  (1/root2))
ssvr16 = np.power(Shear20_value10 * cape5_SMT16 * helic25_value10,  (1/root2))
ssvr17 = np.power(Shear20_value11 * cape5_SMT17 * helic25_value11,  (1/root2))
ssvr18 = np.power(Shear20_value12 * cape5_SMT18 * helic25_value12,  (1/root2))
ssvr19 = np.power(Shear20_value13 * cape5_SMT19 * helic25_value13,  (1/root2))
ssvr20 = np.power(Shear20_value14 * cape5_SMT20 * helic25_value14,  (1/root2))
ssvr21 = np.power(Shear20_value15 * cape5_SMT21 * helic25_value15,  (1/root2))
ssvr22 = np.power(Shear20_value16 * cape5_SMT22 * helic25_value16,  (1/root2))
ssvr23 = np.power(Shear20_value17 * cape5_SMT23 * helic25_value17,  (1/root2))
ssvr24 = np.power(Shear20_value18 * cape5_SMT24 * helic25_value18,  (1/root2))


SS1  = np.where(t_1  >= 10, ssvr1 , 0)
SS2  = np.where(t_2  >= 10, ssvr2 , 0)
SS3  = np.where(t_3  >= 10, ssvr3 , 0)
SS4  = np.where(t_4  >= 10, ssvr4 , 0)
SS5  = np.where(t_5  >= 10, ssvr5 , 0)
SS6  = np.where(t_6  >= 10, ssvr6 , 0)
SS7 = np.where(t1  >= 10, ssvr7, 0)
SS8 = np.where(t2  >= 10, ssvr8, 0)
SS9 = np.where(t3  >= 10, ssvr9, 0)
SS10 = np.where(t4  >= 10, ssvr10, 0)
SS11 = np.where(t5  >= 10, ssvr11, 0)
SS12 = np.where(t6  >= 10, ssvr12, 0)
SS13 = np.where(t7  >= 10, ssvr13, 0)
SS14 = np.where(t8  >= 10, ssvr14, 0)
SS15 = np.where(t9  >= 10, ssvr15, 0)
SS16 = np.where(t10 >= 10, ssvr16, 0)
SS17 = np.where(t11 >= 10, ssvr17, 0)
SS18 = np.where(t12 >= 10, ssvr18, 0)
SS19 = np.where(t13 >= 10, ssvr19, 0)
SS20 = np.where(t14 >= 10, ssvr20, 0)
SS21 = np.where(t15 >= 10, ssvr21, 0)
SS22 = np.where(t16 >= 10, ssvr22, 0)
SS23 = np.where(t17 >= 10, ssvr23, 0)
SS24 = np.where(t18 >= 10, ssvr24, 0)

ssvr1c  = np.power(t_1*  SS1,  (1/root))
ssvr2c  = np.power(t_2*  SS2,  (1/root))
ssvr3c  = np.power(t_3*  SS3,  (1/root))
ssvr4c  = np.power(t_4*  SS4,  (1/root))
ssvr5c  = np.power(t_5*  SS5,  (1/root))
ssvr6c  = np.power(t_6*  SS6,  (1/root))
ssvr7c  = np.power(t1  *  SS7,  (1/root))
ssvr8c  = np.power(t2  *  SS8,  (1/root))
ssvr9c  = np.power(t3  *  SS9,  (1/root))
ssvr10c = np.power(t4  * SS10,  (1/root))
ssvr11c = np.power(t5  * SS11,  (1/root))
ssvr12c = np.power(t6  * SS12,  (1/root))
ssvr13c = np.power(t7  * SS13,  (1/root))
ssvr14c = np.power(t8  * SS14,  (1/root))
ssvr15c = np.power(t9  * SS15,  (1/root))
ssvr16c = np.power(t10 * SS16,  (1/root))
ssvr17c = np.power(t11 * SS17,  (1/root))
ssvr18c = np.power(t12 * SS18,  (1/root))
ssvr19c = np.power(t13 * SS19,  (1/root))
ssvr20c = np.power(t14 * SS20,  (1/root))
ssvr21c = np.power(t15 * SS21,  (1/root))
ssvr22c = np.power(t16 * SS22,  (1/root))
ssvr23c = np.power(t17 * SS23,  (1/root))
ssvr24c = np.power(t18 * SS24,  (1/root))


# In[422]:


def plot_background(ax):
    ax.set_extent([-67.5, -74.5, 17.25, 20.5])
    ax.add_feature(cfeature.COASTLINE, linewidth=1.5)
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=2)

    return ax


fig, axarr = plt.subplots(nrows=4, ncols=3, figsize=(18, 18), constrained_layout=True,
                          subplot_kw={'projection': map_crs})
axlist = axarr.flatten()
for ax in axlist:
    plot_background(ax)

colormap = 'YlOrRd' #matplotlib.colors.ListedColormap(['#00eded','#00a1f5','#0000f5','#00ff00','#00c700','#008f00','#ffff00','#e8bf00','#ff8f00','#ff0000','#cc3300','#990000','#ff00ff','#9933cc'])
clev = [20, 60, 100]
clev2 = [10, 20, 40, 60, 80, 100] #20%,40%,60%,80%,100%

# 1
cf1 = axlist[0].contourf(lons, lats, SS1, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                         norm=plt.Normalize(0, 100))
c1 = axlist[0].contour(lons, lats, Ts1, clev,  colors='k', linewidths=1.8,transform=ccrs.PlateCarree())
axlist[0].clabel(c1, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[0].set_title('REFD 12PM', fontsize=16)
cb1 = fig.colorbar(cf1, ax=axlist[0], orientation='horizontal', shrink=0.74, pad=0)
cb1.set_label('dBZ', size='x-large')

# 2
cf2 = axlist[1].contourf(lons, lats, SS2, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c2 = axlist[1].contour(lons, lats, Ts2, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c2, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[1].set_title('REFD 01PM', fontsize=16)
cb2 = fig.colorbar(cf2, ax=axlist[1], orientation='horizontal', shrink=0.74, pad=0)
cb2.set_label('dBZ', size='x-large')

# 3
cf3 = axlist[2].contourf(lons, lats, SS3, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
c3 = axlist[2].contour(lons, lats, Ts3, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[2].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[2].set_title('REFD 02PM', fontsize=16)
cb3 = fig.colorbar(cf3, ax=axlist[2], orientation='horizontal', shrink=0.74, pad=0)
cb3.set_label('dBZ', size='x-large')

# 4
cf4 = axlist[3].contourf(lons, lats, SS4, clev2, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[3].set_title('REFD 03PM', fontsize=16)
c4 = axlist[3].contour(lons, lats, Ts4, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb4 = fig.colorbar(cf4, ax=axlist[3], orientation='horizontal', shrink=0.74, pad=0)
cb4.set_label('dBZ', size='x-large')

# 5
cf5 = axlist[4].contourf(lons, lats, SS5, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c5 = axlist[4].contour(lons, lats, Ts5, clev,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[4].clabel(c5, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[4].set_title('REFD 04PM', fontsize=16)
cb5 = fig.colorbar(cf5, ax=axlist[4], orientation='horizontal', shrink=0.74, pad=0)
cb5.set_label('dBZ', size='x-large')

# 6
cf6 = axlist[5].contourf(lons, lats, SS6, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c6 = axlist[5].contour(lons, lats, Ts6, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[5].clabel(c6, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[5].set_title('REFD 05PM', fontsize=16)
cb6 = fig.colorbar(cf6, ax=axlist[5], orientation='horizontal', shrink=0.74, pad=0)
cb6.set_label('dBZ', size='x-large')

# 7
cf7 = axlist[6].contourf(lons, lats, SS7, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[6].set_title('REFD 06PM', fontsize=16)
c7 = axlist[6].contour(lons, lats, Ts7, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[6].clabel(c7, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb7 = fig.colorbar(cf7, ax=axlist[6], orientation='horizontal', shrink=0.74, pad=0)
cb7.set_label('dBZ', size='x-large')

# 8
cf8 = axlist[7].contourf(lons, lats, SS8, clev2, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[7].set_title('REFD 07PM', fontsize=16)
c8 = axlist[7].contour(lons, lats, Ts8, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[7].clabel(c8, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb8 = fig.colorbar(cf8, ax=axlist[7], orientation='horizontal', shrink=0.74, pad=0)
cb8.set_label('dBZ', size='x-large')

# 9
cf9 = axlist[8].contourf(lons, lats, SS9, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c9 = axlist[8].contour(lons, lats, Ts9, clev,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[8].clabel(c9, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[8].set_title('REFD 08PM', fontsize=16)
cb9 = fig.colorbar(cf9, ax=axlist[8], orientation='horizontal', shrink=0.74, pad=0)
cb9.set_label('dBZ', size='x-large')

# 10
cf10 = axlist[9].contourf(lons, lats, SS10, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c10 = axlist[9].contour(lons, lats, Ts10, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[9].clabel(c10, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[9].set_title('REFD 09PM', fontsize=16)
cb10 = fig.colorbar(cf10, ax=axlist[9], orientation='horizontal', shrink=0.74, pad=0)
cb10.set_label('dBZ', size='x-large')

# 11
cf11 = axlist[10].contourf(lons, lats, SS11, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[10].set_title('REFD 10PM', fontsize=16)
c11 = axlist[10].contour(lons, lats, Ts11, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[10].clabel(c11, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb11 = fig.colorbar(cf11, ax=axlist[10], orientation='horizontal', shrink=0.74, pad=0)
cb11.set_label('dBZ', size='x-large')

# 12
cf12 = axlist[11].contourf(lons, lats, SS12, clev2, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[11].set_title('REFD 11PM', fontsize=16)
c12 = axlist[11].contour(lons, lats, Ts12, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[11].clabel(c12, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb12 = fig.colorbar(cf12, ax=axlist[11], orientation='horizontal', shrink=0.74, pad=0)
cb12.set_label('dBZ', size='x-large')

fig.suptitle(f'REFLECTIVIDAD DERIVADA 1KM & PROBABILIDAD DE TRONADAS (Tarde-Noche)\nVálido para este {fecha_formateada} \n\nINIT: {hora_formateada} de este {fecha_formateada_dia_anterior}\n', fontsize=20)

fig.savefig(f'{save_path}/D1_TSRD_REFD_12H_PERIOD_TN_RD.png', bbox_inches='tight', dpi=400)


# In[423]:


def plot_background(ax):
    ax.set_extent([-67.5, -74.5, 17.25, 20.5])
    ax.add_feature(cfeature.COASTLINE, linewidth=1.5)
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=2)

    return ax


fig, axarr = plt.subplots(nrows=4, ncols=3, figsize=(18, 18), constrained_layout=True,
                          subplot_kw={'projection': map_crs})
axlist = axarr.flatten()
for ax in axlist:
    plot_background(ax)

colormap = 'YlOrRd' #matplotlib.colors.ListedColormap(['#00eded','#00a1f5','#0000f5','#00ff00','#00c700','#008f00','#ffff00','#e8bf00','#ff8f00','#ff0000','#cc3300','#990000','#ff00ff','#9933cc'])
clev = [20, 60, 80, 100]
clev2 = [10, 20, 40, 60, 80, 100] #20%,40%,60%,80%,100%

# 1
cf1 = axlist[0].contourf(lons, lats, SS13, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                         norm=plt.Normalize(5, 75))
c1 = axlist[0].contour(lons, lats, Ts13, clev,  colors='black', linewidths=1.8,transform=ccrs.PlateCarree())
axlist[0].clabel(c1, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[0].set_title('REFD 12PM', fontsize=16)
cb1 = fig.colorbar(cf1, ax=axlist[0], orientation='horizontal', shrink=0.74, pad=0)
cb1.set_label('dBZ', size='x-large')

# 2
cf2 = axlist[1].contourf(lons, lats, SS14, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c2 = axlist[1].contour(lons, lats, Ts14, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c2, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[1].set_title('REFD 01PM', fontsize=16)
cb2 = fig.colorbar(cf2, ax=axlist[1], orientation='horizontal', shrink=0.74, pad=0)
cb2.set_label('dBZ', size='x-large')

# 3
cf3 = axlist[2].contourf(lons, lats, SS15, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
c3 = axlist[2].contour(lons, lats, Ts15, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[2].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[2].set_title('REFD 02PM', fontsize=16)
cb3 = fig.colorbar(cf3, ax=axlist[2], orientation='horizontal', shrink=0.74, pad=0)
cb3.set_label('dBZ', size='x-large')

# 4
cf4 = axlist[3].contourf(lons, lats, SS16, clev2, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[3].set_title('REFD 03PM', fontsize=16)
c4 = axlist[3].contour(lons, lats, Ts16, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb4 = fig.colorbar(cf4, ax=axlist[3], orientation='horizontal', shrink=0.74, pad=0)
cb4.set_label('dBZ', size='x-large')

# 5
cf5 = axlist[4].contourf(lons, lats, SS17, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c5 = axlist[4].contour(lons, lats, Ts17, clev,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[4].clabel(c5, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[4].set_title('REFD 04PM', fontsize=16)
cb5 = fig.colorbar(cf5, ax=axlist[4], orientation='horizontal', shrink=0.74, pad=0)
cb5.set_label('dBZ', size='x-large')

# 6
cf6 = axlist[5].contourf(lons, lats, SS18, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c6 = axlist[5].contour(lons, lats, Ts18, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[5].clabel(c6, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[5].set_title('REFD 05PM', fontsize=16)
cb6 = fig.colorbar(cf6, ax=axlist[5], orientation='horizontal', shrink=0.74, pad=0)
cb6.set_label('dBZ', size='x-large')

# 7
cf7 = axlist[6].contourf(lons, lats, SS19, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[6].set_title('REFD 06PM', fontsize=16)
c7 = axlist[6].contour(lons, lats, Ts19, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[6].clabel(c7, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb7 = fig.colorbar(cf7, ax=axlist[6], orientation='horizontal', shrink=0.74, pad=0)
cb7.set_label('dBZ', size='x-large')

# 8
cf8 = axlist[7].contourf(lons, lats, SS20, clev2, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[7].set_title('REFD 07PM', fontsize=16)
c8 = axlist[7].contour(lons, lats, Ts20, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[7].clabel(c8, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb8 = fig.colorbar(cf8, ax=axlist[7], orientation='horizontal', shrink=0.74, pad=0)
cb8.set_label('dBZ', size='x-large')

# 9
cf9 = axlist[8].contourf(lons, lats, SS21, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c9 = axlist[8].contour(lons, lats, Ts21, clev,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[8].clabel(c9, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[8].set_title('REFD 08PM', fontsize=16)
cb9 = fig.colorbar(cf9, ax=axlist[8], orientation='horizontal', shrink=0.74, pad=0)
cb9.set_label('dBZ', size='x-large')

# 10
cf10 = axlist[9].contourf(lons, lats, SS22, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c10 = axlist[9].contour(lons, lats, Ts22, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[9].clabel(c10, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[9].set_title('REFD 09PM', fontsize=16)
cb10 = fig.colorbar(cf10, ax=axlist[9], orientation='horizontal', shrink=0.74, pad=0)
cb10.set_label('dBZ', size='x-large')

# 11
cf11 = axlist[10].contourf(lons, lats, SS23, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[10].set_title('REFD 10PM', fontsize=16)
c11 = axlist[10].contour(lons, lats, Ts23, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[10].clabel(c11, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb11 = fig.colorbar(cf11, ax=axlist[10], orientation='horizontal', shrink=0.74, pad=0)
cb11.set_label('dBZ', size='x-large')

# 12
cf12 = axlist[11].contourf(lons, lats, SS24, clev2, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[11].set_title('REFD 11PM', fontsize=16)
c12 = axlist[11].contour(lons, lats, Ts24, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[11].clabel(c12, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb12 = fig.colorbar(cf12, ax=axlist[11], orientation='horizontal', shrink=0.74, pad=0)
cb12.set_label('dBZ', size='x-large')

fig.suptitle(f'REFLECTIVIDAD DERIVADA 1KM & PROBABILIDAD DE TRONADAS (Tarde-Noche)\nVálido para este {fecha_formateada} \n\nINIT: {hora_formateada} de este {fecha_formateada_dia_anterior}\n', fontsize=20)

fig.savefig(f'{save_path}/D1_TSRD_REFD_12H_PERIOD_TN_RD.png', bbox_inches='tight', dpi=400)


# In[424]:


SS_max = np.maximum.reduce([
SS1, 
SS2, 
SS3, 
SS4, 
SS5, 
SS6, 
SS7, 
SS8, 
SS9, 
SS10, 
SS11, 
SS12, 
SS13, 
SS14, 
SS15, 
SS16, 
SS17, 
SS18, 
SS19, 
SS20, 
SS21, 
SS22, 
SS23, 
SS24])

SS_maxSMT = ndimage.gaussian_filter(SS_max, sigma=1.5, order=0)

SSC_max = np.maximum.reduce([
ssvr1c,  
ssvr2c,  
ssvr3c,  
ssvr4c,  
ssvr5c,  
ssvr6c,  
ssvr7c,  
ssvr8c,  
ssvr9c,  
ssvr10c, 
ssvr11c, 
ssvr12c, 
ssvr13c, 
ssvr14c, 
ssvr15c, 
ssvr16c, 
ssvr17c, 
ssvr18c, 
ssvr19c, 
ssvr20c, 
ssvr21c, 
ssvr22c, 
ssvr23c, 
ssvr24c])

SSC_maxSMT = ndimage.gaussian_filter(SSC_max, sigma=2, order=0)


# In[425]:


fig = plt.figure (1,figsize=(20,22))
ax=plt.subplot(1,1,1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space
ax.set_extent ([-67.5, -74.5, 17.25, 20.5], data_crs)
ax.add_feature(cfeature.COASTLINE, linewidth=2)
ax.add_feature(cfeature.BORDERS, linewidth=2, zorder=12)


colormap = 'YlOrRd' #matplotlib.colors.ListedColormap(['#00c700','#ffff00','#ff8f00','#cc3300'])

clev = [10, 20, 40, 60, 80, 100]
clev2 = [5, 20, 40, 60, 80, 100]

cf = ax.contourf(lons,lats, SS_maxSMT, clev, extend='neither', cmap=colormap, transform=data_crs, 
                 norm=plt.Normalize(0, 100))

cb = plt.colorbar(cf, ax=ax, orientation='horizontal',pad=0.05, extendrect='true', ticks=clev)
cb.set_label(r'PORCIENTO', size='xx-large')

cs1 = ax.contour(lons, lats, SS_maxSMT, clev, colors='black',
              linestyles='solid', transform=data_crs)
ax.set_title(f'PROBABILIDAD GENERAL DE CONDICIONES DE TIEMPO SUB-SEVERO | 12AM - 12AM \n{fecha_formateada} | DATA: {hora_formateada}', fontsize=22)
ax.clabel(cs1, fmt='%d', fontsize=20)

# PR COUNTIES SHAPEFILES
shapefile1_path = 'shp/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp'
gdf1 = gpd.read_file(shapefile1_path)
county_PR = ShapelyFeature(gdf1['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_PR)

shapefile2_path = 'shp/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_RD)

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

plt.show()
plt.show()

fig.savefig(f'{save_path}/D1n_TSRD_PROB-AGUAC_TN_RD.png', bbox_inches='tight', dpi=300)


# In[426]:


import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from cartopy.feature import ShapelyFeature
from matplotlib import offsetbox
import matplotlib.patheffects as path_effects

# Define the coordinate reference systems
map_crs = ccrs.PlateCarree()
data_crs = ccrs.PlateCarree()

# Create the figure and axis
fig = plt.figure(1, figsize=(20, 22))
ax = plt.subplot(1, 1, 1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space

# Set the extent of the map
ax.set_extent([-67.5, -72.5, 17.25, 20.25], crs=data_crs)

# Add features to the map
ax.add_feature(cfeature.COASTLINE, linewidth=3.5)
ax.add_feature(cfeature.BORDERS, linewidth=3.5, zorder=3)
ax.add_feature(cfeature.OCEAN, facecolor='#00374d', zorder=3)
ax.add_feature(cfeature.LAND, facecolor='#b3b4b3')
ax.add_feature(cfeature.LAKES, linewidth=2, zorder=3, edgecolor='black', alpha=1)

# Define colormap and contour levels for the first data set
colormap2 = matplotlib.colors.ListedColormap(['#b9eac3', '#79c789', '#478f55', '#02757f', '#015057'])
clev = [20, 60, 80, 100]

# Assuming lons, lats, max_final_rain_int, and Thunder are already defined
# If not, you need to define these variables
# lons = ...
# lats = ...
# max_final_rain_int = ...
# Thunder = ...

# Plot the filled contours
#cf1 = ax.contourf(lons, lats, max_final_rain_int, clev, extend='neither', cmap=colormap2, transform=data_crs, 
                 # norm=plt.Normalize(10, 100))

# Position and customize the color bar
#cax = fig.add_axes([0.515, 0.28, 0.48, 0.04])  # Adjust the position as needed
#cb = plt.colorbar(cf1, cax=cax, orientation='horizontal', extendrect='true', drawedges=True)
#cb.set_ticks([])  # Hide the ticks
#cb.outline.set_edgecolor('k')  # Set color of the outline
#cb.outline.set_linewidth(3)  # Set the width of the outline
#cb.dividers.set_color('k')  # Set color of the dividers
#cb.dividers.set_linewidth(3)  # Set the width of the dividers

# Add Dominican lakes (if the default lakes feature does not include them, create a custom one)
canada_lakes = cfeature.NaturalEarthFeature(
    category='physical',
    name='lakes',
    scale='10m',
    facecolor='none'
)
ax.add_feature(canada_lakes, edgecolor='black', linewidth=1)


# Define the second colormap and contour levels
colormap = 'YlOrRd' #matplotlib.colors.ListedColormap(['#00c700','#ffff00','#ff8f00','#cc3300'])

clev = [10, 20, 40, 60, 80, 100]

# Plot the second set of filled contours
cf = ax.contourf(lons, lats, SS_maxSMT, clev, extend='neither', transform=data_crs, norm=plt.Normalize(10, 100), cmap=colormap, alpha=1)

# Position and customize the second color bar
cax = fig.add_axes([0.1, 0.245, 0.8, 0.04], zorder=0)  # Adjust the position as needed
cb = plt.colorbar(cf, cax=cax, orientation='horizontal', extendrect='true', drawedges=True)
cb.set_ticks([10, 20, 40, 60, 80, 100])  # Hide the ticks
cb.ax.xaxis.set_tick_params(color='white')
plt.setp(plt.getp(cb.ax, 'xticklabels'), color='white', fontsize=20, fontweight='bold')
cb.outline.set_edgecolor('k')  # Set color of the outline
cb.outline.set_linewidth(3)  # Set the width of the outline
cb.dividers.set_color('k')  # Set color of the dividers
cb.dividers.set_linewidth(3)  # Set the width of the dividers

# Plot the second set of line contours
cs1 = ax.contour(lons, lats, SS_maxSMT, clev, colors='black', linestyles='solid', transform=data_crs, linewidths=2, fontsize=40)

# Set titles for the plot
#ax.set_title(f'PROBABILIDAD GENERAL DE CONDICIONES DE TIEMPO SUB-SEVERO | 24 HORAS (12AM - 12AM) \nVálido para este {fecha_formateada}', loc='left', fontsize=22, fontweight='bold')
#ax.set_title(f'INIT: {hora_formateada} de este {fecha_formateada_dia_anterior}', loc='right', fontsize=16, fontweight='bold', style='italic')

# Add shapefile data
shapefile2_path = 'shp/rd/geoBoundaries-DOM-ADM1_simplified.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=1.5)
ax.add_feature(county_RD)

# Add shapefile data
shapefile3_path = 'shp/haiti/ne_10m_admin_0_countries.shp'
gdf3 = gpd.read_file(shapefile3_path)
county_HTI = ShapelyFeature(gdf3['geometry'], ccrs.PlateCarree(), facecolor='grey', edgecolor='black', lw=1, zorder=2)
ax.add_feature(county_HTI)

# Dictionary of important cities with their coordinates
cities = {
    "Santo Domingo": {"lat": 18.4861, "lon": -69.9312},
    "Santiago": {"lat": 19.4792, "lon": -70.6931},
    "La Romana": {"lat": 18.4333, "lon": -68.9667},
    "Punta Cana": {"lat": 18.582, "lon": -68.4055},
    "Puerto Plata": {"lat": 19.7975, "lon": -70.6884},
    "La Vega": {"lat": 19.2232, "lon": -70.5294},
    "Bonao": {"lat": 18.9356, "lon": -70.4094},
    "Baní": {"lat": 18.2796, "lon": -70.3319},
    "Azua": {"lat": 18.4532, "lon": -70.7349},
    "Barahona": {"lat": 18.2085, "lon": -71.1008},
    "Montecristi": {"lat": 19.8489, "lon": -71.6464},
    "Dajabón": {"lat": 19.5483, "lon": -71.7083},
    "Samaná": {"lat": 19.2057, "lon": -69.3367},
    "V. Altagracia": {"lat": 18.6700, "lon": -70.1700},
    "El Seibo": {"lat": 18.7650, "lon": -69.0383},
    "Nagua": {"lat": 19.3833, "lon": -69.8500},
    "San Juan": {"lat": 18.8050, "lon": -71.2300},
    "Pedernales": {"lat": 18.0370, "lon": -71.7440},
    "Ocoa": {"lat": 18.5500, "lon": -70.5000},
    "Oviedo": {"lat": 17.8007, "lon": -71.4008},
    "S. de la Mar": {"lat": 19.0579, "lon": -69.3892},
    "Monte Plata": {"lat": 18.8073, "lon": -69.7850},
    "Pimentel": {"lat": 19.1832, "lon": -70.1085},
    "Mao": {"lat": 19.5511, "lon": -71.0781},
    "Neyba": {"lat": 18.4847, "lon": -71.4194},
    "Pedro Santana": {"lat": 19.1050, "lon": -71.6959},
    "Elías Piña": {"lat": 18.8770, "lon": -71.7048},
    "Restauración": {"lat": 19.3159, "lon": -71.6947},
    "SAJOMA": {"lat": 19.3405, "lon": -70.9376}
}

# Add city names and dots to the plot
for city, coords in cities.items():
    ax.plot(coords["lon"], coords["lat"], 'o', color='k', markersize=10, transform=data_crs, path_effects=[path_effects.withStroke(linewidth=5, foreground='white')])  # Add a red dot
    ax.text(coords["lon"], coords["lat"], city, transform=data_crs, fontsize=22, fontweight='bold',
            ha='left', color='white', path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])

# Dictionary of important cities with their coordinates
cities2 = {
    "Higuey": {"lat": 18.6150, "lon": -68.7070},
    "Constanza": {"lat": 18.9094, "lon": -70.7208},

}

# Add city names and dots to the plot
for city, coords in cities2.items():
    ax.plot(coords["lon"], coords["lat"], 'o', color='k', markersize=10, transform=data_crs, path_effects=[path_effects.withStroke(linewidth=5, foreground='white')])  # Add a red dot
    ax.text(coords["lon"], coords["lat"], city, transform=data_crs, fontsize=22, fontweight='bold',
            ha='right', color='white', path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])

# Add text annotations
text1 = ax.text(0.5, 0.125, 'PROBABILIDADES', ha='center', va='center', fontsize=40, transform=ax.transAxes, fontweight='bold', color='white')
text1.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

text2 = ax.text(0.84, 0.75, f'Válidez del Mapa: \n 12:00 AM - 12:00 AM del \n {fecha_formateada}', ha='center', va='center', fontsize=25, transform=ax.transAxes, fontweight='bold', color='white')
text2.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

text4 = ax.text(0.84, 0.985, f'INIT: {hora_formateada} de este {fecha_formateada_dia_anterior}', ha='center', va='center', fontsize=16, transform=ax.transAxes, fontweight='bold', color='white')
text4.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

text3 = ax.text(0.32, 0.95, 'MAPA DE CONDICIONES SUB-SEVERAS', ha='center', va='center', fontsize=35, transform=ax.transAxes, fontweight='bold', color='white', zorder=5)
text3.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

def add_rounded_rect_with_shadow(ax, xy, width, height, rounding_size=0.1, shadow_offset=(0.02, -0.02)):
    # Add shadow
    shadow = FancyBboxPatch(
        (xy[0] + shadow_offset[0], xy[1] + shadow_offset[1]), width, height,
        boxstyle=f"round,pad=0.05,rounding_size={rounding_size}",
        edgecolor='none', facecolor='black', alpha=0.3,
        transform=data_crs, zorder=3
    )
    ax.add_patch(shadow)

    # Add rectangle
    rect = FancyBboxPatch(
        xy, width, height,
        boxstyle=f"round,pad=0.05,rounding_size={rounding_size}",
        edgecolor='k', facecolor='#f43d25', alpha=1,
        transform=data_crs, linewidth=2, zorder=4
    )
    ax.add_patch(rect)

# Define the position and size of the rectangle
rect_xy = (-72.4, 20.05)
rect_width = 3
rect_height = 0.1

# Add the rectangle with shadow to the plot
add_rounded_rect_with_shadow(ax, rect_xy, rect_width, rect_height)

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

# Save the figure
fig.savefig(f'{save_path}/D1_TSRD_PROB-TRON_24_RD.png', bbox_inches='tight', dpi=300)


# In[427]:


#----------------------------- Severe Weather Conditions Probs --------------------------------


# In[428]:


tenmw35_prob_1 = prob_1.select(name="10 metre wind speed")[2]
tenmw35_prob_2 = prob_2.select(name="10 metre wind speed")[2]
tenmw35_prob_3 = prob_3.select(name="10 metre wind speed")[2]
tenmw35_prob_4 = prob_4.select(name="10 metre wind speed")[2]
tenmw35_prob_5 = prob_5.select(name="10 metre wind speed")[2]
tenmw35_prob_6 = prob_6.select(name="10 metre wind speed")[2]
tenmw35_prob1 = prob1.select(name="10 metre wind speed")[2]
tenmw35_prob2 = prob2.select(name="10 metre wind speed")[2]
tenmw35_prob3 = prob3.select(name="10 metre wind speed")[2]
tenmw35_prob4 = prob4.select(name="10 metre wind speed")[2]
tenmw35_prob5 = prob5.select(name="10 metre wind speed")[2]
tenmw35_prob6 = prob6.select(name="10 metre wind speed")[2]
tenmw35_prob7 = prob7.select(name="10 metre wind speed")[2]
tenmw35_prob8 = prob8.select(name="10 metre wind speed")[2]
tenmw35_prob9 = prob9.select(name="10 metre wind speed")[2]
tenmw35_prob10 = prob10.select(name="10 metre wind speed")[2]
tenmw35_prob11 = prob11.select(name="10 metre wind speed")[2]
tenmw35_prob12 = prob12.select(name="10 metre wind speed")[2]
tenmw35_prob13 = prob13.select(name="10 metre wind speed")[2]
tenmw35_prob14 = prob14.select(name="10 metre wind speed")[2]
tenmw35_prob15 = prob15.select(name="10 metre wind speed")[2]
tenmw35_prob16 = prob16.select(name="10 metre wind speed")[2]
tenmw35_prob17 = prob17.select(name="10 metre wind speed")[2]
tenmw35_prob18 = prob18.select(name="10 metre wind speed")[2]

tenmw35_value_1 = tenmw35_prob_1.values
tenmw35_value_2 = tenmw35_prob_2.values
tenmw35_value_3 = tenmw35_prob_3.values
tenmw35_value_4 = tenmw35_prob_4.values
tenmw35_value_5 = tenmw35_prob_5.values
tenmw35_value_6 = tenmw35_prob_6.values
tenmw35_value1 = tenmw35_prob1.values
tenmw35_value2 = tenmw35_prob2.values
tenmw35_value3 = tenmw35_prob3.values
tenmw35_value4 = tenmw35_prob4.values
tenmw35_value5 = tenmw35_prob5.values
tenmw35_value6 = tenmw35_prob6.values
tenmw35_value7 = tenmw35_prob7.values
tenmw35_value8 = tenmw35_prob8.values
tenmw35_value9 = tenmw35_prob9.values
tenmw35_value10 = tenmw35_prob10.values
tenmw35_value11 = tenmw35_prob11.values
tenmw35_value12 = tenmw35_prob12.values
tenmw35_value13 = tenmw35_prob13.values
tenmw35_value14 = tenmw35_prob14.values
tenmw35_value15 = tenmw35_prob15.values
tenmw35_value16 = tenmw35_prob16.values
tenmw35_value17 = tenmw35_prob17.values
tenmw35_value18 = tenmw35_prob18.values

Shear30_prob_1 = prob_1.select(name="Vertical speed shear")[2]
Shear30_prob_2 = prob_2.select(name="Vertical speed shear")[2]
Shear30_prob_3 = prob_3.select(name="Vertical speed shear")[2]
Shear30_prob_4 = prob_4.select(name="Vertical speed shear")[2]
Shear30_prob_5 = prob_5.select(name="Vertical speed shear")[2]
Shear30_prob_6 = prob_6.select(name="Vertical speed shear")[2]
Shear30_prob1 = prob1.select(name="Vertical speed shear")[2]
Shear30_prob2 = prob2.select(name="Vertical speed shear")[2]
Shear30_prob3 = prob3.select(name="Vertical speed shear")[2]
Shear30_prob4 = prob4.select(name="Vertical speed shear")[2]
Shear30_prob5 = prob5.select(name="Vertical speed shear")[2]
Shear30_prob6 = prob6.select(name="Vertical speed shear")[2]
Shear30_prob7 = prob7.select(name="Vertical speed shear")[2]
Shear30_prob8 = prob8.select(name="Vertical speed shear")[2]
Shear30_prob9 = prob9.select(name="Vertical speed shear")[2]
Shear30_prob10 = prob10.select(name="Vertical speed shear")[2]
Shear30_prob11 = prob11.select(name="Vertical speed shear")[2]
Shear30_prob12 = prob12.select(name="Vertical speed shear")[2]
Shear30_prob13 = prob13.select(name="Vertical speed shear")[2]
Shear30_prob14 = prob14.select(name="Vertical speed shear")[2]
Shear30_prob15 = prob15.select(name="Vertical speed shear")[2]
Shear30_prob16 = prob16.select(name="Vertical speed shear")[2]
Shear30_prob17 = prob17.select(name="Vertical speed shear")[2]
Shear30_prob18 = prob18.select(name="Vertical speed shear")[2]

Shear30_value_1 = Shear30_prob_1.values
Shear30_value_2 = Shear30_prob_2.values
Shear30_value_3 = Shear30_prob_3.values
Shear30_value_4 = Shear30_prob_4.values
Shear30_value_5 = Shear30_prob_5.values
Shear30_value_6 = Shear30_prob_6.values
Shear30_value1 = Shear30_prob1.values
Shear30_value2 = Shear30_prob2.values
Shear30_value3 = Shear30_prob3.values
Shear30_value4 = Shear30_prob4.values
Shear30_value5 = Shear30_prob5.values
Shear30_value6 = Shear30_prob6.values
Shear30_value7 = Shear30_prob7.values
Shear30_value8 = Shear30_prob8.values
Shear30_value9 = Shear30_prob9.values
Shear30_value10 = Shear30_prob10.values
Shear30_value11 = Shear30_prob11.values
Shear30_value12 = Shear30_prob12.values
Shear30_value13 = Shear30_prob13.values
Shear30_value14 = Shear30_prob14.values
Shear30_value15 = Shear30_prob15.values
Shear30_value16 = Shear30_prob16.values
Shear30_value17 = Shear30_prob17.values
Shear30_value18 = Shear30_prob18.values

print(Shear30_prob6)

cape1k_prob_1 = prob_1.select(name="Convective available potential energy")[1]
cape1k_prob_2 = prob_2.select(name="Convective available potential energy")[1]
cape1k_prob_3 = prob_3.select(name="Convective available potential energy")[1]
cape1k_prob_4 = prob_4.select(name="Convective available potential energy")[1]
cape1k_prob_5 = prob_5.select(name="Convective available potential energy")[1]
cape1k_prob_6 = prob_6.select(name="Convective available potential energy")[1]
cape1k_prob1 = prob1.select(name="Convective available potential energy")[1]
cape1k_prob2 = prob2.select(name="Convective available potential energy")[1]
cape1k_prob3 = prob3.select(name="Convective available potential energy")[1]
cape1k_prob4 = prob4.select(name="Convective available potential energy")[1]
cape1k_prob5 = prob5.select(name="Convective available potential energy")[1]
cape1k_prob6 = prob6.select(name="Convective available potential energy")[1]
cape1k_prob7 = prob7.select(name="Convective available potential energy")[1]
cape1k_prob8 = prob8.select(name="Convective available potential energy")[1]
cape1k_prob9 = prob9.select(name="Convective available potential energy")[1]
cape1k_prob10 = prob10.select(name="Convective available potential energy")[1]
cape1k_prob11 = prob11.select(name="Convective available potential energy")[1]
cape1k_prob12 = prob12.select(name="Convective available potential energy")[1]
cape1k_prob13 = prob13.select(name="Convective available potential energy")[1]
cape1k_prob14 = prob14.select(name="Convective available potential energy")[1]
cape1k_prob15 = prob15.select(name="Convective available potential energy")[1]
cape1k_prob16 = prob16.select(name="Convective available potential energy")[1]
cape1k_prob17 = prob17.select(name="Convective available potential energy")[1]
cape1k_prob18 = prob18.select(name="Convective available potential energy")[1]

cape1k_value_1 = cape1k_prob_1.values
cape1k_value_2 = cape1k_prob_2.values
cape1k_value_3 = cape1k_prob_3.values
cape1k_value_4 = cape1k_prob_4.values
cape1k_value_5 = cape1k_prob_5.values
cape1k_value_6 = cape1k_prob_6.values
cape1k_value1 = cape1k_prob1.values
cape1k_value2 = cape1k_prob2.values
cape1k_value3 = cape1k_prob3.values
cape1k_value4 = cape1k_prob4.values
cape1k_value5 = cape1k_prob5.values
cape1k_value6 = cape1k_prob6.values
cape1k_value7 = cape1k_prob7.values
cape1k_value8 = cape1k_prob8.values
cape1k_value9 = cape1k_prob9.values
cape1k_value10 = cape1k_prob10.values
cape1k_value11 = cape1k_prob11.values
cape1k_value12 = cape1k_prob12.values
cape1k_value13 = cape1k_prob13.values
cape1k_value14 = cape1k_prob14.values
cape1k_value15 = cape1k_prob15.values
cape1k_value16 = cape1k_prob16.values
cape1k_value17 = cape1k_prob17.values
cape1k_value18 = cape1k_prob18.values

cape1k_SMT1 = ndimage.gaussian_filter(cape1k_value_1, sigma=1.5, order=0)
cape1k_SMT2 = ndimage.gaussian_filter(cape1k_value_2, sigma=1.5, order=0)
cape1k_SMT3 = ndimage.gaussian_filter(cape1k_value_3, sigma=1.5, order=0)
cape1k_SMT4 = ndimage.gaussian_filter(cape1k_value_4, sigma=1.5, order=0)
cape1k_SMT5 = ndimage.gaussian_filter(cape1k_value_5, sigma=1.5, order=0)
cape1k_SMT6 = ndimage.gaussian_filter(cape1k_value_6, sigma=1.5, order=0)
cape1k_SMT7 = ndimage.gaussian_filter(cape1k_value1, sigma=1.5, order=0)
cape1k_SMT8 = ndimage.gaussian_filter(cape1k_value2, sigma=1.5, order=0)
cape1k_SMT9 = ndimage.gaussian_filter(cape1k_value3, sigma=1.5, order=0)
cape1k_SMT10 = ndimage.gaussian_filter(cape1k_value4, sigma=1.5, order=0)
cape1k_SMT11 = ndimage.gaussian_filter(cape1k_value5, sigma=1.5, order=0)
cape1k_SMT12 = ndimage.gaussian_filter(cape1k_value6, sigma=1.5, order=0)
cape1k_SMT13 = ndimage.gaussian_filter(cape1k_value7, sigma=1.5, order=0)
cape1k_SMT14 = ndimage.gaussian_filter(cape1k_value8, sigma=1.5, order=0)
cape1k_SMT15 = ndimage.gaussian_filter(cape1k_value9, sigma=1.5, order=0)
cape1k_SMT16 = ndimage.gaussian_filter(cape1k_value10,  sigma=1.5, order=0)
cape1k_SMT17 = ndimage.gaussian_filter(cape1k_value11,  sigma=1.5, order=0)
cape1k_SMT18 = ndimage.gaussian_filter(cape1k_value12,  sigma=1.5, order=0)
cape1k_SMT19 = ndimage.gaussian_filter(cape1k_value13,  sigma=1.5, order=0)
cape1k_SMT20 = ndimage.gaussian_filter(cape1k_value14,  sigma=1.5, order=0)
cape1k_SMT21 = ndimage.gaussian_filter(cape1k_value15,  sigma=1.5, order=0)
cape1k_SMT22 = ndimage.gaussian_filter(cape1k_value16,  sigma=1.5, order=0)
cape1k_SMT23 = ndimage.gaussian_filter(cape1k_value17,  sigma=1.5, order=0)
cape1k_SMT24 = ndimage.gaussian_filter(cape1k_value18,  sigma=1.5, order=0)

helic75_prob_1 = prob_1.message(26)
helic75_prob_2 = prob_2.message(26)
helic75_prob_3 = prob_3.message(17)
helic75_prob_4 = prob_4.message(26)
helic75_prob_5 = prob_5.message(26)
helic75_prob_6 = prob_6.message(17)
helic75_prob1 =  prob1.message(26)
helic75_prob2 =  prob2.message(26)
helic75_prob3 =  prob3.message(17)
helic75_prob4 =  prob4.message(26)
helic75_prob5 =  prob5.message(26)
helic75_prob6 =  prob6.message(17)
helic75_prob7 =  prob7.message(26)
helic75_prob8 =  prob8.message(26)
helic75_prob9 =  prob9.message(17)
helic75_prob10 = prob10.message(26)
helic75_prob11 = prob11.message(26)
helic75_prob12 = prob12.message(17)
helic75_prob13 = prob13.message(26)
helic75_prob14 = prob14.message(26)
helic75_prob15 = prob15.message(17)
helic75_prob16 = prob16.message(26)
helic75_prob17 = prob17.message(26)
helic75_prob18 = prob18.message(17)

helic75_value_1 = helic75_prob_1.values
helic75_value_2 = helic75_prob_2.values
helic75_value_3 = helic75_prob_3.values
helic75_value_4 = helic75_prob_4.values
helic75_value_5 = helic75_prob_5.values
helic75_value_6 = helic75_prob_6.values
helic75_value1 = helic75_prob1.values
helic75_value2 = helic75_prob2.values
helic75_value3 = helic75_prob3.values
helic75_value4 = helic75_prob4.values
helic75_value5 = helic75_prob5.values
helic75_value6 = helic75_prob6.values
helic75_value7 = helic75_prob7.values
helic75_value8 = helic75_prob8.values
helic75_value9 = helic75_prob9.values
helic75_value10 = helic75_prob10.values
helic75_value11 = helic75_prob11.values
helic75_value12 = helic75_prob12.values
helic75_value13 = helic75_prob13.values
helic75_value14 = helic75_prob14.values
helic75_value15 = helic75_prob15.values
helic75_value16 = helic75_prob16.values
helic75_value17 = helic75_prob17.values
helic75_value18 = helic75_prob18.values

print('3-----------------------------------------------------------------------------------')
print(helic75_prob_1)
print('3-----------------------------------------------------------------------------------')
print(helic75_prob_2)
print('3-----------------------------------------------------------------------------------')
print(helic75_prob_3)
print('3-----------------------------------------------------------------------------------')
print(helic75_prob_4)


# In[429]:


root2 = 3

svr1  = np.power(Shear30_value_1*  cape1k_SMT1 *    helic75_value_1,  (1/root2))
svr2  = np.power(Shear30_value_2*  cape1k_SMT2 *    helic75_value_2,  (1/root2))
svr3  = np.power(Shear30_value_3*  cape1k_SMT3 *    helic75_value_3,  (1/root2))
svr4  = np.power(Shear30_value_4*  cape1k_SMT4 *    helic75_value_4,  (1/root2))
svr5  = np.power(Shear30_value_5*  cape1k_SMT5 *    helic75_value_5,  (1/root2))
svr6  = np.power(Shear30_value_6*  cape1k_SMT6 *    helic75_value_6,  (1/root2))
svr7  = np.power(Shear30_value1 *  cape1k_SMT7 *    helic75_value1,   (1/root2))
svr8  = np.power(Shear30_value2 *  cape1k_SMT8 *    helic75_value2,   (1/root2))
svr9  = np.power(Shear30_value3 *  cape1k_SMT9 *    helic75_value3,   (1/root2))
svr10 = np.power(Shear30_value4  * cape1k_SMT10 * helic75_value4 ,  (1/root2))
svr11 = np.power(Shear30_value5  * cape1k_SMT11 * helic75_value5 ,  (1/root2))
svr12 = np.power(Shear30_value6  * cape1k_SMT12 * helic75_value6 ,  (1/root2))
svr13 = np.power(Shear30_value7  * cape1k_SMT13 * helic75_value7 ,  (1/root2))
svr14 = np.power(Shear30_value8  * cape1k_SMT14 * helic75_value8 ,  (1/root2))
svr15 = np.power(Shear30_value9  * cape1k_SMT15 * helic75_value9 ,  (1/root2))
svr16 = np.power(Shear30_value10 * cape1k_SMT16 * helic75_value10,  (1/root2))
svr17 = np.power(Shear30_value11 * cape1k_SMT17 * helic75_value11,  (1/root2))
svr18 = np.power(Shear30_value12 * cape1k_SMT18 * helic75_value12,  (1/root2))
svr19 = np.power(Shear30_value13 * cape1k_SMT19 * helic75_value13,  (1/root2))
svr20 = np.power(Shear30_value14 * cape1k_SMT20 * helic75_value14,  (1/root2))
svr21 = np.power(Shear30_value15 * cape1k_SMT21 * helic75_value15,  (1/root2))
svr22 = np.power(Shear30_value16 * cape1k_SMT22 * helic75_value16,  (1/root2))
svr23 = np.power(Shear30_value17 * cape1k_SMT23 * helic75_value17,  (1/root2))
svr24 = np.power(Shear30_value18 * cape1k_SMT24 * helic75_value18,  (1/root2))


S1  = np.where(t_1  >= 20, svr1 , 0)
S2  = np.where(t_2  >= 20, svr2 , 0)
S3  = np.where(t_3  >= 20, svr3 , 0)
S4  = np.where(t_4  >= 20, svr4 , 0)
S5  = np.where(t_5  >= 20, svr5 , 0)
S6  = np.where(t_6  >= 20, svr6 , 0)
S7 = np.where(t1  >= 20, svr7, 0)
S8 = np.where(t2  >= 20, svr8, 0)
S9 = np.where(t3  >= 20, svr9, 0)
S10 = np.where(t4  >= 20, svr10, 0)
S11 = np.where(t5  >= 20, svr11, 0)
S12 = np.where(t6  >= 20, svr12, 0)
S13 = np.where(t7  >= 20, svr13, 0)
S14 = np.where(t8  >= 20, svr14, 0)
S15 = np.where(t9  >= 20, svr15, 0)
S16 = np.where(t10 >= 20, svr16, 0)
S17 = np.where(t11 >= 20, svr17, 0)
S18 = np.where(t12 >= 20, svr18, 0)
S19 = np.where(t13 >= 20, svr19, 0)
S20 = np.where(t14 >= 20, svr20, 0)
S21 = np.where(t15 >= 20, svr21, 0)
S22 = np.where(t16 >= 20, svr22, 0)
S23 = np.where(t17 >= 20, svr23, 0)
S24 = np.where(t18 >= 20, svr24, 0)

svr1c  = np.power(t_1*  S1,  (1/root))
svr2c  = np.power(t_2*  S2,  (1/root))
svr3c  = np.power(t_3*  S3,  (1/root))
svr4c  = np.power(t_4*  S4,  (1/root))
svr5c  = np.power(t_5*  S5,  (1/root))
svr6c  = np.power(t_6*  S6,  (1/root))
svr7c  = np.power(t1  * SS7,  (1/root))
svr8c  = np.power(t2  * S8,  (1/root))
svr9c  = np.power(t3  * S9,  (1/root))
svr10c = np.power(t4  * S10,  (1/root))
svr11c = np.power(t5  * S11,  (1/root))
svr12c = np.power(t6  * S12,  (1/root))
svr13c = np.power(t7  * S13,  (1/root))
svr14c = np.power(t8  * S14,  (1/root))
svr15c = np.power(t9  * S15,  (1/root))
svr16c = np.power(t10 * S16,  (1/root))
svr17c = np.power(t11 * S17,  (1/root))
svr18c = np.power(t12 * S18,  (1/root))
svr19c = np.power(t13 * S19,  (1/root))
svr20c = np.power(t14 * S20,  (1/root))
svr21c = np.power(t15 * S21,  (1/root))
svr22c = np.power(t16 * S22,  (1/root))
svr23c = np.power(t17 * S23,  (1/root))
svr24c = np.power(t18 * S24,  (1/root))


# In[430]:


def plot_background(ax):
    ax.set_extent([-67.5, -74.5, 17.25, 20.5])
    ax.add_feature(cfeature.COASTLINE, linewidth=1.5)
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=2)

    return ax


fig, axarr = plt.subplots(nrows=4, ncols=3, figsize=(18, 18), constrained_layout=True,
                          subplot_kw={'projection': map_crs})
axlist = axarr.flatten()
for ax in axlist:
    plot_background(ax)

colormap = 'YlOrRd' #matplotlib.colors.ListedColormap(['#00eded','#00a1f5','#0000f5','#00ff00','#00c700','#008f00','#ffff00','#e8bf00','#ff8f00','#ff0000','#cc3300','#990000','#ff00ff','#9933cc'])
clev = [20, 40, 80, 100]
clev2 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100] #20%,40%,60%,80%,100%

# 1
cf1 = axlist[0].contourf(lons, lats, S1, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                         norm=plt.Normalize(5, 75))
c1 = axlist[0].contour(lons, lats, Ts1, clev,  colors='black', linewidths=1.8,transform=ccrs.PlateCarree())
axlist[0].clabel(c1, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[0].set_title('REFD 12PM', fontsize=16)
cb1 = fig.colorbar(cf1, ax=axlist[0], orientation='horizontal', shrink=0.74, pad=0)
cb1.set_label('dBZ', size='x-large')

# 2
cf2 = axlist[1].contourf(lons, lats, S2, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c2 = axlist[1].contour(lons, lats, Ts2, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c2, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[1].set_title('REFD 01PM', fontsize=16)
cb2 = fig.colorbar(cf2, ax=axlist[1], orientation='horizontal', shrink=0.74, pad=0)
cb2.set_label('dBZ', size='x-large')

# 3
cf3 = axlist[2].contourf(lons, lats, S3, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
c3 = axlist[2].contour(lons, lats, Ts3, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[2].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[2].set_title('REFD 02PM', fontsize=16)
cb3 = fig.colorbar(cf3, ax=axlist[2], orientation='horizontal', shrink=0.74, pad=0)
cb3.set_label('dBZ', size='x-large')

# 4
cf4 = axlist[3].contourf(lons, lats, S4, clev2, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[3].set_title('REFD 03PM', fontsize=16)
c4 = axlist[3].contour(lons, lats, Ts4, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb4 = fig.colorbar(cf4, ax=axlist[3], orientation='horizontal', shrink=0.74, pad=0)
cb4.set_label('dBZ', size='x-large')

# 5
cf5 = axlist[4].contourf(lons, lats, S5, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c5 = axlist[4].contour(lons, lats, Ts5, clev,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[4].clabel(c5, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[4].set_title('REFD 04PM', fontsize=16)
cb5 = fig.colorbar(cf5, ax=axlist[4], orientation='horizontal', shrink=0.74, pad=0)
cb5.set_label('dBZ', size='x-large')

# 6
cf6 = axlist[5].contourf(lons, lats, S6, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c6 = axlist[5].contour(lons, lats, Ts6, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[5].clabel(c6, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[5].set_title('REFD 05PM', fontsize=16)
cb6 = fig.colorbar(cf6, ax=axlist[5], orientation='horizontal', shrink=0.74, pad=0)
cb6.set_label('dBZ', size='x-large')

# 7
cf7 = axlist[6].contourf(lons, lats, S7, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[6].set_title('REFD 06PM', fontsize=16)
c7 = axlist[6].contour(lons, lats, Ts7, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[6].clabel(c7, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb7 = fig.colorbar(cf7, ax=axlist[6], orientation='horizontal', shrink=0.74, pad=0)
cb7.set_label('dBZ', size='x-large')

# 8
cf8 = axlist[7].contourf(lons, lats, S8, clev2, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[7].set_title('REFD 07PM', fontsize=16)
c8 = axlist[7].contour(lons, lats, Ts8, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[7].clabel(c8, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb8 = fig.colorbar(cf8, ax=axlist[7], orientation='horizontal', shrink=0.74, pad=0)
cb8.set_label('dBZ', size='x-large')

# 9
cf9 = axlist[8].contourf(lons, lats, S9, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c9 = axlist[8].contour(lons, lats, Ts9, clev,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[8].clabel(c9, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[8].set_title('REFD 08PM', fontsize=16)
cb9 = fig.colorbar(cf9, ax=axlist[8], orientation='horizontal', shrink=0.74, pad=0)
cb9.set_label('dBZ', size='x-large')

# 10
cf10 = axlist[9].contourf(lons, lats, S10, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c10 = axlist[9].contour(lons, lats, Ts10, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[9].clabel(c10, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[9].set_title('REFD 09PM', fontsize=16)
cb10 = fig.colorbar(cf10, ax=axlist[9], orientation='horizontal', shrink=0.74, pad=0)
cb10.set_label('dBZ', size='x-large')

# 11
cf11 = axlist[10].contourf(lons, lats, S11, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[10].set_title('REFD 10PM', fontsize=16)
c11 = axlist[10].contour(lons, lats, Ts11, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[10].clabel(c11, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb11 = fig.colorbar(cf11, ax=axlist[10], orientation='horizontal', shrink=0.74, pad=0)
cb11.set_label('dBZ', size='x-large')

# 12
cf12 = axlist[11].contourf(lons, lats, S12, clev2, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[11].set_title('REFD 11PM', fontsize=16)
c12 = axlist[11].contour(lons, lats, Ts12, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[11].clabel(c12, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb12 = fig.colorbar(cf12, ax=axlist[11], orientation='horizontal', shrink=0.74, pad=0)
cb12.set_label('dBZ', size='x-large')

fig.suptitle(f'REFLECTIVIDAD DERIVADA 1KM & PROBABILIDAD DE TRONADAS (Tarde-Noche)\nVálido para este {fecha_formateada} \n\nINIT: {hora_formateada} de este {fecha_formateada_dia_anterior}\n', fontsize=20)

fig.savefig(f'{save_path}/D1_TSRD_REFD_12H_PERIOD_TN_RD.png', bbox_inches='tight', dpi=400)


# In[431]:


def plot_background(ax):
    ax.set_extent([-67.5, -74.5, 17.25, 20.5])
    ax.add_feature(cfeature.COASTLINE, linewidth=1.5)
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=2)

    return ax


fig, axarr = plt.subplots(nrows=4, ncols=3, figsize=(18, 18), constrained_layout=True,
                          subplot_kw={'projection': map_crs})
axlist = axarr.flatten()
for ax in axlist:
    plot_background(ax)

colormap = 'YlOrRd' #matplotlib.colors.ListedColormap(['#00eded','#00a1f5','#0000f5','#00ff00','#00c700','#008f00','#ffff00','#e8bf00','#ff8f00','#ff0000','#cc3300','#990000','#ff00ff','#9933cc'])
clev = [20, 40, 80, 100]
clev2 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100] #20%,40%,60%,80%,100%

# 1
cf1 = axlist[0].contourf(lons, lats, S13, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                         norm=plt.Normalize(5, 75))
c1 = axlist[0].contour(lons, lats, Ts13, clev,  colors='black', linewidths=1.8,transform=ccrs.PlateCarree())
axlist[0].clabel(c1, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[0].set_title('REFD 12PM', fontsize=16)
cb1 = fig.colorbar(cf1, ax=axlist[0], orientation='horizontal', shrink=0.74, pad=0)
cb1.set_label('dBZ', size='x-large')

# 2
cf2 = axlist[1].contourf(lons, lats, S14, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c2 = axlist[1].contour(lons, lats, Ts14, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c2, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[1].set_title('REFD 01PM', fontsize=16)
cb2 = fig.colorbar(cf2, ax=axlist[1], orientation='horizontal', shrink=0.74, pad=0)
cb2.set_label('dBZ', size='x-large')

# 3
cf3 = axlist[2].contourf(lons, lats, S15, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
c3 = axlist[2].contour(lons, lats, Ts15, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[2].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[2].set_title('REFD 02PM', fontsize=16)
cb3 = fig.colorbar(cf3, ax=axlist[2], orientation='horizontal', shrink=0.74, pad=0)
cb3.set_label('dBZ', size='x-large')

# 4
cf4 = axlist[3].contourf(lons, lats, S16, clev2, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[3].set_title('REFD 03PM', fontsize=16)
c4 = axlist[3].contour(lons, lats, Ts16, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb4 = fig.colorbar(cf4, ax=axlist[3], orientation='horizontal', shrink=0.74, pad=0)
cb4.set_label('dBZ', size='x-large')

# 5
cf5 = axlist[4].contourf(lons, lats, S17, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c5 = axlist[4].contour(lons, lats, Ts17, clev,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[4].clabel(c5, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[4].set_title('REFD 04PM', fontsize=16)
cb5 = fig.colorbar(cf5, ax=axlist[4], orientation='horizontal', shrink=0.74, pad=0)
cb5.set_label('dBZ', size='x-large')

# 6
cf6 = axlist[5].contourf(lons, lats, S18, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c6 = axlist[5].contour(lons, lats, Ts18, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[5].clabel(c6, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[5].set_title('REFD 05PM', fontsize=16)
cb6 = fig.colorbar(cf6, ax=axlist[5], orientation='horizontal', shrink=0.74, pad=0)
cb6.set_label('dBZ', size='x-large')

# 7
cf7 = axlist[6].contourf(lons, lats, S19, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[6].set_title('REFD 06PM', fontsize=16)
c7 = axlist[6].contour(lons, lats, Ts19, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[6].clabel(c7, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb7 = fig.colorbar(cf7, ax=axlist[6], orientation='horizontal', shrink=0.74, pad=0)
cb7.set_label('dBZ', size='x-large')

# 8
cf8 = axlist[7].contourf(lons, lats, S20, clev2, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[7].set_title('REFD 07PM', fontsize=16)
c8 = axlist[7].contour(lons, lats, Ts20, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[7].clabel(c8, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb8 = fig.colorbar(cf8, ax=axlist[7], orientation='horizontal', shrink=0.74, pad=0)
cb8.set_label('dBZ', size='x-large')

# 9
cf9 = axlist[8].contourf(lons, lats, S21, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c9 = axlist[8].contour(lons, lats, Ts21, clev,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[8].clabel(c9, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[8].set_title('REFD 08PM', fontsize=16)
cb9 = fig.colorbar(cf9, ax=axlist[8], orientation='horizontal', shrink=0.74, pad=0)
cb9.set_label('dBZ', size='x-large')

# 10
cf10 = axlist[9].contourf(lons, lats, S22, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100))
c10 = axlist[9].contour(lons, lats, Ts22, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[9].clabel(c10, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[9].set_title('REFD 09PM', fontsize=16)
cb10 = fig.colorbar(cf10, ax=axlist[9], orientation='horizontal', shrink=0.74, pad=0)
cb10.set_label('dBZ', size='x-large')

# 11
cf11 = axlist[10].contourf(lons, lats, S23, clev2,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[10].set_title('REFD 10PM', fontsize=16)
c11 = axlist[10].contour(lons, lats, Ts23, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[10].clabel(c11, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb11 = fig.colorbar(cf11, ax=axlist[10], orientation='horizontal', shrink=0.74, pad=0)
cb11.set_label('dBZ', size='x-large')

# 12
cf12 = axlist[11].contourf(lons, lats, S24, clev2, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(0, 100), zorder=0)
axlist[11].set_title('REFD 11PM', fontsize=16)
c12 = axlist[11].contour(lons, lats, Ts24, clev, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[11].clabel(c12, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb12 = fig.colorbar(cf12, ax=axlist[11], orientation='horizontal', shrink=0.74, pad=0)
cb12.set_label('dBZ', size='x-large')

fig.suptitle(f'REFLECTIVIDAD DERIVADA 1KM & PROBABILIDAD DE TRONADAS (Tarde-Noche)\nVálido para este {fecha_formateada} \n\nINIT: {hora_formateada} de este {fecha_formateada_dia_anterior}\n', fontsize=20)

fig.savefig(f'{save_path}/D1_TSRD_REFD_12H_PERIOD_TN_RD.png', bbox_inches='tight', dpi=400)


# In[432]:


S_max = np.maximum.reduce([
S1, 
S2, 
S3, 
S4, 
S5, 
S6, 
S7, 
S8, 
S9, 
S10, 
S11, 
S12, 
S13, 
S14, 
S15, 
S16, 
S17, 
S18, 
S19, 
S20, 
S21, 
S22, 
S23, 
S24])

S_maxSMT = ndimage.gaussian_filter(S_max, sigma=1.5, order=0)


SC_max = np.maximum.reduce([
svr1c,  
svr2c,  
svr3c,  
svr4c,  
svr5c,  
svr6c,  
svr7c,  
svr8c,  
svr9c,  
svr10c, 
svr11c, 
svr12c, 
svr13c, 
svr14c, 
svr15c, 
svr16c, 
svr17c, 
svr18c, 
svr19c, 
svr20c, 
svr21c, 
svr22c, 
svr23c, 
svr24c])

SC_maxSMT = ndimage.gaussian_filter(SC_max, sigma=1.5, order=0)


# In[433]:


fig = plt.figure (1,figsize=(20,22))
ax=plt.subplot(1,1,1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space
ax.set_extent ([-67.5, -74.5, 17.25, 20.5], data_crs)
ax.add_feature(cfeature.COASTLINE, linewidth=2)
ax.add_feature(cfeature.BORDERS, linewidth=2)


colormap = 'YlOrRd' #matplotlib.colors.ListedColormap(['#00c700','#ffff00','#ff8f00','#cc3300'])

clev = [1, 20, 40, 60, 80, 100]
clev2 = [5, 20, 40, 60, 80, 100]

cf = ax.contourf(lons,lats, S_maxSMT, clev, extend='neither', cmap=colormap, transform=data_crs, 
                 norm=plt.Normalize(0, 100))

cb = plt.colorbar(cf, ax=ax, orientation='horizontal',pad=0.05, extendrect='true', ticks=clev)
cb.set_label(r'PORCIENTO', size='xx-large')

cs1 = ax.contour(lons, lats, S_maxSMT, clev, colors='black',
              linestyles='solid', transform=data_crs)
ax.set_title(f'PROBABILIDAD GENERAL DE CONDICIONES DE TIEMPO SEVERO | 12AM - 12AM \n{fecha_formateada} | DATA: {hora_formateada}', fontsize=22)
ax.clabel(cs1, fmt='%d', fontsize=20)

# PR COUNTIES SHAPEFILES
shapefile1_path = 'shp/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp'
gdf1 = gpd.read_file(shapefile1_path)
county_PR = ShapelyFeature(gdf1['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_PR)

shapefile2_path = 'shp/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_RD)

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

plt.show()
plt.show()

fig.savefig(f'{save_path}/D1n_TSRD_PROB-AGUAC_TN_RD.png', bbox_inches='tight', dpi=300)


# In[434]:


import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from cartopy.feature import ShapelyFeature
from matplotlib import offsetbox
import matplotlib.patheffects as path_effects

# Define the coordinate reference systems
map_crs = ccrs.PlateCarree()
data_crs = ccrs.PlateCarree()

# Create the figure and axis
fig = plt.figure(1, figsize=(20, 22))
ax = plt.subplot(1, 1, 1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space

# Set the extent of the map
ax.set_extent([-67.5, -72.5, 17.25, 20.25], crs=data_crs)

# Add features to the map
ax.add_feature(cfeature.COASTLINE, linewidth=3.5)
ax.add_feature(cfeature.BORDERS, linewidth=3.5, zorder=3)
ax.add_feature(cfeature.OCEAN, facecolor='#00374d', zorder=3)
ax.add_feature(cfeature.LAND, facecolor='#b3b4b3')
ax.add_feature(cfeature.LAKES, linewidth=2, zorder=3, edgecolor='black', alpha=1)

# Define colormap and contour levels for the first data set
colormap2 = matplotlib.colors.ListedColormap(['#b9eac3', '#79c789', '#478f55', '#02757f', '#015057'])
clev = [20, 60, 80, 100]

# Assuming lons, lats, max_final_rain_int, and Thunder are already defined
# If not, you need to define these variables
# lons = ...
# lats = ...
# max_final_rain_int = ...
# Thunder = ...

# Plot the filled contours
#cf1 = ax.contourf(lons, lats, max_final_rain_int, clev, extend='neither', cmap=colormap2, transform=data_crs, 
                 # norm=plt.Normalize(10, 100))

# Position and customize the color bar
#cax = fig.add_axes([0.515, 0.28, 0.48, 0.04])  # Adjust the position as needed
#cb = plt.colorbar(cf1, cax=cax, orientation='horizontal', extendrect='true', drawedges=True)
#cb.set_ticks([])  # Hide the ticks
#cb.outline.set_edgecolor('k')  # Set color of the outline
#cb.outline.set_linewidth(3)  # Set the width of the outline
#cb.dividers.set_color('k')  # Set color of the dividers
#cb.dividers.set_linewidth(3)  # Set the width of the dividers

# Add Dominican lakes (if the default lakes feature does not include them, create a custom one)
canada_lakes = cfeature.NaturalEarthFeature(
    category='physical',
    name='lakes',
    scale='10m',
    facecolor='none'
)
ax.add_feature(canada_lakes, edgecolor='black', linewidth=1)


# Define the second colormap and contour levels
colormap = 'YlOrRd' #matplotlib.colors.ListedColormap(['#00c700','#ffff00','#ff8f00','#cc3300'])

clev = [1, 20, 40, 60, 80, 100]

# Plot the second set of filled contours
cf = ax.contourf(lons, lats, S_maxSMT, clev, extend='neither', transform=data_crs, norm=plt.Normalize(10, 100), cmap=colormap, alpha=1)

# Position and customize the second color bar
cax = fig.add_axes([0.1, 0.245, 0.8, 0.04], zorder=0)  # Adjust the position as needed
cb = plt.colorbar(cf, cax=cax, orientation='horizontal', extendrect='true', drawedges=True)
cb.set_ticks([1, 20, 40, 60, 80, 100])  # Hide the ticks
cb.ax.xaxis.set_tick_params(color='white')
plt.setp(plt.getp(cb.ax, 'xticklabels'), color='white', fontsize=20, fontweight='bold')
cb.outline.set_edgecolor('k')  # Set color of the outline
cb.outline.set_linewidth(3)  # Set the width of the outline
cb.dividers.set_color('k')  # Set color of the dividers
cb.dividers.set_linewidth(3)  # Set the width of the dividers

# Plot the second set of line contours
cs1 = ax.contour(lons, lats, S_maxSMT, clev, colors='black', linestyles='solid', transform=data_crs, linewidths=2, fontsize=40)

# Set titles for the plot
#ax.set_title(f'PROBABILIDAD GENERAL DE CONDICIONES DE TIEMPO SUB-SEVERO | 24 HORAS (12AM - 12AM) \nVálido para este {fecha_formateada}', loc='left', fontsize=22, fontweight='bold')
#ax.set_title(f'INIT: {hora_formateada} de este {fecha_formateada_dia_anterior}', loc='right', fontsize=16, fontweight='bold', style='italic')

# Add shapefile data
shapefile2_path = 'shp/rd/geoBoundaries-DOM-ADM1_simplified.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=1.5)
ax.add_feature(county_RD)

# Add shapefile data
shapefile3_path = 'shp/haiti/ne_10m_admin_0_countries.shp'
gdf3 = gpd.read_file(shapefile3_path)
county_HTI = ShapelyFeature(gdf3['geometry'], ccrs.PlateCarree(), facecolor='grey', edgecolor='black', lw=1, zorder=2)
ax.add_feature(county_HTI)

# Dictionary of important cities with their coordinates
cities = {
    "Santo Domingo": {"lat": 18.4861, "lon": -69.9312},
    "Santiago": {"lat": 19.4792, "lon": -70.6931},
    "La Romana": {"lat": 18.4333, "lon": -68.9667},
    "Punta Cana": {"lat": 18.582, "lon": -68.4055},
    "Puerto Plata": {"lat": 19.7975, "lon": -70.6884},
    "La Vega": {"lat": 19.2232, "lon": -70.5294},
    "Bonao": {"lat": 18.9356, "lon": -70.4094},
    "Baní": {"lat": 18.2796, "lon": -70.3319},
    "Azua": {"lat": 18.4532, "lon": -70.7349},
    "Barahona": {"lat": 18.2085, "lon": -71.1008},
    "Montecristi": {"lat": 19.8489, "lon": -71.6464},
    "Dajabón": {"lat": 19.5483, "lon": -71.7083},
    "Samaná": {"lat": 19.2057, "lon": -69.3367},
    "V. Altagracia": {"lat": 18.6700, "lon": -70.1700},
    "El Seibo": {"lat": 18.7650, "lon": -69.0383},
    "Nagua": {"lat": 19.3833, "lon": -69.8500},
    "San Juan": {"lat": 18.8050, "lon": -71.2300},
    "Pedernales": {"lat": 18.0370, "lon": -71.7440},
    "Ocoa": {"lat": 18.5500, "lon": -70.5000},
    "Oviedo": {"lat": 17.8007, "lon": -71.4008},
    "S. de la Mar": {"lat": 19.0579, "lon": -69.3892},
    "Monte Plata": {"lat": 18.8073, "lon": -69.7850},
    "Pimentel": {"lat": 19.1832, "lon": -70.1085},
    "Mao": {"lat": 19.5511, "lon": -71.0781},
    "Neyba": {"lat": 18.4847, "lon": -71.4194},
    "Pedro Santana": {"lat": 19.1050, "lon": -71.6959},
    "Elías Piña": {"lat": 18.8770, "lon": -71.7048},
    "Restauración": {"lat": 19.3159, "lon": -71.6947},
    "SAJOMA": {"lat": 19.3405, "lon": -70.9376}
}

# Add city names and dots to the plot
for city, coords in cities.items():
    ax.plot(coords["lon"], coords["lat"], 'o', color='k', markersize=10, transform=data_crs, path_effects=[path_effects.withStroke(linewidth=5, foreground='white')])  # Add a red dot
    ax.text(coords["lon"], coords["lat"], city, transform=data_crs, fontsize=22, fontweight='bold',
            ha='left', color='white', path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])

# Dictionary of important cities with their coordinates
cities2 = {
    "Higuey": {"lat": 18.6150, "lon": -68.7070},
    "Constanza": {"lat": 18.9094, "lon": -70.7208},

}

# Add city names and dots to the plot
for city, coords in cities2.items():
    ax.plot(coords["lon"], coords["lat"], 'o', color='k', markersize=10, transform=data_crs, path_effects=[path_effects.withStroke(linewidth=5, foreground='white')])  # Add a red dot
    ax.text(coords["lon"], coords["lat"], city, transform=data_crs, fontsize=22, fontweight='bold',
            ha='right', color='white', path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])

# Add text annotations
text1 = ax.text(0.5, 0.125, 'PROBABILIDADES', ha='center', va='center', fontsize=40, transform=ax.transAxes, fontweight='bold', color='white')
text1.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

text2 = ax.text(0.84, 0.75, f'Válidez del Mapa: \n 12:00 AM - 12:00 AM del \n {fecha_formateada}', ha='center', va='center', fontsize=25, transform=ax.transAxes, fontweight='bold', color='white')
text2.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

text4 = ax.text(0.84, 0.985, f'INIT: {hora_formateada} de este {fecha_formateada_dia_anterior}', ha='center', va='center', fontsize=16, transform=ax.transAxes, fontweight='bold', color='white')
text4.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

text3 = ax.text(0.32, 0.95, 'MAPA DE CONDICIONES SEVERAS', ha='center', va='center', fontsize=35, transform=ax.transAxes, fontweight='bold', color='white', zorder=5)
text3.set_path_effects([path_effects.withStroke(linewidth=5, foreground='k')])  # Add white shadow effect

def add_rounded_rect_with_shadow(ax, xy, width, height, rounding_size=0.1, shadow_offset=(0.02, -0.02)):
    # Add shadow
    shadow = FancyBboxPatch(
        (xy[0] + shadow_offset[0], xy[1] + shadow_offset[1]), width, height,
        boxstyle=f"round,pad=0.05,rounding_size={rounding_size}",
        edgecolor='none', facecolor='black', alpha=0.3,
        transform=data_crs, zorder=3
    )
    ax.add_patch(shadow)

    # Add rectangle
    rect = FancyBboxPatch(
        xy, width, height,
        boxstyle=f"round,pad=0.05,rounding_size={rounding_size}",
        edgecolor='k', facecolor='#b60026', alpha=1,
        transform=data_crs, linewidth=2, zorder=4
    )
    ax.add_patch(rect)

# Define the position and size of the rectangle
rect_xy = (-72.4, 20.05)
rect_width = 3
rect_height = 0.1

# Add the rectangle with shadow to the plot
add_rounded_rect_with_shadow(ax, rect_xy, rect_width, rect_height)

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

# Save the figure
fig.savefig(f'{save_path}/D1_TSRD_PROB-TRON_24_RD.png', bbox_inches='tight', dpi=300)


# In[435]:


fig = plt.figure (1,figsize=(20,22))
ax=plt.subplot(1,1,1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space
ax.set_extent ([-64.5, -68, 17.5, 19], data_crs)
ax.add_feature(cfeature.COASTLINE, linewidth=2)
ax.add_feature(cfeature.BORDERS, linewidth=2)


colormap = matplotlib.colors.ListedColormap(['#00c700','#ffff00','#ff8f00','#cc3300'])

clev = [20, 40, 60, 80, 100]

cf = ax.contourf(lons,lats, max_final_rain_int, clev, extend='neither', cmap='viridis', transform=data_crs, 
                 norm=plt.Normalize(1, 100))

cb = plt.colorbar(cf, ax=ax, orientation='horizontal',pad=0.05, extendrect='true', ticks=clev)
cb.set_label(r'PORCIENTO', size='xx-large')

cs1 = ax.contour(lons, lats, max_final_rain_int, clev, colors='black',
              linestyles='solid', transform=data_crs)
ax.set_title(f'PROBABILIDAD DE AGUACEROS TARDE & NOCHE | 12PM - 12AM \n{fecha_formateada} | DATA: {hora_formateada}', fontsize=22)
ax.clabel(cs1, fmt='%d', fontsize=20)

# PR COUNTIES SHAPEFILES
shapefile1_path = 'shp/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp'
gdf1 = gpd.read_file(shapefile1_path)
county_PR = ShapelyFeature(gdf1['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_PR)

shapefile2_path = 'shp/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_RD)

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

plt.show()
plt.show()

fig.savefig(f'{save_path}/D1n_TSRD_PROB-AGUAC_TN_RD.png', bbox_inches='tight', dpi=300)


# In[436]:


fig = plt.figure (1,figsize=(20,22))
ax=plt.subplot(1,1,1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space
ax.set_extent ([-64.5, -68, 17.5, 19], data_crs)
ax.add_feature(cfeature.COASTLINE, linewidth=2)
ax.add_feature(cfeature.BORDERS, linewidth=2)
ax.add_feature(cfeature.STATES, linewidth=2)
ax.add_feature(cfeature.OCEAN, facecolor='#00374d', zorder=12)
ax.add_feature(cfeature.LAND, facecolor='#b3b4b3')


#Filter2 = np.where(Thunder <= 20, max_crain_int == Thunder, max_EAS2p5)


colormap2 = matplotlib.colors.ListedColormap(['#79c789','#478f55','#02757f', '#015057'])

clev = [20, 40, 80, 100]

cf = ax.contourf(lons,lats, max_final_rain_int, clev, extend='neither', cmap=colormap2, transform=data_crs, 
                 norm=plt.Normalize(40, 100))

#cb = plt.colorbar(cf, ax=ax, orientation='horizontal',pad=0.01, extendrect='true', ticks=clev)
#cb.set_label(r'PORCIENTO', size='xx-large')

cs1 = ax.contour(lons, lats, max_final_rain_int, clev, colors='black',
              linestyles='solid', transform=data_crs, zorder=1,linewidths=2)
#ax.clabel(cs1, fmt='%d', fontsize=20)

#------------------------------------------------------------------------------------------------------
Filter = np.where(max_final_rain_int <= 20, 0, Thunder) 

colormap = matplotlib.colors.ListedColormap(['#fefea6','#ffff00','#ff8f00','#cc3300','#9f0101'])

clev = [20, 30, 40, 60, 80, 100]

cf = ax.contourf(lons,lats, Filter, clev, extend='neither', transform=data_crs, 
                norm=plt.Normalize(10, 100), cmap=colormap)

cb = plt.colorbar(cf, ax=ax, orientation='horizontal',pad=0.01, extendrect='true', ticks=clev)
cb.set_label(r'PORCIENTO', size=16)
cb.ax.tick_params(labelsize=16)

cs1 = ax.contour(lons, lats, Filter, clev, colors='black',
                linestyles='solid', transform=data_crs, linewidths=2, fontsize=40)
#ax.clabel(cs1, fmt='%d', fontsize=20)

ax.set_title(f'HREFv3 » EVALUACIÓN DE PROBABILIDADES DE AGUACEROS Y TRONADAS (Experimental) - 24 HORAS (12AM - 12AM) \nVálido para este {fecha_formateada}',loc='left', fontsize=22, fontweight='bold')
ax.set_title(f'INIT: {hora_formateada} de este {fecha_formateada_dia_anterior}', loc='right', fontsize=16, fontweight='bold', style='italic')

# PR COUNTIES SHAPEFILES
shapefile1_path = 'shp/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp'
gdf1 = gpd.read_file(shapefile1_path)
county_PR = ShapelyFeature(gdf1['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_PR)


# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

fig.savefig(f'{save_path}/D1_TSRD_PROB-TRON_24_RD.png', bbox_inches='tight', dpi=300)


# In[437]:


fig = plt.figure (1,figsize=(20,20))
ax=plt.subplot(1,1,1, projection=map_crs)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space
ax.set_extent ([-64.5, -68, 17.5, 19], data_crs)
ax.add_feature(cfeature.STATES, linewidth=2)
ax.add_feature(cfeature.BORDERS, linewidth=2)

colormap = matplotlib.colors.ListedColormap(['#00eded','#00a1f5','#0000f5','#00ff00','#00c700','#008f00','#ffff00',
                                             '#e8bf00','#ff8f00','#ff0000','#cc3300','#990000','#ff00ff','#9933cc'])

clev = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
clev2 = [30, 40, 80, 100]

cf = ax.contourf(lons,lats,REFD_max_value, clev, extend='neither', cmap=colormap, 
                 norm=plt.Normalize(5, 75), transform=data_crs)

cb = plt.colorbar(cf, ax=ax, orientation='horizontal', pad=0.05, extendrect='True', ticks=clev)
cb.set_label(r'Milimetros', size='large')

cs1 = ax.contour(lons, lats, Filter, clev2, colors='black',
                 linestyles='solid', transform=data_crs, linewidths=2)
ax.set_title(f'REFD & THUNDER | 12AM - 12AM \n{fecha_formateada} | DATA: {hora_formateada}', fontsize=22)
ax.clabel(cs1, fmt='%d')

# PR COUNTIES SHAPEFILES
shapefile1_path = 'shp/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp'
gdf1 = gpd.read_file(shapefile1_path)
county_PR = ShapelyFeature(gdf1['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_PR)

shapefile2_path = 'shp/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp'
gdf2 = gpd.read_file(shapefile2_path)
county_RD = ShapelyFeature(gdf2['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)
ax.add_feature(county_RD)

# Add the logo using matplotlib.offsetbox
logo = plt.imread(logo_path)
logo_position = (0.86, 0.91)  # Adjust the position as needed

# Create an offset box for the logo
logo_box = offsetbox.OffsetImage(logo, zoom=0.8, resample=True)
ab = offsetbox.AnnotationBbox(logo_box, (logo_position[0], logo_position[1]), xycoords='axes fraction', boxcoords='axes fraction', frameon=False)

# Add the offset box to the axes
ax.add_artist(ab)

plt.show()
plt.show()

fig.savefig(f'{save_path}/D1_TSRD_REFD_PROB-TRON_24_PR.png', bbox_inches='tight', dpi=300)


# In[438]:


def plot_background(ax):

# PR COUNTIES SHAPEFILES
    shapefile1_path = 'shp/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp'
    gdf1 = gpd.read_file(shapefile1_path)
    county_PR = ShapelyFeature(gdf1['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)

    ax.set_extent([-64.5, -68, 17.5, 19])
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space
    ax.add_feature(cfeature.COASTLINE, linewidth=2)
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=2)
    ax.add_feature(county_PR)

    return ax


fig, axarr = plt.subplots(nrows=4, ncols=3, figsize=(18, 18), constrained_layout=True,
                          subplot_kw={'projection': map_crs})
axlist = axarr.flatten()
for ax in axlist:
    plot_background(ax)

colormap = matplotlib.colors.ListedColormap(['#00eded','#00a1f5','#0000f5','#00ff00','#00c700','#008f00','#ffff00','#e8bf00','#ff8f00','#ff0000','#cc3300','#990000','#ff00ff','#9933cc'])
clev = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
clev2 = [20, 30, 80, 100] #20%,40%,60%,80%,100%

# 1
cf1 = axlist[0].contourf(lons, lats, REFD_1, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                         norm=plt.Normalize(5, 75))
c1 = axlist[0].contour(lons, lats, Ts1, clev2,  colors='black', linewidths=1.8,transform=ccrs.PlateCarree())
axlist[0].clabel(c1, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[0].set_title('REFD 12AM', fontsize=16)
cb1 = fig.colorbar(cf1, ax=axlist[0], orientation='horizontal', shrink=0.74, pad=0)
cb1.set_label('dBZ', size='x-large')

# 2
cf2 = axlist[1].contourf(lons, lats, REFD_2, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c2 = axlist[1].contour(lons, lats, Ts2, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c2, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[1].set_title('REFD 01AM', fontsize=16)
cb2 = fig.colorbar(cf2, ax=axlist[1], orientation='horizontal', shrink=0.74, pad=0)
cb2.set_label('dBZ', size='x-large')

# 3
cf3 = axlist[2].contourf(lons, lats, REFD_3, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75), zorder=0)
c3 = axlist[2].contour(lons, lats, Ts3, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[2].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[2].set_title('REFD 02AM', fontsize=16)
cb3 = fig.colorbar(cf3, ax=axlist[2], orientation='horizontal', shrink=0.74, pad=0)
cb3.set_label('dBZ', size='x-large')

# 4
cf4 = axlist[3].contourf(lons, lats, REFD_4, clev, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75), zorder=0)
axlist[3].set_title('REFD 03AM', fontsize=16)
c4 = axlist[3].contour(lons, lats, Ts4, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb4 = fig.colorbar(cf4, ax=axlist[3], orientation='horizontal', shrink=0.74, pad=0)
cb4.set_label('dBZ', size='x-large')

# 5
cf5 = axlist[4].contourf(lons, lats, REFD_5, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c5 = axlist[4].contour(lons, lats, Ts5, clev2,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[4].clabel(c5, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[4].set_title('REFD 04AM', fontsize=16)
cb5 = fig.colorbar(cf5, ax=axlist[4], orientation='horizontal', shrink=0.74, pad=0)
cb5.set_label('dBZ', size='x-large')

# 6
cf6 = axlist[5].contourf(lons, lats, REFD_6, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c6 = axlist[5].contour(lons, lats, Ts6, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[5].clabel(c6, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[5].set_title('REFD 05AM', fontsize=16)
cb6 = fig.colorbar(cf6, ax=axlist[5], orientation='horizontal', shrink=0.74, pad=0)
cb6.set_label('dBZ', size='x-large')

# 7
cf7 = axlist[6].contourf(lons, lats, REFD1, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75), zorder=0)
axlist[6].set_title('REFD 06AM', fontsize=16)
c7 = axlist[6].contour(lons, lats, Ts7, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[6].clabel(c7, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb7 = fig.colorbar(cf7, ax=axlist[6], orientation='horizontal', shrink=0.74, pad=0)
cb7.set_label('dBZ', size='x-large')

# 8
cf8 = axlist[7].contourf(lons, lats, REFD2, clev, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75), zorder=0)
axlist[7].set_title('REFD 07AM', fontsize=16)
c8 = axlist[7].contour(lons, lats, Ts8, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[7].clabel(c8, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb8 = fig.colorbar(cf8, ax=axlist[7], orientation='horizontal', shrink=0.74, pad=0)
cb8.set_label('dBZ', size='x-large')

# 9
cf9 = axlist[8].contourf(lons, lats, REFD3, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c9 = axlist[8].contour(lons, lats, Ts9, clev2,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[8].clabel(c9, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[8].set_title('REFD 08AM', fontsize=16)
cb9 = fig.colorbar(cf9, ax=axlist[8], orientation='horizontal', shrink=0.74, pad=0)
cb9.set_label('dBZ', size='x-large')

# 10
cf10 = axlist[9].contourf(lons, lats, REFD4, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c10 = axlist[9].contour(lons, lats, Ts10, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[9].clabel(c10, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[9].set_title('REFD 09AM', fontsize=16)
cb10 = fig.colorbar(cf10, ax=axlist[9], orientation='horizontal', shrink=0.74, pad=0)
cb10.set_label('dBZ', size='x-large')

# 11
cf11 = axlist[10].contourf(lons, lats, REFD5, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75), zorder=0)
axlist[10].set_title('REFD 10AM', fontsize=16)
c11 = axlist[10].contour(lons, lats, Ts11, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[10].clabel(c11, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb11 = fig.colorbar(cf11, ax=axlist[10], orientation='horizontal', shrink=0.74, pad=0)
cb11.set_label('dBZ', size='x-large')

# 12
cf12 = axlist[11].contourf(lons, lats, REFD6, clev, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75), zorder=0)
axlist[11].set_title('REFD 11AM', fontsize=16)
c12 = axlist[11].contour(lons, lats, Ts12, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[11].clabel(c12, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb12 = fig.colorbar(cf12, ax=axlist[11], orientation='horizontal', shrink=0.74, pad=0)
cb12.set_label('dBZ', size='x-large')

fig.suptitle(f'REFLECTIVIDAD DERIVADA 1KM & PROBABILIDAD DE TRONADAS (Madrugada-Mañana)\nVálido para este {fecha_formateada} \n\nINIT: {hora_formateada} de este {fecha_formateada_dia_anterior}\n', fontsize=20)

fig.savefig(f'{save_path}/D1_TSRD_REFD_12_PERIOD_MM_RD.png', bbox_inches='tight', dpi=400)


# In[439]:


def plot_background(ax):

# PR COUNTIES SHAPEFILES
    shapefile1_path = 'shp/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp'
    gdf1 = gpd.read_file(shapefile1_path)
    county_PR = ShapelyFeature(gdf1['geometry'], ccrs.PlateCarree(), facecolor='none', edgecolor='black', lw=0.5)

    ax.set_extent([-64.5, -68, 17.5, 19])
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Ensure the figure fills the entire space
    ax.add_feature(cfeature.COASTLINE, linewidth=2)
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=2)
    ax.add_feature(county_PR)

    return ax


fig, axarr = plt.subplots(nrows=4, ncols=3, figsize=(18, 18), constrained_layout=True,
                          subplot_kw={'projection': map_crs})
axlist = axarr.flatten()
for ax in axlist:
    plot_background(ax)

colormap = matplotlib.colors.ListedColormap(['#00eded','#00a1f5','#0000f5','#00ff00','#00c700','#008f00','#ffff00','#e8bf00','#ff8f00','#ff0000','#cc3300','#990000','#ff00ff','#9933cc'])
clev = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
clev2 = [30, 50, 80, 100] #20%,40%,60%,80%,100%

# 1
cf1 = axlist[0].contourf(lons, lats, REFC7, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                         norm=plt.Normalize(5, 75))
c1 = axlist[0].contour(lons, lats, Ts13, clev2,  colors='black', linewidths=1.8,transform=ccrs.PlateCarree())
axlist[0].clabel(c1, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[0].set_title('REFD 12PM', fontsize=16)
cb1 = fig.colorbar(cf1, ax=axlist[0], orientation='horizontal', shrink=0.74, pad=0)
cb1.set_label('dBZ', size='x-large')

# 2
cf2 = axlist[1].contourf(lons, lats, REFC8, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c2 = axlist[1].contour(lons, lats, Ts14, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c2, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[1].set_title('REFD 01PM', fontsize=16)
cb2 = fig.colorbar(cf2, ax=axlist[1], orientation='horizontal', shrink=0.74, pad=0)
cb2.set_label('dBZ', size='x-large')

# 3
cf3 = axlist[2].contourf(lons, lats, REFC9, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75), zorder=0)
c3 = axlist[2].contour(lons, lats, Ts15, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[2].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[2].set_title('REFD 02PM', fontsize=16)
cb3 = fig.colorbar(cf3, ax=axlist[2], orientation='horizontal', shrink=0.74, pad=0)
cb3.set_label('dBZ', size='x-large')

# 4
cf4 = axlist[3].contourf(lons, lats, REFC10, clev, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75), zorder=0)
axlist[3].set_title('REFD 03PM', fontsize=16)
c4 = axlist[3].contour(lons, lats, Ts16, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[1].clabel(c3, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb4 = fig.colorbar(cf4, ax=axlist[3], orientation='horizontal', shrink=0.74, pad=0)
cb4.set_label('dBZ', size='x-large')

# 5
cf5 = axlist[4].contourf(lons, lats, REFC11, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c5 = axlist[4].contour(lons, lats, Ts17, clev2,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[4].clabel(c5, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[4].set_title('REFD 04PM', fontsize=16)
cb5 = fig.colorbar(cf5, ax=axlist[4], orientation='horizontal', shrink=0.74, pad=0)
cb5.set_label('dBZ', size='x-large')

# 6
cf6 = axlist[5].contourf(lons, lats, REFC12, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c6 = axlist[5].contour(lons, lats, Ts18, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[5].clabel(c6, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[5].set_title('REFD 05PM', fontsize=16)
cb6 = fig.colorbar(cf6, ax=axlist[5], orientation='horizontal', shrink=0.74, pad=0)
cb6.set_label('dBZ', size='x-large')

# 7
cf7 = axlist[6].contourf(lons, lats, REFC13, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75), zorder=0)
axlist[6].set_title('REFD 06PM', fontsize=16)
c7 = axlist[6].contour(lons, lats, Ts19, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[6].clabel(c7, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb7 = fig.colorbar(cf7, ax=axlist[6], orientation='horizontal', shrink=0.74, pad=0)
cb7.set_label('dBZ', size='x-large')

# 8
cf8 = axlist[7].contourf(lons, lats, REFC14, clev, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75), zorder=0)
axlist[7].set_title('REFD 07PM', fontsize=16)
c8 = axlist[7].contour(lons, lats, Ts20, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[7].clabel(c8, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb8 = fig.colorbar(cf8, ax=axlist[7], orientation='horizontal', shrink=0.74, pad=0)
cb8.set_label('dBZ', size='x-large')

# 9
cf9 = axlist[8].contourf(lons, lats, REFC15, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c9 = axlist[8].contour(lons, lats, Ts21, clev2,  colors='black', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[8].clabel(c9, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[8].set_title('REFD 08PM', fontsize=16)
cb9 = fig.colorbar(cf9, ax=axlist[8], orientation='horizontal', shrink=0.74, pad=0)
cb9.set_label('dBZ', size='x-large')

# 10
cf10 = axlist[9].contourf(lons, lats, REFC16, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75))
c10 = axlist[9].contour(lons, lats, Ts22, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[9].clabel(c10, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
axlist[9].set_title('REFD 09PM', fontsize=16)
cb10 = fig.colorbar(cf10, ax=axlist[9], orientation='horizontal', shrink=0.74, pad=0)
cb10.set_label('dBZ', size='x-large')

# 11
cf11 = axlist[10].contourf(lons, lats, REFC17, clev,  cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75), zorder=0)
axlist[10].set_title('REFD 10PM', fontsize=16)
c11 = axlist[10].contour(lons, lats, Ts23, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[10].clabel(c11, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb11 = fig.colorbar(cf11, ax=axlist[10], orientation='horizontal', shrink=0.74, pad=0)
cb11.set_label('dBZ', size='x-large')

# 12```
cf12 = axlist[11].contourf(lons, lats, REFC18, clev, cmap=colormap, transform=ccrs.PlateCarree(),
                norm=plt.Normalize(5, 75), zorder=0)
axlist[11].set_title('REFD 11PM', fontsize=16)
c12 = axlist[11].contour(lons, lats, Ts24, clev2, colors='k', linewidths=1.8, transform=ccrs.PlateCarree())
axlist[11].clabel(c12, fontsize=10, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)
cb12 = fig.colorbar(cf12, ax=axlist[11], orientation='horizontal', shrink=0.74, pad=0)
cb12.set_label('dBZ', size='x-large')

fig.suptitle(f'REFLECTIVIDAD DERIVADA 1KM & PROBABILIDAD DE TRONADAS (Tarde-Noche)\nVálido para este {fecha_formateada} \n\nINIT: {hora_formateada} de este {fecha_formateada_dia_anterior}\n', fontsize=20)

fig.savefig(f'{save_path}/D1_TSRD_REFD_12_PERIOD_TN_RD.png', bbox_inches='tight', dpi=400)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




