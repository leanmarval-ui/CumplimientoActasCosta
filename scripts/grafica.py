import matplotlib.pyplot as plt
import numpy as np

def color(v):
    if v < 80:
        return "#c0392b"
    elif v < 90:
        return "#f1c40f"
    else:
        return "#27ae60"

def generar_grafico(df):

    df = df[df["Estado"].fillna("").str.upper() == "EJECUCIÓN"]

    df["CumplimientoSemanal"] *= 100
    df["CumplimientoIntermedia"] *= 100

    df["Promedio"] = (df["CumplimientoSemanal"] + df["CumplimientoIntermedia"]) / 2
    df = df.sort_values("Promedio")

    proyectos = df["Proyecto"]
    y = np.arange(len(proyectos))
    h = 0.32

    fig, ax = plt.subplots(figsize=(13, max(6, len(proyectos)*0.6)))

    bars1 = ax.barh(y-h/2, df["CumplimientoSemanal"], h,
                    color=[color(v) for v in df["CumplimientoSemanal"]],
                    edgecolor="none", label="Semanal")

    bars2 = ax.barh(y+h/2, df["CumplimientoIntermedia"], h,
                    color=[color(v) for v in df["CumplimientoIntermedia"]],
                    edgecolor="none", label="Intermedia")

    for bar in bars1:
        ax.text(5, bar.get_y()+bar.get_height()/2, "Semanal", va="center", color="white", fontsize=8)

    for bar in bars2:
        ax.text(5, bar.get_y()+bar.get_height()/2, "Intermedia", va="center", color="white", fontsize=8)

    for bars in [bars1, bars2]:
        for bar in bars:
            width = bar.get_width()
            ax.text(width+2, bar.get_y()+bar.get_height()/2, f"{width:.0f}%", va="center")

    ax.axvline(80, linestyle="--", color="black")

    ax.set_yticks(y)
    ax.set_yticklabels(proyectos)

    ax.set_xlim(0, df[["CumplimientoSemanal","CumplimientoIntermedia"]].max().max() + 15)

    plt.tight_layout()
    plt.savefig("output/grafico_cumplimiento_proyectos.png", dpi=300)
    plt.close()
