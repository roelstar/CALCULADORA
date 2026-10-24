import streamlit as st
from pathlib import Path


st.set_page_config(
    page_title="ROELSTAR TRADING | Evaluador de Rentabilidad",
    page_icon="⭐",
    layout="wide",
)

# Identidad visual ROELSTAR: el logo debe estar en la misma carpeta que este archivo.
BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "roelstar_logo.png"

st.markdown("""
<style>
    .stApp { background: #f5f7fb; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .roelstar-header {
        background: linear-gradient(120deg, #111318 0%, #25252a 70%, #b51220 100%);
        border-bottom: 4px solid #ed2939; border-radius: 16px;
        padding: 18px 22px; margin-bottom: 18px; color: white;
    }
    .roelstar-header h1 { color: white; margin: 0; font-size: 1.8rem; }
    .roelstar-header p { color: #e5e7eb; margin: 6px 0 0 0; }
    div[data-testid="stMetric"] { background: white; padding: 14px; border-radius: 12px; border: 1px solid #e5e7eb; }
    div[data-testid="stExpander"] { background: white; border-radius: 10px; }
    .stButton>button { background: #c7192d; color: white; border: 0; border-radius: 8px; }
    .stButton>button:hover { background: #a91425; color: white; border: 0; }
</style>
""", unsafe_allow_html=True)

logo_col, title_col = st.columns([1, 3])
with logo_col:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=250)
    else:
        st.markdown("### ⭐ ROELSTAR TRADING")
with title_col:
    st.markdown("""
    <div class="roelstar-header">
      <h1>Evaluador de Rentabilidad e Inversiones</h1>
      <p>Analiza un negocio antes de invertir · Valores en pesos colombianos (COP)</p>
    </div>
    """, unsafe_allow_html=True)

with st.expander("ℹ️ Cómo usar esta calculadora", expanded=False):
    st.markdown("""
    1. Ingresa cifras del mismo período, preferiblemente un mes.
    2. Registra ventas **sin IVA** y costos de los productos/servicios vendidos.
    3. No cuentes dos veces la nómina: los técnicos pueden ir como costo directo
       o como gasto operativo, según tu método, pero no en ambos.
    4. Para evaluar una inversión, registra el capital total que tendrás comprometido.
    5. Los resultados son una estimación gerencial; valida impuestos y criterios contables
       con tu contador.
    """)

st.subheader("1. Datos del negocio")
nombre = st.text_input("Nombre del negocio", value="Mi negocio")
periodo = st.selectbox("Período de los datos", ["Mensual", "Anual"])
factor_anual = 12 if periodo == "Mensual" else 1

def dinero(label, key, help_text=None):
    return st.number_input(
        label,
        min_value=0.0,
        value=0.0,
        step=100000.0,
        format="%.0f",
        key=key,
        help=help_text,
    )

st.subheader("2. Ingresos")
col1, col2 = st.columns(2)
with col1:
    ingresos_servicios = dinero("Mano de obra / servicios ($)", "ing_serv")
    ingresos_repuestos = dinero("Venta de repuestos/productos ($)", "ing_rep")
with col2:
    otros_ingresos = dinero("Otros ingresos operativos ($)", "otros_ing")
    descuentos_devoluciones = dinero(
        "Descuentos y devoluciones ($)", "descuentos",
        "Introduce el total de descuentos/devoluciones no descontado ya de las ventas."
    )

ventas_brutas = ingresos_servicios + ingresos_repuestos + otros_ingresos
ventas = max(0.0, ventas_brutas - descuentos_devoluciones)

st.subheader("3. Costos directos")
st.caption("Costos atribuibles a los productos vendidos o servicios realizados en este período.")
col1, col2 = st.columns(2)
with col1:
    costo_productos = dinero(
        "Costo de repuestos/productos vendidos ($)", "costo_prod",
        "Usa el costo de lo vendido, no el total de compras para inventario."
    )
    costo_tecnicos = dinero(
        "Costo directo de técnicos / prestación ($)", "costo_tec",
        "Incluye salarios y cargas asociadas si los clasificas como costo directo."
    )
with col2:
    insumos_terceros = dinero("Insumos, terceros y otros costos directos ($)", "insumos")
    otros_costos_directos = dinero("Otros costos directos ($)", "otros_costos")

costos_directos = costo_productos + costo_tecnicos + insumos_terceros + otros_costos_directos
utilidad_bruta = ventas - costos_directos
margen_bruto = utilidad_bruta / ventas if ventas else 0.0

st.subheader("4. Gastos operativos del período")
st.caption("Gastos necesarios para funcionar que no hayas incluido en costos directos.")
col1, col2 = st.columns(2)
with col1:
    nomina_admin = dinero("Administración / recepción / asesoría ($)", "nomina_admin")
    arriendo = dinero("Arriendo y administración del local ($)", "arriendo")
    servicios = dinero("Servicios públicos, internet y teléfono ($)", "servicios")
    mercadeo = dinero("Mercadeo, publicidad y ventas ($)", "mercadeo")
with col2:
    herramientas = dinero("Herramientas, mantenimiento y depreciación ($)", "herramientas")
    transporte = dinero("Transporte, software y papelería ($)", "transporte")
    seguros_licencias = dinero("Seguros, licencias y otros gastos ($)", "seguros")
    otros_gastos = dinero("Otros gastos operativos ($)", "otros_gastos")

gastos_operativos = nomina_admin + arriendo + servicios + mercadeo + herramientas + transporte + seguros_licencias + otros_gastos
utilidad_operacional = utilidad_bruta - gastos_operativos
margen_operacional = utilidad_operacional / ventas if ventas else 0.0

st.subheader("5. Gastos financieros e impuestos")
col1, col2 = st.columns(2)
with col1:
    intereses = dinero("Intereses y gastos financieros ($)", "intereses")
    otros_resultados = st.number_input(
        "Otros ingresos (+) o gastos (-) no operativos ($)",
        value=0.0, step=100000.0, format="%.0f",
        help="Escribe un valor positivo para ingresos netos o negativo para gastos netos."
    )
with col2:
    impuestos = dinero("Impuestos estimados del período ($)", "impuestos")
    st.info("El impuesto real depende del régimen tributario y de la situación de la empresa.")

utilidad_antes_impuestos = utilidad_operacional - intereses + otros_resultados
utilidad_neta = utilidad_antes_impuestos - impuestos
margen_neto = utilidad_neta / ventas if ventas else 0.0

st.subheader("6. Inversión y evaluación")
col1, col2 = st.columns(2)
with col1:
    capital_invertido = dinero(
        "Capital total que invertirías ($)", "capital",
        "Incluye compra del negocio, adecuaciones, equipos e inventario inicial, según aplique."
    )
    retorno_objetivo = st.number_input(
        "Rentabilidad anual objetivo (%)", min_value=0.0, value=20.0, step=1.0,
        help="Tu mínimo deseado para comparar oportunidades; no es una garantía."
    )
with col2:
    inversion_adicional = dinero(
        "Inversión adicional prevista ($)", "inversion_adicional",
        "Capital de trabajo o gastos iniciales adicionales que no hayas incluido arriba."
    )
    meses_proyeccion = st.number_input(
        "Meses para recuperar inversión (horizonte)", min_value=1, max_value=120,
        value=36, step=1
    )

capital_total = capital_invertido + inversion_adicional
utilidad_mensual_equivalente = utilidad_neta if periodo == "Mensual" else utilidad_neta / 12
utilidad_anual_equivalente = utilidad_mensual_equivalente * 12
roi_anual = (utilidad_anual_equivalente / capital_total) if capital_total > 0 else None
recuperacion_meses = (capital_total / utilidad_mensual_equivalente) if capital_total > 0 and utilidad_mensual_equivalente > 0 else None
utilidad_anual_objetivo = capital_total * retorno_objetivo / 100
utilidad_mensual_objetivo = utilidad_anual_objetivo / 12

# Punto de equilibrio aproximado: tratar costo de productos + insumos/terceros como variables.
costos_variables_aprox = costo_productos + insumos_terceros + otros_costos_directos
tasa_contribucion = (ventas - costos_variables_aprox) / ventas if ventas > 0 else 0.0
punto_equilibrio = gastos_operativos / tasa_contribucion if tasa_contribucion > 0 else None

st.divider()
st.header("⭐ ROELSTAR | Resultados del análisis")

if ventas <= 0:
    st.warning("Ingresa ventas mayores que cero para calcular los márgenes.")
else:
    m1, m2 = st.columns(2)
    m1.metric("Ventas netas", f"${ventas:,.0f}")
    m2.metric("Utilidad bruta", f"${utilidad_bruta:,.0f}", f"Margen bruto: {margen_bruto:.1%}")

    m3, m4 = st.columns(2)
    m3.metric("Utilidad operacional", f"${utilidad_operacional:,.0f}", f"Margen operacional: {margen_operacional:.1%}")
    m4.metric("Utilidad neta estimada", f"${utilidad_neta:,.0f}", f"Margen neto: {margen_neto:.1%}")

    st.subheader("Lectura rápida")
    if utilidad_neta < 0:
        st.error("El negocio presenta pérdida neta con los datos ingresados. Revisa costos, gastos, precio y volumen de ventas.")
    elif utilidad_neta == 0:
        st.warning("El negocio queda en equilibrio neto: no muestra utilidad después de los conceptos registrados.")
    else:
        st.success(f"El negocio muestra una utilidad neta estimada de ${utilidad_neta:,.0f} por período {periodo.lower()}.")

if capital_total > 0:
    st.subheader("Retorno sobre la inversión")
    a, b = st.columns(2)
    a.metric("Capital total considerado", f"${capital_total:,.0f}")
    if roi_anual is not None:
        b.metric("ROI anual simple estimado", f"{roi_anual:.1%}")
    else:
        b.metric("ROI anual simple estimado", "No disponible")

    if recuperacion_meses is not None:
        st.metric("Tiempo simple de recuperación", f"{recuperacion_meses:.1f} meses")
    else:
        st.metric("Tiempo simple de recuperación", "No recuperable con utilidad positiva actual")

    st.caption("ROI simple = utilidad neta anualizada ÷ capital total. No incluye cambios futuros, deuda, valor de reventa ni el valor del dinero en el tiempo.")

    if roi_anual is not None:
        if roi_anual >= retorno_objetivo / 100 and utilidad_neta > 0:
            st.success(f"El ROI simple supera tu objetivo del {retorno_objetivo:.1f}% anual. Esto no basta por sí solo para decidir invertir: valida riesgos, estabilidad de ventas y flujo de caja.")
        else:
            st.warning(f"El ROI simple no alcanza tu objetivo del {retorno_objetivo:.1f}% anual, o la utilidad actual no es positiva. Revisa los supuestos antes de invertir.")

if punto_equilibrio is not None:
    st.subheader("Punto de equilibrio aproximado")
    st.metric("Ventas necesarias para cubrir gastos operativos", f"${punto_equilibrio:,.0f} por período")
    if ventas >= punto_equilibrio:
        st.caption("Con la aproximación actual, las ventas están por encima del punto de equilibrio operativo estimado.")
    else:
        st.caption("Con la aproximación actual, las ventas están por debajo del punto de equilibrio operativo estimado.")
    st.caption("Estimación simplificada. Clasifica correctamente costos fijos y variables para obtener un resultado fiable.")
else:
    st.info("No se pudo estimar el punto de equilibrio: revisa las ventas y los costos variables aproximados.")

st.subheader("Meta de utilidad")
if capital_total > 0:
    st.write(f"Para lograr un retorno objetivo del **{retorno_objetivo:.1f}% anual**, necesitarías generar aproximadamente **${utilidad_mensual_objetivo:,.0f} de utilidad neta mensual**.")
    st.write(f"Utilidad neta mensual equivalente actual: **${utilidad_mensual_equivalente:,.0f}**.")
else:
    st.write("Ingresa el capital de inversión para calcular la utilidad mensual objetivo.")

st.divider()
st.caption(
    "ROELSTAR TRADING · Aviso: herramienta de análisis preliminar, no asesoría financiera, tributaria ni contable. "
    "La utilidad contable no equivale necesariamente al efectivo disponible. Antes de invertir, "
    "revisa estados financieros, deudas, inventario, impuestos, capital de trabajo y flujo de caja."
)
