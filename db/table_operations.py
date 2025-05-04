from supabase import Client

def create_campanies_table(supabase: Client) -> None:
    """Create the 'campanies' table in the Supabase database."""
    # Define the schema for the 'campanies' table
    