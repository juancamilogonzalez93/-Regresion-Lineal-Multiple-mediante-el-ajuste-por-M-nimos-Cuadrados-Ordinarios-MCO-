import numpy as np
import streamlit as st

st.set_page_config(
    page_title="Simulador de Tráfico de Red - Modelo MCO",
    page_icon="🌐",
    layout="centered",
)

BETA_0 = 4.8177
BETA_1 = -0.0000946
BETA_2 = -0.0057
BETA_3 = -3.8070
ERROR_ESTANDAR = 2.84
Z_95 = 1.96

st.title("🌐 Simulador de Tráfico de Red - Modelo MCO")
st.caption(
    "Predicción del volumen de tráfico (bytes) a partir de un modelo de "
    "regresión lineal múltiple por mínimos cuadrados ordinarios (MCO), "
    "estimado sobre el dataset NSL-KDD."
)

with st.sidebar:
    st.header("Variables del modelo")
    st.markdown(
        """
        **duration**  
        Duración de la conexión, en segundos.

        **count**  
        Número de conexiones al mismo host de destino en los últimos 2 segundos.

        **serror_rate**  
        Proporción de conexiones (entre las del mismo host) que presentaron
        errores de tipo SYN. Toma valores entre 0 y 1.

        **Variable dependiente**  
        Logaritmo natural del volumen de tráfico en bytes (`ln(1 + bytes)`).
        La predicción se transforma de nuevo a bytes con `expm1`.
        """
    )
    st.divider()
    st.subheader("Ecuación MCO")
    st.latex(
        r"\ln(1+\widehat{bytes}) = \beta_0 + \beta_1\,\text{duration}"
        r" + \beta_2\,\text{count} + \beta_3\,\text{serror\_rate}"
    )
    st.markdown(
        f"""
        | Coeficiente | Valor |
        |---|---:|
        | β₀ (constante) | `{BETA_0}` |
        | β₁ (duration) | `{BETA_1}` |
        | β₂ (count) | `{BETA_2}` |
        | β₃ (serror_rate) | `{BETA_3}` |
        """
    )

st.subheader("Parámetros de la conexión")

duration = st.number_input(
    "duration (segundos)",
    min_value=0,
    max_value=10000,
    value=100,
    step=1,
    help="Duración de la conexión en segundos.",
)

count = st.number_input(
    "count",
    min_value=0,
    max_value=1000,
    value=50,
    step=1,
    help="Conexiones al mismo host de destino en los últimos 2 segundos.",
)

serror_rate = st.slider(
    "serror_rate",
    min_value=0.0,
    max_value=1.0,
    value=0.1,
    step=0.01,
    help="Proporción de conexiones con error SYN (0 a 1).",
)

if st.button("🚀 Predecir Tráfico", type="primary"):
    ln_prediccion = (
        BETA_0
        + (BETA_1 * duration)
        + (BETA_2 * count)
        + (BETA_3 * serror_rate)
    )
    trafico_estimado = float(np.expm1(ln_prediccion))

    limite_inferior_ln = ln_prediccion - (Z_95 * ERROR_ESTANDAR)
    limite_superior_ln = ln_prediccion + (Z_95 * ERROR_ESTANDAR)
    limite_inferior = max(0.0, float(np.expm1(limite_inferior_ln)))
    limite_superior = float(np.expm1(limite_superior_ln))

    st.success(
        f"Tráfico estimado: **{trafico_estimado:,.2f} bytes**"
    )
    st.info(
        "Intervalo de predicción al 95% de confianza: "
        f"**[{limite_inferior:,.2f} , {limite_superior:,.2f}] bytes**"
    )
