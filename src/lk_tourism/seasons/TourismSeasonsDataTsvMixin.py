import csv


class TourismSeasonsDataTsvMixin:
    def _parse_country_row(self, row):
        country = row.get("Country", "").strip()
        if country == "Total":
            return None
        return {
            "country": country,
            "monthly": [int(row[m]) for m in self.months],
            "total": int(row["Total"]),
        }

    def _read_country_rows(self, tsv_path):
        rows = []
        with open(tsv_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                parsed = self._parse_country_row(row)
                if parsed:
                    rows.append(parsed)
        return rows

    def _eligible_rows(self, rows):
        total_arrivals = sum(r["total"] for r in rows if r["total"] > 0)
        if total_arrivals <= 0:
            return []
        min_total_arrivals = (
            total_arrivals * self.min_arrivals_percentage / 100.0
        )
        return [
            r
            for r in rows
            if r["total"] >= min_total_arrivals and r["total"] > 0
        ]

    def _build_shape_vectors(self, rows):
        eligible = self._eligible_rows(rows)
        return {
            r["country"]: [m / r["total"] for m in r["monthly"]]
            for r in eligible
        }

    def _build_annual_totals(self, rows):
        eligible = self._eligible_rows(rows)
        return {r["country"]: r["total"] for r in eligible}

    def _build_monthly_totals(self, rows):
        return [
            sum(row["monthly"][i] for row in rows)
            for i in range(len(self.months))
        ]

    def extract_country_analysis_data(self, tsv_path):
        rows = self._read_country_rows(tsv_path)
        return (
            self._build_shape_vectors(rows),
            self._build_annual_totals(rows),
            self._build_monthly_totals(rows),
        )
