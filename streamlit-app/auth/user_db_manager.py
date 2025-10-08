from werkzeug.security import check_password_hash, generate_password_hash
import streamlit as st
from supabase import create_client, Client
from auth.supabase_auth import get_supabase_client, verify_supabase_user

def change_own_password(username: str, current_password: str, new_password: str) -> tuple[bool, str]:
    """
    Allows a company to change its own password after verifying the current one.
    """
    supabase = get_supabase_client()
    if not supabase:
        return False, "Erro ao conectar com o banco de dados"
    
    try:
        # First verify the current password
        if not verify_supabase_user(username, current_password):
            return False, "Senha atual incorreta"
        
        # Generate new password hash
        new_password_hash = generate_password_hash(new_password)
        
        # Update the password in the database
        response = supabase.table("empresas").update({
            "password_hash": new_password_hash
        }).eq("nome_empresa", username).eq("is_active", True).execute()
        
        if response.data:
            return True, "Senha alterada com sucesso!"
        else:
            return False, "Erro ao atualizar a senha"
            
    except Exception as e:
        return False, f"Erro ao alterar senha: {e}"
    
def change_password_form():
    """Display the password change form"""
    st.header("🔑 Alterar Senha")
    st.markdown("Altere sua senha atual preenchendo os campos abaixo.")
    
    with st.form("change_password_form", clear_on_submit=True):
        st.markdown("### Informações de Segurança")
        
        current_password = st.text_input(
            "Senha Atual", 
            type="password",
            help="Digite sua senha atual para confirmar a alteração"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            new_password = st.text_input(
                "Nova Senha", 
                type="password",
                help="A nova senha deve ter pelo menos 8 caracteres"
            )
        with col2:
            confirm_password = st.text_input(
                "Confirmar Nova Senha", 
                type="password",
                help="Digite a nova senha novamente"
            )
        
        submitted = st.form_submit_button(
            "Alterar Senha", 
            type="primary",
            width="stretch"
            )
        
        if submitted:
            # Validation
            if not current_password:
                st.error("Por favor, digite sua senha atual")
                return
            
            if not new_password:
                st.error("Por favor, digite a nova senha")
                return
            
            if len(new_password) < 8:
                st.error("A nova senha deve ter pelo menos 8 caracteres")
                return
            
            if new_password != confirm_password:
                st.error("As senhas não coincidem")
                return
            
            if current_password == new_password:
                st.error("A nova senha deve ser diferente da senha atual")
                return
            
            # Attempt to change password
            username = st.session_state.get("username")
            if not username:
                st.error("Usuário não encontrado na sessão")
                return
            
            with st.spinner("Alterando senha..."):
                success, message = change_own_password(username, current_password, new_password)
            
            if success:
                st.success(message)
            else:
                st.error(message)    
