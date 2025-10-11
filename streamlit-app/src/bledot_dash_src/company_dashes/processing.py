import streamlit as st
from src.bledot_dash_src.session_state import get_session_state
from src.bledot_dash_src.charts import get_colors, create_speed_chart, create_card_chart


def run_processing_dash():
    st.header("Processamento")

    company_data = get_session_state("company_data")
    summary_data = company_data["summary_stats"]
    issues = get_session_state("issues")

    col1, col2, col3 = st.columns([1, 1, 1.8])

    with col1:
        # cpu usage
        color_val_cpu_usage, color_avg_cpu_usage = get_colors("cpu_usage", issues)

        st.altair_chart(
            create_speed_chart(
                val=summary_data["avg_metrics"]["cpu_usage"] * 100,
                start_val=0,
                end_val=100,
                min_val=summary_data["min_metrics"]["cpu_usage"] * 100,
                max_val=summary_data["max_metrics"]["cpu_usage"] * 100,
                color_val=color_val_cpu_usage,
                color_avg=color_avg_cpu_usage,
                format_str="{:.0f} %",
                title="Uso da CPU",
            )
        )

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

    with col2:
        # gpu usage
        color_val_gpu_usage, color_avg_gpu_usage = get_colors("gpu_usage", issues)

        st.altair_chart(
            create_speed_chart(
                val=summary_data["avg_metrics"]["gpu_usage"] * 100,
                start_val=0,
                end_val=100,
                min_val=summary_data["min_metrics"]["gpu_usage"] * 100,
                max_val=summary_data["max_metrics"]["gpu_usage"] * 100,
                color_val=color_val_gpu_usage,
                color_avg=color_avg_gpu_usage,
                format_str="{:.0f} %",
                title="Uso da GPU",
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

    with col3:
        # gpu volt
        st.altair_chart(
            create_card_chart(
                val=summary_data["avg_metrics"]["gpu_voltage"],
                format_str="{:.1f}",
                title="Voltagem da GPU",
                height=240,
            )
        )

        subcol1, subcol2 = st.columns([1, 1])
        with subcol1:
            st.altair_chart(
                create_card_chart(
                    val=summary_data["avg_metrics"]["fan_rpm_cpu"],
                    format_str="{:.0f}",
                    title="RPM da CPU",
                    height=240,
                )
            )

        with subcol2:
            st.altair_chart(
                create_card_chart(
                    val=summary_data["avg_metrics"]["fan_rpm_gpu"],
                    format_str="{:.0f}",
                    title="RPM da GPU",
                    height=240,
                )
            )
