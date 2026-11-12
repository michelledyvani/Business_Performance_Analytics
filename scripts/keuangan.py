"""Rekonsiliasi laba operasi dan anggaran Northeast Division tahun 2011."""
import csv
from collections import defaultdict
from decimal import Decimal
from project_files import source_file, save_csv

url = ('https://raw.githubusercontent.com/microsoft/sql-server-samples/master/'
       'samples/databases/adventure-works/data-warehouse-install-script/FactFinance.csv')
groups = {
    'Pendapatan': {52, 53, 54, 101},
    'HPP': {56, 57},
    'Biaya operasi': {60,61,62,63,65,66,67,68,69,71,72,73,74,76,77,78,80,81,82,83,84,85,87},
}
account_group = {account: group for group, accounts in groups.items() for account in accounts}
amounts = defaultdict(Decimal)
months = defaultdict(set)
with source_file('FactFinance.csv', url).open(encoding='utf-8-sig', newline='') as handle:
    for _, date_key, org, dept, scenario, account, amount, _ in csv.reader(handle, delimiter='|'):
        key = int(account)
        group = account_group.get(key)
        if org != '3' or not date_key.startswith('2011') or scenario not in {'1','2'} or group is None:
            continue
        month = date_key[:6]
        months[scenario].add(month)
        sign = -1 if key in {53, 54} else 1
        amounts[month, scenario, group] += Decimal(amount) * sign
common = sorted(months['1'] & months['2'])
if not common:
    raise ValueError('Tidak ada bulan dengan realisasi dan anggaran.')
rows = []
for scenario, label in [('1', 'Aktual'), ('2', 'Anggaran')]:
    sales, cogs, opex = [sum(amounts[m, scenario, g] for m in common) for g in groups]
    rows.append((label, len(common), sales, cogs, opex, sales - cogs - opex))
save_csv('keuangan.csv', ['skenario','jumlah_bulan','pendapatan','hpp','opex','laba_operasi'], rows)
for row in rows:
    print(*row, sep=' | ')
