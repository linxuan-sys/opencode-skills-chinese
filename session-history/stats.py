import sqlite3, json
from pathlib import Path

DB = Path(__import__("os").environ.get("OPENCODE_DB", str(Path.home() / ".local/share/opencode/opencode.db")))


def show_stats():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    print("=" * 50)
    print("  Session Statistics")
    print("=" * 50)

    c.execute("SELECT COUNT(*) FROM session")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM session WHERE time_archived IS NOT NULL")
    archived = c.fetchone()[0]
    active = total - archived
    print(f"\nTotal sessions: {total}")
    print(f"  Active:   {active} ({active * 100 // total}%)")
    print(f"  Archived: {archived} ({archived * 100 // total}%)")

    print(f"\n{'─' * 50}")
    print("  Top 10 Models by Usage")
    print(f"{'─' * 50}")
    c.execute("SELECT model FROM session")
    models = {}
    for row in c.fetchall():
        try:
            m = json.loads(row[0])
            m_id = m.get("id", "unknown")
        except Exception:
            m_id = "unknown"
        models[m_id] = models.get(m_id, 0) + 1
    for m_id, cnt in sorted(models.items(), key=lambda x: -x[1])[:10]:
        bar = "█" * min(cnt, 30)
        print(f"  {cnt:3d}  {bar}  {m_id[:50]}")

    print(f"\n{'─' * 50}")
    print("  Top 5 Token Consumption")
    print(f"{'─' * 50}")
    c.execute(
        "SELECT title, model, tokens_input + tokens_output AS total_tokens "
        "FROM session ORDER BY total_tokens DESC LIMIT 5"
    )
    for i, r in enumerate(c.fetchall(), 1):
        title, model, tt = r
        title_clean = (title or "(Untitled)").replace("\n", " ")[:35]
        print(f"  {i}. {tt:>10,}  {title_clean}")

    print(f"\n{'─' * 50}")
    print("  Sessions per Month")
    print(f"{'─' * 50}")
    c.execute("""
        SELECT strftime('%Y-%m', time_created/1000, 'unixepoch') AS ym,
               COUNT(*) AS cnt
        FROM session
        GROUP BY ym
        ORDER BY ym DESC
    """)
    for r in c.fetchall():
        ym, cnt = r
        bar = "█" * cnt
        print(f"  {ym}: {cnt:3d}  {bar}")

    print(f"\n{'─' * 50}")
    print("  Agent Distribution")
    print(f"{'─' * 50}")
    c.execute("SELECT agent, COUNT(*) AS cnt FROM session GROUP BY agent ORDER BY cnt DESC")
    for r in c.fetchall():
        agent, cnt = r
        if agent:
            bar = "█" * min(cnt, 30)
            print(f"  {agent:15}  {cnt:3d}  {bar}")

    conn.close()


if __name__ == "__main__":
    show_stats()
