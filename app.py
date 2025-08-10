import streamlit as st
import pandas as pd

with st.container():
    st.title("Aura do 114")
    st.subheader(f"Contador de Aura do apartamento 114 A")
    st.write("Não nos responsabilizamos por fraudes no sistema de pontuação.")
with st.container():

    # Lista de pessoas e pontos iniciais
    nomes = ["Madeira 🪵", "Alagoas 🏖️", "Wolverine ⚔️", "Dino 🦖" , "Smoke 💨" , "Joker 🤡"]

    # Inicializa pontos no session_state
    if "pontos" not in st.session_state:
        st.session_state.pontos = {nome: 100 for nome in nomes}

    st.title("🎩 Placar de Pontos")

    for nome in nomes:
        col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1])
        
        col1.write(f"**{nome}** — {st.session_state.pontos[nome]} pontos")
        
        # Valor que o usuário quer alterar
        valor = col2.number_input(f"Valor ", min_value=1, step=1, value=1, key=f"valor_{nome}")
        
        # Escolha de operação
        operacao = col3.selectbox(f"Ação ", ["Somar", "Subtrair"], key=f"op_{nome}")
        
        # Botão para aplicar
        if col4.button("Aplicar", key=f"aplicar_{nome}"):
            if operacao == "Somar":
                st.session_state.pontos[nome] += valor
            else:
                st.session_state.pontos[nome] -= valor

    # Criar DataFrame ordenado por pontuação
    df = pd.DataFrame(list(st.session_state.pontos.items()), columns=["Nome", "Pontos"])
    df = df.sort_values(by="Pontos", ascending=False).reset_index(drop=True)
    df.index = df.index + 1  # Começa do 1

    st.subheader("📊 Ranking")
    st.table(df)
st.subheader("📝 Histórico de Alterações")
with st.container():
    # Inicializa histórico no session_state
    if "historico" not in st.session_state:
        st.session_state.historico = []

    # Campos para entrada
    with st.form("form_historico"):
        data = st.date_input("Data da alteração")
        nome_responsavel = st.text_input("Quem fez a alteração")
        descricao = st.text_area("Justificativa")
        
        submitted = st.form_submit_button("Registrar")
        if submitted:
            st.session_state.historico.append({
                "Data": str(data),
                "Responsável": nome_responsavel,
                "Justificativa": descricao
            })
            st.success("Alteração registrada no histórico!")

    # Exibe histórico se houver
    if st.session_state.historico:
        df_hist = pd.DataFrame(st.session_state.historico)
        st.table(df_hist)
