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

    /* FONDO GENERAL */

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background-color: #F7FAFC !important;
    }


    /* TEXTO GENERAL */

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
    }


    /* SIDEBAR */

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


    /* CAMPO DE FECHAS */

    [data-testid="stSidebar"]
    [data-testid="stDateInput"]
    div[data-baseweb="input"] {
        background-color: #111820 !important;
        border: 1px solid #111820 !important;
        border-radius: 10px !important;
    }

    [data-testid="stSidebar"]
    [data-testid="stDateInput"]
    div[data-baseweb="input"] > div {
        background-color: #111820 !important;
    }

    [data-testid="stSidebar"]
    [data-testid="stDateInput"]
    div[data-baseweb="base-input"] {
        background-color: #111820 !important;
    }

    /* TEXTO DE FECHAS BLANCO */

    [data-testid="stSidebar"]
    [data-testid="stDateInput"]
    input {
        background-color: #111820 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        caret-color: #FFFFFF !important;
        opacity: 1 !important;
        font-weight: 500 !important;
    }

    [data-testid="stSidebar"]
    [data-testid="stDateInput"]
    input::placeholder {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"]
    [data-testid="stDateInput"]
    button {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        color: #183B4E !important;
    }

    [data-testid="stSidebar"]
    [data-testid="stDateInput"]
    button svg {
        color: #183B4E !important;
        fill: #183B4E !important;
    }


    /* SELECTBOX */

    [data-testid="stSidebar"]
    div[data-baseweb="select"] > div {
        background-color: #111820 !important;
        border: 1px solid #111820 !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"]
    div[data-baseweb="select"] span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"]
    div[data-baseweb="select"] svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }


    /* MENÚ DESPLEGABLE */

    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    div[data-baseweb="menu"] ul {
        background-color: #FFFFFF !important;
    }

    div[role="option"] {
        background-color: #FFFFFF !important;
        color: #172B35 !important;
    }

    div[role="option"] * {
        color: #172B35 !important;
    }

    div[role="option"]:hover {
        background-color: #DCECF2 !important;
    }


    /* CALENDARIO */

    div[data-baseweb="calendar"] {
        background-color: #FFFFFF !important;
        color: #172B35 !important;
    }

    div[data-baseweb="calendar"] * {
        color: #172B35 !important;
        opacity: 1 !important;
    }


    /* MÉTRICAS */

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
    }

    [data-testid="stMetricValue"] {
        color: #183B4E !important;
    }


    /* CAJAS INFORMATIVAS */

    .info-card {
        background-color: #FFFFFF;
        border: 1px solid #DCE7EC;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
        color: #1F2933 !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.04);
    }


    /* TARJETAS DE INSIGHT */

    .insight-card {
        background-color: #EEF7FA;
        border-left: 5px solid #4FA8A1;
        border-radius: 12px;
        padding: 15px 18px;
        margin-top: 4px;
        margin-bottom: 20px;
        color: #183B4E !important;
        line-height: 1.55;
    }

    .insight-card strong {
        color: #102A36 !important;
    }


    .insight-red {
        background-color: #FFF1F1;
        border-left: 5px solid #E57373;
    }


    .insight-blue {
        background-color: #EEF6FD;
        border-left: 5px solid #5E9ED6;
    }


    .insight-yellow {
        background-color: #FFF8E8;
        border-left: 5px solid #E4A94F;
    }


    .insight-green {
        background-color: #EFF9F2;
        border-left: 5px solid #69B984;
    }


    /* EXPANDERS */

    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1px solid #DCE7EC !important;
    }


    /* DIVISORES */

    hr {
        border-color: #CBDDE3 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# COLORES DE GRÁFICAS
# =========================================================

GRAPH_TEXT = "#102A36"
GRAPH_SECONDARY_TEXT = "#29434E"
GRAPH_GRID = "#CFDCE1"
GRAPH_BACKGROUND = "#FFFFFF"


# =========================================================
# FUNCIÓN DE ESTILO PARA GRÁFICAS
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

    axis_types = {
        "bar",
        "histogram",
        "scatter",
        "box",
        "violin"
    }

    has_axes = any(
        trace.type in axis_types
        for trace in fig.data
    )

    if has_axes:

        fig.update_xaxes(
            showgrid=True,
            gridcolor=GRAPH_GRID,
            gridwidth=1,

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
# FUNCIÓN PARA MOSTRAR INSIGHTS
# =========================================================

def insight(
    emoji,
    title,
    text,
    color_class=""
):

    st.markdown(
        f"""
        <div class="insight-card {color_class}">
            <strong>{emoji} {title}</strong><br>
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# ARCHIVO CSV
# =========================================================

CSV_PATH = (
    Path(__file__).parent
    / "proyecto_integrador_eafit_max30102.csv"
)


# =========================================================
# CARGA Y PREPARACIÓN DE DATOS
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(CSV_PATH)

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True,
        errors="coerce"
    )

    # Convertir a hora de Colombia
    df["timestamp_local"] = (
        df["timestamp"]
        .dt.tz_convert("America/Bogota")
    )

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

    df["measurement_status"] = (
        df["measurement_status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

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
    la cantidad de usos del dispositivo y
    la calidad de las mediciones.

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
# FECHAS
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
# ESTUDIANTE
# =========================================================

student_options = (
    ["Todos"]

    + sorted(
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
# ESTADO
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
# USO POR DÍA
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


# Insight de uso diario

peak_day_row = measurements_day.loc[
    measurements_day["Mediciones"].idxmax()
]

peak_day = peak_day_row["date"]

peak_day_measurements = int(
    peak_day_row["Mediciones"]
)

daily_average = (
    measurements_day["Mediciones"]
    .mean()
)

peak_day_percentage = (
    peak_day_measurements
    / total_measurements
    * 100
)


insight(
    "📌",
    "Resultado principal",
    (
        f"El día con mayor uso fue "
        f"<strong>{peak_day.strftime('%d/%m/%Y')}</strong>, "
        f"con <strong>{peak_day_measurements} mediciones</strong>. "
        f"Esto representa el <strong>{peak_day_percentage:.1f}%</strong> "
        f"de todas las mediciones visibles. "
        f"El promedio diario fue de "
        f"<strong>{daily_average:.1f} mediciones</strong>."
    )
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

        hr_data = (
            valid_filtered["heart_rate_bpm"]
            .dropna()
        )


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


        # Estadísticas BPM

        hr_mean = hr_data.mean()

        hr_median = hr_data.median()

        hr_q1 = hr_data.quantile(0.25)

        hr_q3 = hr_data.quantile(0.75)


        insight(
            "❤️",
            "¿Qué nos muestra?",
            (
                f"Las mediciones válidas tienen un promedio de "
                f"<strong>{hr_mean:.1f} BPM</strong> "
                f"y una mediana de "
                f"<strong>{hr_median:.1f} BPM</strong>. "
                f"El 50% central de los registros se encuentra "
                f"aproximadamente entre "
                f"<strong>{hr_q1:.1f} y {hr_q3:.1f} BPM</strong>."
            ),
            "insight-red"
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

        spo2_data = (
            valid_filtered["spo2_percent"]
            .dropna()
        )


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


        # Estadísticas SpO2

        spo2_mean = spo2_data.mean()

        spo2_median = spo2_data.median()

        spo2_q1 = spo2_data.quantile(0.25)

        spo2_q3 = spo2_data.quantile(0.75)


        insight(
            "🫁",
            "¿Qué nos muestra?",
            (
                f"La SpO₂ estimada promedio de las mediciones válidas "
                f"es de <strong>{spo2_mean:.1f}%</strong>, "
                f"con una mediana de "
                f"<strong>{spo2_median:.1f}%</strong>. "
                f"El 50% central de los valores está entre "
                f"<strong>{spo2_q1:.1f}% y {spo2_q3:.1f}%</strong>."
            ),
            "insight-blue"
        )


    else:

        st.info(
            "No hay mediciones válidas de SpO₂."
        )


# =========================================================
# HORARIOS Y ESTADO
# =========================================================

st.subheader(
    "🕒 ¿Cuándo y cómo se utiliza el tótem?"
)


graph3, graph4 = st.columns(2)


# =========================================================
# HORAS DE USO
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
            "hour":
            "Hora del día",

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


    peak_hour_row = hourly.loc[
        hourly["Mediciones"].idxmax()
    ]

    peak_hour = int(
        peak_hour_row["hour"]
    )

    peak_hour_count = int(
        peak_hour_row["Mediciones"]
    )

    peak_hour_percentage = (
        peak_hour_count
        / total_measurements
        * 100
    )


    insight(
        "🕒",
        "Hora de mayor actividad",
        (
            f"El horario con más registros fue entre "
            f"<strong>{peak_hour:02d}:00 y "
            f"{peak_hour:02d}:59</strong>, "
            f"con <strong>{peak_hour_count} mediciones</strong>. "
            f"Representa aproximadamente el "
            f"<strong>{peak_hour_percentage:.1f}%</strong> "
            f"de la actividad mostrada."
        ),
        "insight-yellow"
    )


# =========================================================
# CALIDAD DE LAS MEDICIONES
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


    valid_count = (
        filtered["measurement_status"]
        .eq("valid")
        .sum()
    )


    valid_percentage = (
        valid_count
        / total_measurements
        * 100
    )


    insight(
        "✅",
        "Calidad de los registros",
        (
            f"De las <strong>{total_measurements} mediciones</strong>, "
            f"<strong>{valid_count}</strong> fueron válidas "
            f"(<strong>{valid_percentage:.1f}%</strong>) "
            f"y <strong>{invalid_count}</strong> fueron inválidas "
            f"(<strong>{invalid_percentage:.1f}%</strong>)."
        ),
        "insight-green"
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


# Insight calidad señal

signal_valid = (
    filtered.loc[
        filtered["measurement_status"] == "valid",
        "signal_quality"
    ]
    .dropna()
)


signal_invalid = (
    filtered.loc[
        filtered["measurement_status"] == "invalid",
        "signal_quality"
    ]
    .dropna()
)


if (
    not signal_valid.empty
    and
    not signal_invalid.empty
):

    median_valid = (
        signal_valid.median()
    )

    median_invalid = (
        signal_invalid.median()
    )


    difference = (
        median_valid
        - median_invalid
    )


    if difference > 0:

        comparison_text = (
            f"La mediana de señal de los registros válidos "
            f"es <strong>{median_valid:.3f}</strong>, "
            f"mientras que la de los inválidos es "
            f"<strong>{median_invalid:.3f}</strong>. "
            f"En estos datos, las mediciones válidas presentan "
            f"una mediana de señal "
            f"<strong>{difference:.3f} puntos mayor</strong>."
        )

    elif difference < 0:

        comparison_text = (
            f"La mediana de señal de los registros válidos "
            f"es <strong>{median_valid:.3f}</strong>, "
            f"mientras que la de los inválidos es "
            f"<strong>{median_invalid:.3f}</strong>. "
            f"En este filtro, la diferencia observada es de "
            f"<strong>{abs(difference):.3f} puntos</strong> "
            f"a favor de los registros inválidos."
        )

    else:

        comparison_text = (
            f"Las mediciones válidas e inválidas tienen "
            f"la misma mediana de calidad de señal: "
            f"<strong>{median_valid:.3f}</strong>."
        )


    insight(
        "📡",
        "Relación con la calidad de señal",
        comparison_text
    )


else:

    signal_all = (
        filtered["signal_quality"]
        .dropna()
    )


    if not signal_all.empty:

        insight(
            "📡",
            "Calidad de señal",
            (
                f"La mediana de calidad de señal de los registros "
                f"mostrados es <strong>{signal_all.median():.3f}</strong>. "
                f"La escala va de 0 a 1, donde un valor más alto "
                f"representa una mejor calidad de señal."
            )
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


    individual1, individual2 = st.columns(2)


    # =====================================================
    # BPM INDIVIDUAL
    # =====================================================

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


        student_valid_hr = (
            student_data.loc[
                student_data["measurement_status"] == "valid",
                "heart_rate_bpm"
            ]
            .dropna()
        )


        if not student_valid_hr.empty:

            insight(
                "❤️",
                "Resumen del estudiante",
                (
                    f"En sus mediciones válidas, "
                    f"<strong>{individual_student}</strong> registra "
                    f"un promedio de "
                    f"<strong>{student_valid_hr.mean():.1f} BPM</strong>. "
                    f"El valor mínimo observado es "
                    f"<strong>{student_valid_hr.min():.1f}</strong> "
                    f"y el máximo es "
                    f"<strong>{student_valid_hr.max():.1f} BPM</strong>."
                ),
                "insight-red"
            )


    # =====================================================
    # SPO2 INDIVIDUAL
    # =====================================================

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


        student_valid_spo2 = (
            student_data.loc[
                student_data["measurement_status"] == "valid",
                "spo2_percent"
            ]
            .dropna()
        )


        if not student_valid_spo2.empty:

            insight(
                "🫁",
                "Resumen del estudiante",
                (
                    f"En las mediciones válidas de "
                    f"<strong>{individual_student}</strong>, "
                    f"la SpO₂ estimada promedio es "
                    f"<strong>{student_valid_spo2.mean():.1f}%</strong>. "
                    f"Los valores observados van desde "
                    f"<strong>{student_valid_spo2.min():.1f}%</strong> "
                    f"hasta "
                    f"<strong>{student_valid_spo2.max():.1f}%</strong>."
                ),
                "insight-blue"
            )


else:

    st.info(
        "No existen estudiantes disponibles "
        "con los filtros seleccionados."
    )


st.markdown("---")


# =========================================================
# ANÁLISIS GENERAL
# =========================================================

st.subheader(
    "🔍 Principales hallazgos"
)


daily_counts = (
    filtered
    .groupby("date")
    .size()
)


top_day = (
    daily_counts.idxmax()
)


top_day_count = int(
    daily_counts.max()
)


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
# HALLAZGOS EN TARJETAS
# =========================================================

h1, h2, h3 = st.columns(3)


with h1:

    insight(
        "📅",
        "Día más activo",
        (
            f"<strong>{top_day.strftime('%d/%m/%Y')}</strong><br>"
            f"{top_day_count} mediciones registradas."
        )
    )


with h2:

    insight(
        "🕒",
        "Hora más activa",
        (
            f"<strong>{top_hour:02d}:00 – "
            f"{top_hour:02d}:59</strong><br>"
            f"{top_hour_count} mediciones registradas."
        ),
        "insight-yellow"
    )


with h3:

    insight(
        "🎓",
        "Estudiante con más usos",
        (
            f"<strong>{top_student}</strong><br>"
            f"{top_student_count} mediciones registradas."
        ),
        "insight-green"
    )


# =========================================================
# INTERPRETACIÓN GENERAL
# =========================================================

st.markdown(
    f"""
### 🧠 Lectura general de los resultados

- 📊 El período seleccionado contiene **{total_measurements} mediciones**
  realizadas por **{unique_students} estudiantes diferentes**.

- 📅 La mayor actividad se registró el
  **{top_day.strftime("%d/%m/%Y")}**, con
  **{top_day_count} mediciones**.

- 🕒 La hora de mayor utilización fue entre
  **{top_hour:02d}:00 y {top_hour:02d}:59**.

- 🎓 **{top_student}** fue el estudiante con mayor cantidad de usos,
  con **{top_student_count} registros**.

- ✅ **{valid_percentage:.1f}%** de los registros mostrados son
  mediciones válidas.

- ⚠️ **{invalid_percentage:.1f}%** de los registros corresponden
  a mediciones inválidas.
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

    Los valores permiten analizar patrones y cambios en las
    mediciones registradas, pero no permiten determinar por sí solos
    el estado general de salud de una persona.

    El sensor MAX30102 del ejercicio no debe considerarse un
    dispositivo médico validado.

    Este dashboard no realiza diagnósticos ni clasificaciones clínicas.
    """
)


# =========================================================
# TABLA
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
