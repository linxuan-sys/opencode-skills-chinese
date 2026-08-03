import sqlite3, json, datetime, sys
from pathlib import Path

DB = Path(__import__("os").environ.get("OPENCODE_DB", str(Path.home() / ".local/share/opencode/opencode.db")))


def view_session(session_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        "SELECT title, time_created, time_archived, model, agent, directory, tokens_input, tokens_output "
        "FROM session WHERE id = ?", (session_id,)
    )
    s = c.fetchone()
    if not s:
        print(f"Session not found: {session_id}")
        conn.close()
        return
    title, tc, ta, model, agent, directory, ti, to_ = s
    tc_str = datetime.datetime.fromtimestamp(tc / 1000).strftime("%Y-%m-%d %H:%M:%S")
    ta_str = datetime.datetime.fromtimestamp(ta / 1000).strftime("%Y-%m-%d %H:%M:%S") if ta else "Not archived"
    print("=" * 60)
    print(f"  Title: {title or '(Untitled)'}")
    print(f"  Time:  {tc_str}")
    print(f"  Archived: {ta_str}")
    print(f"  Agent: {agent}  |  Directory: {directory}")
    print(f"  Tokens: in↑{ti:,} out↓{to_:,}")
    print(f"  ID: {session_id}")
    print("=" * 60 + "\n")

    c.execute("""
        SELECT m.id, m.time_created, p.id as part_id, p.data
        FROM part p
        JOIN message m ON p.message_id = m.id
        WHERE m.session_id = ?
        ORDER BY m.time_created, p.id
    """, (session_id,))
    parts = c.fetchall()
    print(f"Total {len(parts)} message part(s)\n")

    for mid, tc, part_id, data in parts:
        try:
            d = json.loads(data)
            dtype = d.get("type", "")
            ts = datetime.datetime.fromtimestamp(tc / 1000).strftime("%H:%M:%S") if tc else ""

            if dtype == "text":
                txt = d.get("text", "")
                role_info = " (user)" if d.get("role") == "user" else ""
                if txt:
                    role_label = role_info[1:] if role_info else "assistant"
                    print(f"[{ts}] {role_label}:")
                    for line in txt.split("\n"):
                        if line.strip():
                            print(f"  {line}")
                    print()

            elif dtype == "tool":
                tool_name = d.get("tool", "")
                state = d.get("state", {})
                status = state.get("status", "")
                inp = state.get("input", {})
                outp = state.get("output", "")
                print(f"[{ts}] 🛠 {tool_name} [{status}]")
                inp_s = json.dumps(inp, ensure_ascii=False)[:400]
                print(f"    input: {inp_s}")
                if outp:
                    outp_s = str(outp)[:400]
                    print(f"    output: {outp_s}")
                print()

            elif dtype == "image":
                print(f"[{ts}] 🖼 image: {str(d)[:400]}\n")

        except Exception:
            pass

    conn.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="View opencode session message history.")
    parser.add_argument("session_id", help="Session ID (e.g. ses_xxx)")
    args = parser.parse_args()
    view_session(args.session_id)
