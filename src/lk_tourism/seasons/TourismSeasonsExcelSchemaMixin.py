class TourismSeasonsExcelSchemaMixin:
    def _normalize_token(self, value):
        text = "" if value is None else str(value)
        text = text.strip().lower().replace(" ", "")
        return text.replace("-", "").replace("_", "")

    def _to_int(self, value):
        text = "" if value is None else str(value).strip().replace(",", "")
        if text == "" or text.lower() == "nan":
            text = "0"
        try:
            return int(round(float(text)))
        except ValueError:
            return 0

    def _excel_path_for_year(self, year):
        matches = sorted(self.data_dir.glob(f"*{year}*.xlsx"))
        if not matches:
            raise FileNotFoundError(f"Missing Excel file for year {year}")
        return matches[0]

    def _yearly_tsv_path(self, year):
        return self.data_dir / self.yearly_tsv_template.format(year=year)

    def _row_tokens(self, df, row_idx):
        return [
            self._normalize_token(item) for item in df.iloc[row_idx].tolist()
        ]

    def _is_header_tokens(self, tokens):
        month_hits = sum(
            1 for token in tokens if token in self.month_token_map
        )
        return "country" in tokens and month_hits >= 8

    def _find_header_row(self, df):
        for row_idx in range(len(df.index)):
            if self._is_header_tokens(self._row_tokens(df, row_idx)):
                return row_idx
        raise ValueError("Could not detect header row in Excel sheet")

    def _init_column_indexes(self):
        return None, {}, None

    def _apply_column_token(
        self,
        token,
        col_idx,
        country_col,
        month_cols,
        total_col,
    ):
        if token == "country":
            country_col = col_idx
        if token in self.month_token_map:
            month_cols[self.month_token_map[token]] = col_idx
        if token.startswith("total"):
            total_col = col_idx
        return country_col, month_cols, total_col

    def _validate_column_indexes(self, country_col, month_cols):
        if country_col is None:
            raise ValueError("Country column not found in Excel header")
        missing = [month for month in self.months if month not in month_cols]
        if missing:
            raise ValueError(f"Missing month columns: {missing}")

    def _column_indexes(self, header_values):
        country_col, month_cols, total_col = self._init_column_indexes()
        for col_idx, raw in enumerate(header_values):
            token = self._normalize_token(raw)
            country_col, month_cols, total_col = self._apply_column_token(
                token,
                col_idx,
                country_col,
                month_cols,
                total_col,
            )
        self._validate_column_indexes(country_col, month_cols)
        return country_col, month_cols, total_col
