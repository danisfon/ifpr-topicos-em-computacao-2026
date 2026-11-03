import json
from datetime import datetime, timezone
from pathlib import Path


class ScoreStore:
    def __init__(self, path: Path | None = None):
        self.path = path or Path(__file__).resolve().parents[2] / 'data' / 'scores.json'

    def read(self) -> list[dict]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding='utf-8'))
        if not isinstance(data, list) or any(
            not isinstance(row, dict) or not isinstance(row.get('name'), str)
            or type(row.get('score')) is not int or row['score'] < 0
            or not isinstance(row.get('date'), str) for row in data
        ):
            raise ValueError('Histórico inválido; arquivo preservado.')
        return sorted(data, key=lambda row: row['score'], reverse=True)

    def save_match(self, players) -> None:
        rows = self.read()
        date = datetime.now(timezone.utc).isoformat(timespec='seconds')
        rows.extend({'name': p.name, 'score': p.score, 'date': date} for p in players)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix('.tmp')
        temporary.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
        temporary.replace(self.path)
