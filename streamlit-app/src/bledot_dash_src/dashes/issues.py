import streamlit as st
from src.bledot_dash_src.session_state import get_session_state


def run_issues_dash():
    st.title("Máquinas comprometidas")

    company_machines = get_session_state("company_data")["machines"]
    machines_with_issues = get_session_state("machines_with_issues")
    metrics_threshold = get_session_state("metrics_threshold")

    is_first = True
    for machine_id, issues in machines_with_issues.items():
        if is_first:
            is_first = False
        else:
            st.divider()

        machine = company_machines[company_machines["id"] == machine_id]
        machine_label = machine["label_maquina"].item()
        st.header(machine_label)
        st.markdown(f"**ID**: {machine_id}")
        st.subheader("Falhas detectadas")
        for issue in issues:
            st.markdown(f"- {metrics_threshold[issue]['str']}")

