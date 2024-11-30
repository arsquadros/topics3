import streamlit as st

from langchain_community.document_loaders import PyPDFLoader

import requests
import os

base_path = os.path.dirname(os.path.abspath(__file__))

grok_key = os.getenv("GROK_API_KEY", "")

if grok_key == "":
    full_message = "API key not found. Please add it to the environment keys as GROK_API_KEY. You can do this by running in windows:\
        \n\n```cmd \nsetx GROK_API_KEY \"your_api_key_here\" \n```\n\nor in linux:\n\n```bash \nexport GROK_API_KEY=\"your_api_key_here\" \n```"
    raise ValueError(full_message)


def ask_question(context, question):
    prompt = f"Responda à pergunta descrita após a tag **Pergunta:** com base no texto dentro da tag **Contexto:**\n\n**Contexto:** {context}\n\n**Pergunta:** {question}\n\n**Resposta:**"
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {grok_key}"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [{
                "role": "system",
                "content": "Assistente conversacional para responder perguntas baseadas em um contexto. É sempre educado e gentil, e finaliza todos os textos pedindo que envie uma nova pergunta no mesmo campo."
            },
            {
                "role": "user",
                "content": prompt
            }]
        }
    )
    print(response.json())
    return response.json()["choices"][0]["message"]["content"]

def pdf_to_txt(file):
    with open("temp.pdf", "wb") as f2:
        f2.write(file.read())
    
    loader = PyPDFLoader("temp.pdf")
    docs = loader.load()

    os.remove("temp.pdf")

    return "\n".join([doc.page_content for doc in docs])

# Definindo o título da aplicação

st.title("Perguntas e Respostas")

# Definindo o contexto a partir do envio de um arquivo PDF

uploaded_file = st.file_uploader("Escolha um arquivo PDF para servir de contexto para a LLM. Tenha em mente que arquivos muito extensos não serão aceitos.", type="pdf")

if uploaded_file is not None:
    with st.spinner("Por favor, aguarde enquanto o texto é extraído..."):
        text = pdf_to_txt(uploaded_file)

    if text:
        question = st.text_input("Possui alguma pergunta em mente?")

        if st.button("Enviar"):
            with st.spinner("Por favor, aguarde enquanto a resposta é gerada..."):
                answer = ask_question(text, question)
            st.write(answer)
