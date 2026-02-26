import matplotlib.ticker as mtick


class TourismSeasonsChartClusterShapesCoreMixin:
    def _format_share_pct(self, value):
        return f"{value * 100:.1f}%"

    def _annotate_centroid_span(self, axis, centroid, color):
        top_value = max(centroid)
        bottom_value = min(centroid)
        span_value = top_value - bottom_value

        if span_value == 0:
            axis.annotate(
                f"Span: {self._format_share_pct(span_value)}",
                xy=(0.98, top_value),
                xytext=(-4, 10),
                xycoords=("axes fraction", "data"),
                textcoords="offset points",
                ha="right",
                va="bottom",
                fontsize=10,
                color="black",
                fontweight="bold",
            )
            return

        axis.annotate(
            "",
            xy=(0.985, top_value),
            xytext=(0.985, bottom_value),
            xycoords=("axes fraction", "data"),
            textcoords=("axes fraction", "data"),
            arrowprops={
                "arrowstyle": "<->",
                "color": color,
                "lw": 2.0,
                "linestyle": ":",
            },
        )

        axis.annotate(
            f"Span: {self._format_share_pct(span_value)}",
            xy=(0.985, bottom_value + (span_value / 2)),
            xytext=(-8, 0),
            xycoords=("axes fraction", "data"),
            textcoords="offset points",
            ha="right",
            va="center",
            fontsize=10,
            color="black",
            fontweight="bold",
        )

    def _annotate_centroid_extrema(self, axis, centroid, color):
        top_index = max(range(len(centroid)), key=lambda idx: centroid[idx])
        bottom_index = min(range(len(centroid)), key=lambda idx: centroid[idx])

        if top_index == bottom_index:
            value = centroid[top_index]
            axis.annotate(
                (
                    f"Top/Bottom: {self.months[top_index]} "
                    f"({self._format_share_pct(value)})"
                ),
                xy=(self.months[top_index], value),
                xytext=(12, 14),
                textcoords="offset points",
                fontsize=10,
                color="black",
                fontweight="bold",
            )
            return

        top_value = centroid[top_index]
        axis.annotate(
            (
                f"Top: {self.months[top_index]} "
                f"({self._format_share_pct(top_value)})"
            ),
            xy=(self.months[top_index], top_value),
            xytext=(12, 14),
            textcoords="offset points",
            fontsize=10,
            color="black",
            fontweight="bold",
        )

        bottom_value = centroid[bottom_index]
        axis.annotate(
            (
                f"Bottom: {self.months[bottom_index]} "
                f"({self._format_share_pct(bottom_value)})"
            ),
            xy=(self.months[bottom_index], bottom_value),
            xytext=(12, -16),
            textcoords="offset points",
            fontsize=10,
            color="black",
            fontweight="bold",
        )

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
        self._annotate_centroid_extrema(axis, centroid, color)
        self._annotate_centroid_span(axis, centroid, color)

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
