import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np


class TourismSeasonsChartCentroidsMixin:
    def _centroid_monthly_arrivals(self, cluster_result):
        monthly_arrivals = []
        for cluster_id, centroid in enumerate(cluster_result["centroids"]):
            cluster_total_arrivals = cluster_result["summary"][cluster_id][
                "total_arrivals"
            ]
            monthly_arrivals.append(
                np.array(centroid, dtype=float) * float(cluster_total_arrivals)
            )
        return monthly_arrivals

    def _plot_cluster_centroids(
        self,
        cluster_result,
        output_path,
        year_label,
    ):
        k = cluster_result["k"]
        centroids = self._centroid_monthly_arrivals(cluster_result)
        palette = self._cluster_palette(k)
        x_positions = np.arange(len(self.months))
        labels = [
            self._cluster_label(cluster_result, cluster_id)
            for cluster_id in range(k)
        ]

        figure, axis = plt.subplots(figsize=(16, 9))
        axis.stackplot(
            x_positions,
            *centroids,
            colors=palette,
            labels=labels,
            alpha=0.9,
        )

        axis.set_title(
            (
                "Sri Lanka Tourism: Cluster Centroid Monthly Arrivals "
                f"({year_label})"
            ),
            fontsize=16,
        )
        axis.set_ylabel("Total arrivals")
        axis.set_xlabel("Month")
        axis.set_xticks(x_positions)
        axis.set_xticklabels(self.months)
        axis.tick_params(axis="x", rotation=45)
        axis.yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
        axis.legend(frameon=False)
        self._add_source_footer(figure, year_label=year_label)
        figure.tight_layout(rect=(0, 0.03, 1, 1))
        figure.savefig(output_path, dpi=220)
        plt.close(figure)

    def save_chart_centroids(self, cluster_result, yearly_cluster_results):
        self._plot_cluster_centroids(
            cluster_result,
            os.path.join(self.images_dir, "cluster-centroids.png"),
            year_label=self.data_year,
        )
        if not yearly_cluster_results:
            return

        for year in self.analysis_years:
            year_key = str(year)
            if year_key not in yearly_cluster_results:
                continue
            self._plot_cluster_centroids(
                yearly_cluster_results[year_key],
                os.path.join(self.images_dir, f"cluster-centroids-{year}.png"),
                year_label=year_key,
            )
