import streamlit as st
import pandas as pd
from dashboard.api_client import api_get, api_post

st.set_page_config(
    page_title="Aurora TMS | Centro de Comando",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ Aurora TMS - Centro de Comando")
st.caption("Painel operacional com inteligência logística e execução automática.")

dashboard_data, dashboard_err = api_get("/relatorios/dashboard")
oraculo_data, oraculo_err = api_get("/oraculo/plano-tatico")

if dashboard_err:
    st.error(f"Falha ao carregar dashboard: {dashboard_err}")
else:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🚛 Caminhões disponíveis", dashboard_data.get("caminhoes_disponiveis", 0))
    c2.metric("🛣️ Viagens ativas", dashboard_data.get("viagens_ativas", 0))
    c3.metric("📦 Cargas no pátio", dashboard_data.get("cargas_patio", 0))
    c4.metric("✅ Cargas entregues", dashboard_data.get("cargas_entregues", 0))

st.divider()

st.subheader("📡 Oráculo Logístico")
if oraculo_err:
    st.error(f"Falha ao carregar plano tático: {oraculo_err}")
else:
    resumo = oraculo_data.get("resumo", {})
    col1, col2, col3 = st.columns(3)
    col1.metric("Rotas sugeridas", resumo.get("rotas_sugeridas", 0))
    col2.metric("Cargas alocadas", resumo.get("cargas_alocadas", 0))
    col3.metric("Aproveitamento global", f"{resumo.get('aproveitamento_global_pct', 0)}%")

    rotas = oraculo_data.get("rotas_sugeridas", [])
    if rotas:
        st.write("### Rotas sugeridas")
        for rota in rotas:
            with st.expander(f"{rota['caminhao']} → {rota['destino']} | {rota['classificacao_rota']}"):
                st.write(f"**Ocupação:** {rota['ocupacao_pct']}%")
                st.write(f"**Peso ocupado:** {rota['peso_ocupado_kg']} kg")
                st.write(f"**Peso livre:** {rota['peso_livre_kg']} kg")
                st.write(f"**Valor total:** R$ {rota['valor_total_mercadoria']}")
                st.write("**Cargas recomendadas:**")
                st.dataframe(pd.DataFrame(rota["cargas_recomendadas"]), use_container_width=True, hide_index=True)

st.divider()

st.subheader("⚙️ Execução Automática do Plano")
origem_padrao = st.text_input("Origem padrão", value="Pátio Central")
iniciar_viagens = st.checkbox("Iniciar viagens automaticamente", value=False)

if st.button("🚀 Executar Plano Automático", use_container_width=True):
    with st.spinner("Executando plano do Oráculo..."):
        resultado, erro = api_post(
            "/oraculo/executar-plano",
            {
                "origem_padrao": origem_padrao,
                "iniciar_viagens": iniciar_viagens,
            },
        )

    if erro:
        st.error(f"Falha na execução: {erro}")
    else:
        st.success("Plano executado com sucesso.")
        st.write(f"**Viagens criadas:** {resultado.get('total_viagens_criadas', 0)}")
        st.write(f"**Erros:** {resultado.get('total_erros', 0)}")

        viagens = resultado.get("viagens_criadas", [])
        if viagens:
            st.dataframe(pd.DataFrame(viagens), use_container_width=True, hide_index=True)

        erros = resultado.get("erros", [])
        if erros:
            st.warning("Algumas rotas falharam:")
            for erro_item in erros:
                st.write(f"- {erro_item}")