import pandas as pd
import os
import calendar

from parametros import *
from logica import *
from grafica import generar_grafico

print("Leyendo archivo...")

df_proyectos = pd.read_excel(archivo, sheet_name="ProyectosBogota")
df_intermedia = pd.read_excel(archivo, sheet_name="ReunionesIntermedias")
df_semanal = pd.read_excel(archivo, sheet_name="ReunionesSemanales")

# LIMPIEZA
df_proyectos["Proyecto"] = df_proyectos["Proyecto"].apply(limpiar_texto)
df_intermedia["Proyecto"] = df_intermedia["Proyecto"].apply(limpiar_texto)
df_semanal["Proyecto"] = df_semanal["Proyecto"].apply(limpiar_texto)

# CALENDARIO
fechas_mes = pd.date_range(
    start=f"{ANIO}-{MES:02d}-01",
    end=f"{ANIO}-{MES:02d}-{calendar.monthrange(ANIO, MES)[1]}"
)

print("Calculando calendario teórico...")

df_proyectos["PosibleIntermedia"] = df_proyectos["DiaIntermedia"].apply(lambda x: calcular_posibles(x, fechas_mes))
df_proyectos["PosibleSemanal"] = df_proyectos["DiaSemanal"].apply(lambda x: calcular_posibles(x, fechas_mes))

df_proyectos["ConteoIntermedia"] = df_proyectos["PosibleIntermedia"].apply(contar_fechas_y_dividir)
df_proyectos["ConteoSemanal"] = df_proyectos["PosibleSemanal"].apply(contar_fechas_y_dividir)

# (aquí puedes seguir pegando tu lógica de merge y cumplimiento tal cual)

os.makedirs("output", exist_ok=True)

# GENERAR GRAFICO
generar_grafico(comparacion)

print("Proceso finalizado")
