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
