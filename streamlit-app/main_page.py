import streamlit as st
from src.bledot_dash_src.session_state import init_session_state


def config_page():
    """Configures page layout"""


def run_page():
    """Runs page script"""
    init_session_state("database_url", st.secrets.supabase["SUPABASE_URL"])
    init_session_state("database_key", st.secrets.supabase["SUPABASE_KEY"])
    st.switch_page("pages/company_dash.py")


if __name__ == "__main__":
    config_page()
    run_page()
