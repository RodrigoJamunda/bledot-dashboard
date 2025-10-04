# bledot-dashboard
Dashboard for centralizing and displaying hardware and software KPIs

## Install Requirements

Run the following command to install the required dependencies (inside the streamlit-app directory).

```bash
pip install -r requirements.txt
```

### Developers

To enable dynamic reference to the internal modules, run the following command.
```bash
pip install -e .
```

## Local Running

Create a ```secrets.toml``` file in the streamlit-app/.streamlit directory with the following data.
```toml
SUPABASE_URL="your_supabase_url"
SUPABASE_KEY="your_key"
```

Then, run the dashboard by running the following script (inside the streamlit-app directory).
```bash
streamlit run main_page.py
```
