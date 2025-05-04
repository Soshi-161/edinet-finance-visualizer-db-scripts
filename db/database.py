from supabase import create_client, Client
from dotenv import load_dotenv
import os

def create_supabase_client() -> Client:
    # Load environment variables from .env file
    load_dotenv()

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise EnvironmentError("Please set the SUPABASE_URL and SUPABASE_KEY environment variables.")

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase

if __name__ == "__main__":
    # Example usage
    supabase_client = create_supabase_client()
    print("Supabase client created successfully (database.py).")
    # You can now use supabase_client to interact with your Supabase database.