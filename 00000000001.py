# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import hashlib
import json

DB_FILE = "cache.db"

# ------------------------
# DATABASE SETUP & UTILS
# ------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qa_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            evaluation_config TEXT,
            cache_key TEXT UNIQUE,

            -- RAG fields
            question TEXT,
            context TEXT,
            answer TEXT,

            -- Summarization fields
            source_document TEXT,
            generated_summary TEXT,

            -- Final cached response
            response_json TEXT
        )
    """)

    # Index for fast lookup
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cache_key ON qa_cache(cache_key)")

    conn.commit()
    conn.close()


def get_connection():
    return sqlite3.connect(DB_FILE)


def compute_hash(*values: str) -> str:
    """Compute SHA256 hash from multiple string values."""
    combined = "||".join(values)
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()


# ------------------------
# FASTAPI SETUP
# ------------------------
app = FastAPI()


class QARequest(BaseModel):
    evaluation_config: str

    # RAG fields
    question: str | None = None
    context: str | None = None
    answer: str | None = None

    # Summarization fields
    source_document: str | None = None
    generated_summary: str | None = None


@app.on_event("startup")
def startup():
    init_db()


# ------------------------
# MAIN LOGIC: EVALUATE + CACHE
# ------------------------
@app.post("/evaluate")
def evaluate(req: QARequest):

    # -----------------------------
    # Compute the cache key (hash)
    # -----------------------------
    if req.evaluation_config.upper() == "RAG":
        cache_key = compute_hash(
            req.question or "",
            req.context or "",
            req.answer or ""
        )

    elif req.evaluation_config.upper() == "SUMMARIZATION":
        cache_key = compute_hash(
            req.source_document or "",
            req.generated_summary or ""
        )

    else:
        return {"error": "Unknown evaluation_config. Use RAG or SUMMARIZATION"}

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------
    # Check cache hit
    # -----------------------------
    cursor.execute(
        "SELECT response_json FROM qa_cache WHERE cache_key=?",
        (cache_key,)
    )
    row = cursor.fetchone()

    if row:
        conn.close()
        return {
            "cached": True,
            "response": json.loads(row[0])
        }

    # -----------------------------
    # PROCESSING (YOUR REAL LOGIC HERE)
    # Replace this with your LLM / evaluation logic
    # -----------------------------
    result = {
        "status": "ok",
        "score": 0.95,
        "message": f"Generated fresh response for {req.evaluation_config}"
    }

    response_json = json.dumps(result)

    # -----------------------------
    # Save the new response
    # -----------------------------
    cursor.execute("""
        INSERT OR REPLACE INTO qa_cache (
            evaluation_config,
            cache_key,

            question, context, answer,
            source_document, generated_summary,

            response_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        req.evaluation_config,
        cache_key,

        req.question,
        req.context,
        req.answer,

        req.source_document,
        req.generated_summary,

        response_json
    ))

    conn.commit()
    conn.close()

    return {
        "cached": False,
        "response": result
    }