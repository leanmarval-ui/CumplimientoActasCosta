import pandas as pd
import numpy as np
from datetime import timedelta
import calendar
from parametros import ANIO, MES, festivos, mapa_dias

# LIMPIEZA
def limpiar_texto(texto):
    if pd.isna(texto):
        return texto
    return str(texto).strip().upper()

# FUNCIONES BASE
def es_habil(fecha):
    if fecha.weekday() == 6:
        return False
    if fecha in festivos:
        return False
    return True

def obtener_dos_siguientes(fecha):
    return [fecha + timedelta(days=i) for i in range(1,3) if (fecha + timedelta(days=i)).month == MES]

def siguiente_habil(fecha):
    siguiente = fecha + timedelta(days=1)
    while not es_habil(siguiente):
        siguiente += timedelta(days=1)
    return siguiente

# CALCULO POSIBLES
def calcular_posibles(dia_base, fechas_mes):
    if pd.isna(dia_base):
        return ""

    dia_base = str(dia_base).upper().strip()
    if dia_base not in mapa_dias:
        return ""

    numero_dia = mapa_dias[dia_base]
    posibles = []

    for fecha in fechas_mes:
        if fecha.weekday() == numero_dia:
            if fecha in festivos:
                posibles.extend(obtener_dos_siguientes(fecha))
            else:
                posibles.append(fecha)
                siguiente = siguiente_habil(fecha)
                if siguiente.month == MES:
                    posibles.append(siguiente)

    posibles = sorted(set(posibles))
    return ", ".join([f.strftime("%Y-%m-%d") for f in posibles])

# CONTEOS
def contar_fechas(valor):
    if pd.isna(valor) or valor == "":
        return 0
    return len([x for x in str(valor).split(",") if x.strip() != ""])

def contar_fechas_y_dividir(valor):
    return contar_fechas(valor) // 2

# COINCIDENCIAS
def coincidencias_inteligente(lista1, lista2):
    if pd.isna(lista1) or pd.isna(lista2):
        return ""

    fechas1 = sorted(set(pd.to_datetime(x.strip()).normalize() for x in str(lista1).split(",") if x.strip()))
    fechas2 = sorted(set(pd.to_datetime(x.strip()).normalize() for x in str(lista2).split(",") if x.strip()))

    coincidencias = []

    for f2 in fechas2:
        for f1 in fechas1:
            if f2 == f1 or f2 == f1 + pd.Timedelta(days=1):
                coincidencias.append(f1)
                break

    return ", ".join([f.strftime("%Y-%m-%d") for f in coincidencias])
# ==================================
# FUNCION PRINCIPAL
# ==================================
def procesar_todo(df_proyectos, df_intermedia, df_semanal, fechas_mes):

    # =========================
    # CALENDARIO TEORICO
    # =========================
    df_proyectos["PosibleIntermedia"] = df_proyectos["DiaIntermedia"].apply(
        lambda x: calcular_posibles(x, fechas_mes)
    )

    df_proyectos["PosibleSemanal"] = df_proyectos["DiaSemanal"].apply(
        lambda x: calcular_posibles(x, fechas_mes)
    )

    df_proyectos["ConteoIntermedia"] = df_proyectos["PosibleIntermedia"].apply(contar_fechas_y_dividir)
    df_proyectos["ConteoSemanal"] = df_proyectos["PosibleSemanal"].apply(contar_fechas_y_dividir)

    # =========================
    # AGRUPAR REALES (QUITAR DUPLICADOS POR DIA)
    # =========================
  df_intermedia["fecha de fin"] = pd.to_datetime(df_intermedia["fecha de fin"]).dt.normalize()
df_semanal["fecha de fin"] = pd.to_datetime(df_semanal["fecha de fin"]).dt.normalize()

   df_intermedia = df_intermedia.drop_duplicates(subset=["Proyecto", "fecha de fin"])
df_semanal = df_semanal.drop_duplicates(subset=["Proyecto", "fecha de fin"])

    df_intermedia_group = df_intermedia.groupby("Proyecto")["fecha de fin"].apply(
        lambda x: ", ".join(sorted(set(x.dt.strftime("%Y-%m-%d"))))
    ).reset_index()

   df_semanal_group = df_semanal.groupby("Proyecto")["fecha de fin"].apply(
        lambda x: ", ".join(sorted(set(x.dt.strftime("%Y-%m-%d"))))
    ).reset_index()

    df_intermedia_group.rename(columns={"Fecha": "RealIntermedia"}, inplace=True)
    df_semanal_group.rename(columns={"Fecha": "RealSemanal"}, inplace=True)

    # =========================
    # MERGE
    # =========================
    comparacion = df_proyectos.merge(df_intermedia_group, on="Proyecto", how="left")
    comparacion = comparacion.merge(df_semanal_group, on="Proyecto", how="left")

    # =========================
    # COINCIDENCIAS
    # =========================
    comparacion["CoincidenciasIntermedia"] = comparacion.apply(
        lambda row: coincidencias_inteligente(row["PosibleIntermedia"], row["RealIntermedia"]), axis=1
    )

    comparacion["CoincidenciasSemanal"] = comparacion.apply(
        lambda row: coincidencias_inteligente(row["PosibleSemanal"], row["RealSemanal"]), axis=1
    )

    comparacion["ConteoCoincidenciasIntermedia"] = comparacion["CoincidenciasIntermedia"].apply(contar_fechas)
    comparacion["ConteoCoincidenciasSemanal"] = comparacion["CoincidenciasSemanal"].apply(contar_fechas)

    # =========================
    # CUMPLIMIENTO
    # =========================
    comparacion["CumplimientoIntermedia"] = np.where(
        comparacion["ConteoIntermedia"] == 0,
        0,
        comparacion["ConteoCoincidenciasIntermedia"] / comparacion["ConteoIntermedia"]
    )

    comparacion["CumplimientoSemanal"] = np.where(
        comparacion["ConteoSemanal"] == 0,
        0,
        comparacion["ConteoCoincidenciasSemanal"] / comparacion["ConteoSemanal"]
    )

    # 🔥 evitar >100%
    comparacion["CumplimientoIntermedia"] = comparacion["CumplimientoIntermedia"].clip(upper=1)
    comparacion["CumplimientoSemanal"] = comparacion["CumplimientoSemanal"].clip(upper=1)

    return comparacion
