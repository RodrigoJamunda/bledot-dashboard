import streamlit as st
from .supabase_auth import verify_supabase_user, get_user_role_and_id
import base64
import os

def get_image_base64(image_path):
    """ Converts image to base64 to embed in CSS """
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

def authenticate():
    """
    Manages the authentication process, displaying a login page
    with split screen layout
    """
    # Initialize session state keys if they do not exist
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
    # User is already authenticated, ensure sidebar is shown
        st.markdown("""
        <style>
            /* Show sidebar for authenticated users */
            .css-1d391kg, .css-1lcbmhc, .css-1outpf7, section[data-testid="stSidebar"] {
                display: block !important;
            }
            
            /* Reset main container for normal app view */
            .main .block-container { 
                padding: 1rem !important; 
                margin: 0 !important; 
                max-width: none !important;
                width: auto !important;
            }
            .main { 
                padding: 0 !important; 
                margin: 0 !important;
            }
            
            /* Reset app layout */
            .stApp {
                margin-left: auto !important;
                width: auto !important;
                max-width: none !important;
            }
            
            /* Reset overflow */
            .main, .stApp, html, body {
                overflow-x: auto !important;
                overflow-y: auto !important;
            }
        </style>
        """, unsafe_allow_html=True)
        return True

    # Color for background of left column
    blue_background_color = "#4793EA"
    darker_blue_background_color = "#1E2A3B"

    # Get logo in base64
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    logo_base64 = get_image_base64(logo_path) if get_image_base64(logo_path) else ""
    logo2_path = os.path.join(os.path.dirname(__file__), "logo2.png")
    logo2_base64 = get_image_base64(logo2_path) if get_image_base64(logo2_path) else ""

    # Styled CSS for login page
    st.markdown(f"""
        <style>
            /* Reset e Layout Base */
            .main .block-container {{ 
                padding: 0 !important; 
                margin: 0 !important; 
                max-width: 100% !important;
                width: 100vw !important;
            }}
            .main {{ 
                padding: 0 !important; 
                margin: 0 !important;
            }}
            header, footer {{ visibility: hidden; }}
            
            /* Esconder sidebar completamente durante login */
            .css-1d391kg, .css-1lcbmhc, .css-1outpf7, section[data-testid="stSidebar"] {{
                display: none !important;
            }}
            
            /* Garantir que o app ocupe toda a tela */
            .stApp {{
                margin-left: 0 !important;
                width: 100vw !important;
                max-width: 100vw !important;
            }}
            
            /* Remover overflow e scroll */
            .main, .stApp, html, body {{
                overflow-x: hidden !important;
                overflow-y: hidden !important;
            }}
            
            /* Garantir cobertura de altura completa */
            .stApp {{ background: transparent !important; }}
            
            /* Container de Bloco Horizontal */
            div[data-testid="stHorizontalBlock"] {{ 
                height: 100vh !important; 
                overflow: hidden !important; 
                gap: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
                display: flex !important;
                flex-direction: row !important;
            }}

            /* Coluna Esquerda */
            div[data-testid="stHorizontalBlock"] > div:nth-child(1) {{
                background-color: {blue_background_color} !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: center !important;
                align-items: center !important;
                height: 100vh !important;
                width: 70% !important;
                flex: none !important;
                padding: 0 !important;
                margin: 0 !important;
            }}
            
            /* Garantir que todos os elementos filhos herdem o fundo laranja */
            div[data-testid="stHorizontalBlock"] > div:nth-child(1) * {{
                background: transparent !important;
            }}
            
            .brand-container {{
                color: white !important;
                text-align: center !important;
                background: transparent !important;
            }}
            .brand-logo img {{
                width: 350px !important;
                height: auto !important;
                margin-bottom: 1rem !important;
            }}
            .brand-title {{
                font-size: 5rem !important;
                font-weight: bold !important;
                margin-top: -10px !important;
                color: white !important;
            }}

            /* Coluna Direita (Branca) */
            div[data-testid="stHorizontalBlock"] > div:nth-child(2) {{
                background-color: #FFFFFF !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                height: 100vh !important;
                width: 30% !important;
                flex: none !important;
                padding: 2rem !important;
                margin: 0 !important;
            }}
            
            /* Garantir que elementos filhos específicos herdem o fundo branco, mas não os botões */
            div[data-testid="stHorizontalBlock"] > div:nth-child(2) div:not(.stButton):not([data-testid="stForm"]) {{
                background: transparent !important;
            }}
            
            .login-container {{
                width: 100% !important;
                max-width: 350px !important;
                background: transparent !important;
            }}
            .login-logo img {{
                width: 80px !important;
                height: auto !important;
            }}
            .login-title {{
                font-size: 2rem !important;
                font-weight: bold !important;
                color: {blue_background_color} !important;
                text-align: center !important;
                margin-top: 10px !important;
            }}
            .login-subtitle {{
                color: #b0b0b0 !important;
                text-align: center !important;
                margin-bottom: 2rem !important;
            }}

            /* Estilização do Formulário */
            .stTextInput label {{
                color: #b0b0b0 !important;
                font-weight: normal !important;
                font-size: 0.9rem !important;
            }}
            .stTextInput input {{
                border-radius: 25px !important;
                border: 1px solid #e6e6e6 !important;
                background-color: #fafafa !important;
                color: #333333 !important;
                box-shadow: none !important;
            }}
            
            /* Garantir visibilidade do texto em temas escuros */
            .stTextInput > div > div > input {{
                background-color: #fafafa !important;
                color: #333333 !important;
                border: 1px solid #e6e6e6 !important;
                box-shadow: none !important;
            }}
            .stTextInput > div > div > input:focus {{
                background-color: #ffffff !important;
                color: #333333 !important;
                border: 2px solid {blue_background_color} !important;
                outline: none !important;
                box-shadow: none !important;
            }}
            
            /* Remover bordas escuras do container do input */
            .stTextInput > div {{
                border: none !important;
                box-shadow: none !important;
            }}
            .stTextInput > div > div {{
                border: none !important;
                box-shadow: none !important;
            }}
            
            /* Estilizar placeholder text */
            .stTextInput input::placeholder {{
                color: #999999 !important;
            }}
            
            /* Garantir que o container do botão e o botão sejam visíveis */
            div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton {{
                background: transparent !important;
                display: block !important;
                visibility: visible !important;
            }}
            
            .stButton > button {{
                background: {blue_background_color} !important;
                color: white !important;
                border: none !important;
                border-radius: 25px !important;
                padding: 0.75rem 2rem !important;
                font-size: 1.1rem !important;
                font-weight: 600 !important;
                width: 100% !important;
                margin-top: 1rem !important;
                display: block !important;
                visibility: visible !important;
                opacity: 1 !important;
            }}
            .stButton > button:hover {{
                background: {darker_blue_background_color} !important;
            }}
        </style>
    """, unsafe_allow_html=True)

    # Create a 70/30 split layout
    left_col, right_col = st.columns([7, 3], gap="small")

    with left_col:
        st.markdown(f"""
            <div class="brand-container" style="height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;">
                <div class="brand-logo">
                    <img src="data:image/png;base64,{logo_base64}" alt="Bledot Logo"
                        style="display:block;margin:auto;max-width:80vw;max-height:80vh;width:100%;height:auto;">
                </div>
            </div>
        """, unsafe_allow_html=True)


    with right_col:
        st.markdown(f"""
            <div class="login-container">
                <div class="login-logo">
                    <img src="data:image/png;base64,{logo2_base64}" alt="Bledot Logo">
                </div>
                <div class="login-title">Bem-vindo(a)!</div>
                <p class="login-subtitle">Informe seu e-mail/usuário e senha para continuar.</p>
            </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Nome da Empresa")
        password = st.text_input("Senha", type="password")

        if st.button("Continuar", use_container_width=True):
            if username and password:
                if verify_supabase_user(username, password):
                    # Well authenticated
                    role, company_id = get_user_role_and_id(username)

                    if not role:
                        st.error("Não foi possível determinar o papel do usuário.")
                        st.stop()
                    
                    # Save authentication state
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.role = role
                    
                    # Redirect based on role
                    if role == 'admin':
                        st.switch_page("pages/admin_dash.py")
                    elif role == 'client':
                        if company_id:
                            st.session_state.company_id = company_id
                            st.switch_page("pages/company_dash.py")
                        else:
                            st.error("ID da empresa cliente não encontrado.")
                    else:
                        st.error("Papel de usuário desconhecido.")
                else:
                    st.error("Empresa ou senha incorretos", icon="🔒")
            else:
                st.error("Por favor, preencha todos os campos", icon="⚠️")

    return False

def logout():
    """ Removes authentication and session states """
    keys_to_del = ["authenticated", "username", "role", "show_admin", "sidebar_state"]
    for key in keys_to_del:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()