"""
Подготовка README к публикации на PyPI:
относительные ссылки (типа <a href="README.en.md">) и GitHub-алерты (типа "> [!WARNING]") преобразуются в абсолютные.

Скрипт правит README на месте, запускается только в одноразовом CI-checkout'е прямо перед ``python -m build``.
Результат не коммитится: на GitHub README должен остаться с относительными ссылками и живыми алертами.

Запуск:
    python scripts/prepare_pypi_readme.py            # только при CI=true
    python scripts/prepare_pypi_readme.py --force    # локально, осознанно
    python scripts/prepare_pypi_readme.py --dry-run  # показать замены, ничего не записывая

Повторный запуск скрипта ничего не меняет (абсолютные ссылки пропускаются).
"""

from __future__ import annotations
from pathlib import Path

import argparse
import os
import re
import sys

DEFAULT_REPO = "n1xsi/PyCustomRand"
DEFAULT_BRANCH = "main"

ABSOLUTE_PREFIXES = ("http://", "https://", "//", "#", "mailto:", "data:", "tel:")

ALERT_LABELS = {
    "NOTE": "ℹ️ Note",
    "TIP": "💡 Tip",
    "IMPORTANT": "❗ Important",
    "WARNING": "⚠️ Warning",
    "CAUTION": "🔴 Caution",
}

# Ссылки в Markdown: группы — префикс "!" (картинка), текст, путь, необязательный title
MD_LINK_RE = re.compile(r'(!?)\[([^\]]*)\]\(\s*([^)\s]+)((?:\s+"[^"]*")?)\s*\)')

# Атрибуты href/src в HTML-вставках
HTML_ATTR_RE = re.compile(r'\b(href|src)=(["\'])([^"\']+)\2')

# Строка GitHub-алерта: "> [!WARNING]" с возможными вложенными "> "
ALERT_RE = re.compile(r"^(?P<quote>(?:\s*>\s*)+)\[!(?P<kind>[A-Z]+)\]\s*$")


def is_relative(target: str) -> bool:
    """Проверяет, что ссылка указывает на файл в репозитории, а не во внешний мир."""
    target = target.strip()
    if not target:
        return False
    return not target.lower().startswith(ABSOLUTE_PREFIXES)


def to_absolute(target: str, repo: str, branch: str, raw: bool) -> str:
    """Превращает относительный путь в абсолютный GitHub-URL.

    Для картинок нужен raw-домен (иначе отдастся HTML-страница вместо файла),
    для обычных ссылок — привычный blob-URL.
    """
    path = target.lstrip("./")
    # Разделение путу и хвоста с якорем/запросом, чтобы не поломать "docs/file.md#section"
    match = re.match(r"([^#?]*)([#?].*)?$", path)
    file_part = match.group(1)
    suffix = match.group(2) or ""

    if raw:
        base = f"https://raw.githubusercontent.com/{repo}/{branch}/"
    else:
        base = f"https://github.com/{repo}/blob/{branch}/"
    return f"{base}{file_part}{suffix}"


def convert(text: str, repo: str, branch: str) -> tuple[str, list[str]]:
    """Возвращает преобразованный текст и список описаний внесённых замен."""
    changes: list[str] = []
    out_lines: list[str] = []
    in_fence = False
    fence_marker = ""

    for lineno, line in enumerate(text.splitlines(keepends=True), start=1):
        stripped = line.lstrip()
        fence_match = re.match(r"(```+|~~~+)", stripped)
        if fence_match:
            marker = fence_match.group(1)[:3]
            if not in_fence:
                in_fence, fence_marker = True, marker
            elif marker == fence_marker:
                in_fence, fence_marker = False, ""
            out_lines.append(line)
            continue

        if in_fence:
            out_lines.append(line)
            continue

        # GitHub-алерты -> обычная жирная строка в цитате
        alert_match = ALERT_RE.match(line.rstrip("\n"))
        if alert_match and alert_match.group("kind") in ALERT_LABELS:
            kind = alert_match.group("kind")
            label = ALERT_LABELS[kind]
            newline = "\n" if line.endswith("\n") else ""
            line = f"{alert_match.group('quote')}**{label}**{newline}"
            changes.append(f"  строка {lineno}: [!{kind}] -> **{label}**")
            out_lines.append(line)
            continue

        # Относительные Markdown-ссылки -> абсолютные
        def md_sub(m: re.Match) -> str:
            bang, label, target, title = m.groups()
            if not is_relative(target):
                return m.group(0)
            absolute = to_absolute(target, repo, branch, raw=bool(bang))
            changes.append(f"  строка {lineno}: {target} -> {absolute}")
            return f"{bang}[{label}]({absolute}{title})"

        line = MD_LINK_RE.sub(md_sub, line)

        # Относительные href/src в HTML-вставках -> абсолютные
        def html_sub(m: re.Match) -> str:
            attr, quote, target = m.groups()
            if not is_relative(target):
                return m.group(0)
            absolute = to_absolute(target, repo, branch, raw=(attr == "src"))
            changes.append(f"  строка {lineno}: {attr}={target} -> {absolute}")
            return f"{attr}={quote}{absolute}{quote}"

        line = HTML_ATTR_RE.sub(html_sub, line)
        out_lines.append(line)

    return "".join(out_lines), changes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "files", nargs="*", default=["README.md"], type=Path,
        help="Файлы для обработки (по умолчанию README.md)",
    )
    parser.add_argument(
        "--repo", default=os.environ.get("GITHUB_REPOSITORY") or DEFAULT_REPO,
        help="Репозиторий в формате owner/name",
    )
    parser.add_argument(
        "--branch", default=DEFAULT_BRANCH,
        help="Ветка, на которую указывают абсолютные ссылки",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Показать замены, ничего не записывая",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Разрешить запуск вне CI (файлы будут перезаписаны!)",
    )
    args = parser.parse_args(argv)

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    # Защита от случайного локального запуска:
    # скрипт перезаписывает README, и такие правки легко утекут в коммит
    in_ci = os.environ.get("CI", "").lower() in {"1", "true", "yes"}
    if not (in_ci or args.force or args.dry_run):
        print(
            "Отказ: скрипт перезаписывает README на месте и предназначен для CI.\n"
            "Запустите с --dry-run, чтобы посмотреть замены, "
            "или с --force, если правка файлов в рабочей копии — то, что нужно.",
            file=sys.stderr,
        )
        return 2

    print(f"Подготовка README для PyPI (репозиторий {args.repo}, ветка {args.branch})")

    exit_code = 0
    for path in args.files:
        if not path.is_file():
            print(f"Отказ: файл не найден — {path}", file=sys.stderr)
            exit_code = 1
            continue

        original = path.read_text(encoding="utf-8")
        converted, changes = convert(original, args.repo, args.branch)

        if not changes:
            print(f"{path}: правок не требуется")
            continue

        print(f"{path}: замен — {len(changes)}")
        for change in changes:
            print(change)

        if args.dry_run:
            print(f"{path}: --dry-run, файл не изменён")
        else:
            path.write_text(converted, encoding="utf-8")
            print(f"{path}: записан")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
