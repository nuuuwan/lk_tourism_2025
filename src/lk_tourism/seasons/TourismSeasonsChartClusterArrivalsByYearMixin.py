import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


class TourismSeasonsChartClusterArrivalsByYearMixin:
    def _plot_cluster_arrivals_by_year(
        self, yearly_cluster_results, output_path
    ):
        if not yearly_cluster_results:
            return
        years = self._available_years_in_results(yearly_cluster_results)
        if not years:
            return

        k = yearly_cluster_results[years[0]]["k"]
        palette = self._cluster_palette(k)
        figure, axis = plt.subplots(figsize=(16, 9))
        self._plot_cluster_arrivals_bars(
            axis,
            yearly_cluster_results,
            years,
            k,
            palette,
        )
        axis.set_title(
            "Sri Lanka Tourism: Total Arrivals per Cluster by Year",
            fontsize=16,
        )
        axis.set_xlabel("Year")
        axis.set_ylabel("Total arrivals")
        axis.yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
        axis.legend(frameon=False)
        self._add_source_footer(figure, year_label=self.data_year)
        figure.tight_layout(rect=(0, 0.03, 1, 1))
        figure.savefig(output_path, dpi=220)
        plt.close(figure)

    def save_chart_cluster_arrivals_by_year(self, yearly_cluster_results):
        self._plot_cluster_arrivals_by_year(
            yearly_cluster_results,
            os.path.join(self.images_dir, "cluster-arrivals-by-year.png"),
        )
