import streamlit as st
import pandas as pd
import numpy as np
from src.bledot_dash_src.session_state import get_session_state
from src.bledot_dash_src.charts import (
    get_colors,
    create_hsbar_chart,
    create_speed_chart,
    create_card_chart,
    create_line_chart,
)


def run_specifics_dash():
    st.header("Propriedades")

    machine_data = get_session_state("machine_data")
    issues = machine_data["issues"][get_session_state("machine_id")]
    config = machine_data["config"]

    st.subheader("Configuração")
    st.write(f"**Nome do host:** {config['host_name']}")
    st.write(f"**Modelo:** {config['model']}")
    st.write(f"**Sistema operacional:** {config['operation_sys']}")
    st.write(f"**Versão do OS:** {config['os_version']}")
    st.write(f"**Processador:** {config['processor']}")
    if config['gpu_name'] is not None:
        st.write(f"**Placa gráfica:** {config['gpu_name']}")
    else:
        st.write(f"**Placa gráfica:** {config['inter_gpu_name']}")

    st.write(f"**Placa mãe:** {config['motherboard_manuf']} {config['motherboard_name']}")
    st.write(f"**SN da placa mãe:** {config['motherboard_snum']}")

    st.subheader("Rede")
    st.write(f"**Endereço MAC:** {config['mac']}")
    st.write(f"**IPv4:** {config['ipv4']}")
    st.write(f"**IPv6:** {config['ipv6']}")

    st.subheader("Localização")
    st.write(f"**Cidade:** {config['city']}")
    st.write(f"**Região:** {config['region_name']}")
    st.write(f"**País:** {config['country']}")
    st.write(f"**Latitude:** {config['lat']}")
    st.write(f"**Longitude:** {config['lon']}")

    st.subheader("Softwares instalados")
    st.dataframe(pd.Series(config['installed_softwares'], name="Softwares instalados"), hide_index=True)
