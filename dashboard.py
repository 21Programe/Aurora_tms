import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Aurora TMS | Painel Tático",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = "http://127.0.0.1:8000"

# ============================================================
# CSS CUSTOMIZADO - VISUAL TÁTICO / EXECUTIVO
# ============================================================
st.markdown("""
<style>
    html, body, [class*="css"] {
        background-color: #0b0f14;
        color: #e8edf2;
    }

    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        color: #00ff88;
        letter-spacing: 1px;
        margin-bottom: 0.2rem;
        text-shadow: 0 0 12px rgba(0,255,136,0.25);
    }

    .sub-title {
        text-align: center;
        font-size: 1rem;
        color: #9aa4af;
        margin-bottom: 0.6rem;
    }

    .verse-box {
        text-align: center;
        background: linear-gradient(90deg, rgba(0,255,136,0.08), rgba(0,200,255,0.06));
        border: 1px solid rgba(0,255,136,0.18);
        border-radius: 14px;
        padding: 14px 18px;
        color: #d9fbe8;
        margin-bottom: 1rem;
        font-size: 0.96rem;
    }

    .status-card {
        background: #111821;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 16px;
        margin-top: 8px;
        box-shadow: 0 0 18px rgba(0,0,0,0.25);
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.2rem;
    }

    .section-caption {
        font-size: 0.92rem;
        color: #9aa4af;
        margin-bottom: 0.9rem;
    }

    .footer-box {
        text-align: center;
        padding: 18px;
        border-radius: 14px;
        background: linear-gradient(90deg, rgba(255,255,255,0.03), rgba(0,255,136,0.04));
        border: 1px solid rgba(255,255,255,0.05);
        color: #a9b4be;
        margin-top: 18px;
    }

    .mini-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(0,255,136,0.08);
        border: 1px solid rgba(0,255,136,0.15);
        color: #9ef7c2;
        font-size: 0.85rem;
        margin: 4px;
    }

    div[data-testid="metric-container"] {
        background: #111821;
        border: 1px solid rgba(255,255,255,0.05);
        padding: 14px;
        border-radius: 16px;
        box-shadow: 0 0 14px rgba(0,0,0,0.18);
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# FUNÇÕES DE COMUNICAÇÃO COM A API
# ============================================================
@st.cache_data(ttl=5)
def fetch_dashboard():
    try:
        res = requests.get(f"{API_URL}/dashboard", timeout=4)
        return res.json() if res.status_code == 200 else {}
    except requests.RequestException:
        return None

@st.cache_data(ttl=5)
def fetch_frota():
    try:
        res = requests.get(f"{API_URL}/relatorios/frota/ocupacao", timeout=4)
        return res.json() if res.status_code == 200 else []
    except requests.RequestException:
        return []

@st.cache_data(ttl=5)
def fetch_alertas():
    try:
        res = requests.get(f"{API_URL}/cargas/alertas", timeout=4)
        return res.json() if res.status_code == 200 else []
    except requests.RequestException:
        return []

# NOVA FUNÇÃO: Chama a Inteligência Artificial
def fetch_oraculo():
    try:
        res = requests.get(f"{API_URL}/oraculo/plano-tatico", timeout=10)
        if res.status_code == 200:
            return res.json()
        else:
            return {"erro": res.json().get("detail", "Erro desconhecido")}
    except requests.RequestException:
        return {"erro": "Falha de conexão com o Oráculo"}
def executar_plano_automatico(origem_padrao: str = "Pátio Central", iniciar_viagens: bool = False):
    try:
        res = requests.post(
            f"{API_URL}/oraculo/executar-plano",
            json={
                "origem_padrao": origem_padrao,
                "iniciar_viagens": iniciar_viagens
            },
            timeout=10
        )
        return res.json(), res.status_code
    except requests.RequestException as e:
        return {"detail": str(e)}, 500
# ============================================================
# CABEÇALHO
# ============================================================
st.markdown("<div class='main-title'>AURORA TMS - CENTRO DE COMANDO</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Painel operacional logístico com leitura executiva, supervisão tática e inteligência visual</div>", unsafe_allow_html=True)

st.markdown("""
<div class='verse-box'>
    <strong>Salmo 23:1</strong> — “O Senhor é o meu pastor; nada me faltará.”
    <br>
    <span style="color:#a6b8c8;">
        Direção, ordem e provisão aplicadas à operação: visão clara, controle total e resposta rápida.
    </span>
</div>
""", unsafe_allow_html=True)

# ============================================================
# BARRA SUPERIOR DE CONTROLE
# ============================================================
top_col1, top_col2, top_col3 = st.columns([1.3, 1, 1])

with top_col1:
    st.markdown(
        f"<span class='mini-badge'>🕒 Última leitura: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</span>",
        unsafe_allow_html=True
    )

with top_col2:
    if st.button("🔄 Atualizar Painel", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

with top_col3:
    st.markdown(
        "<span class='mini-badge'>🛡️ Aurora TMS Core Online</span>",
        unsafe_allow_html=True
    )


st.subheader("⚙️ Execução Automática do Plano")
st.caption("Transforma a sugestão do Oráculo em viagens reais, com reserva automática de cargas.")

col_auto1, col_auto2 = st.columns([2, 1])

with col_auto1:
    origem_execucao = st.text_input("Origem padrão das viagens automáticas", value="Pátio Central")

with col_auto2:
    iniciar_auto = st.checkbox("Já iniciar viagens", value=False)

if st.button("🚀 Executar Plano Automático", use_container_width=True):
    with st.spinner("Executando plano do Oráculo..."):
        resultado_exec, status_exec = executar_plano_automatico(
            origem_padrao=origem_execucao,
            iniciar_viagens=iniciar_auto
        )

    if status_exec == 200:
        st.success("Plano executado com sucesso.")

        st.write(f"**Viagens criadas:** {resultado_exec.get('total_viagens_criadas', 0)}")
        st.write(f"**Erros:** {resultado_exec.get('total_erros', 0)}")

        viagens = resultado_exec.get("viagens_criadas", [])
        if viagens:
            df_viagens_exec = pd.DataFrame([
                {
                    "viagem_id": v["viagem_id"],
                    "codigo": v["codigo"],
                    "destino": v["destino"],
                    "status": v["status"],
                    "caminhao_id": v["caminhao_id"],
                    "motorista_id": v["motorista_id"],
                    "total_cargas": len(v.get("cargas_reservadas", [])),
                }
                for v in viagens
            ])
            st.dataframe(df_viagens_exec, use_container_width=True, hide_index=True)

        erros_exec = resultado_exec.get("erros", [])
        if erros_exec:
            st.warning("Algumas rotas não foram executadas:")
            for err in erros_exec:
                st.write(f"- {err}")

        st.cache_data.clear()
    else:
        st.error(resultado_exec.get("detail", "Falha ao executar plano automático."))



st.divider()

# ============================================================
# CARGA DOS DADOS
# ============================================================
dados_dash = fetch_dashboard()
dados_frota = fetch_frota()
dados_alertas = fetch_alertas()

# ============================================================
# ESTADO DE CONEXÃO
# ============================================================
if dados_dash is None:
    st.error("⚠️ FALHA DE CONEXÃO: a API FastAPI não está respondendo. Verifique se o Uvicorn está ativo em http://127.0.0.1:8000")
else:
    # ========================================================
    # MÉTRICAS PRINCIPAIS
    # ========================================================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🚛 Caminhões Disponíveis",
            value=f"{dados_dash.get('caminhoes_disponiveis', 0)} / {dados_dash.get('caminhoes_total', 0)}"
        )

    with col2:
        st.metric(
            label="🛣️ Viagens Ativas",
            value=dados_dash.get('viagens_ativas', 0)
        )

    with col3:
        st.metric(
            label="📦 Cargas no Pátio",
            value=dados_dash.get('cargas_patio', 0),
            delta="Atenção operacional",
            delta_color="inverse"
        )

    with col4:
        st.metric(
            label="✅ Cargas Entregues",
            value=dados_dash.get('cargas_entregues', 0),
            delta="Performance positiva",
            delta_color="normal"
        )

    st.write("")

    # ========================================================
    # PAINEL PRINCIPAL
    # ========================================================
    col_esquerda, col_direita = st.columns([2.2, 1])

    with col_esquerda:
        st.markdown("<div class='section-title'>📊 Nível de Ocupação da Frota</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='section-caption'>Análise de aproveitamento dos veículos. Ociosidade e sobrecarga drenam margem operacional.</div>",
            unsafe_allow_html=True
        )

        if dados_frota:
            df_frota = pd.DataFrame(dados_frota)

            if "ocupacao_pct" in df_frota.columns:
                df_frota["ocupacao_label"] = df_frota["ocupacao_pct"].map(lambda x: f"{x:.1f}%")

                fig = px.bar(
                    df_frota,
                    x="placa",
                    y="ocupacao_pct",
                    text="ocupacao_label",
                    color="ocupacao_pct",
                    color_continuous_scale=["#00ff88", "#ffee55", "#ff4d4d"],
                    labels={
                        "placa": "Veículo",
                        "ocupacao_pct": "Ocupação (%)"
                    },
                    range_y=[0, 110]
                )

                fig.update_traces(
                    textposition="outside",
                    marker_line_width=0
                )

                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#e8edf2",
                    xaxis_title="Frota",
                    yaxis_title="Percentual de ocupação",
                    coloraxis_showscale=False,
                    margin=dict(l=10, r=10, t=10, b=10)
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Os dados da frota foram recebidos, mas a coluna 'ocupacao_pct' não está disponível.")
        else:
            st.info("Nenhum dado de ocupação disponível no momento.")

    with col_direita:
        st.markdown("<div class='section-title'>🚨 Alertas de Prazo</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='section-caption'>Cargas com risco de rompimento de SLA nas próximas 24 horas.</div>",
            unsafe_allow_html=True
        )

        if dados_alertas:
            df_alertas = pd.DataFrame(dados_alertas)

            colunas_exibidas = [col for col in ["nf", "destino", "status"] if col in df_alertas.columns]

            if colunas_exibidas:
                st.dataframe(
                    df_alertas[colunas_exibidas],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning("Os alertas foram carregados, mas as colunas esperadas não vieram da API.")
        else:
            st.success("Toda a operação está dentro do prazo. Nenhum alerta crítico detectado.")

    st.write("")

    # ========================================================
    # PAINEL TÁTICO SECUNDÁRIO
    # ========================================================
    st.markdown("<div class='section-title'>🧠 Leitura Tática da Operação</div>", unsafe_allow_html=True)
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)

    cam_total = dados_dash.get("caminhoes_total", 0)
    cam_disp = dados_dash.get("caminhoes_disponiveis", 0)
    viagens_ativas = dados_dash.get("viagens_ativas", 0)
    cargas_patio = dados_dash.get("cargas_patio", 0)
    cargas_entregues = dados_dash.get("cargas_entregues", 0)

    if cam_total > 0 and cam_disp == 0:
        st.warning("Toda a frota cadastrada está comprometida. Capacidade de resposta imediata reduzida.")
    elif cam_total > 0 and cam_disp < cam_total:
        st.info("Parte da frota está em uso. Operação em regime de consumo logístico moderado.")
    else:
        st.success("Frota com boa folga operacional e prontidão elevada.")

    if viagens_ativas > 0:
        st.write(f"• Há **{viagens_ativas} viagem(ns) ativa(s)** em monitoramento.")
    else:
        st.write("• Nenhuma viagem ativa neste momento.")

    if cargas_patio > 0:
        st.write(f"• Existem **{cargas_patio} carga(s) em pátio**, exigindo atenção para evitar custo parado.")
    else:
        st.write("• Não há acúmulo relevante de cargas em pátio.")

    st.write(f"• Total de cargas concluídas com sucesso: **{cargas_entregues}**.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # ========================================================
    # NOVO: SESSÃO DO ORÁCULO IA
    # ========================================================
    st.markdown("<div class='section-title'>🧭 Motor de Inteligência: Geração de Rotas</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-caption'>Cálculo de Bin Packing para alocação perfeita de cargas nos caminhões vazios.</div>", unsafe_allow_html=True)
    
    if st.button("🚀 Executar Leitura Tática (Gerar Rotas)", type="primary"):
        with st.spinner("O Oráculo está cruzando o pátio com a capacidade da frota..."):
            resultado_ia = fetch_oraculo()

            if "erro" in resultado_ia:
                st.warning(f"Aviso do Sistema: {resultado_ia['erro']}")
            else:
                st.success(f"Plano Gerado com Sucesso! Aproveitamento Global: {resultado_ia['resumo']['aproveitamento_global_pct']}%")
                
                # Renderiza cada rota sugerida em caixas expansíveis
                for rota in resultado_ia['rotas_sugeridas']:
                    with st.expander(f"🚛 Caminhão {rota['caminhao']} ({rota['tipo']}) ➔ Destino: {rota['destino']} | Ocupação: {rota['ocupacao_pct']}%"):
                        st.write(f"**Capacidade Total:** {rota['capacidade_total_kg']} kg | **Peso Carregado:** {rota['peso_ocupado_kg']} kg | **Espaço Livre:** {rota['peso_livre_kg']} kg")
                        
                        # Tabela com as NFs
                        df_cargas = pd.DataFrame(rota['cargas_recomendadas'])
                        st.dataframe(df_cargas[['nf', 'descricao', 'peso_kg']], use_container_width=True, hide_index=True)

    st.divider()

    # ========================================================
    # RODAPÉ
    # ========================================================
    st.markdown("""
    <div class='footer-box'>
        <strong>Aurora TMS</strong> • Painel de Supervisão Logística
        <br><br>
        <span style="color:#c7d2db;">
            “Ainda que eu ande pelo vale da sombra da morte, não temerei mal algum, porque tu estás comigo.”
        </span>
        <br>
        <span style="font-size: 0.88rem; color:#91a0ac;">
            Salmo 23:4 aplicado como princípio de resiliência operacional, direção e estabilidade sob pressão.
        </span>
        <br><br>
        <span style="font-size: 0.84rem; color:#7f8b96;">
            Sistema de otimização logística desenvolvido por 21Programe • Acesso Nível: Root
        </span>
    </div>
    """, unsafe_allow_html=True)