from supabase import create_client, Client
import os, dotenv
dotenv.load_dotenv()


url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_ANON")

if url and key:
    supabase: Client = create_client(url, key)
    print("Successful connection till now.")
else:
    print("Failed to connect to Supabase. SUPABASE_URL and SUPABASE_ANON must be set in the environment variables.")
