import streamlit as st
import numpy as np
from src.bledot_dash_src.session_state import get_session_state
from src.bledot_dash_src.charts import (
    get_colors,
    create_card_chart,
    create_speed_chart,
)


def run_software_dash():
    st.header("Software")

    machine_data = get_session_state("machine_data")
    issues = machine_data["issues"][get_session_state("machine_id")]

    col1, col2 = st.columns([1, 1])

    with col1:
        # firewall
        if "firewall_active" in issues:
            val_chart = "INATIVO"
        else:
            val_chart = "ATIVO"

        color_val_firewall, color_avg_firewall = get_colors("firewall_active", issues)

        st.altair_chart(
            create_card_chart(
                val=val_chart,
                format_str="{}",
                title="Status do Firewall",
                color=color_avg_firewall,
            )
        )

        # failed_logins
        color_val_login_fail, color_avg_login_fail = get_colors("failed_logins", issues)

        st.altair_chart(
            create_speed_chart(
                val=machine_data["avg_metrics"]["failed_logins"],
                start_val=0,
                end_val=20,
                min_val=machine_data["min_metrics"]["failed_logins"],
                max_val=machine_data["max_metrics"]["failed_logins"],
                color_val=color_val_login_fail,
                color_avg=color_avg_login_fail,
                format_str="{:.0f}",
                title="Tentativas de login falhas",
            )
        )

    with col2:
        # idle
        color_val_idle, color_avg_idle = get_colors("idle", issues)
        if "click_rate" in issues and "keypress_rate" in issues:
            idle = "Ociosa"
        else:
            idle = "Não ociosa"

        st.altair_chart(
            create_card_chart(
                val=idle,
                format_str="{}",
                title="Máquinas ociosas",
                color=color_avg_idle,
                height=250,
            )
        )

        # packet loss
        color_val_packet_loss, color_avg_packet_loss = get_colors("packet_loss", issues)
        avg_packet_loss = machine_data["pkg_loss_mean"]

        st.altair_chart(
            create_card_chart(
                val=avg_packet_loss,
                format_str="{:.1f} %",
                title="Packet Loss",
                color=color_avg_packet_loss,
                height=225,
            )
        )

