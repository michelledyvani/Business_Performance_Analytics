"""Hitung penjualan dan struk unik dari kedua lembar transaksi UCI."""
from collections import defaultdict
from datetime import datetime
from io import BytesIO
from zipfile import ZipFile

from openpyxl import load_workbook
from project_files import source_file, save_csv

URL = 'https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip'
cutoff = datetime(2010, 12, 1)
orders = defaultdict(set)
revenue_pence = defaultdict(int)

with ZipFile(source_file('retail.zip', URL)) as archive:
    workbook = load_workbook(BytesIO(archive.read('online_retail_II.xlsx')),
                             read_only=True, data_only=True)

for sheet_index, sheet in enumerate(workbook.worksheets):
    print('Membaca', sheet.title, flush=True)
    for invoice, code, name, qty, when, price, buyer, country in sheet.iter_rows(
            min_row=2, values_only=True):
        # Pada periode yang beririsan, ambil transaksi dari lembar kedua.
        if when is None or (sheet_index == 0 and when >= cutoff) or (sheet_index == 1 and when < cutoff):
            continue
        if not invoice or str(invoice).upper().startswith('C'):
            continue
        if not qty or qty <= 0 or not price or price <= 0:
            continue
        product = str(code)
        if len(product) < 5 or not product[:5].isdigit():
            continue
        for year in [str(when.year), 'Semua tahun']:
            orders[year].add(str(invoice))
            revenue_pence[year] += round(qty * price * 100)
workbook.close()
rows = [(year, len(orders[year]), f'{revenue_pence[year] / 100:.2f}')
        for year in sorted(orders)]
save_csv('penjualan.csv', ['periode', 'pesanan_unik', 'penjualan_GBP'], rows)
for row in rows:
    print(*row, sep=' | ')
