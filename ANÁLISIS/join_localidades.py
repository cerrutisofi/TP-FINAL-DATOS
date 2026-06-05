# Acá vamos a hacer el join de las bases de Geolocalización de Vicente López y el set de Censo 2022
import pandas as pd
import numpy as np
# Se definen los dataset para trabajar con ellos
df_censo = pd.read_excel('/Users/juanmaseibane/Documents/COSAS MER/JOIN VILO/Censo 2022 - Vicente López.xlsx')
print(df_censo.head())
# Agregué una columna "LOCALIDAD" en el dataset de geolocalización para poder hacer el joim
df_geolocalizacion_localidades = pd.read_excel('/Users/juanmaseibane/Documents/COSAS MER/JOIN VILO/Geolocalización Vicente López - Unificado-modif.xlsx')
print(df_geolocalizacion_localidades.head())
# Ignoro espacios en blanco y mayúsculas para hacer bien el join por localidades
df_censo["Localidades"]= (df_censo["Localidades"] .str.strip() .str.lower())
df_geolocalizacion_localidades["Localidades"]= (df_geolocalizacion_localidades["Localidades"] .str.strip() .str.lower())
# Hago el join
df_juntos = pd.merge(df_geolocalizacion_localidades, df_censo, on = "Localidades" , how = "left")
print (df_juntos.head())

print(df_juntos.columns.tolist())
df_juntos.to_excel("geolocalizacion_censo_join.xlsx",index=False)