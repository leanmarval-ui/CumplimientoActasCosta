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
# EJECUTAR LOGICA (NO TOCAR)
# =========================
comparacion = procesar_todo(
    df_proyectos,
    df_intermedia,
    df_semanal,
    fechas_mes
)

# =========================
# CREAR OUTPUT
# =========================
os.makedirs("output", exist_ok=True)

# =========================
# ✅ EXCEL COMPLETO (SIN RECORTAR)
# =========================
comparacion.to_excel("output/resultados_completos.xlsx", index=False)

print("Excel completo generado")

# =========================
# ARCHIVOS ADICIONALES (SIN AFECTAR EL PRINCIPAL)
# =========================

# TEORICO
comparacion[[
    "Proyecto",
    "PosibleIntermedia",
    "PosibleSemanal"
]].to_excel("output/calendario_teorico.xlsx", index=False)

# REAL
comparacion[[
    "Proyecto",
    "RealIntermedia",
    "RealSemanal"
]].to_excel("output/calendario_real.xlsx", index=False)

# COMPARADO
comparacion[[
    "Proyecto",
    "CoincidenciasIntermedia",
    "CoincidenciasSemanal",
    "CumplimientoIntermedia",
    "CumplimientoSemanal"
]].to_excel("output/calendario_comparado.xlsx", index=False)

print("Calendarios generados")

# =========================
# 🔥 GRAFICO (FORZAR ACTUALIZACION)
# =========================
generar_grafico(comparacion.copy())

print("Gráfico actualizado")

print("Proceso finalizado correctamente ✅")
