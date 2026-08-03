import sqlite3, json, datetime, sys
from pathlib import Path

DB = Path(__import__("os").environ.get("OPENCODE_DB", str(Path.home() / ".local/share/opencode/opencode.db")))


def search_sessions(keyword="", status="all", model_filter="", date_from="", date_to="", limit=50):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    conditions = []
    params = []
    if keyword:
        conditions.append(
            "(s.title LIKE ? OR s.id IN (SELECT DISTINCT m.session_id FROM message m WHERE m.data LIKE ?))"
        )
        params.extend([f"%{keyword}%", f"%{keyword}%"])
    if status == "archived":
        conditions.append("s.time_archived IS NOT NULL")
    elif status == "active":
        conditions.append("s.time_archived IS NULL")
    if model_filter:
        conditions.append("s.model LIKE ?")
        params.append(f"%{model_filter}%")
    if date_from:
        conditions.append("s.time_created >= ?")
        params.append(int(datetime.datetime.strptime(date_from, "%Y-%m-%d").timestamp() * 1000))
    if date_to:
        conditions.append("s.time_created <= ?")
        params.append(int(datetime.datetime.strptime(date_to + " 23:59:59", "%Y-%m-%d %H:%M:%S").timestamp() * 1000))
    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    c.execute(f"""
        SELECT s.id, s.title, s.time_created, s.time_archived,
               s.model, s.tokens_input, s.tokens_output, s.cost, s.agent, s.directory
        FROM session s
        {where}
        ORDER BY s.time_created DESC
        LIMIT ?
    """, params + [limit])
    rows = c.fetchall()
    print(f"Found {len(rows)} result(s)\n")
    for r in rows:
        sid, title, tc, ta, model, ti, to_, cost, agent, directory = r
        tc_str = datetime.datetime.fromtimestamp(tc / 1000).strftime("%Y-%m-%d %H:%M:%S")
        ta_str = datetime.datetime.fromtimestamp(ta / 1000).strftime("%Y-%m-%d %H:%M:%S") if ta else "-"
        try:
            m = json.loads(model)
            m_id = m.get("id", model)
        except Exception:
            m_id = str(model)[:35]
        status_str = "[Archived]" if ta else "[Active]"
        title_clean = (title or "(Untitled)").replace("\n", " ")[:45]
        print(f"{status_str} {tc_str} | {title_clean}")
        print(f"        Model: {m_id[:40]} | Tokens: in↑{ti:,} out↓{to_:,} | agent: {agent}")
        print(f"        ID: {sid}")
        if directory:
            print(f"        Directory: {directory}")
        print()
    conn.close()
    return rows


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Search opencode session history.")
    parser.add_argument("keyword", nargs="?", default="", help="Title keyword to search")
    parser.add_argument("status", nargs="?", default="all", choices=["active", "archived", "all"])
    parser.add_argument("model", nargs="?", default="", help="Model ID keyword filter")
    parser.add_argument("date_from", nargs="?", default="", help="Start date (YYYY-MM-DD)")
    parser.add_argument("date_to", nargs="?", default="", help="End date (YYYY-MM-DD)")
    args = parser.parse_args()
    search_sessions(keyword=args.keyword, status=args.status, model_filter=args.model,
                    date_from=args.date_from, date_to=args.date_to)
