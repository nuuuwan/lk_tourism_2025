class TourismSeasonsExcelRowParseMixin:
    def _excel_country(self, df, row_idx, country_col):
        cell = df.iat[row_idx, country_col]
        return "" if cell is None else str(cell).strip()

    def _excel_row_state(self, country):
        normalized = country.lower()
        if country == "" or normalized == "nan":
            return "skip"
        if normalized == "total":
            return "stop"
        return "data"

    def _excel_monthly_values(self, df, row_idx, month_cols):
        return [
            self._to_int(df.iat[row_idx, month_cols[month]])
            for month in self.months
        ]

    def _excel_effective_total(self, df, row_idx, monthly, total_col):
        total = sum(monthly)
        if total_col is None:
            return total
        parsed = self._to_int(df.iat[row_idx, total_col])
        return parsed if parsed > 0 else total

    def _parsed_excel_row(self, df, row_idx, year, column_info):
        country_col, month_cols, total_col = column_info
        country = self._excel_country(df, row_idx, country_col)
        state = self._excel_row_state(country)
        row = None
        if state == "stop":
            row = "STOP"
        elif state == "data":
            monthly = self._excel_monthly_values(df, row_idx, month_cols)
            total = self._excel_effective_total(
                df,
                row_idx,
                monthly,
                total_col,
            )
            if total > 0:
                row = {
                    "country": country,
                    "monthly": monthly,
                    "total": total,
                    "year": year,
                }
        return row
