from werkzeug.security import check_password_hash
import streamlit as st
from supabase import create_client, Client

def get_supabase_client() -> Client:
    """Returns a configured Supabase client."""
    url = st.secrets.supabase.get("SUPABASE_URL")
    key = st.secrets.supabase.get("SUPABASE_KEY")
    
    if not url or not key:
        st.error("URL ou KEY do Supabase não configurados.")
        return None
    
    try:
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro ao criar cliente Supabase: {e}")
        return None

def get_user_role_and_id(username: str):
    """Search the role and company ID from the database."""
    supabase = get_supabase_client()
    if not supabase:
        return None, None
        
    try:
        response = supabase.table("empresas").select("role, id").eq("nome_empresa", username).eq("is_active", True).execute()
        
        if response.data:
            data = response.data[0]
            return data.get("role"), str(data.get("id"))
        
        return None, None
    except Exception as e:
        st.error(f"Erro ao buscar usuário: {e}")
        return None, None

def verify_supabase_user(username: str, password: str) -> bool:
    """
    Verify a user's credentials against the Supabase database.
    """
    supabase = get_supabase_client()
    if not supabase:
        return False
        
    try:
        response = supabase.table("empresas").select("password_hash").eq("nome_empresa", username).eq("is_active", True).execute()
        
        if not response.data:
            return False
            
        stored_hash = response.data[0].get("password_hash")
        if not stored_hash:
            return False
        
        return check_password_hash(stored_hash, password)
    except Exception as e:
        st.error(f"Erro de autenticação: {e}")
        return False

def get_company_id(username: str) -> str | None:
    """
    Takes a company name (username) and return its corresponding company ID from the database.
    """
    supabase = get_supabase_client()
    if not supabase:
        return None

    try:
        response = supabase.table("empresas").select("id").eq("nome_empresa", username).execute()
        
        if response.data:
            return str(response.data[0].get("id"))
        
        return None
    except Exception as e:
        st.error(f"Erro ao buscar ID da empresa: {e}")
        return None