import streamlit as st

st.title("Aura")
pontos = st.number_input("Digite sua pontuação", min_value=0)
st.write(f"Sua pontuação é: {pontos}")
