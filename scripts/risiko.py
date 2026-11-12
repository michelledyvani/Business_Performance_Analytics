"""Bandingkan jadwal per proyek dengan tanggal selesai pertama yang teramati."""
from collections import Counter, defaultdict
import csv
from datetime import datetime
from project_files import source_file, save_csv

url = 'https://data.cityofnewyork.us/api/views/95tx-snak/rows.csv?accessType=DOWNLOAD'
with source_file('schedule.csv', url).open(encoding='utf-8-sig', newline='') as handle:
    raw = sorted(csv.DictReader(handle), key=lambda item: item['Reporting Period'])
keys = Counter((r['PID'], r['Reporting Period']) for r in raw)
baseline = {}
counts = defaultdict(Counter)
for r in raw:
    pid = r['PID']
    period = r['Reporting Period']
    if not pid or not period or keys[pid, period] != 1:
        continue
    try:
        finish = datetime.strptime(r['Completion Date'], '%m/%d/%Y').date()
    except ValueError:
        continue
    if not 1900 <= finish.year <= 2100:
        continue
    original = baseline.setdefault(pid, finish)
    days = (finish - original).days
    counts[period]['tracked'] += 1
    counts[period]['late'] += int(days > 0)
    counts[period]['severe'] += int(days > 90)
rows = [(p, c['tracked'], c['late'], c['severe']) for p, c in sorted(counts.items())]
save_csv('risiko.csv', ['periode', 'jadwal_dipantau', 'mundur', 'mundur_lebih_90_hari'], rows)
for row in rows:
    print(*row, sep=' | ')
