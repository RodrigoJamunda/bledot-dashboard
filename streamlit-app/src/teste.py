import os
import pandas as pd
import json
from dotenv import load_dotenv
from SupabaseData import SupabaseData

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment or set them directly for testing
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL or SUPABASE_KEY not set!")
    print("Please create a .env file with these values or set them manually in this script.")
    exit(1)

def pretty_print_df(df, max_rows=5):
    if df is None or df.empty:
        print("Empty DataFrame or None")
        return
    
    print(f"DataFrame shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print("Sample data:")
    pd.set_option('display.max_columns', 10)
    print(df.head(max_rows))
    print("-" * 80)

def pretty_print_dict(d):
    if not d:
        print("Empty dictionary or None")
        return
    
    print(json.dumps(d, indent=2, default=str))
    print("-" * 80)

def test_supabase_data():
    # Initialize the SupabaseData class with explicit credentials
    print("Initializing SupabaseData...")
    supabase = SupabaseData(SUPABASE_URL, SUPABASE_KEY)
    
    # Test parameters
    enterprise_id = "test-enterprise-id"
    machine_id = "test-machine-id"
    
    print(f"\n1. Testing get_client_data for enterprise ID: {enterprise_id}")
    client_data = supabase.get_client_data(enterprise_id)
    pretty_print_dict(client_data)
    
    print(f"\n2. Testing get_client_machines for enterprise ID: {enterprise_id}")
    machines_df = supabase.get_client_machines(enterprise_id)
    pretty_print_df(machines_df)
    
    print(f"\n3. Testing get_latest_metrics_by_client for enterprise ID: {enterprise_id}")
    metrics_df = supabase.get_latest_metrics_by_client(enterprise_id, limit=10)
    pretty_print_df(metrics_df)
    
    print(f"\n4. Testing get_machine_metrics_history for machine ID: {machine_id}")
    history_df = supabase.get_machine_metrics_history(machine_id, days=3)
    pretty_print_df(history_df)
    
    print(f"\n5. Testing get_client_summary_stats for enterprise ID: {enterprise_id}")
    stats = supabase.get_client_summary_stats(enterprise_id)
    pretty_print_dict(stats)
    
    print(f"\n6. Testing load_client_dashboard_data for enterprise ID: {enterprise_id}")
    dashboard_data = supabase.load_client_dashboard_data(enterprise_id)
    print("Dashboard data keys:", list(dashboard_data.keys()))
    print("\nClient info:")
    pretty_print_dict(dashboard_data.get('client_info', {}))
    print("\nSummary stats:")
    pretty_print_dict(dashboard_data.get('summary_stats', {}))
    
    print("\nNumber of machines:", len(dashboard_data.get('machines', pd.DataFrame())))
    print("Number of metrics:", len(dashboard_data.get('latest_metrics', pd.DataFrame())))
    
    print("\nTest complete!")

if __name__ == "__main__":
    test_supabase_data()