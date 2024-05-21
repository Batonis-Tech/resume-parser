# import json
# import os
#
# import openai
# import streamlit as st
#
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
#
# from app.settings import settings
#
# os.environ['OPENAI_API_KEY'] = settings.OPENAI_API_KEY
#
#
# def load_document(file):
#     from langchain.document_loaders import UnstructuredFileLoader
#     loader = UnstructuredFileLoader(file)
#     data = loader.load()
#     return data
#
#
# def chunk_data(data, chunk_size=256, chunk_overlap=20):
#     from langchain.text_splitter import RecursiveCharacterTextSplitter
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#     chunks = text_splitter.split_documents(data)
#     return chunks
#
#
# def create_embeddings(chunks):
#     embeddings = OpenAIEmbeddings()
#     vector_store = Chroma.from_documents(chunks, embeddings)
#     return vector_store
#
#
# def ask_and_get_answer(vector_store, query, k=1):
#     from langchain.chains import RetrievalQA
#     from langchain.chat_models import ChatOpenAI
#
#     llm = ChatOpenAI(model='gpt-4o', temperature=1)
#     retriever = vector_store.as_retriever(search_type='mmr', search_kwargs={'k': 5})
#     chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
#
#     answer = chain(query)
#     return answer['result']
#
#
# def start_over_with_new_document():
#     st.session_state.text_input = ''
#
#     del st.session_state.vs
#
#     st.info('Пожалуйста добавьте новое резюме для продолжения анализа')
#
#
# def get_prompt(file_data) -> str:
#     # prompt = (
#     #     f"Выдели из содержимого этого файла ,только следующую информацию: — фамилия (surname) — имя ("
#     #     f"name) — отчество (patronymic) — телефон (phone) — telegram (telegram) — email (email) — языки, в виде массива строк (languages). Оформи эти данные в JSON, "
#     #     f"где данные в скобках это ключи для JSON с, если каких-то значений не хватает, то заполни их null. следуй "
#     #     f"строго по шаблону. Содержимое файла: {data}"
#     # )
#
#     prompt = (
#         f"Выдели из содержимого этого файла, только следующую информацию: — фамилия (surname) — имя ("
#         f"name) — отчество (patronymic) — телефон (phone) — telegram (telegram) — email (email) — город проживания ("
#         f"city) — желаемая должность (desired_position) — зарплата (salary) — занятость (employment) — активно или нет"
#         f"ищет работу (actively_looking_for_job) — общий опыт (total_experience) — ключевые навыки (key_skills) — "
#         f"раздел обо мне (about_me) — языки, в виде массива строк (languages) — образование, в виде строки (education) "
#         f"— сертификаты, в виде массива строк (certificates) Далее опыт работы в компаниях (work_experience), "
#         f"но не более 10 шт: — наименование компании (company_name) — год начала (start_year) — год конец (end_year) — "
#         f"срок работы (duration) — должность (position) — описание (description). Оформи эти данные в JSON, "
#         f"где данные в скобках это ключи для JSON с, если каких-то значений не хватает, то заполни их null. следуй "
#         f"строго по шаблону. Содержимое файла: {file_data}"
#     )
#
#     return prompt
#
#
# def get_parsed_cv():
#     if hasattr(st.session_state, 'vs'):
#         del st.session_state.vs
#         st.session_state.text_input = ''
#
#     uploaded_file = st.file_uploader('Загрузите резюме для анализа:')
#
#     if uploaded_file:
#
#         with st.spinner('Обработка запроса...'):
#
#             if not os.path.exists('./docs/'):
#                 os.mkdir('./docs/')
#
#             all_chunks = []
#
#             print(all_chunks)
#
#             bytes_data = uploaded_file.read()
#             file_name = os.path.join('./docs/', uploaded_file.name)
#             with open(file_name, 'wb') as f:
#                 f.write(bytes_data)
#
#             data = load_document(file_name)
#
#             from openai import OpenAI
#             client = OpenAI(api_key=settings.OPENAI_API_KEY)
#
#             response = client.chat.completions.create(
#                 model='gpt-4o',
#                 messages=[
#                     {'role': 'system', 'content': get_prompt(data[0].page_content)}
#                 ]
#             )
#
#             answer = response.choices[0].message.content
#
#             clear_answer = build_dict_from_answer(answer=answer)
#             build_parsed_cv_in_text(clear_answer)
#
#             # data = json.loads(response_text)
#             #
#             # print(json.dumps(data, indent=4, ensure_ascii=False))
#             #
#             # st.text_area(json.dumps(data, indent=4, ensure_ascii=False))
#             # chunks = chunk_data(data, chunk_size=8192)
#             # all_chunks.extend(chunks)
#             #
#             # vector_store = create_embeddings(chunks)
#             #
#             # st.session_state.vs = vector_store
#             # st.success('Загружено и обработано успешно')
#             #
#             for file in os.listdir('./docs/'):
#                 os.remove(os.path.join('./docs/', file))
#
#             os.rmdir('./docs/')
#
#     # if uploaded_file and 'vs' in st.session_state:
#     #
#     #     if 'vs' in st.session_state:
#     #         vector_store = st.session_state.vs
#     #         answer = ask_and_get_answer(vector_store,
#     #                                     query=get_prompt(uploaded_file.name))
#     #
#     #         clear_answer = build_dict_from_answer(answer=answer)
#     #         build_parsed_cv_in_text(clear_answer)
#     #
#     #         st.session_state.text_input = answer
#     #
#     #     if st.session_state.text_input:
#     #         st.button('Добавить новое резюме', on_click=start_over_with_new_document, key='new_question_new_context')
#
#
# def build_dict_from_answer(answer: str) -> dict:
#     answer = answer.replace('```', '')
#     answer = answer.replace('json', '')
#
#     return json.loads(answer)
#
#
# def build_parsed_cv_in_text(answer: dict):
#     st.subheader('Ответ:')
#     st.json(answer)
#
