import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import seaborn as sns


class TourismSeasonsChartHeatmapMixin:
    def _plot_shape_heatmap(
        self,
        shape_vectors,
        annual_totals,
        cluster_result,
        output_path,
    ):
        assignments = cluster_result["assignments"]
        matrix, labels, break_lines = self._heatmap_rows_with_cluster_gaps(
            shape_vectors,
            annual_totals,
            assignments,
            cluster_result["k"],
        )
        mask = np.isnan(matrix)

        figure, axis = plt.subplots(figsize=(9, 9))
        sns.heatmap(
            matrix,
            cmap="Reds",
            mask=mask,
            xticklabels=self.months,
            yticklabels=labels,
            cbar_kws={"label": "Monthly share (%)"},
            ax=axis,
        )
        colorbar = axis.collections[0].colorbar
        colorbar.formatter = mtick.PercentFormatter(xmax=1.0)
        colorbar.update_ticks()
        self._apply_heatmap_axis_format(axis, break_lines)
        self._add_source_footer(figure)
        figure.tight_layout(rect=(0, 0.03, 1, 1))
        figure.savefig(output_path, dpi=220)
        plt.close(figure)

    def save_chart_heatmap(self, shape_vectors, annual_totals, cluster_result):
        self._plot_shape_heatmap(
            shape_vectors,
            annual_totals,
            cluster_result,
            os.path.join(self.images_dir, "cluster-seasons-heatmap.png"),
        )
