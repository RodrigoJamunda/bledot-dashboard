import streamlit as st
from auth.admin_db_manager import list_companies, add_company, set_company_password

def config_page():
    st.set_page_config(layout="wide", page_title="Admin - Bledot")

def run_page():
    # Only allow access if user is admin
    if st.session_state.get("role") != "admin":
        st.error("Acesso não autorizado.")
        st.switch_page("main_page.py")

    st.title(f"Painel de Administração - Bem-vindo(a), {st.session_state.get('username')}!")
    st.markdown("Gerencie as empresas clientes abaixo.")

    # Create new company section
    with st.expander("➕ Criar Nova Empresa Cliente", expanded=False):
        with st.form("new_company_form", clear_on_submit=True):
            new_company_name = st.text_input("Nome da Nova Empresa")
            submitted = st.form_submit_button("Criar Empresa")
            
            if submitted and new_company_name:
                success, message = add_company(new_company_name, st.session_state.get("username"))
                if success:
                    st.success(message)
                else:
                    st.error(message)
    
    # Update password section
    with st.expander("🔑 Definir Senha Padrão/Atualizar Senha", expanded=False):
        with st.form("set_password_form", clear_on_submit=True):
            target_company_name = st.text_input("Nome da Empresa Alvo")
            new_password = st.text_input("Nova Senha", type="password")
            submitted_pass = st.form_submit_button("Definir Senha")

            if submitted_pass and target_company_name and new_password:
                success, message = set_company_password(target_company_name, new_password)
                if success:
                    st.success(message)
                else:
                    st.error(message)

    # List of companies
    st.divider()
    st.header("Empresas Clientes Cadastradas")
    
    companies = list_companies()
    if not companies:
        st.info("Nenhuma empresa cliente encontrada.")
    else:
        # Show companies in a table
        st.dataframe(
            companies,
            column_config={
                "id": "ID da Empresa (UUID)",
                "nome_empresa": "Nome da Empresa",
                "data_criacao": "Data de Criação",
                "is_active": "Ativa?"
            },
            use_container_width=True,
            hide_index=True
        )
        
    if st.button("Logout"):
        from auth.auth_handler import logout
        logout()

if __name__ == "__main__":
    config_page()
    run_page()