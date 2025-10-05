import streamlit as st
from bledot_dash_src.session_state import get_session_state
from bledot_dash_src.charts import (
    get_colors,
    create_hsbar_chart,
    create_speed_chart,
    create_card_chart,
)


def run_overview_dash():
    st.title("Visão Geral")

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
            # disk space
            color_val_disk_space, color_avg_disk_space = get_colors(
                "disk_usage_root", issues
            )
            st.altair_chart(
                create_hsbar_chart(
                    val=summary_data["avg_metrics"]["disk_usage_root"] * 100,
                    min_val=summary_data["min_metrics"]["disk_usage_root"] * 100,
                    max_val=summary_data["max_metrics"]["disk_usage_root"] * 100,
                    color_val=color_val_disk_space,
                    color_avg=color_avg_disk_space,
                    format_str="{:.0f} %",
                    title="Uso de armazenamento",
                    width=480,
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
