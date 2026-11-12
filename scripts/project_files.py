"""Unduh data sekali, lalu simpan hasil analisis di folder hasil."""
import csv
from pathlib import Path
from shutil import copyfileobj
from tempfile import NamedTemporaryFile
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]

def source_file(name, url):
    raw = ROOT / 'data' / 'raw'
    raw.mkdir(parents=True, exist_ok=True)
    target = raw / name
    if target.exists():
        return target
    print('Mengunduh', name, flush=True)
    with NamedTemporaryFile(dir=raw, delete=False) as temp:
        scratch = Path(temp.name)
    try:
        request = Request(url, headers={'User-Agent': 'BusinessPerformanceAnalytics/1.0'})
        with urlopen(request, timeout=120) as remote, scratch.open('wb') as local:
            copyfileobj(remote, local)
        scratch.replace(target)
    finally:
        scratch.unlink(missing_ok=True)
    return target

def save_csv(name, columns, records):
    folder = ROOT / 'hasil'
    folder.mkdir(exist_ok=True)
    path = folder / name
    with NamedTemporaryFile(mode='w', newline='', encoding='utf-8-sig',
                            dir=folder, delete=False) as temp:
        writer = csv.writer(temp)
        writer.writerow(columns)
        writer.writerows(records)
    Path(temp.name).replace(path)
    print('Tersimpan:', path)
