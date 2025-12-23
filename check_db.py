from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_SERVICE_KEY')
)

result = supabase.table('knowledge_base').select('id', count='exact').execute()
print(f"Total rows: {result.count}")

recent = supabase.table('knowledge_base').select('id, title, created_at').order('created_at', desc=True).limit(10).execute()
print("\nMost recent 10:")
for doc in recent.data:
    print(f"  - {doc['title']}")