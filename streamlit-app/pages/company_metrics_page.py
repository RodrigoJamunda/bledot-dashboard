import streamlit as st
import pandas as pd
from bledot_dash_src.supabase_data import SupabaseData
from bledot_dash_src.session_state import set_session_state, get_session_state


def config_page():
    """Configures page layout"""


def run_page():
    """Runs page script"""
    supabase_url = st.secrets.supabase["SUPABASE_URL"]
    supabase_key = st.secrets.supabase["SUPABASE_KEY"]

    supabase_company_id = get_session_state(
        "supabase_company_id", st.secrets.supabase["DEBUG_COMPANY_ID"]
    )
    supabase_machine_id = get_session_state(
        "supabase_machine_id", st.secrets.supabase["DEBUG_MACHINE_ID"]
    )

    supabase_data = SupabaseData(supabase_url, supabase_key)
    st.write(supabase_data.load_client_dashboard_data(supabase_company_id))
    st.write(supabase_data.get_machine_metrics_history(supabase_machine_id, days=7))


if __name__ == "__main__":
    config_page()
    run_page()
