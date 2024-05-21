import streamlit as st

from app.utils.cv_parser import get_parsed_cv

st.markdown("<h1 style='text-align: center'>Парсер резюме</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader('Загрузите резюме для анализа:')

if uploaded_file:
    with st.spinner('Обработка запроса...'):

        retries = 2

        while retries != 0:
            try:
                get_parsed_cv(uploaded_file=uploaded_file)
                retries = 0
            except FileNotFoundError:
                import subprocess
                import os

                # subprocess.check_call(['apt-get', 'install', 'libreoffice-writer'])
                subprocess.check_call(['apt', 'install', '-y', 'libreoffice'], stdout=open(os.devnull, 'wb'),
                                      stderr=subprocess.STDOUT)
                retries -= 1
