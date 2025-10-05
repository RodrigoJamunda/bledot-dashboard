import streamlit as st
from bledot_dash_src.supabase_data import SupabaseData
from bledot_dash_src.session_state import (
    init_session_state,
    set_session_state,
    get_session_state,
    check_session_state,
)
from bledot_dash_src.dashes.overview import run_overview_dash
from bledot_dash_src.dashes.processing import run_processing_dash
from bledot_dash_src.dashes.hardware import run_hardware_dash
from bledot_dash_src.dashes.software import run_software_dash
from bledot_dash_src.dashes.idle import run_idle_dash


def make_sidebar(tab_options: list[str]) -> str:
    init_session_state("selected_tab", tab_options[0])

    with st.sidebar:
        st.title("Bledot")
        st.divider()

        for tab_option in tab_options:
            if tab_option == get_session_state("selected_tab"):
                button_type = "primary"
            else:
                button_type = "tertiary"

            if st.button(
                label=tab_option,
                key=f"tab_button_{tab_option}",
                type=button_type,
                use_container_width=True,
            ):
                set_session_state("selected_tab", tab_option)
                st.rerun()

    return get_session_state("selected_tab")


def config_page():
    """Configures page layout"""
    st.set_page_config(layout="wide")


def run_page():
    """Runs page script"""

    if not check_session_state("database_url") or not check_session_state(
        "database_key"
    ):
        st.switch_page("main_page.py")

    init_session_state(
        "company_id", st.secrets.supabase["DEBUG_COMPANY_ID"]
    )  # DEBUG ONLY

    if not "company_data" in st.session_state:
        supabase_data = SupabaseData(
            url=get_session_state("database_url"), key=get_session_state("database_key")
        )

        company_data = supabase_data.load_client_dashboard_data(
            get_session_state("company_id")
        )

        init_session_state("company_data", company_data)
    else:
        company_data = get_session_state("company_data")

    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    with col1:
        target_machine_label = st.selectbox(
            "Máquinas", options=company_data["machines"]["label_maquina"]
        )
    with col2:
        if st.button("Ver mais informações", type="primary"):
            set_session_state(
                "machine_id",
                company_data["machines"][
                    target_machine_label == company_data["machines"]["label_maquina"]
                ]["id"].item(),
            )

            st.switch_page("pages/machine_dash.py")

    tab_options = [
        "Visão Geral",
        "Processamento",
        "Hardware",
        "Software",
        "Ociosidade",
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
        run_idle_dash()


if __name__ == "__main__":
    config_page()
    run_page()
