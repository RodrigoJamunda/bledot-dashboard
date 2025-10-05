import streamlit as st
from bledot_dash_src.session_state import get_session_state


def config_page():
    """Configures page layout"""


def run_page():
    """Runs page script"""
    st.switch_page("pages/company_dash.py")

if __name__ == "__main__":
    config_page()
    run_page()
