import streamlit as st
import bcrypt

# Configuração da página
st.set_page_config(
    page_title="Login | Bledot",
)

def show_login_form():
    """Mostra o formulário de login e gerencia a autenticação para múltiplos usuários."""
    with st.form("login_form"):
        st.header("Login")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")

    if submitted:
        # Pega a tabela de todos os usuários do arquivo de segredos
        all_users = st.secrets["users"]
        
        # Verifica se o nome de usuário fornecido existe na nossa lista de usuários
        if username in all_users:
            # Pega o hash da senha correspondente àquele usuário
            stored_hashed_password = all_users[username]["hashed_password"]
            
            # Verifica se a senha fornecida corresponde ao hash armazenado
            if bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")
        else:
            st.error("Usuário ou senha inválidos.")

def show_main_page():
    """Mostra o conteúdo principal da aplicação após o login."""
    st.title("Página Principal")
    st.write("Você está logado!")
    st.write("Agora você pode acessar as outras páginas disponíveis na barra lateral.")
    
    # Adicionar aqui qualquer outro conteúdo da página principal

def show_logout_button():
    """Mostra o botão de logout na barra lateral."""
    st.sidebar.success(f"Bem-vindo, {st.session_state.get('username', '')}!")
    if st.sidebar.button("Logout"):
        # Limpa o session_state para deslogar
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun() # Recarrega a página para mostrar o formulário de login novamente


# --- LÓGICA PRINCIPAL ---
# Verifica se o usuário já está logado
if st.session_state.get("logged_in", False):
    show_logout_button()
    show_main_page()
else:
    show_login_form()