import json
import os

import streamlit as st

from app.settings import settings

from pypandoc.pandoc_download import download_pandoc

download_pandoc()

os.environ['OPENAI_API_KEY'] = settings.OPENAI_API_KEY


def load_document(file):
    from langchain.document_loaders import UnstructuredFileLoader
    loader = UnstructuredFileLoader(file)
    data = loader.load()
    return data


def get_prompt(file_data) -> str:
    prompt = (
        f"Выдели из содержимого этого файла, только следующую информацию: — фамилия (surname) — имя ("
        f"name) — отчество (patronymic) — телефон (phone) — telegram (telegram) — email (email) — город проживания ("
        f"city) — желаемая должность (desired_position) — зарплата (salary) — занятость (employment) — активно или нет"
        f"ищет работу (actively_looking_for_job) — общий опыт (total_experience) — ключевые навыки, в виде массива строк (key_skills) — "
        f"раздел обо мне (about_me) — языки, в виде массива строк (languages) — образование, в виде строки (education) "
        f"— сертификаты, в виде массива строк (certificates) Далее опыт работы в компаниях (work_experience), "
        f"но не более 10 шт: — наименование компании (company_name) — год начала (start_year) — год конец (end_year) — "
        f"срок работы (duration) — должность (position) — описание (description). Оформи эти данные в JSON, "
        f"где данные в скобках это ключи для JSON с, если каких-то значений не хватает, то заполни их null. следуй "
        f"строго по шаблону. Содержимое файла: {file_data}"
    )

    return prompt


def get_parsed_cv(uploaded_file):
    if not os.path.exists('./docs/'):
        os.mkdir('./docs/')

    bytes_data = uploaded_file.read()
    file_name = os.path.join('./docs/', uploaded_file.name)
    with open(file_name, 'wb') as f:
        f.write(bytes_data)

    data = load_document(file_name)

    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': get_prompt(data[0].page_content)}
        ]
    )

    answer = response.choices[0].message.content

    clear_answer = build_dict_from_answer(answer=answer)
    build_parsed_cv_in_text(clear_answer)

    for file in os.listdir('./docs/'):
        os.remove(os.path.join('./docs/', file))

    os.rmdir('./docs/')


def build_dict_from_answer(answer: str) -> dict:
    answer = answer.replace('```', '')
    answer = answer.replace('json', '')

    return json.loads(answer)


def build_parsed_cv_in_text(answer: dict):
    st.subheader('Ответ:')
    st.json(answer)
