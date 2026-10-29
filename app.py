import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# =========================================================
# CONFIGURACIÓN DE LA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Dashboard Tótem de Bienestar",
    page_icon="❤️",
    layout="wide"
)


# =========================================================
# ESTILO VISUAL
# =========================================================

st.markdown("""
<style>

/* Fondo general */
.stApp {
    background-color: #F7FAFC;
}

/* Texto general */
.stApp,
.stApp p,
.stApp span,
.stApp label {
    color: #263238;
}

/* Títulos */
h1, h2, h3 {
    color: #24465A !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #EDF6F8;
    border-right: 1px solid #D9E7EB;
}

[data-testid="stSidebar"] * {
    color: #263238 !important;
}

/* Tarjetas de métricas */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE7EC;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.04);
}

[data-testid="stMetricLabel"] p {
    color: #607D8B !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #24465A !important;
}

/* Cajas de información */
.info-card {
    background-color: #FFFFFF;
    border: 1px solid #DCE7EC;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
    color: #263238 !important;
}

/* Expander */
[data-testid="stExpander"] {
    background-color: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #DCE7EC;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# ARCHIVO CSV
# =========================================================

CSV_PATH = (
    Path(__file__).parent
    / "proyecto_integrador_eafit_max30102.csv"
)


# =========================================================
# CARGA Y LIMPIEZA DE DATOS
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(CSV_PATH)

    # Convertir fecha
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True,
        errors="coerce"
    )

    # Convertir de UTC a hora de Colombia
    df["timestamp_local"] = (
        df["timestamp"]
        .dt.tz_convert("America/Bogota")
    )

    # Variables numéricas
    df["heart_rate_bpm"] = pd.to_numeric(
        df["heart_rate_bpm"],
        errors="coerce"
    )

    df["spo2_percent"] = pd.to_numeric(
        df["spo2_percent"],
        errors="coerce"
    )

    df["signal_quality"] = pd.to_numeric(
        df["signal_quality"],
        errors="coerce"
    )

    # Normalizar estado
    df["measurement_status"] = (
        df["measurement_status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Variables auxiliares para gráficas
    df["date"] = df["timestamp_local"].dt.date
    df["hour"] = df["timestamp_local"].dt.hour

    return df


try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "No se encontró el archivo "
        "'proyecto_integrador_eafit_max30102.csv'."
    )

    st.stop()


# =========================================================
# ENCABEZADO
# =========================================================

st.title("❤️ Dashboard del Tótem de Bienestar")

st.markdown("""
<div class="info-card">

<b>¿Qué muestra este dashboard?</b><br><br>

Este tablero permite analizar las mediciones registradas por un
tótem IoT utilizado por estudiantes.

Se estudian principalmente la
<b>frecuencia cardíaca</b>,
la <b>saturación estimada de oxígeno</b>,
la cantidad de usos del dispositivo y
la calidad de las mediciones.

</div>
""", unsafe_allow_html=True)


# =========================================================
# FILTROS
# =========================================================

st.sidebar.header("🔎 Filtros")


# ---------------------------------------------------------
# FECHAS
# ---------------------------------------------------------

min_date = df["date"].min()
max_date = df["date"].max()


date_selection = st.sidebar.date_input(
    "📅 Rango de fechas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# Manejar selección de una sola fecha
if isinstance(date_selection, (tuple, list)):

    if len(date_selection) == 2:

        start_date = date_selection[0]
        end_date = date_selection[1]

    else:

        start_date = date_selection[0]
        end_date = date_selection[0]

else:

    start_date = date_selection
    end_date = date_selection


# ---------------------------------------------------------
# ESTUDIANTE
# ---------------------------------------------------------

student_options = (
    ["Todos"]
    + sorted(df["student_id"].unique().tolist())
)


selected_student = st.sidebar.selectbox(
    "🎓 Estudiante",
    student_options
)


# ---------------------------------------------------------
# ESTADO
# ---------------------------------------------------------

selected_status = st.sidebar.selectbox(
    "✅ Estado de la medición",
    [
        "Todos",
        "Valid",
        "Invalid"
    ]
)


# =========================================================
# APLICAR FILTROS
# =========================================================

filtered = df[
    (df["date"] >= start_date)
    &
    (df["date"] <= end_date)
].copy()


if selected_student != "Todos":

    filtered = filtered[
        filtered["student_id"]
        == selected_student
    ]


if selected_status != "Todos":

    filtered = filtered[
        filtered["measurement_status"]
        == selected_status.lower()
    ]


# =========================================================
# VERIFICAR DATOS
# =========================================================

if filtered.empty:

    st.warning(
        "No hay registros que coincidan con los filtros seleccionados."
    )

    st.stop()


# =========================================================
# MEDICIONES VÁLIDAS
# =========================================================

valid_filtered = filtered[
    filtered["measurement_status"]
    == "valid"
]


# =========================================================
# INDICADORES GENERALES
# =========================================================

st.subheader("📌 Indicadores generales")


total_measurements = len(filtered)

unique_students = filtered[
    "student_id"
].nunique()


if not valid_filtered.empty:

    avg_hr = valid_filtered[
        "heart_rate_bpm"
    ].mean()

    avg_spo2 = valid_filtered[
        "spo2_percent"
    ].mean()

else:

    avg_hr = None
    avg_spo2 = None


invalid_count = (
    filtered["measurement_status"]
    == "invalid"
).sum()


invalid_percentage = (
    invalid_count
    / total_measurements
    * 100
)


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "📊 Mediciones",
    f"{total_measurements:,}"
)


col2.metric(
    "🎓 Estudiantes",
    unique_students
)


col3.metric(
    "❤️ BPM promedio",
    f"{avg_hr:.1f}"
    if avg_hr is not None
    else "N/D"
)


col4.metric(
    "🫁 SpO₂ promedio",
    f"{avg_spo2:.1f} %"
    if avg_spo2 is not None
    else "N/D"
)


col5.metric(
    "⚠️ Mediciones inválidas",
    f"{invalid_percentage:.1f} %"
)


st.caption(
    "Los promedios de BPM y SpO₂ se calculan únicamente "
    "con mediciones marcadas como válidas."
)


st.markdown("---")


# =========================================================
# VISUALIZACIÓN 1
# MEDICIONES POR DÍA
# =========================================================

st.subheader("📅 Uso del tótem a través del tiempo")


measurements_day = (
    filtered
    .groupby("date")
    .size()
    .reset_index(name="Mediciones")
)


fig_day = px.bar(

    measurements_day,

    x="date",

    y="Mediciones",

    title="Cantidad de mediciones por día",

    labels={
        "date": "Fecha",
        "Mediciones": "Número de mediciones"
    },

    color_discrete_sequence=[
        "#69B3A2"
    ]
)


fig_day.update_layout(

    template="plotly_white",

    paper_bgcolor="#FFFFFF",

    plot_bgcolor="#FFFFFF",

    font=dict(
        color="#263238"
    ),

    xaxis=dict(
        gridcolor="#EDF2F4"
    ),

    yaxis=dict(
        gridcolor="#EDF2F4"
    ),

    showlegend=False
)


st.plotly_chart(
    fig_day,
    use_container_width=True
)


# =========================================================
# VISUALIZACIONES 2 Y 3
# DISTRIBUCIONES BPM Y SPO2
# =========================================================

st.subheader("❤️ Indicadores fisiológicos")


graph1, graph2 = st.columns(2)


# ---------------------------------------------------------
# FRECUENCIA CARDÍACA
# ---------------------------------------------------------

with graph1:

    if not valid_filtered.empty:

        fig_hr = px.histogram(

            valid_filtered,

            x="heart_rate_bpm",

            nbins=20,

            title="Distribución de frecuencia cardíaca",

            labels={
                "heart_rate_bpm":
                "Frecuencia cardíaca (BPM)"
            },

            color_discrete_sequence=[
                "#F28B82"
            ]
        )


        fig_hr.update_layout(

            template="plotly_white",

            paper_bgcolor="#FFFFFF",

            plot_bgcolor="#FFFFFF",

            font=dict(
                color="#263238"
            ),

            yaxis_title="Cantidad de mediciones",

            showlegend=False
        )


        st.plotly_chart(
            fig_hr,
            use_container_width=True
        )


        st.caption(
            "Cada barra muestra cuántas mediciones "
            "se encuentran dentro de un rango de BPM."
        )

    else:

        st.info(
            "No hay mediciones válidas de frecuencia cardíaca."
        )


# ---------------------------------------------------------
# SPO2
# ---------------------------------------------------------

with graph2:

    if not valid_filtered.empty:

        fig_spo2 = px.histogram(

            valid_filtered,

            x="spo2_percent",

            nbins=20,

            title="Distribución de saturación de oxígeno",

            labels={
                "spo2_percent":
                "SpO₂ estimada (%)"
            },

            color_discrete_sequence=[
                "#82B1FF"
            ]
        )


        fig_spo2.update_layout(

            template="plotly_white",

            paper_bgcolor="#FFFFFF",

            plot_bgcolor="#FFFFFF",

            font=dict(
                color="#263238"
            ),

            yaxis_title="Cantidad de mediciones",

            showlegend=False
        )


        st.plotly_chart(
            fig_spo2,
            use_container_width=True
        )


        st.caption(
            "La gráfica permite observar en qué valores "
            "se concentran las mediciones de SpO₂."
        )

    else:

        st.info(
            "No hay mediciones válidas de SpO₂."
        )


# =========================================================
# VISUALIZACIONES 4 Y 5
# HORARIOS Y ESTADOS
# =========================================================

st.subheader("🕒 ¿Cuándo y cómo se utiliza el tótem?")


graph3, graph4 = st.columns(2)


# ---------------------------------------------------------
# USO POR HORA
# ---------------------------------------------------------

with graph3:

    hourly = (
        filtered
        .groupby("hour")
        .size()
        .reset_index(name="Mediciones")
    )


    fig_hour = px.bar(

        hourly,

        x="hour",

        y="Mediciones",

        title="Mediciones según la hora del día",

        labels={
            "hour": "Hora",
            "Mediciones": "Número de mediciones"
        },

        color_discrete_sequence=[
            "#F6C177"
        ]
    )


    fig_hour.update_layout(

        template="plotly_white",

        paper_bgcolor="#FFFFFF",

        plot_bgcolor="#FFFFFF",

        font=dict(
            color="#263238"
        ),

        showlegend=False
    )


    fig_hour.update_xaxes(
        dtick=1
    )


    st.plotly_chart(
        fig_hour,
        use_container_width=True
    )


    st.caption(
        "Las barras más altas indican los horarios "
        "en los que el tótem fue utilizado más veces."
    )


# ---------------------------------------------------------
# MEDICIONES VÁLIDAS E INVÁLIDAS
# ---------------------------------------------------------

with graph4:

    status_counts = (
        filtered[
            "measurement_status"
        ]
        .value_counts()
        .reset_index()
    )


    status_counts.columns = [
        "Estado",
        "Cantidad"
    ]


    fig_status = px.pie(

        status_counts,

        names="Estado",

        values="Cantidad",

        hole=0.55,

        title="Calidad de las mediciones",

        color="Estado",

        color_discrete_map={
            "valid": "#82C99A",
            "invalid": "#F28B82"
        }
    )


    fig_status.update_layout(

        template="plotly_white",

        paper_bgcolor="#FFFFFF",

        font=dict(
            color="#263238"
        )
    )


    st.plotly_chart(
        fig_status,
        use_container_width=True
    )


    st.caption(
        "Verde = medición válida. "
        "Rojo = medición inválida."
    )


# =========================================================
# VISUALIZACIÓN EXTRA
# CALIDAD DE SEÑAL
# =========================================================

st.subheader("📶 Calidad de la señal")


fig_signal = px.box(

    filtered,

    x="measurement_status",

    y="signal_quality",

    color="measurement_status",

    title="Calidad de señal según el estado de la medición",

    labels={
        "measurement_status": "Estado",
        "signal_quality": "Calidad de señal"
    },

    color_discrete_map={
        "valid": "#82C99A",
        "invalid": "#F28B82"
    }
)


fig_signal.update_layout(

    template="plotly_white",

    paper_bgcolor="#FFFFFF",

    plot_bgcolor="#FFFFFF",

    font=dict(
        color="#263238"
    ),

    showlegend=False
)


st.plotly_chart(
    fig_signal,
    use_container_width=True
)


st.caption(
    "La calidad de señal está expresada entre 0 y 1. "
    "Valores más cercanos a 1 representan una mejor señal."
)


st.markdown("---")


# =========================================================
# SEGUIMIENTO INDIVIDUAL
# =========================================================

st.subheader("🎓 Seguimiento individual")


st.write(
    "Selecciona un estudiante para consultar "
    "su histórico de mediciones."
)


# Mantener los filtros de fecha y estado,
# pero permitir escoger cualquier estudiante
# dentro de ese período.

individual_base = df[
    (df["date"] >= start_date)
    &
    (df["date"] <= end_date)
].copy()


if selected_status != "Todos":

    individual_base = individual_base[
        individual_base[
            "measurement_status"
        ]
        == selected_status.lower()
    ]


available_students = sorted(
    individual_base[
        "student_id"
    ].unique()
)


if available_students:

    # Si ya se seleccionó un estudiante arriba,
    # usarlo como valor inicial cuando sea posible.

    default_index = 0


    if (
        selected_student != "Todos"
        and
        selected_student in available_students
    ):

        default_index = (
            available_students
            .index(selected_student)
        )


    individual_student = st.selectbox(

        "Estudiante para seguimiento",

        available_students,

        index=default_index,

        key="individual_student"
    )


    student_data = individual_base[
        individual_base[
            "student_id"
        ]
        == individual_student
    ].sort_values(
        "timestamp_local"
    )


    # -----------------------------------------------------
    # DATOS DEL ESTUDIANTE
    # -----------------------------------------------------

    first_measurement = (
        student_data[
            "timestamp_local"
        ]
        .min()
    )


    last_measurement = (
        student_data[
            "timestamp_local"
        ]
        .max()
    )


    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "🎓 Estudiante",
        individual_student
    )


    c2.metric(
        "📊 Mediciones",
        len(student_data)
    )


    c3.metric(
        "⏮️ Primera medición",
        first_measurement.strftime(
            "%d/%m/%Y %H:%M"
        )
    )


    c4.metric(
        "⏭️ Última medición",
        last_measurement.strftime(
            "%d/%m/%Y %H:%M"
        )
    )


    # -----------------------------------------------------
    # EVOLUCIÓN INDIVIDUAL
    # -----------------------------------------------------

    individual1, individual2 = st.columns(2)


    with individual1:

        fig_ind_hr = px.line(

            student_data,

            x="timestamp_local",

            y="heart_rate_bpm",

            markers=True,

            color="measurement_status",

            title="❤️ Evolución de frecuencia cardíaca",

            labels={
                "timestamp_local":
                "Fecha y hora",

                "heart_rate_bpm":
                "Frecuencia cardíaca (BPM)",

                "measurement_status":
                "Estado"
            },

            color_discrete_map={
                "valid": "#E57373",
                "invalid": "#B0BEC5"
            }
        )


        fig_ind_hr.update_layout(

            template="plotly_white",

            paper_bgcolor="#FFFFFF",

            plot_bgcolor="#FFFFFF",

            font=dict(
                color="#263238"
            )
        )


        st.plotly_chart(
            fig_ind_hr,
            use_container_width=True
        )


    with individual2:

        fig_ind_spo2 = px.line(

            student_data,

            x="timestamp_local",

            y="spo2_percent",

            markers=True,

            color="measurement_status",

            title="🫁 Evolución de SpO₂",

            labels={
                "timestamp_local":
                "Fecha y hora",

                "spo2_percent":
                "SpO₂ estimada (%)",

                "measurement_status":
                "Estado"
            },

            color_discrete_map={
                "valid": "#64B5F6",
                "invalid": "#B0BEC5"
            }
        )


        fig_ind_spo2.update_layout(

            template="plotly_white",

            paper_bgcolor="#FFFFFF",

            plot_bgcolor="#FFFFFF",

            font=dict(
                color="#263238"
            )
        )


        st.plotly_chart(
            fig_ind_spo2,
            use_container_width=True
        )


else:

    st.info(
        "No existen estudiantes disponibles "
        "con los filtros seleccionados."
    )


st.markdown("---")


# =========================================================
# ANÁLISIS AUTOMÁTICO
# =========================================================

st.subheader("🔍 Análisis e interpretación")


# ---------------------------------------------------------
# HALLAZGO 1: DÍA CON MÁS USO
# ---------------------------------------------------------

daily_counts = filtered.groupby(
    "date"
).size()


top_day = daily_counts.idxmax()

top_day_count = daily_counts.max()


# ---------------------------------------------------------
# HALLAZGO 2: HORA CON MÁS USO
# ---------------------------------------------------------

hour_counts = filtered.groupby(
    "hour"
).size()


top_hour = int(
    hour_counts.idxmax()
)

top_hour_count = int(
    hour_counts.max()
)


# ---------------------------------------------------------
# HALLAZGO 3: ESTUDIANTE MÁS FRECUENTE
# ---------------------------------------------------------

student_counts = filtered[
    "student_id"
].value_counts()


top_student = student_counts.index[0]

top_student_count = int(
    student_counts.iloc[0]
)


# ---------------------------------------------------------
# MOSTRAR HALLAZGOS
# ---------------------------------------------------------

st.markdown(
    f"""
### 1. 📅 Día de mayor utilización

El día con mayor cantidad de mediciones dentro de los filtros
seleccionados fue **{top_day.strftime("%d/%m/%Y")}**,
con **{top_day_count} mediciones**.

---

### 2. 🕒 Horario de mayor utilización

La hora con mayor actividad fue entre
**{top_hour:02d}:00 y {top_hour:02d}:59**,
con **{top_hour_count} mediciones**.

---

### 3. 🎓 Estudiante con más registros

El estudiante con mayor número de mediciones fue
**{top_student}**, con **{top_student_count} registros**.

---

### 4. ⚠️ Calidad de los registros

Dentro del período analizado,
**{invalid_percentage:.1f}% de las mediciones fueron inválidas**
({invalid_count} de {total_measurements} registros).
"""
)


# =========================================================
# LIMITACIONES
# =========================================================

st.warning("""
⚠️ **Importante sobre la interpretación de los datos**

Las mediciones de frecuencia cardíaca y SpO₂ mostradas en este
dashboard pertenecen a un escenario educativo y no permiten,
por sí solas, determinar el estado general de salud de una persona.

El sensor MAX30102 utilizado en este ejercicio no debe interpretarse
como un dispositivo médico validado y este dashboard no realiza
diagnósticos ni clasificaciones clínicas.
""")


# =========================================================
# TABLA DE DATOS
# =========================================================

with st.expander(
    "📋 Ver registros utilizados"
):

    table = filtered[
        [
            "timestamp_local",
            "student_id",
            "nfc_id",
            "device_id",
            "heart_rate_bpm",
            "spo2_percent",
            "signal_quality",
            "measurement_status"
        ]
    ].copy()


    table.columns = [
        "Fecha y hora",
        "Estudiante",
        "NFC",
        "Dispositivo",
        "BPM",
        "SpO₂ (%)",
        "Calidad de señal",
        "Estado"
    ]


    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )
