import streamlit as st
import os
import logging
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(
    logging.WARNING
)


st.set_page_config(
    page_title="Admin",
    page_icon=os.path.join("images", "favicon.ico"),
    layout="wide",
    menu_items=None,
)

mod_page_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(mod_page_style, unsafe_allow_html=True)


col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image(os.path.join("images", "logo.png"))

st.write("# LinkedIn TPS AI Risk Finder")

st.write(
    """
         * If you want to ingest data (pdf, websites, etc.), then use the `Ingest Data` tab
         * If you want to explore how your data was chunked, check the `Explore Data` tab
         * If you want to adapt the underlying prompts, logging settings and others, use the `Configuration` tab
         """
)
