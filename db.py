import os

from dotenv import load_dotenv
from supabase import create_client

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


# Create a Supabase client using `SUPABASE_URL` and `SUPABASE_KEY` from .env
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_ANON = os.environ.get('SUPABASE_ANON')

if not SUPABASE_URL or not SUPABASE_ANON:
    # Client creation will fail later if keys are missing; keep a helpful message
    _supabase = None
else:
    _supabase = create_client(SUPABASE_URL, SUPABASE_ANON)


def insert_message(name: str | None, email: str | None, message: str):
    """Insert a message row into the `messages` table.

    Returns the inserted row (list) on success, raises Exception on failure.
    """
    if _supabase is None:
        raise RuntimeError('Supabase client not configured. Set SUPABASE_URL and SUPABASE_ANON in .env')

    payload = {
        'name': name,
        'email': email,
        'message': message,
    }
    resp = _supabase.table('messages').insert(payload).execute()
    # resp may be a dict-like object with keys `data` and `error`
    data = getattr(resp, 'data', None) or resp.get('data') if isinstance(resp, dict) else None
    error = getattr(resp, 'error', None) or resp.get('error') if isinstance(resp, dict) else None
    if error:
        raise RuntimeError(error)
    return data


def fetch_messages(limit: int = 10):
    """Fetch recent messages from Supabase `messages` table.

    Returns a list of dicts (could be empty).
    """
    if _supabase is None:
        raise RuntimeError('Supabase client not configured. Set SUPABASE_URL and SUPABASE_KEY in .env')

    resp = (
        _supabase
        .table('messages')
        .select('*')
        .order('created_at', desc=True)
        .limit(limit)
        .execute()
    )
    data = getattr(resp, 'data', None) or resp.get('data') if isinstance(resp, dict) else None
    error = getattr(resp, 'error', None) or resp.get('error') if isinstance(resp, dict) else None
    if error:
        raise RuntimeError(error)
    return data or []
