import pandas as pd


class TourismSeasonsExcelPipelineMixin:
    def _read_year_rows_from_excel(self, year):
        df = pd.read_excel(
            self._excel_path_for_year(year),
            sheet_name=0,
            header=None,
        )
        header_idx = self._find_header_row(df)
        country_col, month_cols, total_col = self._column_indexes(
            df.iloc[header_idx].tolist()
        )
        column_info = (country_col, month_cols, total_col)

        rows = []
        for row_idx in range(header_idx + 1, len(df.index)):
            row = self._parsed_excel_row(
                df,
                row_idx,
                year,
                column_info,
            )
            if row is None:
                continue
            if row == "STOP":
                break
            rows.append(row)
        return rows

    def _collect_yearly_rows(self):
        yearly_paths = {}
        all_rows = []
        for year in self.analysis_years:
            rows = sorted(
                self._read_year_rows_from_excel(year),
                key=lambda item: (-item["total"], item["country"]),
            )
            yearly_path = self._yearly_tsv_path(year)
            self._write_aggregated_tsv(rows, yearly_path)
            yearly_paths[year] = yearly_path

        for year in self.analysis_years:
            rows = self._read_country_rows(yearly_paths[year])
            all_rows.extend([{**row, "year": year} for row in rows])
        return yearly_paths, all_rows

    def build_aggregated_tsv_from_excels(self):
        yearly_paths, all_rows = self._collect_yearly_rows()
        rows, year_totals = self._aggregate_rows_across_years(all_rows)
        self._write_aggregated_tsv(rows, self.aggregated_tsv_path)
        return self.aggregated_tsv_path, year_totals, yearly_paths
