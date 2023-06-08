import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub

def get_pdf_text(pdf_docs):
    # Obtiene el texto de un archivo PDF
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    # Divide el texto en fragmentos
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    # Obtiene el vector store de los fragmentos de texto
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    # Obtiene la cadena de conversación
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def main():
    load_dotenv()
    st.set_page_config(page_title="ChatPDF", page_icon=":speech_balloon:")
    st.write(css, unsafe_allow_html=True)  # Aplicar el estilo personalizado

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("ChatPDF :speech_balloon:")

    user_question = st.text_input("Haz una pregunta sobre tus documentos:", value="", key="user_input")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Tus documentos")
        pdf_docs = st.file_uploader(
            "Sube tus PDFs aquí y haz clic en 'Procesar'", accept_multiple_files=True)
        if st.button("Procesar"):
            with st.spinner("Procesando"):
                # obtener el texto de los PDFs
                raw_text = get_pdf_text(pdf_docs)

                # obtener los fragmentos de texto
                text_chunks = get_text_chunks(raw_text)

                # crear el vector store
                vectorstore = get_vectorstore(text_chunks)

                # crear la cadena de conversación
                st.session_state.conversation = get_conversation_chain(vectorstore)


def handle_userinput(user_question):
    # Maneja la entrada del usuario y genera una respuesta
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

    st.session_state.user_input = ""


if __name__ == '__main__':
    main()
