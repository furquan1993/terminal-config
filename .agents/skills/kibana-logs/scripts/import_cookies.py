#!/usr/bin/env python3
"""Import a copied Cookie header without displaying credentials (Python 3.8+)."""
import argparse
import getpass
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def report(**fields):
    for key, value in fields.items():
        print(f'{key}: {json.dumps(value, ensure_ascii=False)}')


class Parser(argparse.ArgumentParser):
    def error(self, message):
        # argparse's usual error can echo accidentally pasted credentials.
        report(error='Invalid arguments.', help='Use --help; never pass cookies as arguments.')
        raise SystemExit(2)


def cookie_rows(raw, host):
    if raw.lower().startswith('cookie:'):
        raw = raw[7:]
    raw = raw.strip()
    if not raw or any(ord(c) < 32 or ord(c) == 127 for c in raw):
        raise ValueError('Expected one nonempty Cookie header value.')
    rows, names = [], set()
    for item in raw.split(';'):
        name, separator, value = item.strip().partition('=')
        if (not separator or not re.fullmatch(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+", name)
                or any(ord(c) > 126 or c.isspace() for c in value)):
            raise ValueError('Invalid Cookie header; copy only the header value.')
        if name in names:
            raise ValueError('Duplicate cookie names; select a request with an unambiguous Cookie header.')
        names.add(name)
        rows.append('\t'.join([host, 'FALSE', '/', 'TRUE', '0', name, value]))
    return '# Netscape HTTP Cookie File\n' + '\n'.join(rows) + '\n', len(rows)


def save_private(path, content):
    path = Path(path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if path.is_symlink():
        raise ValueError('Cookie destination must not be a symbolic link.')
    # Write privately, then replace atomically; invalid input leaves old cookies intact.
    fd, temporary = tempfile.mkstemp(prefix='.cookies-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            os.fchmod(stream.fileno(), 0o600)
            stream.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return path


def main():
    parser = Parser(description=__doc__, epilog='Examples: import_cookies.py --prompt; import_cookies.py --clipboard')
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--prompt', action='store_true', help='Hidden input in a user-accessible terminal')
    source.add_argument('--clipboard', action='store_true', help='Import macOS clipboard after user copies the Cookie header')
    source.add_argument('--stdin', action='store_true', help='Read from a protected local pipe; never put cookies in shell text')
    parser.add_argument('--host', default='kibana.concentricai.com', help='Exact HTTPS host; default: kibana.concentricai.com')
    parser.add_argument('--output', default='~/.config/kibana/cookies.txt', help='Private cookie file destination')
    args = parser.parse_args()
    try:
        if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?', args.host) or '..' in args.host:
            raise ValueError('Host must be a hostname without a scheme, port, or path.')
        if args.prompt:
            if not sys.stdin.isatty():
                raise ValueError('No interactive terminal; use --clipboard on macOS or --stdin from a private file.')
            raw = getpass.getpass('Paste Kibana Cookie header (hidden): ')
        elif args.clipboard:
            if sys.platform != 'darwin':
                raise ValueError('Clipboard mode supports macOS; use --prompt or --stdin.')
            result = subprocess.run(['pbpaste'], capture_output=True, text=True, timeout=10, check=True)
            raw = result.stdout
        else:
            raw = sys.stdin.read(131073)
        if len(raw) > 131072:
            raise ValueError('Cookie header exceeds the supported size.')
        content, count = cookie_rows(raw, args.host.lower())
        path = save_private(args.output, content)
        report(status='saved', cookies=count, path=str(path), help='Validate with a bounded Kibana data views request.')
        return 0
    except ValueError as error:
        report(error=str(error), help='Retry with a fresh Cookie header; existing cookies were not changed.')
    except (OSError, subprocess.SubprocessError, EOFError, KeyboardInterrupt):
        report(error='Cookie import did not complete.', help='Check input access and destination permissions, then retry.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
