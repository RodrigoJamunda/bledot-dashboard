import streamlit as st
from src.bledot_dash_src.session_state import init_session_state
from auth.auth_handler import authenticate, logout  # imports authentication functions

def config_page():
    """Configures page layout"""
    sidebar_state = "expanded" if st.session_state.get("authenticated", False) else "collapsed"
    st.set_page_config(
        page_title="Homepage",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state=sidebar_state,
    )

def run_page():
    """Runs page script"""
    # Authentication: if not authenticated, show login screen
    if not authenticate():
        st.stop()
    # Logout button
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Logout", width="stretch"):
            logout()
            st.experimental_rerun()
    # Initialize session variables
    init_session_state("database_url", st.secrets.supabase["SUPABASE_URL"])
    init_session_state("database_key", st.secrets.supabase["SUPABASE_KEY"])
    # Redirect to main page
    st.switch_page("pages/company_dash.py")

if __name__ == "__main__":
    config_page()
    run_page()