import sqlite3, json, pathlib, datetime as dt

import os
DB = pathlib.Path(os.environ.get("AGENT_DB_PATH") or pathlib.Path(__file__).resolve().parent / "calls.db")  # tests point this at a temp file

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, ts TEXT, lead_id TEXT, kind TEXT, payload TEXT);
CREATE TABLE IF NOT EXISTS dnc (lead_id TEXT PRIMARY KEY, ts TEXT, reason TEXT);
CREATE TABLE IF NOT EXISTS declines (lead_id TEXT, card_id TEXT, ts TEXT, reason TEXT, PRIMARY KEY (lead_id, card_id));
CREATE TABLE IF NOT EXISTS links (idem_key TEXT PRIMARY KEY, ts TEXT, lead_id TEXT, card_id TEXT, channel TEXT, reference TEXT);
CREATE TABLE IF NOT EXISTS callbacks (id INTEGER PRIMARY KEY, ts TEXT, lead_id TEXT, when_text TEXT, note TEXT, kind TEXT);
CREATE TABLE IF NOT EXISTS calls (conversation_id TEXT PRIMARY KEY, ts TEXT, lead_id TEXT, outcome TEXT, duration_secs INTEGER, analysis TEXT, transcript TEXT);
"""

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.executescript(SCHEMA)
    return c

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

def log(lead_id: str, kind: str, payload: dict):
    with conn() as c:
        c.execute("INSERT INTO events(ts, lead_id, kind, payload) VALUES (?,?,?,?)", (now(), lead_id, kind, json.dumps(payload)))

def events(lead_id: str | None = None, limit: int = 100):
    with conn() as c:
        q = "SELECT * FROM events" + (" WHERE lead_id=?" if lead_id else "") + " ORDER BY id DESC LIMIT ?"
        rows = c.execute(q, ((lead_id, limit) if lead_id else (limit,))).fetchall()
    return [dict(r) | {"payload": json.loads(r["payload"])} for r in rows]

def is_dnc(lead_id: str) -> bool:
    with conn() as c:
        return c.execute("SELECT 1 FROM dnc WHERE lead_id=?", (lead_id,)).fetchone() is not None

def add_dnc(lead_id: str, reason: str):
    with conn() as c:
        c.execute("INSERT OR REPLACE INTO dnc(lead_id, ts, reason) VALUES (?,?,?)", (lead_id, now(), reason))

def remove_dnc(lead_id: str):
    with conn() as c:
        c.execute("DELETE FROM dnc WHERE lead_id=?", (lead_id,))

def get_link(idem_key: str):
    with conn() as c:
        r = c.execute("SELECT * FROM links WHERE idem_key=?", (idem_key,)).fetchone()
    return dict(r) if r else None

def put_link(idem_key: str, lead_id: str, card_id: str, channel: str, reference: str):
    with conn() as c:
        c.execute("INSERT INTO links VALUES (?,?,?,?,?,?)", (idem_key, now(), lead_id, card_id, channel, reference))

def add_callback(lead_id: str, when_text: str, note: str, kind: str):
    with conn() as c:
        c.execute("INSERT INTO callbacks(ts, lead_id, when_text, note, kind) VALUES (?,?,?,?,?)", (now(), lead_id, when_text, note, kind))

def save_call(conversation_id: str, lead_id: str, outcome: str, duration: int, analysis: dict, transcript: list):
    with conn() as c:
        c.execute("INSERT OR REPLACE INTO calls VALUES (?,?,?,?,?,?,?)",
                  (conversation_id, now(), lead_id, outcome, duration, json.dumps(analysis), json.dumps(transcript)))

def calls(limit: int = 50):
    with conn() as c:
        rows = c.execute("SELECT conversation_id, ts, lead_id, outcome, duration_secs, analysis FROM calls ORDER BY ts DESC LIMIT ?", (limit,)).fetchall()
    return [dict(r) | {"analysis": json.loads(r["analysis"] or "{}")} for r in rows]


def mark_declined(lead_id: str, card_id: str, reason: str):
    with conn() as c:
        c.execute("INSERT OR REPLACE INTO declines VALUES (?,?,?,?)", (lead_id, card_id, now(), reason))

def declined(lead_id: str, card_id: str):
    with conn() as c:
        r = c.execute("SELECT ts, reason FROM declines WHERE lead_id=? AND card_id=?", (lead_id, card_id)).fetchone()
    return dict(r) if r else None

def clear_declines(lead_id: str):
    with conn() as c:
        c.execute("DELETE FROM declines WHERE lead_id=?", (lead_id,))
