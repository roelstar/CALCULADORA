import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="ROELSTAR TRADING | Evaluador de Rentabilidad",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "roelstar_logo.png"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp { background: #f3f5f9; color: #15233b; }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.1rem; padding-bottom: 2.2rem; max-width: 1400px; }
.roelstar-banner {
  background: linear-gradient(120deg,#111318 0%,#292a2f 72%,#c7192d 100%);
  border-bottom: 5px solid #ed2939; border-radius: 18px;
  padding: 22px 26px; color: white; margin-bottom: 18px;
  box-shadow: 0 8px 22px rgba(20,30,50,.12);
}
.roelstar-banner h1 { color: white; font-size: clamp(1.35rem,2.4vw,2.1rem); margin: 0; line-height:1.2; }
.roelstar-banner p { color:#f0f0f2; margin:8px 0 0 0; font-size:.98rem; }
.section-card { background:white; border:1px solid #e5eaf1; border-radius:15px; padding:16px 18px; margin:8px 0 14px 0; }
.section-title { font-size:1.05rem; font-weight:800; color:#172b4d; margin-bottom:10px; }
.kpi {
  border-radius: 15px; padding: 16px 17px; min-height: 118px;
  border: 1px solid rgba(20,40,80,.06); background:white;
  box-shadow: 0 3px 10px rgba(20,30,50,.04); margin-bottom: 12px;
}
.kpi-label { color:#273650; font-size:.87rem; font-weight:650; }
.kpi-value { font-size:clamp(1.15rem,2vw,1.7rem); font-weight:800; line-height:1.35; margin-top:5px; overflow-wrap:anywhere; }
.kpi-sub { font-size:.79rem; margin-top:4px; color:#475569; }
.kpi-blue { background:#e5f0ff; } .kpi-green { background:#e5f7ec; }
.kpi-orange { background:#fff0e2; } .kpi-purple { background:#f1e8ff; }
.kpi-red { background:#ffe9e9; } .kpi-yellow { background:#fff6d8; }
.stButton>button[kind="primary"] { background:#c7192d; border:0; color:white; border-radius:10px; font-weight:700; }
.stButton>button[kind="primary"]:hover { background:#a91425; color:white; }
div[data-testid="stTabs"] button { font-weight:700; }
div[data-testid="stMetric"] { background:white; border:1px solid #e5eaf1; border-radius:12px; padding:12px; }
div[data-testid="stNumberInput"] input { font-variant-numeric: tabular-nums; }
.small-note { color:#5b6576; font-size:.82rem; }
</style>
""", unsafe_allow_html=True)

def cop(value):
    return "$ " + f"{value:,.0f}".replace(",", ".")

def kpi(label, value, sub="", color="blue"):
    st.markdown(
        f'<div class="kpi kpi-{color}"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>',
        unsafe_allow_html=True
    )

logo_col, title_col = st.columns([1.15, 3.85], vertical_alignment="center")
with logo_col:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    else:
        st.markdown("## ⭐ ROELSTAR")
with title_col:
    st.markdown("""
    <div class="roelstar-banner">
      <h1>Evaluador de Rentabilidad e Inversiones</h1>
      <p>Analiza cuánto gana un negocio, su punto de equilibrio y si vale la pena invertir · COP</p>
    </div>
    """, unsafe_allow_html=True)

with st.expander("Cómo usar el evaluador", expanded=False):
    st.markdown("""
    - Ingresa datos del mismo período (mensual o anual) y ventas preferiblemente sin IVA.
    - Registra el costo de lo vendido, no todas las compras de inventario.
    - No contabilices la nómina dos veces: en costo directo o en gastos operativos.
    - El ROI y la recuperación son estimaciones simples, no garantías de rendimiento.
    - Valida impuestos y clasificación contable con tu contador.
    """)

tab_datos, tab_resultados, tab_graficos, tab_analisis = st.tabs(
    ["🧾 Datos del negocio", "📊 Resultados", "📈 Gráficos", "🧠 Análisis"]
)

with tab_datos:
    st.markdown('<div class="section-title">1 · Información del negocio</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        nombre = st.text_input("Nombre del negocio", "Taller de motocicletas")
    with c2:
        tipo = st.selectbox("Tipo de negocio", ["Taller de motocicletas", "Almacén de repuestos", "Taller y repuestos", "Otro negocio"])
    with c3:
        periodo = st.selectbox("Período de análisis", ["Mensual", "Anual"])
    factor_anual = 12 if periodo == "Mensual" else 1

    st.markdown('<div class="section-title">2 · Ingresos del período</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: ingresos_servicios = st.number_input("Mano de obra / servicios ($)", min_value=0, value=30000000, step=500000, format="%d")
    with c2: ingresos_repuestos = st.number_input("Venta de repuestos/productos ($)", min_value=0, value=20000000, step=500000, format="%d")
    with c3: otros_ingresos = st.number_input("Otros ingresos ($)", min_value=0, value=0, step=100000, format="%d")
    descuentos = st.number_input("Descuentos y devoluciones ($)", min_value=0, value=0, step=100000, format="%d")
    ventas_brutas = ingresos_servicios + ingresos_repuestos + otros_ingresos
    ventas = max(0, ventas_brutas - descuentos)
    st.caption(f"Total de ingresos netos del período: **{cop(ventas)}**")

    st.markdown('<div class="section-title">3 · Costos directos</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: costo_productos = st.number_input("Costo de repuestos/productos vendidos ($)", min_value=0, value=12000000, step=250000, format="%d")
    with c2: costo_tecnicos = st.number_input("Técnicos / mano de obra directa ($)", min_value=0, value=0, step=250000, format="%d")
    with c3: insumos = st.number_input("Insumos y terceros ($)", min_value=0, value=3000000, step=100000, format="%d")
    with c4: otros_costos = st.number_input("Otros costos directos ($)", min_value=0, value=0, step=100000, format="%d")
    costos_directos = costo_productos + costo_tecnicos + insumos + otros_costos
    utilidad_bruta = ventas - costos_directos
    margen_bruto = utilidad_bruta / ventas if ventas else 0

    st.markdown('<div class="section-title">4 · Gastos operativos</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: nomina_admin = st.number_input("Nómina administrativa / asesores ($)", min_value=0, value=12000000, step=250000, format="%d")
    with c2: arriendo = st.number_input("Arriendo ($)", min_value=0, value=3000000, step=100000, format="%d")
    with c3: servicios = st.number_input("Servicios públicos y comunicaciones ($)", min_value=0, value=800000, step=100000, format="%d")
    with c4: mercadeo = st.number_input("Mercadeo y publicidad ($)", min_value=0, value=0, step=100000, format="%d")
    c1,c2,c3,c4 = st.columns(4)
    with c1: herramientas = st.number_input("Herramientas / mantenimiento ($)", min_value=0, value=1500000, step=100000, format="%d")
    with c2: transporte = st.number_input("Transporte / software / papelería ($)", min_value=0, value=0, step=100000, format="%d")
    with c3: seguros = st.number_input("Seguros / licencias ($)", min_value=0, value=0, step=100000, format="%d")
    with c4: otros_gastos = st.number_input("Otros gastos operativos ($)", min_value=0, value=2500000, step=100000, format="%d")
    gastos_operativos = nomina_admin + arriendo + servicios + mercadeo + herramientas + transporte + seguros + otros_gastos
    utilidad_operacional = utilidad_bruta - gastos_operativos
    margen_operacional = utilidad_operacional / ventas if ventas else 0

    st.markdown('<div class="section-title">5 · Financiación e impuestos</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: intereses = st.number_input("Intereses y gastos financieros ($)", min_value=0, value=500000, step=100000, format="%d")
    with c2: otros_resultados = st.number_input("Otros ingresos (+) o gastos (-) ($)", value=0, step=100000, format="%d")
    with c3: tasa_impuesto = st.number_input("Tasa efectiva estimada de impuesto (%)", min_value=0.0, max_value=50.0, value=25.0, step=1.0)
    utilidad_antes_impuestos = utilidad_operacional - intereses + otros_resultados
    impuesto_estimado = max(0, utilidad_antes_impuestos) * tasa_impuesto / 100
    utilidad_neta = utilidad_antes_impuestos - impuesto_estimado
    margen_neto = utilidad_neta / ventas if ventas else 0

    st.markdown('<div class="section-title">6 · Inversión</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: capital_invertido = st.number_input("Capital total a invertir ($)", min_value=0, value=200000000, step=1000000, format="%d")
    with c2: inversion_adicional = st.number_input("Inversión adicional ($)", min_value=0, value=0, step=500000, format="%d")
    with c3: retorno_objetivo = st.number_input("Retorno anual objetivo (%)", min_value=0.0, max_value=200.0, value=20.0, step=1.0)
    capital_total = capital_invertido + inversion_adicional
    st.caption("Los datos de ejemplo sirven solo para mostrar cómo funciona. Sustitúyelos por tus cifras reales.")

utilidad_mensual = utilidad_neta if periodo == "Mensual" else utilidad_neta / 12
utilidad_anual = utilidad_mensual * 12
roi_anual = utilidad_anual / capital_total if capital_total > 0 else None
recuperacion_meses = capital_total / utilidad_mensual if capital_total > 0 and utilidad_mensual > 0 else None
costos_variables = costo_productos + insumos + otros_costos
tasa_contribucion = (ventas - costos_variables) / ventas if ventas > 0 else 0
punto_equilibrio = gastos_operativos / tasa_contribucion if tasa_contribucion > 0 else None
utilidad_objetivo_mes = capital_total * retorno_objetivo / 100 / 12

with tab_resultados:
    st.markdown(f"### Resumen financiero · {nombre or tipo}")
    st.caption(f"Valores del período: {periodo.lower()} · Moneda: pesos colombianos (COP)")
    a,b,c,d = st.columns(4)
    with a: kpi("Ingresos netos", cop(ventas), "Ventas menos descuentos", "blue")
    with b: kpi("Utilidad bruta", cop(utilidad_bruta), f"Margen bruto: {margen_bruto:.1%}", "green")
    with c: kpi("Utilidad operacional", cop(utilidad_operacional), f"Margen operacional: {margen_operacional:.1%}", "orange")
    with d: kpi("Utilidad neta estimada", cop(utilidad_neta), f"Margen neto: {margen_neto:.1%}", "purple")
    st.markdown("#### Indicadores clave")
    a,b,c,d = st.columns(4)
    with a: kpi("ROI anual simple", f"{roi_anual:.1%}" if roi_anual is not None else "N/D", "Utilidad anual ÷ capital", "green")
    with b: kpi("Recuperación simple", f"{recuperacion_meses:.1f} meses" if recuperacion_meses is not None else "N/D", "Con utilidad positiva", "blue")
    with c: kpi("Punto de equilibrio", cop(punto_equilibrio) if punto_equilibrio is not None else "N/D", f"Ventas por período ({periodo.lower()})", "yellow")
    with d: kpi("Utilidad neta anualizada", cop(utilidad_anual), "Si se mantiene el resultado", "red")
    st.markdown("#### Evaluación preliminar")
    if ventas <= 0:
        st.warning("Ingresa ventas mayores que cero para evaluar los márgenes.")
    elif utilidad_neta < 0:
        st.error("Con estas cifras el negocio presenta pérdida neta. Revisa precios, costos, nómina y gastos fijos.")
    elif roi_anual is not None and roi_anual >= retorno_objetivo / 100:
        st.success(f"El ROI simple estimado supera el objetivo del {retorno_objetivo:.1f}% anual. Antes de invertir, valida estabilidad de ventas, deudas y flujo de caja.")
    else:
        st.warning(f"El ROI simple estimado no alcanza el objetivo del {retorno_objetivo:.1f}% anual. Revisa los supuestos antes de tomar una decisión.")
    st.info(f"Para alcanzar el retorno objetivo indicado, la utilidad neta mensual requerida sería aproximadamente **{cop(utilidad_objetivo_mes)}**.")
    st.caption("ROI y recuperación son estimaciones simples. No sustituyen un flujo de caja proyectado ni un análisis contable completo.")

with tab_graficos:
    st.markdown("### Estructura financiera")
    chart_df = pd.DataFrame({
        "Concepto": ["Ingresos", "Costos directos", "Gastos operativos", "Utilidad neta"],
        "Valor": [ventas, costos_directos, gastos_operativos, utilidad_neta]
    })
    fig = px.bar(chart_df, x="Concepto", y="Valor", text="Valor", color="Concepto",
                 title="Ingresos y resultados del período")
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig.update_layout(showlegend=False, plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                      yaxis_title="Pesos colombianos (COP)", xaxis_title="", margin=dict(l=10,r=10,t=60,b=10))
    st.plotly_chart(fig, use_container_width=True)
    distribution = pd.DataFrame({
        "Categoría": ["Costos directos", "Gastos operativos", "Financieros e impuestos", "Utilidad neta"],
        "Valor": [costos_directos, gastos_operativos, max(0, intereses + impuesto_estimado), max(0, utilidad_neta)]
    })
    distribution = distribution[distribution["Valor"] > 0]
    if not distribution.empty:
        fig2 = px.pie(distribution, names="Categoría", values="Valor", hole=.52, title="Distribución de ingresos")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=10,r=10,t=60,b=10))
        st.plotly_chart(fig2, use_container_width=True)

with tab_analisis:
    st.markdown("### Análisis gerencial")
    rows = [
        ("Ingresos netos", ventas),
        ("Costos directos", costos_directos),
        ("Utilidad bruta", utilidad_bruta),
        ("Gastos operativos", gastos_operativos),
        ("Utilidad operacional", utilidad_operacional),
        ("Intereses", intereses),
        ("Impuestos estimados", impuesto_estimado),
        ("Utilidad neta", utilidad_neta),
    ]
    summary = pd.DataFrame(rows, columns=["Concepto", "Valor (COP)"])
    summary["Valor (COP)"] = summary["Valor (COP)"].map(cop)
    st.dataframe(summary, use_container_width=True, hide_index=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("#### Lectura de márgenes")
        st.write(f"- **Margen bruto:** {margen_bruto:.1%}")
        st.write(f"- **Margen operacional:** {margen_operacional:.1%}")
        st.write(f"- **Margen neto:** {margen_neto:.1%}")
        st.write(f"- **ROI anual simple:** {roi_anual:.1%}" if roi_anual is not None else "- **ROI anual simple:** no disponible")
    with c2:
        st.markdown("#### Punto de equilibrio")
        if punto_equilibrio is not None:
            st.write(f"Ventas aproximadas para cubrir gastos operativos: **{cop(punto_equilibrio)}** por período.")
            st.write(f"Ventas actuales: **{cop(ventas)}**.")
            st.write("Las ventas están por encima de ese umbral aproximado." if ventas >= punto_equilibrio else "Las ventas están por debajo de ese umbral aproximado.")
        else:
            st.write("No se pudo calcular con la estructura de costos actual.")
    st.download_button(
        "Descargar resumen CSV",
        data=summary.to_csv(index=False).encode("utf-8-sig"),
        file_name="reporte_roelstar.csv",
        mime="text/csv",
        type="primary",
    )

st.markdown("---")
st.markdown('<div class="small-note">ROELSTAR TRADING · Herramienta de análisis preliminar. Los resultados dependen de la calidad de los datos y no constituyen asesoría financiera, tributaria ni contable.</div>', unsafe_allow_html=True)
