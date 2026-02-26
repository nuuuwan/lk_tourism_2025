import matplotlib.ticker as mtick


class TourismSeasonsChartClusterShapesCoreMixin:
    def _country_linewidth(self, country, countries, annual_totals):
        cluster_arrivals = [annual_totals[name] for name in countries]
        min_arrivals = min(cluster_arrivals)
        max_arrivals = max(cluster_arrivals)
        if max_arrivals == min_arrivals:
            return 2.0
        scale = (annual_totals[country] - min_arrivals) / (
            max_arrivals - min_arrivals
        )
        return 1.2 + 3.0 * scale

    def _plot_cluster_country_lines(
        self,
        axis,
        countries,
        shape_vectors,
        annual_totals,
        color,
    ):
        for country in countries:
            axis.plot(
                self.months,
                shape_vectors[country],
                color=color,
                alpha=0.2,
                linewidth=self._country_linewidth(
                    country, countries, annual_totals
                ),
                label=self._format_country_label(country, annual_totals),
            )

    def _plot_cluster_reference_lines(
        self,
        axis,
        centroid,
        cluster_label,
        color,
    ):
        axis.plot(
            self.months,
            centroid,
            color=color,
            alpha=1.0,
            linewidth=3,
            marker="o",
            label=f"{cluster_label} centroid",
        )
        axis.axhline(
            y=self.uniform_monthly_share,
            color="#555555",
            linestyle=":",
            linewidth=1.5,
            label="Uniform monthly share (8.33%)",
        )

    def _style_cluster_shape_axis(self, axis, cluster_label):
        axis.set_title(
            f"Sri Lanka Tourism: Monthly Arrival Shapes - {cluster_label}",
            fontsize=16,
        )
        axis.set_ylabel("Monthly share of annual arrivals")
        axis.set_xlabel("Month")
        axis.tick_params(axis="x", rotation=45)
        axis.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
        axis.legend(
            frameon=False,
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            fontsize=9,
        )
