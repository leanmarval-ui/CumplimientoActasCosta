import pandas as pd

# ARCHIVOS
archivo = "input/Reuniones.xlsx"

salida_teorico = "output/calendario_teorico.xlsx"
salida_real = "output/calendario_real.xlsx"
salida_comparado = "output/calendario_comparado.xlsx"

# PARAMETROS
ANIO = 2026
MES = 2

festivos = [
"2026-01-01","2026-01-12","2026-03-23","2026-04-02","2026-04-03",
"2026-05-01","2026-05-18","2026-06-08","2026-06-15","2026-06-29",
"2026-07-20","2026-08-07","2026-08-17","2026-10-12","2026-11-02",
"2026-11-16","2026-12-08","2026-12-25"
]

festivos = [pd.to_datetime(f) for f in festivos]

# MAPA DIAS
mapa_dias = {
"LUNES":0,"MARTES":1,"MIERCOLES":2,"MIÉRCOLES":2,
"JUEVES":3,"VIERNES":4,"SABADO":5,"SÁBADO":5,"DOMINGO":6
}
