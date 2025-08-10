import streamlit as st
import pandas as pd
import os
import tempfile
from datetime import datetime

POINTS_FILE = "placar.csv"
HIST_FILE = "historico.csv"

# ---------- Funções de persistência ----------
def load_points(nomes):
    if os.path.exists(POINTS_FILE):
        df = pd.read_csv(POINTS_FILE)
        return {row["Nome"]: int(row["Pontos"]) for _, row in df.iterrows()}
    else:
        return {nome: 100 for nome in nomes}

def save_points(points):
    df = pd.DataFrame(list(points.items()), columns=["Nome", "Pontos"])
    tmp = tempfile.NamedTemporaryFile(delete=False, dir=".", suffix=".csv")
    tmp.close()
    df.to_csv(tmp.name, index=False)
    os.replace(tmp.name, POINTS_FILE)

def load_history():
    if os.path.exists(HIST_FILE):
        return pd.read_csv(HIST_FILE).to_dict("records")
    else:
        return []

def append_history(entry):
    df_new = pd.DataFrame([entry])
    if os.path.exists(HIST_FILE):
        df_old = pd.read_csv(HIST_FILE)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new
    tmp = tempfile.NamedTemporaryFile(delete=False, dir=".", suffix=".csv")
    tmp.close()
    df.to_csv(tmp.name, index=False)
    os.replace(tmp.name, HIST_FILE)

# ---------- Interface ----------
with st.container():
    st.title("Aura do 114")
    st.subheader("Contador de Aura do apartamento 114 A")
    st.write("Não nos responsabilizamos por fraudes no sistema de pontuação.")

with st.container():
    nomes = ["Madeira 🪵", "Alagoas 🏖️", "Wolverine ⚔️", "Dino 🦖", "Smoke 💨", "Joker 🤡"]

    # Carrega do CSV (ou inicializa)
    if "pontos" not in st.session_state:
        st.session_state.pontos = load_points(nomes)

    st.title("🎩 Placar de Pontos")

    for nome in nomes:
        col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1])
        
        col1.write(f"**{nome}** — {st.session_state.pontos[nome]} pontos")
        valor = col2.number_input("Valor", min_value=1, step=1, value=1, key=f"valor_{nome}")
        operacao = col3.selectbox("Ação", ["Somar", "Subtrair"], key=f"op_{nome}")
        
        if col4.button("Aplicar", key=f"aplicar_{nome}"):
            pontos = load_points(nomes)  # sempre lê do arquivo antes
            delta = valor if operacao == "Somar" else -valor
            pontos[nome] += delta
            save_points(pontos)
            st.session_state.pontos = pontos

            # Adiciona entrada automática no histórico
            append_history({
                "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Responsável": "Sistema",
                "Nome Alterado": nome,
                "Mudança": delta,
                "Justificativa": "(sem justificativa)"
            })

            st.rerun()

    # Ranking
    df = pd.DataFrame(list(st.session_state.pontos.items()), columns=["Nome", "Pontos"])
    df = df.sort_values(by="Pontos", ascending=False).reset_index(drop=True)
    df.index = df.index + 1
    st.subheader("📊 Ranking")
    st.table(df)

# ---------- Histórico ----------
st.subheader("📝 Histórico de Alterações")
if "historico" not in st.session_state:
    st.session_state.historico = load_history()

with st.container():
    with st.form("form_historico"):
        data = st.date_input("Data da alteração")
        nome_responsavel = st.text_input("Quem fez a alteração")
        descricao = st.text_area("Justificativa")
        
        submitted = st.form_submit_button("Registrar")
        if submitted:
            entry = {
                "Data": str(data),
                "Responsável": nome_responsavel,
                "Nome Alterado": "",
                "Mudança": 0,
                "Justificativa": descricao
            }
            append_history(entry)
            st.session_state.historico = load_history()
            st.success("Alteração registrada no histórico!")
            st.rerun()

    if st.session_state.historico:
        df_hist = pd.DataFrame(st.session_state.historico)
        st.table(df_hist)
st.subheader("⚙️ Administração")

col_a, col_b = st.columns(2)

# Botão para resetar placar
if col_a.button("🔄 Resetar Placar"):
    from pathlib import Path
    nomes = ["Madeira 🪵", "Alagoas 🏖️", "Wolverine ⚔️", "Dino 🦖", "Smoke 💨", "Joker 🤡"]
    pontos_iniciais = {nome: 100 for nome in nomes}
    save_points(pontos_iniciais)
    st.session_state.pontos = pontos_iniciais
    st.success("Placar resetado com sucesso!")
    st.rerun()

# Botão para apagar histórico
if col_b.button("🗑️ Apagar Histórico"):
    if os.path.exists(HIST_FILE):
        os.remove(HIST_FILE)
    st.session_state.historico = []
    st.success("Histórico apagado com sucesso!")
    st.rerun()


