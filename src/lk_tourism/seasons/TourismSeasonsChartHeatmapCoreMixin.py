import warnings

import numpy as np


class TourismSeasonsChartHeatmapCoreMixin:
    def _heatmap_rows_with_cluster_gaps(
        self,
        shape_vectors,
        annual_totals,
        assignments,
        k,
    ):
        warnings.warn(
            "Heatmap chart helpers are deprecated and will be removed in a future release.",
            DeprecationWarning,
            stacklevel=2,
        )
        rows = []
        labels = []
        cluster_break_lines = []
        row_index = 0
        for cluster_id in range(k):
            countries = self._cluster_countries_by_arrivals(
                shape_vectors,
                annual_totals,
                assignments,
                cluster_id,
            )
            for country in countries:
                rows.append(shape_vectors[country])
                labels.append(
                    self._format_country_label(country, annual_totals)
                )
                row_index += 1
            if cluster_id < k - 1:
                rows.append([np.nan] * len(self.months))
                labels.append("")
                cluster_break_lines.append(row_index)
                row_index += 1
        return np.array(rows, dtype=float), labels, cluster_break_lines

    def _apply_heatmap_axis_format(self, axis, break_lines):
        warnings.warn(
            "Heatmap chart helpers are deprecated and will be removed in a future release.",
            DeprecationWarning,
            stacklevel=2,
        )
        for break_line in break_lines:
            axis.hlines(
                break_line,
                *axis.get_xlim(),
                colors="white",
                linewidth=6,
            )
        axis.set_title(
            "Sri Lanka Tourism: Country Shape Heatmap (Grouped by Cluster)",
            fontsize=15,
        )
        axis.set_xlabel("Month")
        axis.set_ylabel("Country")
