import csv


class TourismSeasonsExcelAggregateMixin:
    def _aggregate_rows_across_years(self, year_rows):
        by_country = {}
        year_totals = {year: 0 for year in self.analysis_years}
        for row in year_rows:
            country = row["country"]
            if country not in by_country:
                by_country[country] = {
                    "country": country,
                    "monthly": [0] * len(self.months),
                    "total": 0,
                }
            by_country[country]["monthly"] = [
                left + right
                for left, right in zip(
                    by_country[country]["monthly"], row["monthly"]
                )
            ]
            by_country[country]["total"] += row["total"]
            year_totals[row["year"]] += row["total"]
        rows = sorted(
            by_country.values(),
            key=lambda item: (-item["total"], item["country"]),
        )
        return rows, year_totals

    def _write_aggregated_tsv(self, rows, output_path):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter="\t")
            writer.writerow(["Rank", "Country", *self.months, "Total"])
            total = 0
            for index, row in enumerate(rows, start=1):
                writer.writerow(
                    [index, row["country"], *row["monthly"], row["total"]]
                )
                total += row["total"]
            month_totals = [
                sum(row["monthly"][i] for row in rows)
                for i in range(len(self.months))
            ]
            writer.writerow(["-", "Total", *month_totals, total])
