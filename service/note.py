from dataclasses import dataclass
from pathlib import Path


@dataclass
class NoteService:
    notes_dir: Path

    def __post_init__(self):
        self.notes_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, task_id: int) -> Path:
        return self.notes_dir / f"task_{task_id}.md"

    def read(self, task_id: int) -> str:
        path = self._path(task_id)
        if not path.exists():
            return ''
        return path.read_text(encoding='utf-8')

    def write(self, task_id: int, content: str) -> None:
        self._path(task_id).write_text(content or '', encoding='utf-8')

    def preview(self, content: str) -> str | None:
        raw = (content or '').strip()
        if not raw:
            return None
        lines = raw.splitlines()
        preview = '\n'.join(lines[:3]).strip()
        return preview or None
