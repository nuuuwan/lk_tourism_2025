import seaborn as sns


class TourismSeasonsChartUtilsMixin:
    def _cluster_palette(self, k):
        return sns.color_palette("Set2", n_colors=k)

    def _format_arrivals_k(self, total_arrivals):
        return f"{int(round(total_arrivals / 1000.0))}K"

    def _format_country_label(self, country, annual_totals):
        return (
            f"{country} ({self._format_arrivals_k(annual_totals[country])})"
        )

    def _cluster_total_arrivals(self, cluster_result, cluster_id):
        for row in cluster_result.get("summary", []):
            if row.get("cluster") == cluster_id:
                return row.get("total_arrivals", 0)
        return 0

    def _cluster_label(self, cluster_result, cluster_id):
        arrivals = self._cluster_total_arrivals(cluster_result, cluster_id)
        return f"Cluster {cluster_id} ({self._format_arrivals_k(arrivals)})"

    def _cluster_countries_by_arrivals(
        self,
        shape_vectors,
        annual_totals,
        assignments,
        cluster_id,
    ):
        return sorted(
            (
                country
                for country in shape_vectors
                if assignments[country] == cluster_id
            ),
            key=lambda country: (-annual_totals[country], country),
        )

    def _country_name_for_plotly(self, country):
        rename = {
            "Russian Federation": "Russia",
            "Czech Republic": "Czechia",
            "United States": "United States of America",
            "South Korea": "Korea, South",
        }
        return rename.get(country, country)

    def _cluster_rgb_color(self, cluster_id, k):
        red, green, blue = self._cluster_palette(k)[cluster_id]
        return f"rgb({int(red * 255)}, {int(green * 255)}, {int(blue * 255)})"

    def _add_source_footer(
        self, figure, include_filter=True, year_label=None
    ):
        filter_text = "All countries included"
        if include_filter:
            filter_k = self._format_arrivals_k(self.min_annual_arrivals)
            filter_text = (
                f"Includes countries with at least {filter_k} arrivals/year"
            )
        figure.text(
            0.01,
            0.01,
            (
                f"Data Source: {self.data_source} | "
                f"Analysis: {self.analysis_by} | "
                f"Year: {year_label or self.data_year} | "
                f"{filter_text}"
            ),
            ha="left",
            va="bottom",
            fontsize=10,
            color="#555555",
            fontfamily=self.font_family,
        )
