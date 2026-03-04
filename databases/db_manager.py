import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- User Operations ---
async def add_user(user_id: int, username: str, full_name: str):
    data = {
        "id": user_id,
        "username": username,
        "full_name": full_name
    }
    supabase.table("users").upsert(data).execute()

async def get_user(user_id: int):
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    return response.data[0] if response.data else None

async def get_all_users():
    response = supabase.table("users").select("*").execute()
    return response.data

async def get_users_count():
    response = supabase.table("users").select("id", count="exact").execute()
    return response.count

async def block_user(user_id: int, status: bool = True):
    supabase.table("users").update({"is_blocked": status}).eq("id", user_id).execute()

# --- Download Operations ---
async def log_download(user_id: int, url: str, file_type: str, platform: str = "unknown"):
    data = {
        "user_id": user_id,
        "url": url,
        "file_type": file_type,
        "platform": platform
    }
    supabase.table("downloads").insert(data).execute()

async def get_downloads_count():
    response = supabase.table("downloads").select("id", count="exact").execute()
    return response.count

# --- Settings Operations ---
async def get_setting(key: str):
    response = supabase.table("settings").select("value").eq("key", key).execute()
    return response.data[0]["value"] if response.data else None

async def update_setting(key: str, value: str):
    supabase.table("settings").upsert({"key": key, "value": value}).execute()
