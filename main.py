import streamlit as st

from app.utils.cv_parser import get_parsed_cv
# from app.utils.download_required_packages import download_package

# download_package('libreoffice')
# download_package('libreoffice-writer')

st.markdown("<h1 style='text-align: center'>Парсер резюме</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader('Загрузите резюме для анализа:')

if uploaded_file:
    with st.spinner('Обработка запроса...'):
        get_parsed_cv(uploaded_file=uploaded_file)
