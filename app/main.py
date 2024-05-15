import streamlit as st


st.markdown("<h1 style='text-align: center'>Парсер резюме</h1>",unsafe_allow_html=True)

cv = st.file_uploader(label='Загрузите резюме')


def parse_cv():
    st.subheader("Опыт:")
    st.text("""Какой-то опыт""")
    st.subheader("Сам файл")
    st.text(cv)


parse_cv()
