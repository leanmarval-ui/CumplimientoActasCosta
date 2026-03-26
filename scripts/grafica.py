import matplotlib.pyplot as plt
import numpy as np
import os

def generar_grafico(comparacion):

    proyectos = comparacion["Proyecto"]
    intermedia = comparacion["CumplimientoIntermedia"]
    semanal = comparacion["CumplimientoSemanal"]

    y = np.arange(len(proyectos))
    altura = 0.4

    plt.figure(figsize=(12,6))

    # =========================
    # FUNCION DE COLORES
    # =========================
    def color(valor):
        if valor >= 0.9:
            return "green"
        elif valor >= 0.8:
            return "gold"
        else:
            return "red"

    colores_intermedia = [color(v) for v in intermedia]
    colores_semanal = [color(v) for v in semanal]

    # =========================
    # BARRAS
    # =========================
    plt.barh(y - altura/2, intermedia, height=altura, color=colores_intermedia)
    plt.barh(y + altura/2, semanal, height=altura, color=colores_semanal)

    plt.yticks(y, proyectos)

    # =========================
    # LINEA META
    # =========================
    plt.axvline(x=0.8, color='black', linestyle='--', label='Meta 80%')

    # =========================
    # TITULO
    # =========================
    plt.title("Cumplimiento de Reuniones por Proyecto", fontsize=14, fontweight='bold')

    # =========================
    # TEXTO DENTRO DE BARRAS
    # =========================
    for i, v in enumerate(intermedia):
        if v > 0.05:  # evitar que se vea feo si es muy pequeño
            plt.text(v/2, i - altura/2, f"Intermedia\n{v:.0%}", 
                     va='center', ha='center', color='white', fontsize=8, fontweight='bold')

    for i, v in enumerate(semanal):
        if v > 0.05:
            plt.text(v/2, i + altura/2, f"Semanal\n{v:.0%}", 
                     va='center', ha='center', color='white', fontsize=8, fontweight='bold')

    # =========================
    # FORMATO
    # =========================
    plt.xlim(0, 1)
    plt.xlabel("Cumplimiento")
    plt.legend()

    plt.tight_layout()

    # =========================
    # GUARDAR
    # =========================
    os.makedirs("output", exist_ok=True)
    plt.savefig("output/grafico.png")

    plt.close()
