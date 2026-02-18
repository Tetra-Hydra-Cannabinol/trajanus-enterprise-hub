import pickle
from pathlib import Path
from googleapiclient.discovery import build

CREDENTIALS_PATH = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/Credentials/token.pickle")
with open(CREDENTIALS_PATH, "rb") as token:
    creds = pickle.load(token)

service = build("drive", "v3", credentials=creds)

# Known folder IDs from reorganization
ai_dev_id = "1VVeotAPnechdDPfLnDTiOZqKA5ZEQDRM"

def get_path(file_id, depth=0):
    if depth > 10:
        return []
    try:
        file = service.files().get(fileId=file_id, fields="name, parents").execute()
        name = file.get("name")
        parents = file.get("parents", [])
        if parents:
            parent_path = get_path(parents[0], depth + 1)
            return parent_path + [name]
        return [name]
    except Exception as e:
        print(f"Error at depth {depth}: {e}")
        return []

print("Tracing path to AI-Development folder...")
path = get_path(ai_dev_id)
print()
print("=" * 60)
print("FULL GOOGLE DRIVE PATH:")
print("=" * 60)
print(" > ".join(path))
print()
print("Direct link:")
print(f"https://drive.google.com/drive/folders/{ai_dev_id}")
