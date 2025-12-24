#!/usr/bin/env python3
"""
TKB Hierarchy Verification Script
Verifies the reorganization of TKB documents into hierarchical structure.
"""

import pickle
from pathlib import Path
from googleapiclient.discovery import build

# Load credentials
CREDENTIALS_PATH = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/Credentials/token.pickle")
with open(CREDENTIALS_PATH, 'rb') as token:
    creds = pickle.load(token)

service = build('drive', 'v3', credentials=creds)

# Folder mapping from reorganization
FOLDER_MAPPING = {
    "AI-Development": {
        "id": "1VVeotAPnechdDPfLnDTiOZqKA5ZEQDRM",
        "subcategories": {
            "Vector-Databases": {
                "id": "1CyPdA2P8L6QX9kgO-zVUPsWlq33kIALH",
                "subcategories": {
                    "Pgvector": "1ZEXnEvPNY5UJ4kG_AdSBpD7tVwT-Ps7s",
                    "Embeddings": "1JTJokrAHCvhCDL_UCLOeZaG7zrMZCnKr"
                }
            },
            "RAG-Systems": {
                "id": "1yen7kXl_OEaOfLq7xPXCsefEB8XiZS2y",
                "subcategories": {
                    "Chunking-Strategies": "1HyzOUkL4LXlieqVduH9oK86_KiSAlvio",
                    "Retrieval-Optimization": "12vANqS-5hxMMvMKg6OKv0AuAoQz7BHbd",
                    "RAG-Monitoring": "1JLiW8EYkukpL8skddI3Rdkg2MichhjvM"
                }
            },
            "MCP-Protocol": {
                "id": "1F80KfxPqtAmEHmdBnQSnmnD-AdtjfnZl",
                "subcategories": {
                    "MCP-Servers": "1E3hOFQayFqd1jIHFXYoszOsH8J-wNIvU",
                    "MCP-Integration": "1phzW4iLMRd8LXzSJ4_BE4OdmAyIvvIhB",
                    "MCP-Best-Practices": "1VjCg-62mKv4ZRuqBkx2tXS4N_YL0_Y4s"
                }
            },
            "Agents": {
                "id": "1m7Jfg4yYc0ju6y66Ze0gYofjTGH6-AKY",
                "subcategories": {
                    "Claude-Agent-SDK": "1PZgmgTK2rRX56fT7XplUTq9UsBZ_52QA",
                    "Multi-Agent-Systems": "15mZAR2aKo4GMG0hTLbJP8je-Waq1yG9X",
                    "Agent-Patterns": "1vse4iTsXUuwCgxQ4N53BUKoVKodEt5lQ"
                }
            },
            "Playwright-Testing": {
                "id": "1IejLg3KXaPP_P0V3lY7VV0CikxcOamGz",
                "subcategories": {
                    "Screenshots": "1L6eGQAHfzZVXnfnRHjBdpX3sLULkRCYk",
                    "Testing-Guides": "1xWDbJgEb-M5RmSIdipAqrxr4sEeiAj2m"
                }
            },
            "Google-Cloud-APIs": {
                "id": "1Ig9rBkVlmnInkoFAPp4bU1wTZjb7cYzv",
                "subcategories": {
                    "Drive-Storage": "1hnaXAL3d_3jl_77-PjvFbz-ZH86qo3kd"
                }
            },
            "Supabase": {
                "id": "1_D1_jIk4Es584_boGBuufU-SK3fD-7RF",
                "subcategories": {
                    "Connection-Management": "1u9c20bMPGqqQUbUuDlxkWSHzIDvsIKKj",
                    "Row-Level-Security": "1-T8-rC8IPibhaxiGhTj5OPHDws2kdobZ"
                }
            },
            "Uncategorized": {"id": "1S6o0H3B-0mQr8vsz9AjccfDkS6ot0rS2", "subcategories": {}}
        }
    },
    "Software-Tools": {
        "id": "1xMWr71AGbZOfnOjAy8IoVOt75Kf_KMAx",
        "subcategories": {
            "Electron": {
                "id": "1Z013rGfmAq0cajx-owYhZbQC1pESX5wb",
                "subcategories": {
                    "IPC-Communication": "1tIZlepsnA6Ev9k-a3VbPHtuVrWCPWUYS",
                    "Python-Integration": "1XG8pUuPmDDe640Hq3Fpv9Oco03rVRVLw",
                    "Security-Architecture": "1ZKa6AwEoGP2UDoYFB-fAd_FR2eJVHno-"
                }
            },
            "Google-APIs": {
                "id": "190qRynHfLoM3tRzm5ZxOL3gBobCN-acB",
                "subcategories": {
                    "Drive-API": "15KqUJdJuWviN1X6QzgNpOSEhqQjUzmYE",
                    "Docs-API": "1IANgmpt01BjVt96qtEcsnkCnBJflMFLY"
                }
            },
            "Python-Development": {
                "id": "1e1R06cPSb33ThdJa2BQ8kxcfPX2WZvdf",
                "subcategories": {
                    "Subprocess": "1R3FJJwZNu99dLK7BNLVbO1Z91UvliWk3",
                    "Security": "1Ima9-fAHJQBEJbDgGh-9osAxCZ7_XCSv"
                }
            },
            "JavaScript-Libraries": {
                "id": "1AEGn4ET1C_jrkQlqZU3r0HrxhM_N1QTT",
                "subcategories": {
                    "File-Management": "17PSc521QnP1IfdVNLFsFK_Z_7pXYZ-Nq",
                    "Frameworks": "1elmLVWqTjE6UldS4lFE-J1Otsn-GFSH-"
                }
            },
            "Supabase-Tools": {"id": "187RbdafOWb78aiW68NzbILe79p5kUpfZ", "subcategories": {}},
            "Uncategorized": {"id": "1vDXU5KuwMim6Ec8ISFvRsz7dwJ1yEWrC", "subcategories": {}}
        }
    },
    "Technical-Guides": {
        "id": "1guwUKpc4vUnsuZ0pibalGV0jzBnYZO1n",
        "subcategories": {
            "MCP-Setup": {"id": "1JgNsEn2kO9pvBzgPi2sJXCqIaNVVft2r", "subcategories": {}},
            "Node-Documentation": {"id": "1_-QliWlVIUWkWJhm5FdOPetI3rM_41kz", "subcategories": {}},
            "Documentation-Standards": {"id": "19YX43HKRLrXTGaqCXhDj7XdKrl1x2p-2", "subcategories": {}},
            "Playwright-Setup": {"id": "1CKw3j_NnX8fNNOPniEaZXiT1JbghN1S7", "subcategories": {}},
            "Python-Guides": {"id": "1LLEbgYAYLF0SpLP17VDrvPnuB3rHEkzL", "subcategories": {}},
            "Uncategorized": {"id": "10ljPu1uN01qSFh1zn4BxV4VabiE_N-fo", "subcategories": {}}
        }
    },
    "QCM-Quality": {
        "id": "1ehvTr0P1xQzpKmqOVyiIE-FHR8B66Zpv",
        "subcategories": {
            "Documentation": {"id": "1eaDQTMhG6CPKFaIDiY4_AB-8QQ16dS3W", "subcategories": {}},
            "Uncategorized": {"id": "1SikVzdCNx0IYD3kXnQYqRXiJhTZXqyRY", "subcategories": {}}
        }
    }
}

def count_docs_in_folder(folder_id):
    """Count Google Docs in a specific folder."""
    query = f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.document' and trashed = false"
    results = service.files().list(q=query, pageSize=100, fields='files(id, name)').execute()
    return len(results.get('files', []))

def traverse_hierarchy(structure, indent=0, path=""):
    """Traverse folder hierarchy and count documents."""
    total = 0
    report_lines = []

    for name, data in structure.items():
        folder_id = data["id"] if isinstance(data, dict) else data
        subcats = data.get("subcategories", {}) if isinstance(data, dict) else {}

        current_path = f"{path}/{name}" if path else name
        count = count_docs_in_folder(folder_id)
        total += count

        prefix = "  " * indent
        entry = f"{prefix}{name}: {count} docs"
        report_lines.append(entry)
        try:
            print(entry)
        except UnicodeEncodeError:
            print(entry.encode('ascii', 'replace').decode('ascii'))

        if subcats:
            sub_total, sub_lines = traverse_hierarchy(subcats, indent + 1, current_path)
            total += sub_total
            report_lines.extend(sub_lines)

    return total, report_lines

print("=" * 60)
print("TKB HIERARCHICAL VERIFICATION REPORT")
print("=" * 60)
print()

total_docs, report = traverse_hierarchy(FOLDER_MAPPING)

print()
print("=" * 60)
print(f"TOTAL DOCUMENTS: {total_docs}")
print("=" * 60)

# Check for any docs left at TKB root
tkb_root_id = "1-TiF-1XsOJXHLBmBGqW-FdQqHC6wXSRC"
root_count = count_docs_in_folder(tkb_root_id)
print(f"\nDocs remaining at TKB root: {root_count}")

if root_count == 0 and total_docs > 160:
    print("\n[SUCCESS] All documents properly organized into hierarchy!")
else:
    print(f"\n[WARNING] Check needed - root has {root_count} orphan docs")
