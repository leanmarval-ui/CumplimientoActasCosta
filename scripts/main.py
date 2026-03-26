import pandas as pd
import os
import calendar

from parametros import *
from logica import *
from grafica import generar_grafico

print("🔥 EJECUTANDO MAIN 🔥")
print("Leyendo archivo...")

# =========================
# LECTURA DE ARCHIVOS
# =========================
df_proyectos = pd.read_excel(archivo, sheet_name="ProyectosBogota")
df_intermedia = pd.read_excel(archivo, sheet_name="ReunionesIntermedias")
df_semanal = pd.read_excel(archivo, sheet_name="ReunionesSemanales")

# =========================
# LIMPIEZA
# =========================
df_proyectos["Proyecto"] = df_proyectos["Proyecto"].apply(limpiar_texto)
df_intermedia["Proyecto"] = df_intermedia["Proyecto"].apply(limpiar_texto)
df_semanal["Proyecto"] = df_semanal["Proyecto"].apply(limpiar_texto)

# =========================
# CALENDARIO
# =========================
fechas_mes = pd.date_range(
    start=f"{ANIO}-{MES:02d}-01",
    end=f"{ANIO}-{MES:02d}-{calendar.monthrange(ANIO, MES)[1]}"
)

print("Calculando calendario teórico...")

# =========================
# EJECUTAR LOGICA COMPLETA
# =========================
comparacion = procesar_todo(
    df_proyectos,
    df_intermedia,
    df_semanal,
    fechas_mes
)

# =========================
# CREAR CARPETA OUTPUT
# =========================
os.makedirs("output", exist_ok=True)

# =========================
# EXPORTAR EXCEL GENERAL
# =========================
ruta_excel = f"output/resultados_{ANIO}_{MES:02d}.xlsx"
comparacion.to_excel(ruta_excel, index=False)

print(f"Excel general generado: {ruta_excel}")

# =========================
# EXPORTAR CALENDARIOS
# =========================

# CALENDARIO TEÓRICO
df_teorico = comparacion[[
    "Proyecto",
    "PosibleIntermedia",
    "PosibleSemanal"
]]
df_teorico.to_excel("output/calendario_teorico.xlsx", index=False)

# CALENDARIO REAL
df_real = comparacion[[
    "Proyecto",
    "RealIntermedia",
    "RealSemanal"
]]
df_real.to_excel("output/calendario_real.xlsx", index=False)

# CALENDARIO COMPARADO
df_comparado = comparacion[[
    "Proyecto",
    "CoincidenciasIntermedia",
    "CoincidenciasSemanal",
    "CumplimientoIntermedia",
    "CumplimientoSemanal"
]]
df_comparado.to_excel("output/calendario_comparado.xlsx", index=False)

print("Archivos de calendario generados")

# =========================
# GENERAR GRAFICO
# =========================
generar_grafico(comparacion)

print("Gráfico generado")

# =========================
# FIN
# =========================
print("Proceso finalizado correctamente ✅")
