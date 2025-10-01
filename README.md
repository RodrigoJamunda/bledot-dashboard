# bledot-dashboard
Dashboard for centralizing and displaying hardware and software KPIs
## Install Requirements
```bash
pip install -r requirements.txt
```
## Create a .env file
```python
SUPABASE_URL="https:url"
SUPABASE_KEY="key"
```
## Testing
Select a specifc client to test and a machine and change it in ```teste.py```:
```python
def test_supabase_data():
    (...)
    
    # Test parameters
    enterprise_id = "test_client_id"
    machine_id = "test_machine_id"
```

Run:
```bash
python streamlit-app\src\teste.py
```