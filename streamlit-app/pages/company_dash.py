import streamlit as st
from src.bledot_dash_src.supabase_data import SupabaseData
from src.bledot_dash_src.session_state import (
    init_session_state,
    set_session_state,
    get_session_state,
    check_session_state,
)
from src.bledot_dash_src.dashes.overview import run_overview_dash
from src.bledot_dash_src.dashes.processing import run_processing_dash
from src.bledot_dash_src.dashes.hardware import run_hardware_dash
from src.bledot_dash_src.dashes.software import run_software_dash

def make_sidebar(tab_options: list[str]) -> str:
    init_session_state("selected_tab", tab_options[0])

    with st.sidebar:
        st.title("Bledot")
        st.divider()

        for tab_option in tab_options:
            if st.button(tab_option, width='stretch'):
                set_session_state("selected_tab", tab_option)

        st.divider()
        if st.session_state.get("role") == "admin":
            if st.button("Área do administrador", width='stretch'):
                st.switch_page("pages/admin_dash.py")
        
        if st.button("Logout", width='stretch'):
            from auth.auth_handler import logout
            logout()

    return get_session_state("selected_tab")

def config_page():
    """Configures page layout"""
    st.set_page_config(layout="wide", page_title="Dashboard - Bledot")

def run_page():
    """Runs page script"""

    # Verify if user is authenticated and company_id is set
    if not check_session_state("authenticated") or not check_session_state("company_id"):
        st.switch_page("main_page.py")

    with st.spinner("Carregando dados..."):
        company_id = get_session_state("company_id")

        # Load data only if not already loaded or if company_id has changed
        if "company_data" not in st.session_state or st.session_state.get("loaded_company_id") != company_id:
            # Load and return Supabase Database Client
            supabase_data = SupabaseData()
            company_data = supabase_data.load_client_dashboard_data(company_id)
            
            # Store data in session
            set_session_state("company_data", company_data)
            set_session_state("loaded_company_id", company_id)
        else:
            company_data = get_session_state("company_data")

    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    with col1:
        if not company_data["machines"].empty:
            
            # Verify if there is a 'label_maquina' or similar column
            machine_columns = company_data["machines"].columns
            machine_label_col = None
            
            for col in ['label_maquina', 'nome_maquina', 'machine_name', 'name', 'id']:
                if col in machine_columns:
                    machine_label_col = col
                    break
            
            if machine_label_col:
                target_machine_label = st.selectbox(
                    "Selecione uma máquina:",
                    company_data["machines"][machine_label_col].unique()
                )
            else:
                st.warning("Nenhuma coluna de identificação de máquina encontrada")
                target_machine_label = None
        else:
            st.info("Nenhuma máquina encontrada para esta empresa")
            target_machine_label = None
            
    with col2:
        if st.button("Ver mais informações", type="primary") and target_machine_label:
            set_session_state("target_machine", target_machine_label)
            st.switch_page("pages/machine_dash.py")

    summary_data = company_data["summary_stats"]
    issues = set()
    for issue_list in summary_data["machines_with_issues"].values():
        for issue in issue_list:
            issues.add(issue)

    set_session_state("issues", issues)

    tab_options = ["Visão Geral", "Processamento", "Hardware", "Software"]

    tab_option = make_sidebar(tab_options)

    if tab_option == tab_options[0]:
        run_overview_dash()
    elif tab_option == tab_options[1]:
        run_processing_dash()
    elif tab_option == tab_options[2]:
        run_hardware_dash()
    elif tab_option == tab_options[3]:
        run_software_dash()

if __name__ == "__main__":
    config_page()
    run_page()