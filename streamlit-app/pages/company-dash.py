import streamlit as st
from bledot_dash_src.session_state import (
    init_session_state,
    set_session_state,
    get_session_state,
)
from bledot_dash_src.dashes.overview import run_overview_dash
from bledot_dash_src.dashes.processing import run_processing_dash
from bledot_dash_src.dashes.hardware import run_hardware_dash
from bledot_dash_src.dashes.software import run_software_dash
from bledot_dash_src.dashes.idle import run_idle_dash


def make_sidebar():
    tab_options = [
        "Geral",
        "Processamento",
        "Hardware",
        "Software",
        "Ociosidade",
    ]
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


def run_page():
    """Runs page script"""

    tab_option = make_sidebar()
    match tab_option:
        case "Geral":
            run_overview_dash()
        case "Processamento":
            run_processing_dash()
        case "Hardware":
            run_hardware_dash()
        case "Software":
            run_software_dash()
        case "Ociosidade":
            run_idle_dash()


if __name__ == "__main__":
    config_page()
    run_page()
