import streamlit as st
from typing import Any


def init_session_state(key: str, value: Any) -> Any:
    """Initializes a session state variable if it has no value

    Args:
        key: key for session state variable
        value: value of session state variable
    """
    if key not in st.session_state:
        st.session_state[key] = value

    return st.session_state[key]

def set_session_state(key: str, value: Any) -> None:
    """Sets a session state variable

    Args:
        key: key for session state variable
        value: value of session state variable
    """
    st.session_state[key] = value


def get_session_state(key: str, default: Any = None) -> Any:
    """Gets a session state variable

    Args:
        key: key for session state variable
        default: default value of session state variable if it doesn't exist

    Returns:
        Value of session state variable associated with key"""
    if key not in st.session_state:
        return default

    return st.session_state[key]
