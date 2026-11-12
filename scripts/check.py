from pathlib import Path
import csv
from math import isclose

data = Path(__file__).resolve().parents[1] / "data"

def values(project, table, scope):
    with (data / project / (table + ".csv")).open(encoding="utf-8") as handle:
        row = next(item for item in csv.DictReader(handle) if item["Pilihan"] == scope)
    return [float(row[f"K{i}"]) for i in range(1, 5)]

risk = values("01-risiko-proyek", "RISK_KPI", "2026-05")
assert risk[:3] == [1554, 1133, 1050]
print("OK - jadwal Mei 2026")

sales = values("02-penjualan-pelanggan", "SALES_KPI", "Semua tahun")
sales_2010 = values("02-penjualan-pelanggan", "SALES_KPI", "2010")
assert sales[1] == 39516 and sales_2010[1] == 19627
print("OK - pesanan semua tahun dan 2010")

finance = values("03-kinerja-keuangan", "FINANCE_KPI", "Semua kuartal")
with (data / "03-kinerja-keuangan" / "FINANCE_Grafik_1.csv").open(encoding="utf-8") as handle:
    actual = {row["Kategori"]: 1000 * float(row["Realisasi"]) for row in csv.DictReader(handle)
              if row["Pilihan"] == "Semua kuartal"}
assert isclose(actual["Pendapatan"] - actual["HPP"] - actual["Biaya operasi"], finance[2])
print("OK - rekonsiliasi laba operasi")
