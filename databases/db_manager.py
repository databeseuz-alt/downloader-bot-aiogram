import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def add_user(user_id: int, username: str, full_name: str):
    data = {
        "id": user_id,
        "username": username,
        "full_name": full_name
    }
    supabase.table("users").upsert(data).execute()

async def get_all_users():
    response = supabase.table("users").select("*").execute()
    return response.data

async def get_users_count():
    response = supabase.table("users").select("id", count="exact").execute()
    return response.count

async def log_download(user_id: int, url: str, file_type: str):
    data = {
        "user_id": user_id,
        "url": url,
        "file_type": file_type
    }
    supabase.table("downloads").insert(data).execute()
