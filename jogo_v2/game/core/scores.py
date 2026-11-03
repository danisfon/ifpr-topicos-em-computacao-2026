import json
import unicodedata
from datetime import datetime, timezone
from pathlib import Path


class ScoreStore:
    def __init__(self, path: Path | None = None):
        self.path = path or Path(__file__).resolve().parents[2] / 'data' / 'scores.json'

    @staticmethod
    def clean_name(name: str) -> str:
        return ' '.join(unicodedata.normalize('NFKC', name).split())

    @classmethod
    def name_key(cls, name: str) -> str:
        return cls.clean_name(name).casefold()

    @property
    def players_path(self) -> Path:
        return self.path.with_name('players.json')

    def registered_names(self) -> list[str]:
        names = []
        if self.players_path.exists():
            names = json.loads(self.players_path.read_text(encoding='utf-8'))
            if not isinstance(names, list) or any(not isinstance(name, str) for name in names):
                raise ValueError('Cadastro inválido; arquivo preservado.')
        return names + [row['name'] for row in self.read()]

    def validate_names(self, names, registered) -> list[str]:
        used = {self.name_key(name) for name in registered}
        errors = []
        for i, name in enumerate(names):
            clean = self.clean_name(name)
            if not clean:
                errors.append('Digite um nome para este piloto.')
            elif len(clean) > 18:
                errors.append('Use no máximo 18 caracteres.')
            elif self.name_key(clean) in used:
                errors.append('Este nome já foi usado. Escolha outro.')
            elif any(self.name_key(clean) == self.name_key(other) for other in names[:i]):
                errors.append('Os pilotos precisam de nomes diferentes.')
            else:
                errors.append('')
        return errors

    def register_names(self, names) -> tuple[str, str]:
        registered = self.registered_names()
        errors = self.validate_names(names, registered)
        if any(errors):
            raise ValueError(next(error for error in errors if error))
        cleaned = tuple(self.clean_name(name) for name in names)
        self.players_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.players_path.with_suffix('.tmp')
        temporary.write_text(json.dumps(list(dict.fromkeys(registered + list(cleaned))), ensure_ascii=False, indent=2), encoding='utf-8')
        temporary.replace(self.players_path)
        return cleaned

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
