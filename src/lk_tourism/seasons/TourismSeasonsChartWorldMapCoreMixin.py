import plotly.graph_objects as go


class TourismSeasonsChartWorldMapCoreMixin:
    def _add_world_map_cluster_trace(
        self,
        fig,
        cluster_result,
        cluster_id,
        cluster_countries,
        cluster_color,
    ):
        cluster_name = self._cluster_label(cluster_result, cluster_id)
        cluster_arrivals = self._cluster_total_arrivals(
            cluster_result, cluster_id
        )
        total_arrivals = self._cluster_total_arrivals_all(cluster_result)
        cluster_share = self._format_pct(
            self._safe_share(cluster_arrivals, total_arrivals)
        )
        fig.add_trace(
            go.Choropleth(
                locations=[
                    self._country_name_for_plotly(c) for c in cluster_countries
                ],
                z=[1] * len(cluster_countries),
                locationmode="country names",
                colorscale=[[0.0, cluster_color], [1.0, cluster_color]],
                showscale=False,
                name=cluster_name,
                showlegend=False,
                marker_line_color="white",
                marker_line_width=0.5,
                hovertemplate=(
                    "<b>%{location}</b><br>Cluster "
                    f"{cluster_id} ({cluster_share})"
                    "<extra></extra>"
                ),
            )
        )
        fig.add_trace(
            go.Scattergeo(
                lon=[None],
                lat=[None],
                mode="markers",
                marker=dict(size=10, color=cluster_color),
                name=cluster_name,
                showlegend=True,
                hoverinfo="skip",
            )
        )

    def _world_map_cluster_countries(self, countries, assignments, cluster_id):
        return [
            country
            for country in countries
            if assignments[country] == cluster_id
        ]

    def _add_world_map_cluster_series(
        self, fig, countries, assignments, cluster_result, k
    ):
        for cluster_id in range(k):
            cluster_countries = self._world_map_cluster_countries(
                countries,
                assignments,
                cluster_id,
            )
            if not cluster_countries:
                continue
            self._add_world_map_cluster_trace(
                fig,
                cluster_result,
                cluster_id,
                cluster_countries,
                self._cluster_rgb_color(cluster_id, k),
            )

    def _world_map_title(self):
        return {
            "text": (
                "Sri Lanka Tourism: "
                f"World Map of Country Clusters ({self.data_year})"
            ),
            "font": {"size": 30},
        }

    def _world_map_geo(self):
        return {
            "showframe": False,
            "showcoastlines": True,
            "coastlinecolor": "white",
            "showland": True,
            "landcolor": "#e6e6e6",
            "bgcolor": "white",
            "projection_type": "natural earth",
        }
