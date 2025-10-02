import os
import pandas as pd
import streamlit as st
from supabase import create_client, Client
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pytz

class SupabaseData:
    def __init__(self, url=None, key=None):
        #Allow passing credentials directly or use environment variables
        self.url = url or st.secrets.supabase["DEBUG_SUPABASE_URL"]
        self.key = key or st.secrets.supabase["DEBUG_SUPABASE_KEY"]

        # DEBUG:
        # self.url = url or os.getenv("SUPABASE_URL")
        # self.key = key or os.getenv("SUPABASE_KEY")
        
        #Check if credentials are available
        if not self.url or not self.key:
            print("Error: Supabase credentials not found. Please set SUPABASE_URL and SUPABASE_KEY environment variables.")
        else:
            self.client = self._get_client()
    
    #Load and return Supabase Database Client
    def _get_client(self) -> Client:
        return create_client(self.url, self.key)
    
    def _handle_error(self, error_msg: str, e: Exception) -> None:
        full_error = f"{error_msg}: {e}"
        #Check if running in Streamlit
        if 'st' in globals():
            st.error(full_error)
        else:
            print(f"ERROR: {full_error}")
        return None
    
    def _convert_timestamps(self, df: pd.DataFrame, timestamp_columns: List[str] | None = None) -> pd.DataFrame:
        if df.empty:
            return df
            
        #Default timestamp columns if none specified
        if timestamp_columns is None:
            timestamp_columns = ['data_coleta', 'data_registro', 'ultimo_contato', 'timestamp']
        
        #Convert each column if it exists in the DataFrame
        for col in timestamp_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        
        return df
    
    def _get_metrics_kpi(self, metrics_df: pd.DataFrame, default: float = 0.0):
        avg_metrics = {}
        max_metrics = {}
        min_metrics = {}
        for metric_label in metrics_df.columns:
            if metrics_df.empty:
                average_metrics[metric_label] = default
                continue

            metric_series = metrics_df[metric_label].dropna()[metrics_df[metric_label].apply(
                lambda x: isinstance(x, int) or isinstance(x, float)
            )]
            if metric_series.empty:
                # average_metrics[metric_label] = default
                continue

            avg_metrics[metric_label] = metric_series.mean()
            max_metrics[metric_label] = metric_series.max()
            min_metrics[metric_label] = metric_series.min()

        return avg_metrics, max_metrics, min_metrics

    #Load client data by ID
    def get_client_data(self, client_id: str) -> Dict:
        try:
            response = self.client.table("empresas").select("*").eq("id", client_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            self._handle_error("Error loading client data", e)
            return {}
    
    #Load all machines for a specific client
    def get_client_machines(self, client_id: str) -> pd.DataFrame:
        try:
            response = self.client.table("maquinas").select("*").eq("id_empresa", client_id).execute()
            
            if not response.data:
                return pd.DataFrame()
                
            df = pd.DataFrame(response.data)
            df = self._convert_timestamps(df, ['data_registro', 'ultimo_contato'])
            return df
            
        except Exception as e:
            self._handle_error("Error loading client machines", e)
            return pd.DataFrame()
    
    #Load latest metrics for all machines of a client
    def get_latest_metrics_by_client(self, client_id: str, limit: int = 100) -> pd.DataFrame:
        try:
            # First get all machine IDs for this client
            machines_response = self.client.table("maquinas").select("id").eq("id_empresa", client_id).execute()
            
            if not machines_response.data:
                return pd.DataFrame()
                
            machine_ids = [machine['id'] for machine in machines_response.data]
            
            # Now get metrics for these machines
            metrics_response = self.client.table("metricas_maquina") \
                .select("*") \
                .in_("id_maquina", machine_ids) \
                .order("data_coleta", desc=True) \
                .limit(limit) \
                .execute()
            
            if not metrics_response.data:
                print(f"No metrics found for machines: {machine_ids}")
                return pd.DataFrame()
                
            # Get machine details for these metrics
            df = pd.DataFrame(metrics_response.data)
            df = self._convert_timestamps(df, ['data_coleta'])
            
            # If we need machine details, we can join them later
            return df
            
        except Exception as e:
            self._handle_error(f"Error loading client's metrics: {e}", e)
            return pd.DataFrame()
    #Load specific machine metrics history
    def get_machine_metrics_history(self, machine_id: str, days: int = 7) -> pd.DataFrame:
        try:
            # Print the machine ID we're querying for
            print(f"Getting metrics for machine ID: {machine_id}")
            
            # Direct query without start_date filter first to see if ANY records exist
            response = self.client.table("metricas_maquina") \
                .select("*") \
                .eq("id_maquina", machine_id) \
                .limit(5) \
                .execute()
            
            # Print raw response for debugging
            print(f"Raw response: {response}")
            print(f"Data count: {len(response.data) if response.data else 0}")
            
            # Now try with the date filter
            start_date = (datetime.now(pytz.UTC) - timedelta(days=days)).isoformat()
            
            response_with_date = self.client.table("metricas_maquina") \
                .select("*") \
                .eq("id_maquina", machine_id) \
                .gte("data_coleta", start_date) \
                .order("data_coleta", desc=True) \
                .execute()
            
            if not response_with_date.data:
                print(f"No recent metrics found for machine {machine_id} after {start_date}")
                
                if response.data:  # If we found records without the date filter
                    print("Returning older records instead")
                    df = pd.DataFrame(response.data)
                    df = self._convert_timestamps(df, ['data_coleta'])
                    return df
                return pd.DataFrame()
                    
            df = pd.DataFrame(response_with_date.data)
            df = self._convert_timestamps(df, ['data_coleta'])
            return df
            
        except Exception as e:
            self._handle_error(f"Error loading machine history: {str(e)}", e)
            return pd.DataFrame()
    
    #Stats summary (demo)
    def get_client_summary_stats(self, client_id: str) -> Dict:
        machines_df = self.get_client_machines(client_id)
        metrics_df = self.get_latest_metrics_by_client(client_id)
        
        if machines_df.empty:
            return {
                'total_machines': 0,
                'active_machines': 0,
                'offline_machines': 0,
                'avg_cpu_usage': 0,
                'avg_ram_usage': 0,
                'machines_with_issues': 0
            }
        
        total_machines = len(machines_df)
        
        #Active machines
        cutoff_time = datetime.now(pytz.UTC) - timedelta(hours=24)
        active_machines = len(machines_df[machines_df['ultimo_contato'] > cutoff_time]) if not machines_df.empty else 0
        offline_machines = total_machines - active_machines
        
        #Mean CPU and RAM usage from latest metrics
        avg_metrics, max_metrics, min_metrics = self._get_metrics_kpi(metrics_df)
        
        #Machines with issues (CPU > 80% or RAM > 90%) -> demo
        self._metrics_threshold = {
            'cpu_usage': 0.8,
            'ram_usage': 0.9,
            'cpu_temperature': 80,
            'gpu_temperature': 80
        }

        machines_with_issues = 0
        issue_series = pd.Series([])
        if not metrics_df.empty:
            for metric_label, metric_threshold in self._metrics_threshold.items():
                if metric_label not in metrics_df.columns:
                    continue

                high_metric = metrics_df[metric_label] > metric_threshold
                issue_series = issue_series | high_metric

            machines_with_issues = metrics_df["id_maquina"][issue_series].tolist()
        
        return {
            'total_machines': total_machines,
            'active_machines': active_machines,
            'offline_machines': offline_machines,
            'avg_metrics': avg_metrics,
            'max_metrics': max_metrics,
            'min_metrics': min_metrics,
            'machines_with_issues': machines_with_issues
        }
    
    #Load all relevant data for client dashboard
    def load_client_dashboard_data(self, client_id: Optional[str] = None) -> Dict:
        #If no client_id provided, try to get from session state
        if not client_id:
            client_id = st.session_state.get('client_id') if 'st' in globals() else None
        
        if not client_id:
            if 'st' in globals():
                st.error("Client ID not found. Please login again.")
            else:
                print("ERROR: Client ID not found")
            return {}
        
        #Load all relevant data
        client_data = self.get_client_data(client_id)
        machines_df = self.get_client_machines(client_id)
        metrics_df = self.get_latest_metrics_by_client(client_id)
        summary_stats = self.get_client_summary_stats(client_id)
        
        return {
            'client_info': client_data,
            'machines': machines_df,
            'latest_metrics': metrics_df,
            'summary_stats': summary_stats,
            'client_id': client_id
        }
