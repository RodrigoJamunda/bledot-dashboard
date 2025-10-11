import streamlit as st
import numpy as np
from src.bledot_dash_src.session_state import get_session_state
from src.bledot_dash_src.charts import (
    get_colors,
    create_hsbar_chart,
    create_card_chart,
    create_speed_chart,
    create_line_chart
)


def run_hardware_dash():
    st.header("Hardware")

    company_data = get_session_state("company_data")
    summary_data = company_data["summary_stats"]
    issues = get_session_state("issues")

    col1, col2 = st.columns([1, 1])

    with col1:
        # disk space (root)
        color_val_disk_space_root, color_avg_disk_space_root = get_colors(
            "disk_usage_root", issues
        )
        st.altair_chart(
            create_hsbar_chart(
                val=summary_data["avg_metrics"]["disk_usage_root"] * 100,
                min_val=summary_data["min_metrics"]["disk_usage_root"] * 100,
                max_val=summary_data["max_metrics"]["disk_usage_root"] * 100,
                color_val=color_val_disk_space_root,
                color_avg=color_avg_disk_space_root,
                format_str="{:.0f} %",
                title="Uso de armazenamento (root)",
                width=480,
                height=250,
            )
        )

        # disk space (home)
        color_val_disk_space_home, color_avg_disk_space_home = get_colors(
            "disk_usage_home", issues
        )
        st.altair_chart(
            create_hsbar_chart(
                val=summary_data["avg_metrics"]["disk_usage_home"] * 100,
                min_val=summary_data["min_metrics"]["disk_usage_home"] * 100,
                max_val=summary_data["max_metrics"]["disk_usage_home"] * 100,
                color_val=color_val_disk_space_home,
                color_avg=color_avg_disk_space_home,
                format_str="{:.0f} %",
                title="Uso de armazenamento (home)",
                width=480,
                height=250,
            )
        )

        # disk space (boot)
        color_val_disk_space_boot, color_avg_disk_space_boot = get_colors(
            "disk_usage_boot", issues
        )
        st.altair_chart(
            create_hsbar_chart(
                val=summary_data["avg_metrics"]["disk_usage_boot"] * 100,
                min_val=summary_data["min_metrics"]["disk_usage_boot"] * 100,
                max_val=summary_data["max_metrics"]["disk_usage_boot"] * 100,
                color_val=color_val_disk_space_boot,
                color_avg=color_avg_disk_space_boot,
                format_str="{:.0f} %",
                title="Uso de armazenamento (boot)",
                width=480,
                height=250,
            )
        )

    with col2:
        subcol1, subcol2 = st.columns([1, 1])

        with subcol1:
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

            # smart
            if "smart_overall" in issues:
                val_chart = "FALHA"
            else:
                val_chart = "OK"

            color_val_smart, color_avg_smart = get_colors("smart_overall", issues)

            st.altair_chart(
                create_card_chart(
                    val=val_chart,
                    format_str="{}",
                    title="Diagnóstico SMART",
                    color=color_avg_smart,
                    height=175,
                )
            )

        with subcol2:
            # battery life
            # color_val_ram_usage, color_avg_ram_usage = get_colors("battery_health", issues)

            st.altair_chart(
                create_speed_chart(
                    val=summary_data["avg_metrics"]["battery_health"] * 100,
                    start_val=0,
                    end_val=100,
                    min_val=summary_data["min_metrics"]["battery_health"] * 100,
                    max_val=summary_data["max_metrics"]["battery_health"] * 100,
                    # color_val=color_val_ram_usage,
                    # color_avg=color_avg_ram_usage,
                    format_str="{:.0f} %",
                    title="Saúde da bateria",
                )
            )

            # swap/paging
            # color_val_ram_usage, color_avg_ram_usage = get_colors("battery_health", issues)

            st.altair_chart(
                create_speed_chart(
                    val=summary_data["avg_metrics"]["swap_usage"] * 100,
                    start_val=0,
                    end_val=100,
                    min_val=summary_data["min_metrics"]["swap_usage"] * 100,
                    max_val=summary_data["max_metrics"]["swap_usage"] * 100,
                    # color_val=color_val_ram_usage,
                    # color_avg=color_avg_ram_usage,
                    format_str="{:.0f} %",
                    title="Uso de swap",
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

