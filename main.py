# 


import os
import shutil
import streamlit as st
from streamlit_chat import message
from llm import Llm
from constants import UPLOADS_PATH


class Chat:
    st.set_page_config(page_title="Chat with your documents")
    st.header("Chat with your documents")

    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state["messages"] = []
        if "assistant" not in st.session_state:
            st.session_state["assistant"] = Llm()

        st.session_state["ingestion_spinner"] = st.empty()
    
    def window(self):
        self.display_load_document()
        self.display_messages()
        st.text_input("Message", key="user_input", on_change=self.process_input)

    def display_load_document(self):
        st.subheader("Upload a document")
        st.file_uploader(
            "Upload document",
            type=["pdf", "md", "docx"],
            key="file_uploader",
            on_change=self.read_and_save_file,
            label_visibility="collapsed",
            accept_multiple_files=True,
        )

    def display_messages(self):
        st.subheader("Chat")
        for i, (msg, is_user) in enumerate(st.session_state["messages"]):
            message(msg, is_user=is_user, key=str(i))
        st.session_state["thinking_spinner"] = st.empty()


    def process_input(self):
        if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
            user_text = st.session_state["user_input"].strip()
            with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
                agent_text = st.session_state["assistant"].ask(user_text)

            st.session_state["messages"].append((user_text, True))
            st.session_state["messages"].append((agent_text, False))


    def read_and_save_file(self):
        st.session_state["messages"] = []
        st.session_state["user_input"] = ""

        if os.path.exists("uploads"):
            shutil.rmtree("uploads")
            os.makedirs("uploads")
        else:
            os.makedirs("uploads")

        for file in st.session_state["file_uploader"]:
            file_contents = file.read()
            with open(os.path.join("uploads", file.name), "wb") as f:
                f.write(file_contents)

            with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}"):
                st.session_state["assistant"].get_chat_chain(UPLOADS_PATH + file.name)



if __name__ == "__main__":
    interface = Chat()
    interface.window()