import streamlit as st
import pandas as pd
from bledot_dash_src.supabase_data import SupabaseData
from bledot_dash_src.session_state import set_session_state, get_session_state


def config_page():
    """Configures page layout"""


def run_page():
    """Runs page script"""
    debug_supabase_url = st.secrets.supabase["DEBUG_SUPABASE_URL"]
    debug_supabase_key = st.secrets.supabase["DEBUG_SUPABASE_KEY"]

    supabase_url = get_session_state("supabase_url", debug_supabase_url)
    supabase_key = get_session_state("supabase_key", debug_supabase_key)
    supabase_company_id = st.secrets.supabase["DEBUG_COMPANY_ID"]
    # supabase_machine_id = st.secrets.supabase["DEBUG_MACHINE_ID"]

    supabase_data = SupabaseData(supabase_url, supabase_key)
    st.write(supabase_data.load_client_dashboard_data(supabase_company_id))


if __name__ == "__main__":
    config_page()
    run_page()
