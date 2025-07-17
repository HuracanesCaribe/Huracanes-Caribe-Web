from pathlib import Path

print("[DEBUG] main.py started")

class Reporter:
    def __init__(self, issue_dt):
        timestamp_str = issue_dt.strftime("%Y%m%dT%H%MZ")
        self.rows = [("area", "invest", "status", "reason")]

        base_dir = Path(__file__).resolve().parent
        self.path = base_dir / f"decision_{timestamp_str}.csv"

    def log(self, area, invest, status, reason):
        self.rows.append((area, invest, status, reason))

    def dump(self):
        print(f"[DEBUG] Saving debug CSV to: {self.path}")  # Add this line
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w") as f:
            for row in self.rows:
                f.write(",".join("" if r is None else str(r) for r in row) + "\n")

def build_outlook():
    print("[DEBUG] build_outlook called")
    # ... rest of the function ...
