import streamlit as st
import numpy as np
from src.bledot_dash_src.session_state import get_session_state
from src.bledot_dash_src.charts import (
    get_colors,
    create_hsbar_chart,
    create_speed_chart,
    create_card_chart,
    create_line_chart,
)


def run_overview_dash():
    st.header("Visão Geral")

    company_data = get_session_state("company_data")
    summary_data = company_data["summary_stats"]
    issues = get_session_state("issues")

    col1, col2 = st.columns([2, 1])

    with col1:
        subcol1, subcol2 = st.columns([1, 1])

        with subcol1:
            # hardware fails
            color_val_fails, color_avg_fails = get_colors(
                "recent_hardware_failures", issues
            )
            st.altair_chart(
                create_card_chart(
                    val=summary_data["avg_metrics"]["recent_hardware_failures"],
                    format_str="{:.0f}",
                    title="Histórico de falhas recentes",
                    color=color_avg_fails,
                )
            )

        with subcol2:
            # idle
            color_val_idle, color_avg_idle = get_colors("idle", issues)
            num_idle = 0
            for issues in summary_data["machines_with_issues"].values():
                if "click_rate" in issues and "keypress_rate" in issues:
                    num_idle += 1

            st.altair_chart(
                create_card_chart(
                    val=num_idle,
                    format_str="{}",
                    title="Máquinas ociosas",
                    color=color_avg_idle,
                )
            )

        # power consumption
        color_val_power_consumption, color_avg_power_consumption = get_colors(
            "instant_power_consumption", issues
        )

        power_consumption_threshold = get_session_state("metrics_threshold")[
            "instant_power_consumption"
        ]["val"]

        st.altair_chart(
            create_line_chart(
                val=summary_data["power_consumption_hist"]["avg"],
                min_val=summary_data["power_consumption_hist"]["min"],
                max_val=summary_data["power_consumption_hist"]["max"],
                title="Consumo energético (W)",
                color_val=color_val_power_consumption,
                color_avg=color_avg_power_consumption,
                start_val=max(
                    0, np.min(summary_data["power_consumption_hist"]["min"]) - 2
                ),
                end_val=max(
                    power_consumption_threshold + 2,
                    np.max(summary_data["power_consumption_hist"]["max"]) + 2,
                ),
                threshold=power_consumption_threshold,
            )
        )

    with col2:
        # cpu temperature
        color_val_cpu_temp, color_avg_cpu_temp = get_colors("cpu_temperature", issues)

        st.altair_chart(
            create_speed_chart(
                val=summary_data["avg_metrics"]["cpu_temperature"],
                start_val=30,
                end_val=100,
                min_val=summary_data["min_metrics"]["cpu_temperature"],
                max_val=summary_data["max_metrics"]["cpu_temperature"],
                color_val=color_val_cpu_temp,
                color_avg=color_avg_cpu_temp,
                format_str="{:.0f} \u00b0C",
                title="Temperatura da CPU",
            )
        )

        # gpu temperature
        color_val_gpu_temp, color_avg_gpu_temp = get_colors("gpu_temperature", issues)

        st.altair_chart(
            create_speed_chart(
                val=summary_data["avg_metrics"]["gpu_temperature"],
                start_val=30,
                end_val=100,
                min_val=summary_data["min_metrics"]["gpu_temperature"],
                max_val=summary_data["max_metrics"]["gpu_temperature"],
                color_val=color_val_gpu_temp,
                color_avg=color_avg_gpu_temp,
                format_str="{:.0f} \u00b0C",
                title="Temperatura da GPU",
            )
        )

        # ram usage
        color_val_ram_usage, color_avg_ram_usage = get_colors("ram_usage", issues)

        st.altair_chart(
            create_speed_chart(
                val=summary_data["avg_metrics"]["ram_usage"] * 100,
                start_val=0,
                end_val=100,
                min_val=summary_data["min_metrics"]["ram_usage"] * 100,
                max_val=summary_data["max_metrics"]["ram_usage"] * 100,
                color_val=color_val_ram_usage,
                color_avg=color_avg_ram_usage,
                format_str="{:.0f} %",
                title="Uso de RAM",
            )
        )

    # st.write(summary_data)
