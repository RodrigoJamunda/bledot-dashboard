import streamlit as st
import traceback
from src.bledot_dash_src.supabase_data import SupabaseData
from src.bledot_dash_src.session_state import (
    init_session_state,
    set_session_state,
    get_session_state,
    check_session_state,
)
from src.bledot_dash_src.machine_dashes.overview import run_overview_dash
from src.bledot_dash_src.machine_dashes.processing import run_processing_dash
from src.bledot_dash_src.machine_dashes.hardware import run_hardware_dash
from src.bledot_dash_src.machine_dashes.software import run_software_dash
from src.bledot_dash_src.machine_dashes.issues import run_issues_dash
from src.bledot_dash_src.machine_dashes.specifics import run_specifics_dash
from auth.user_db_manager import change_password_form
from auth.auth_handler import logout


def make_sidebar(tab_options: list[str]) -> str:
    with st.spinner("Processando..."):
        init_session_state("selected_tab", tab_options[0])
        company_data = get_session_state("company_data")

    with st.sidebar:
        st.markdown(
            "<h1 style='text-align: center; font-size: 52px; font-weight: bold'>Bledot</h1>",
            unsafe_allow_html=True,
        )
        st.divider()

        for tab_option in tab_options:
            if tab_option == "Alterar Senha":
                st.divider()

            if st.button(tab_option, width="stretch"):
                set_session_state("selected_tab", tab_option)

        st.divider()

        # Verify if there is a 'label_maquina' or similar column
        machine_columns = company_data["machines"].columns
        machine_label_col = None

        for col in ["label_maquina", "nome_maquina", "machine_name", "name", "id"]:
            if col in machine_columns:
                machine_label_col = col
                break

        if machine_label_col:
            target_machine_label = st.selectbox(
                "Selecione uma máquina:",
                company_data["machines"][machine_label_col].unique(),
            )
        else:
            st.warning("Nenhuma coluna de identificação de máquina encontrada")
            target_machine_label = None

        if (
            st.button("Ver informações da máquina", type="secondary", width="stretch")
            and target_machine_label
        ):
            set_session_state("target_machine", target_machine_label)
            st.switch_page("pages/machine_dash.py")

        if st.button("Voltar à página da empresa", type="secondary", width="stretch"):
            st.switch_page("pages/company_dash.py")

        st.divider()
        if st.session_state.get("role") == "admin":
            if st.button("Área do administrador", width="stretch"):
                st.switch_page("pages/admin_dash.py")

        if st.button("Logout", width="stretch"):
            logout()

    return get_session_state("selected_tab")


def config_page():
    """Configures page layout"""
    st.set_page_config(layout="wide", page_title="Dashboard - Bledot")


def run_page():
    """Runs page script"""


    with st.spinner("Carregando dados..."):
        # Verify if user is authenticated and company_id is set
        if not check_session_state("authenticated") or not check_session_state(
            "company_id"
        ):
            st.switch_page("main_page.py")

        if not check_session_state("target_machine"):
            st.switch_page("pages/company_dash.py")

        machine_label = get_session_state("target_machine")
        company_data = get_session_state("company_data")
        machine_id = company_data["machines"][
            company_data["machines"]["label_maquina"] == machine_label
        ]["id"].item()
        set_session_state("machine_id", machine_id)

        # Load data only if not already loaded or if company_id has changed
        if (
            "machine_data" not in st.session_state
            or st.session_state.get("loaded_machine_id") != machine_id
        ):
            # Load and return Supabase Database Client
            supabase_data = SupabaseData()
            machine_data = supabase_data.get_machine_metrics_history(machine_id)

            # Store data in session
            set_session_state("machine_data", machine_data)
            set_session_state("loaded_machine_id", machine_id)
        else:
            machine_data = get_session_state("machine_data")

        st.title(f"Métricas - {company_data['client_info']['nome_empresa']} - {machine_label}")

        if machine_data:
            tab_options = [
                "Visão Geral",
                "Processamento",
                "Hardware",
                "Software",
                "Propriedades",
                "Alterar Senha",
            ]

            tab_option = make_sidebar(tab_options)

            if tab_option == tab_options[0]:
                run_overview_dash()
            elif tab_option == tab_options[1]:
                run_processing_dash()
            elif tab_option == tab_options[2]:
                run_hardware_dash()
            elif tab_option == tab_options[3]:
                run_software_dash()
            elif tab_option == tab_options[4]:
                run_specifics_dash()
            elif tab_option == tab_options[5]:
                change_password_form()

        else:
            st.info("Nenhuma informação encontrada para esta máquina")
            tab_options = ["Alterar Senha"]
            tab_option = make_sidebar(tab_options)

            if tab_option == tab_options[0]:
                change_password_form()


if __name__ == "__main__":
    config_page()
    run_page()
