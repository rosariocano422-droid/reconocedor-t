import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Reconocedor de T", page_icon="🔤", layout="wide")

st.title("🔤 Máquina Reconocedora de la Letra T")
st.markdown("### ¿Puede una máquina reconocer patrones ajustando números?")
st.markdown("---")

st.markdown("""
**¿Cómo funciona?**
- Cada imagen es una cuadrícula de 3x3 pixeles (1 = activo, 0 = apagado)
- Cada pixel tiene un peso ajustable
- La máquina multiplica cada pixel por su peso y suma todo
- El puntaje resultante indica qué tan parecida es la imagen a una T
""")

st.markdown("---")

# ============================================================
# IMÁGENES BINARIAS
# ============================================================
imagenes_T = {
    "T normal": [
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0]
    ],
    "T centrada": [
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0]
    ],
    "T variante": [
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0]
    ],
}

imagenes_NO_T = {
    "Cruz (+)": [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ],
    "L invertida": [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1]
    ],
    "Diagonal": [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ],
    "Cuadrado": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ],
    "Fila central": [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ],
    "T invertida": [
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 1]
    ],
}

# ============================================================
# SECCIÓN 1: PESOS
# ============================================================
st.header("🎛️ Paso 1: Ajusta los pesos de cada posición")
st.markdown("Cada slider controla el peso de un pixel en la cuadrícula 3x3. Muévelos para ver cómo cambia el puntaje.")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Fila 1**")
    w00 = st.slider("Pos (1,1)", -5.0, 5.0, 2.0, 0.5, key="w00")
    w10 = st.slider("Pos (2,1)", -5.0, 5.0, -1.0, 0.5, key="w10")
    w20 = st.slider("Pos (3,1)", -5.0, 5.0, -1.0, 0.5, key="w20")

with col2:
    st.markdown("**Fila 2**")
    w01 = st.slider("Pos (1,2)", -5.0, 5.0, 2.0, 0.5, key="w01")
    w11 = st.slider("Pos (2,2)", -5.0, 5.0, 3.0, 0.5, key="w11")
    w21 = st.slider("Pos (3,2)", -5.0, 5.0, 3.0, 0.5, key="w21")

with col3:
    st.markdown("**Fila 3**")
    w02 = st.slider("Pos (1,3)", -5.0, 5.0, 2.0, 0.5, key="w02")
    w12 = st.slider("Pos (2,3)", -5.0, 5.0, -1.0, 0.5, key="w12")
    w22 = st.slider("Pos (3,3)", -5.0, 5.0, -1.0, 0.5, key="w22")

pesos = [
    [w00, w01, w02],
    [w10, w11, w12],
    [w20, w21, w22]
]

# Threshold
st.markdown("---")
threshold = st.slider("🎯 Umbral (threshold): puntaje mínimo para considerar que ES una T", -10.0, 20.0, 5.0, 0.5)

st.markdown("---")

# ============================================================
# FUNCIÓN DE PUNTUACIÓN
# ============================================================
def calcular_puntaje(imagen, pesos):
    total = 0
    pasos = []
    for i in range(3):
        for j in range(3):
            valor = imagen[i][j] * pesos[i][j]
            total += valor
            pasos.append((i, j, imagen[i][j], pesos[i][j], valor))
    return total, pasos

# ============================================================
# FUNCIÓN PARA DIBUJAR CUADRÍCULA
# ============================================================
def dibujar_imagen(imagen, titulo, puntaje, es_T, threshold):
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_aspect('equal')
    ax.axis('off')

    for i in range(3):
        for j in range(3):
            color = '#2E75B6' if imagen[i][j] == 1 else '#F0F0F0'
            rect = patches.Rectangle((j, 2 - i), 1, 1,
                                      linewidth=2, edgecolor='#CCCCCC',
                                      facecolor=color)
            ax.add_patch(rect)
            ax.text(j + 0.5, 2 - i + 0.5, str(imagen[i][j]),
                    ha='center', va='center',
                    fontsize=14, fontweight='bold',
                    color='white' if imagen[i][j] == 1 else '#999999')

    color_titulo = '#1a7a1a' if puntaje >= threshold else '#cc0000'
    resultado = "✅ ES T" if puntaje >= threshold else "❌ NO es T"
    ax.set_title(f"{titulo}\nPuntaje: {puntaje:.1f} | {resultado}",
                 fontsize=10, color=color_titulo, fontweight='bold')
    plt.tight_layout()
    return fig

# ============================================================
# SECCIÓN 2: VISUALIZACIÓN DE IMÁGENES T
# ============================================================
st.header("✅ Imágenes que SÍ son T")

cols = st.columns(3)
for idx, (nombre, imagen) in enumerate(imagenes_T.items()):
    puntaje, _ = calcular_puntaje(imagen, pesos)
    with cols[idx]:
        fig = dibujar_imagen(imagen, nombre, puntaje, True, threshold)
        st.pyplot(fig)
        plt.close()

st.markdown("---")

# ============================================================
# SECCIÓN 3: VISUALIZACIÓN DE IMÁGENES NO T
# ============================================================
st.header("❌ Imágenes que NO son T")

cols2 = st.columns(3)
for idx, (nombre, imagen) in enumerate(imagenes_NO_T.items()):
    puntaje, _ = calcular_puntaje(imagen, pesos)
    with cols2[idx % 3]:
        fig = dibujar_imagen(imagen, nombre, puntaje, False, threshold)
        st.pyplot(fig)
        plt.close()

st.markdown("---")

# ============================================================
# SECCIÓN 4: DETALLE DE CÁLCULO
# ============================================================
st.header("🔢 Paso 2: Ve el cálculo detallado de cualquier imagen")

todas_imagenes = {**imagenes_T, **imagenes_NO_T}
imagen_seleccionada = st.selectbox("Selecciona una imagen para ver el cálculo paso a paso:",
                                    list(todas_imagenes.keys()))

imagen = todas_imagenes[imagen_seleccionada]
puntaje_total, pasos = calcular_puntaje(imagen, pesos)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📐 Matriz de la imagen")
    for fila in imagen:
        st.text("  ".join(str(p) for p in fila))

    st.subheader("⚖️ Matriz de pesos actuales")
    for fila in pesos:
        st.text("  ".join(f"{p:+.1f}" for p in fila))

with col2:
    st.subheader("🧮 Cálculo paso a paso")
    formula = " + ".join([f"({p[2]}×{p[3]:+.1f})" for p in pasos])
    st.markdown(f"**Fórmula:** `y = {formula}`")
    st.markdown(f"**Puntaje total:** `{puntaje_total:.2f}`")
    st.markdown(f"**Umbral:** `{threshold}`")

    if puntaje_total >= threshold:
        st.success(f"✅ Puntaje {puntaje_total:.2f} ≥ {threshold} → La máquina dice: **ES una T**")
    else:
        st.error(f"❌ Puntaje {puntaje_total:.2f} < {threshold} → La máquina dice: **NO es una T**")

st.markdown("---")

# ============================================================
# SECCIÓN 5: MARCADOR GENERAL
# ============================================================
st.header("🏆 Marcador: ¿Qué tan bien están calibrados tus pesos?")

correctas_T = sum(1 for img in imagenes_T.values()
                  if calcular_puntaje(img, pesos)[0] >= threshold)
correctas_NO_T = sum(1 for img in imagenes_NO_T.values()
                     if calcular_puntaje(img, pesos)[0] < threshold)

total_correctas = correctas_T + correctas_NO_T
total_imagenes = len(imagenes_T) + len(imagenes_NO_T)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("✅ T reconocidas correctamente", f"{correctas_T} / {len(imagenes_T)}")
with col2:
    st.metric("❌ NO-T rechazadas correctamente", f"{correctas_NO_T} / {len(imagenes_NO_T)}")
with col3:
    st.metric("🎯 Precisión total", f"{total_correctas} / {total_imagenes}")

st.progress(total_correctas / total_imagenes)

if total_correctas == total_imagenes:
    st.success("🏆 ¡Perfecto! Tus pesos clasifican correctamente todas las imágenes.")
    st.balloons()
elif total_correctas >= total_imagenes * 0.7:
    st.warning("😊 ¡Muy bien! Sigue ajustando los pesos para mejorar.")
else:
    st.error("🔧 Sigue experimentando con los pesos y el umbral.")

st.markdown("---")
st.markdown("🎓 **Aplicación desarrollada para la asignatura: Autómatas, Gramáticas y Lenguaje - IU Digital de Antioquia**")
