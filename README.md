# Simulador de Tráfico de Red - Modelo MCO

Aplicación local en Streamlit que estima el volumen de tráfico de una conexión de red (en bytes) mediante **regresión lineal múltiple por mínimos cuadrados ordinarios (MCO)**. Los coeficientes están fijos y provienen de un ajuste sobre el dataset **NSL-KDD**.

El modelo predice el logaritmo del tráfico y luego lo transforma a bytes con la función inversa `expm1`. También muestra un intervalo de predicción aproximado al 95% de confianza.

## Variables del modelo

| Variable | Descripción |
|---|---|
| `duration` | Duración de la conexión, en segundos. |
| `count` | Número de conexiones al mismo host de destino en los últimos 2 segundos. |
| `serror_rate` | Proporción de conexiones al mismo host que presentaron errores SYN (entre 0 y 1). |
| Tráfico (bytes) | Variable dependiente. El modelo se estima sobre `ln(1 + bytes)`. |

## Ecuación MCO

\[
\ln(1 + \widehat{\text{bytes}}) = \beta_0 + \beta_1 \cdot \text{duration} + \beta_2 \cdot \text{count} + \beta_3 \cdot \text{serror\_rate}
\]

| Coeficiente | Variable | Valor |
|---|---|---:|
| β₀ | Constante | 4.8177 |
| β₁ | `duration` | -0.0000946 |
| β₂ | `count` | -0.0057 |
| β₃ | `serror_rate` | -3.8070 |

La predicción puntual en bytes es:

\[
\widehat{\text{bytes}} = \exp(\ln(1 + \widehat{\text{bytes}})) - 1
\]

El intervalo de predicción al 95% usa un error estándar de `2.84` y `Z = 1.96` sobre la escala logarítmica, y luego se transforma con la misma función inversa. El límite inferior se trunca en 0.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```
