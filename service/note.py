from dataclasses import dataclass
from pathlib import Path
import re


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
        if not preview:
            return None

        # Упрощённое "разметочное" очищение для превью:
        # - убираем заголовки (#, ## и т.п. в начале строки)
        # - убираем маркеры списков (-, *, +, 1.)
        # - убираем обрамления **bold**, *italic*, `code`, ```блоки```
        # - убираем одиночные # внутри, если они окружены пробелами
        cleaned = preview
        # заголовки
        cleaned = re.sub(r'^\s*#{1,6}\s*', '', cleaned, flags=re.MULTILINE)
        # маркеры списков
        cleaned = re.sub(r'^\s*[-*+]\s+', '', cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r'^\s*\d+\.\s+', '', cleaned, flags=re.MULTILINE)
        # обрамляющие символы форматирования
        cleaned = re.sub(r'`{3}.*?`{3}', '', cleaned, flags=re.DOTALL)  # многострочные блоки
        cleaned = re.sub(r'`([^`]+)`', r'\1', cleaned)
        cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)
        cleaned = re.sub(r'\*([^*]+)\*', r'\1', cleaned)
        cleaned = re.sub(r'__([^_]+)__', r'\1', cleaned)
        cleaned = re.sub(r'_([^_]+)_', r'\1', cleaned)
        # одиночные # между пробелами
        cleaned = re.sub(r'\s#\s', ' ', cleaned)

        cleaned = cleaned.strip()
        return cleaned or None
