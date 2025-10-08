import psycopg2
import streamlit as st
from werkzeug.security import generate_password_hash
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

def list_companies():
    """List all client companies from the database."""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        response = supabase.table("empresas").select("id, nome_empresa, data_criacao, is_active").eq("role", "client").order("nome_empresa").execute()
        return response.data
    except Exception as e:
        st.error(f"Erro ao listar empresas: {e}")
        return []

def add_company(company_name: str, created_by: str):
    """Add a new client company to the database."""
    supabase = get_supabase_client()
    if not supabase:
        return False, "Falha na conexão com o Supabase."

    try:
        response = supabase.table("empresas").insert({
            "nome_empresa": company_name,
            "created_by": created_by,
            "role": "client"
        }).execute()
        
        return True, f"Empresa '{company_name}' criada com sucesso!"
    except Exception as e:
        if "duplicate key" in str(e).lower():
            return False, f"A empresa '{company_name}' já existe."
        return False, f"Erro ao criar empresa: {e}"

def set_company_password(company_name: str, plain_password: str):
    """Set or update the password for a client company."""
    supabase = get_supabase_client()
    if not supabase:
        return False, "Falha na conexão com o Supabase."
        
    password_hash = generate_password_hash(plain_password)
    
    try:
        response = supabase.table("empresas").update({
            "password_hash": password_hash
        }).eq("nome_empresa", company_name).eq("role", "client").execute()
        
        if not response.data:
            return False, f"Empresa cliente '{company_name}' não encontrada."
            
        return True, f"Senha da empresa '{company_name}' atualizada com sucesso!"
    except Exception as e:
        return False, f"Erro ao atualizar senha: {e}"