import numpy as np


class TourismSeasonsChartClusterArrivalsByYearCoreMixin:
    def _available_years_in_results(self, yearly_cluster_results):
        years = [str(year) for year in self.analysis_years]
        return [year for year in years if year in yearly_cluster_results]

    def _cluster_arrivals_for_years(
        self,
        yearly_cluster_results,
        cluster_id,
        years,
    ):
        arrivals = []
        for year in years:
            summary_row = next(
                row
                for row in yearly_cluster_results[year]["summary"]
                if row["cluster"] == cluster_id
            )
            arrivals.append(summary_row["total_arrivals"])
        return arrivals

    def _plot_cluster_arrivals_bars(
        self,
        axis,
        yearly_cluster_results,
        available_years,
        k,
        palette,
    ):
        x_positions = np.arange(len(available_years))
        bar_width = 0.8 / k

        for cluster_id in range(k):
            arrivals = self._cluster_arrivals_for_years(
                yearly_cluster_results,
                cluster_id,
                available_years,
            )
            offset = (cluster_id - (k - 1) / 2) * bar_width
            axis.bar(
                x_positions + offset,
                arrivals,
                width=bar_width,
                color=palette[cluster_id],
                label=(
                    f"Cluster {cluster_id} "
                    f"({self._format_arrivals_k(sum(arrivals))})"
                ),
            )

        axis.set_xticks(x_positions)
        axis.set_xticklabels(available_years)
