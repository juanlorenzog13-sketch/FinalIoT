import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="Dashboard Tótem de Bienestar",
    page_icon="❤️",
    layout="wide"
)


# =========================================================
# ESTILOS VISUALES
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       FONDO GENERAL
    ===================================================== */

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background-color: #F7FAFC !important;
    }


    /* =====================================================
       TEXTO GENERAL
    ===================================================== */

    .stApp,
    .stApp p,
    .stApp span,
    .stApp label {
        color: #1F2933;
        opacity: 1 !important;
    }


    h1, h2, h3 {
        color: #183B4E !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }


    /* =====================================================
       SIDEBAR
    ===================================================== */

    [data-testid="stSidebar"] {
        background-color: #EAF4F7 !important;
        border-right: 1px solid #CBDDE3 !important;
    }

    [data-testid="stSidebar"] > div {
        background-color: #EAF4F7 !important;
    }


    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #1F3440 !important;
        opacity: 1 !important;
    }


    /* =====================================================
       TODOS LOS INPUTS
    ===================================================== */

    [data-testid="stSidebar"] div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        border: 1px solid #AFC5CE !important;
        border-radius: 10px !important;
        color: #172B35 !important;
    }


    [data-testid="stSidebar"] div[data-baseweb="input"] > div {
        background-color: #FFFFFF !important;
        color: #172B35 !important;
    }


    [data-testid="stSidebar"] div[data-baseweb="base-input"] {
        background-color: #FFFFFF !important;
        color: #172B35 !important;
    }


    [data-testid="stSidebar"] input {
        background-color: #FFFFFF !important;
        color: #172B35 !important;
        -webkit-text-fill-color: #172B35 !important;
        caret-color: #172B35 !important;
        opacity: 1 !important;
        font-weight: 500 !important;
    }


    [data-testid="stSidebar"] input::placeholder {
        color: #526772 !important;
        -webkit-text-fill-color: #526772 !important;
        opacity: 1 !important;
    }


    /* =====================================================
       INPUT DE FECHAS
    ===================================================== */

    [data-testid="stSidebar"] [data-testid="stDateInput"] {
        background-color: transparent !important;
    }


    [data-testid="stSidebar"]
    [data-testid="stDateInput"]
    div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        border: 1px solid #AFC5CE !important;
        border-radius: 10px !important;
        color: #172B35 !important;
    }


    [data-testid="stSidebar"]
    [data-testid="stDateInput"]
    div[data-baseweb="input"] > div {
        background-color: #FFFFFF !important;
        color: #172B35 !important;
    }


    [data-testid="stSidebar"]
    [data-testid="stDateInput"]
    input {
        background-color: #FFFFFF !important;
        color: #172B35 !important;
        -webkit-text-fill-color: #172B35 !important;
        opacity: 1 !important;
    }


    [data-testid="stSidebar"]
    [data-testid="stDateInput"]
    button {
        background-color: #FFFFFF !important;
        color: #315767 !important;
        border: none !important;
    }


    [data-testid="stSidebar"]
    [data-testid="stDateInput"]
    button svg {
        color: #315767 !important;
        fill: #315767 !important;
        opacity: 1 !important;
    }


    /* =====================================================
       SELECTBOX
    ===================================================== */

    [data-testid="stSidebar"]
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #AFC5CE !important;
        border-radius: 10px !important;
        color: #172B35 !important;
    }


    [data-testid="stSidebar"]
    div[data-baseweb="select"] span {
        color: #172B35 !important;
        -webkit-text-fill-color: #172B35 !important;
        opacity: 1 !important;
    }


    [data-testid="stSidebar"]
    div[data-baseweb="select"] svg {
        color: #315767 !important;
        fill: #315767 !important;
        opacity: 1 !important;
    }


    /* =====================================================
       MENÚS DESPLEGABLES
    ===================================================== */

    div[data-baseweb="popover"] {
        background-color: #FFFFFF !important;
    }


    div[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
    }


    div[data-baseweb="menu"] ul {
        background-color: #FFFFFF !important;
    }


    div[role="option"] {
        background-color: #FFFFFF !important;
        color: #172B35 !important;
        opacity: 1 !important;
    }


    div[role="option"] * {
        color: #172B35 !important;
        opacity: 1 !important;
    }


    div[role="option"]:hover {
        background-color: #DCECF2 !important;
        color: #102A36 !important;
    }


    /* =====================================================
       CALENDARIO
    ===================================================== */

    div[data-baseweb="calendar"] {
        background-color: #FFFFFF !important;
        color: #172B35 !important;
    }


    div[data-baseweb="calendar"] * {
        color: #172B35 !important;
        opacity: 1 !important;
    }


    /* =====================================================
       MÉTRICAS
    ===================================================== */

    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE7EC !important;
        border-radius: 16px !important;
        padding: 18px !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
    }


    [data-testid="stMetricLabel"] p {
        color: #455A64 !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }


    [data-testid="stMetricValue"] {
        color: #183B4E !important;
        opacity: 1 !important;
    }


    /* =====================================================
       CAJAS
    ===================================================== */

    .info-card {
        background-color: #FFFFFF;
        border: 1px solid #DCE7EC;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
        color: #1F2933 !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.04);
    }


    /* =====================================================
       EXPANDERS
    ===================================================== */

    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1px solid #DCE7EC !important;
    }


    /* =====================================================
       TABLA
    ===================================================== */

    [data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
    }


    /* =====================================================
       LÍNEAS
    ===================================================== */

    hr {
        border-color: #CBDDE3 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# COLORES GENERALES DE LAS GRÁFICAS
# =========================================================

GRAPH_TEXT = "#102A36"
GRAPH_SECONDARY_TEXT = "#29434E"
GRAPH_GRID = "#CFDCE1"
GRAPH_BACKGROUND = "#FFFFFF"


# =========================================================
# FUNCIÓN PARA DAR ESTILO A TODAS LAS GRÁFICAS
# =========================================================

def style_chart(fig):

    fig.update_layout(
        template="plotly_white",

        paper_bgcolor=GRAPH_BACKGROUND,
        plot_bgcolor=GRAPH_BACKGROUND,

        font=dict(
            color=GRAPH_TEXT,
            size=15
        ),

        title=dict(
            font=dict(
                color=GRAPH_TEXT,
                size=21
            )
        ),

        legend=dict(
            font=dict(
                color=GRAPH_TEXT,
                size=14
            )
        ),

        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#90A4AE",

            font=dict(
                color="#000000",
                size=14
            )
        )
    )


    # Las gráficas Pie no tienen ejes
    axis_chart_types = {
        "bar",
        "histogram",
        "scatter",
        "box",
        "violin"
    }

    has_axes = any(
        trace.type in axis_chart_types
        for trace in fig.data
    )


    if has_axes:

        fig.update_xaxes(
            showgrid=True,
            gridcolor=GRAPH_GRID,
            gridwidth=1,

            zerolinecolor=GRAPH_GRID,

            tickfont=dict(
                color=GRAPH_SECONDARY_TEXT,
                size=14
            ),

            title_font=dict(
                color=GRAPH_TEXT,
                size=16
            ),

            linecolor="#90A4AE",
            tickcolor="#607D8B"
        )


        fig.update_yaxes(
            showgrid=True,
            gridcolor=GRAPH_GRID,
            gridwidth=1,

            zerolinecolor=GRAPH_GRID,

            tickfont=dict(
                color=GRAPH_SECONDARY_TEXT,
                size=14
            ),

            title_font=dict(
                color=GRAPH_TEXT,
                size=16
            ),

            linecolor="#90A4AE",
            tickcolor="#607D8B"
        )


    return fig


# =========================================================
# ARCHIVO CSV
# =========================================================

CSV_PATH = (
    Path(__file__).parent
    / "proyecto_integrador_eafit_max30102.csv"
)


# =========================================================
# CARGA DE DATOS
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(CSV_PATH)


    # Fecha
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True,
        errors="coerce"
    )


    # Convertir a hora Colombia
    df["timestamp_local"] = (
        df["timestamp"]
        .dt.tz_convert("America/Bogota")
    )


    # Datos numéricos
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


    # Estado
    df["measurement_status"] = (
        df["measurement_status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )


    # Fecha y hora auxiliares
    df["date"] = (
        df["timestamp_local"]
        .dt.date
    )


    df["hour"] = (
        df["timestamp_local"]
        .dt.hour
    )


    return df


# =========================================================
# ABRIR CSV
# =========================================================

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

st.title(
    "❤️ Dashboard del Tótem de Bienestar"
)


st.markdown(
    """
    <div class="info-card">

    <b>¿Qué muestra este dashboard?</b><br><br>

    Este tablero permite analizar las mediciones registradas
    por un tótem IoT utilizado por estudiantes.

    Se estudian principalmente la
    <b>frecuencia cardíaca</b>,
    la <b>saturación estimada de oxígeno</b>,
    la cantidad de usos del dispositivo
    y la calidad de las mediciones.

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FILTROS
# =========================================================

st.sidebar.header(
    "🔎 Filtros"
)


# =========================================================
# FILTRO FECHAS
# =========================================================

min_date = df["date"].min()
max_date = df["date"].max()


date_selection = st.sidebar.date_input(
    "🗓️ Rango de fechas",

    value=(
        min_date,
        max_date
    ),

    min_value=min_date,
    max_value=max_date
)


if isinstance(
    date_selection,
    (tuple, list)
):

    if len(date_selection) == 2:

        start_date = date_selection[0]

        end_date = date_selection[1]

    elif len(date_selection) == 1:

        start_date = date_selection[0]

        end_date = date_selection[0]

    else:

        start_date = min_date

        end_date = max_date

else:

    start_date = date_selection

    end_date = date_selection


# =========================================================
# FILTRO ESTUDIANTE
# =========================================================

student_options = (
    ["Todos"]
    +
    sorted(
        df["student_id"]
        .dropna()
        .unique()
        .tolist()
    )
)


selected_student = st.sidebar.selectbox(
    "🎓 Estudiante",
    student_options
)


# =========================================================
# FILTRO ESTADO
# =========================================================

selected_status = st.sidebar.selectbox(
    "✅ Estado de la medición",

    [
        "Todos",
        "Válidas",
        "Inválidas"
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


if selected_status == "Válidas":

    filtered = filtered[
        filtered["measurement_status"]
        == "valid"
    ]


elif selected_status == "Inválidas":

    filtered = filtered[
        filtered["measurement_status"]
        == "invalid"
    ]


# =========================================================
# VALIDAR DATOS
# =========================================================

if filtered.empty:

    st.warning(
        "No hay registros que coincidan "
        "con los filtros seleccionados."
    )

    st.stop()


# =========================================================
# DATOS VÁLIDOS
# =========================================================

valid_filtered = filtered[
    filtered["measurement_status"]
    == "valid"
]


# =========================================================
# INDICADORES
# =========================================================

st.subheader(
    "📌 Indicadores generales"
)


total_measurements = len(filtered)


unique_students = (
    filtered["student_id"]
    .nunique()
)


if not valid_filtered.empty:

    avg_hr = (
        valid_filtered["heart_rate_bpm"]
        .mean()
    )


    avg_spo2 = (
        valid_filtered["spo2_percent"]
        .mean()
    )

else:

    avg_hr = None

    avg_spo2 = None


invalid_count = (
    filtered["measurement_status"]
    .eq("invalid")
    .sum()
)


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
    "⚠️ Inválidas",
    f"{invalid_percentage:.1f} %"
)


st.caption(
    "Los promedios de BPM y SpO₂ utilizan "
    "únicamente mediciones válidas."
)


st.markdown("---")


# =========================================================
# GRÁFICA 1
# MEDICIONES POR DÍA
# =========================================================

st.subheader(
    "📅 Uso del tótem a través del tiempo"
)


measurements_day = (
    filtered
    .groupby("date")
    .size()
    .reset_index(
        name="Mediciones"
    )
)


fig_day = px.bar(
    measurements_day,

    x="date",
    y="Mediciones",

    title="Cantidad de mediciones por día",

    labels={
        "date": "Fecha",
        "Mediciones":
        "Número de mediciones"
    },

    color_discrete_sequence=[
        "#4FA8A1"
    ]
)


style_chart(fig_day)


fig_day.update_layout(
    showlegend=False
)


st.plotly_chart(
    fig_day,
    use_container_width=True
)


# =========================================================
# GRÁFICAS BPM Y SPO2
# =========================================================

st.subheader(
    "❤️ Indicadores fisiológicos"
)


graph1, graph2 = st.columns(2)


# =========================================================
# BPM
# =========================================================

with graph1:

    if not valid_filtered.empty:

        fig_hr = px.histogram(
            valid_filtered,

            x="heart_rate_bpm",

            nbins=20,

            title=(
                "Distribución de "
                "frecuencia cardíaca"
            ),

            labels={
                "heart_rate_bpm":
                "Frecuencia cardíaca (BPM)"
            },

            color_discrete_sequence=[
                "#E57373"
            ]
        )


        fig_hr.update_layout(
            yaxis_title="Cantidad de mediciones",
            showlegend=False
        )


        style_chart(fig_hr)


        st.plotly_chart(
            fig_hr,
            use_container_width=True
        )


        st.caption(
            "Cada barra muestra cuántas "
            "mediciones están dentro de "
            "un rango de BPM."
        )

    else:

        st.info(
            "No hay mediciones válidas "
            "de frecuencia cardíaca."
        )


# =========================================================
# SPO2
# =========================================================

with graph2:

    if not valid_filtered.empty:

        fig_spo2 = px.histogram(
            valid_filtered,

            x="spo2_percent",

            nbins=20,

            title=(
                "Distribución de "
                "saturación de oxígeno"
            ),

            labels={
                "spo2_percent":
                "SpO₂ estimada (%)"
            },

            color_discrete_sequence=[
                "#5E9ED6"
            ]
        )


        fig_spo2.update_layout(
            yaxis_title="Cantidad de mediciones",
            showlegend=False
        )


        style_chart(fig_spo2)


        st.plotly_chart(
            fig_spo2,
            use_container_width=True
        )


        st.caption(
            "La gráfica muestra en qué "
            "valores se concentran las "
            "mediciones de SpO₂."
        )

    else:

        st.info(
            "No hay mediciones válidas de SpO₂."
        )


# =========================================================
# HORARIOS Y ESTADOS
# =========================================================

st.subheader(
    "🕒 ¿Cuándo y cómo se utiliza el tótem?"
)


graph3, graph4 = st.columns(2)


# =========================================================
# HORARIOS
# =========================================================

with graph3:

    hourly = (
        filtered
        .groupby("hour")
        .size()
        .reset_index(
            name="Mediciones"
        )
    )


    fig_hour = px.bar(
        hourly,

        x="hour",
        y="Mediciones",

        title="Mediciones según la hora del día",

        labels={
            "hour": "Hora del día",
            "Mediciones":
            "Número de mediciones"
        },

        color_discrete_sequence=[
            "#E4A94F"
        ]
    )


    style_chart(fig_hour)


    fig_hour.update_layout(
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
        "Las barras más altas muestran "
        "las horas en las que el tótem "
        "fue utilizado más veces."
    )


# =========================================================
# ESTADO DE MEDICIONES
# =========================================================

with graph4:

    status_counts = (
        filtered["measurement_status"]
        .value_counts()
        .reset_index()
    )


    status_counts.columns = [
        "Estado",
        "Cantidad"
    ]


    status_counts["Estado"] = (
        status_counts["Estado"]
        .replace({
            "valid": "Válida",
            "invalid": "Inválida"
        })
    )


    fig_status = px.pie(
        status_counts,

        names="Estado",
        values="Cantidad",

        hole=0.55,

        title="Calidad de las mediciones",

        color="Estado",

        color_discrete_map={
            "Válida": "#69B984",
            "Inválida": "#E57373"
        }
    )


    style_chart(fig_status)


    fig_status.update_traces(
        textposition="auto",

        textfont=dict(
            color="#102A36",
            size=16
        ),

        marker=dict(
            line=dict(
                color="#FFFFFF",
                width=2
            )
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
# CALIDAD DE SEÑAL
# =========================================================

st.subheader(
    "📶 Calidad de la señal"
)


signal_data = filtered.copy()


signal_data["Estado"] = (
    signal_data["measurement_status"]
    .replace({
        "valid": "Válida",
        "invalid": "Inválida"
    })
)


fig_signal = px.box(
    signal_data,

    x="Estado",
    y="signal_quality",

    color="Estado",

    title=(
        "Calidad de señal según "
        "el estado de la medición"
    ),

    labels={
        "Estado": "Estado",
        "signal_quality":
        "Calidad de señal"
    },

    color_discrete_map={
        "Válida": "#69B984",
        "Inválida": "#E57373"
    }
)


style_chart(fig_signal)


fig_signal.update_layout(
    showlegend=False
)


st.plotly_chart(
    fig_signal,
    use_container_width=True
)


st.caption(
    "La calidad de señal se expresa entre 0 y 1. "
    "Los valores cercanos a 1 representan "
    "una mejor calidad de señal."
)


st.markdown("---")


# =========================================================
# SEGUIMIENTO INDIVIDUAL
# =========================================================

st.subheader(
    "🎓 Seguimiento individual"
)


st.write(
    "Selecciona un estudiante para consultar "
    "su histórico de mediciones."
)


individual_base = df[
    (df["date"] >= start_date)
    &
    (df["date"] <= end_date)
].copy()


if selected_status == "Válidas":

    individual_base = individual_base[
        individual_base["measurement_status"]
        == "valid"
    ]


elif selected_status == "Inválidas":

    individual_base = individual_base[
        individual_base["measurement_status"]
        == "invalid"
    ]


available_students = sorted(
    individual_base["student_id"]
    .dropna()
    .unique()
    .tolist()
)


if available_students:

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
        "👤 Estudiante para seguimiento",

        available_students,

        index=default_index,

        key="individual_student"
    )


    student_data = (
        individual_base[
            individual_base["student_id"]
            == individual_student
        ]
        .sort_values(
            "timestamp_local"
        )
    )


    # =====================================================
    # DATOS DEL ESTUDIANTE
    # =====================================================

    first_measurement = (
        student_data["timestamp_local"]
        .min()
    )


    last_measurement = (
        student_data["timestamp_local"]
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


    # =====================================================
    # GRÁFICAS INDIVIDUALES
    # =====================================================

    individual1, individual2 = st.columns(2)


    with individual1:

        fig_ind_hr = px.line(
            student_data,

            x="timestamp_local",
            y="heart_rate_bpm",

            markers=True,

            color="measurement_status",

            title=(
                "❤️ Evolución de "
                "frecuencia cardíaca"
            ),

            labels={
                "timestamp_local":
                "Fecha y hora",

                "heart_rate_bpm":
                "Frecuencia cardíaca (BPM)",

                "measurement_status":
                "Estado"
            },

            color_discrete_map={
                "valid": "#D85C5C",
                "invalid": "#667780"
            }
        )


        style_chart(fig_ind_hr)


        fig_ind_hr.update_traces(
            line=dict(
                width=3
            ),

            marker=dict(
                size=8
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
                "valid": "#448FC4",
                "invalid": "#667780"
            }
        )


        style_chart(fig_ind_spo2)


        fig_ind_spo2.update_traces(
            line=dict(
                width=3
            ),

            marker=dict(
                size=8
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

st.subheader(
    "🔍 Análisis e interpretación"
)


# Día con más uso
daily_counts = (
    filtered
    .groupby("date")
    .size()
)


top_day = daily_counts.idxmax()


top_day_count = int(
    daily_counts.max()
)


# Hora con más uso
hour_counts = (
    filtered
    .groupby("hour")
    .size()
)


top_hour = int(
    hour_counts.idxmax()
)


top_hour_count = int(
    hour_counts.max()
)


# Estudiante con más registros
student_counts = (
    filtered["student_id"]
    .value_counts()
)


top_student = (
    student_counts.index[0]
)


top_student_count = int(
    student_counts.iloc[0]
)


# =========================================================
# HALLAZGOS
# =========================================================

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

st.warning(
    """
    ⚠️ **Importante sobre la interpretación de los datos**

    Las mediciones de frecuencia cardíaca y SpO₂ mostradas
    en este dashboard pertenecen a un escenario educativo.

    Estas variables no permiten, por sí solas, determinar
    el estado general de salud de una persona.

    El sensor MAX30102 no debe interpretarse como un
    dispositivo médico validado.

    Este dashboard no realiza diagnósticos médicos
    ni clasificaciones clínicas.
    """
)


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


    table["measurement_status"] = (
        table["measurement_status"]
        .replace({
            "valid": "Válida",
            "invalid": "Inválida"
        })
    )


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
