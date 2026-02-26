import os

import plotly.graph_objects as go


class TourismSeasonsChartWorldMapMixin:
    def _world_map_annotation(self):
        return {
            "text": (
                f"Data Source: {self.data_source} | "
                f"Analysis: {self.analysis_by} | "
                f"Year: {self.data_year} | "
                "Includes countries with at least "
                f"{self.min_arrivals_percentage:.2f}% of total arrivals"
            ),
            "x": 0,
            "y": 0,
            "xref": "paper",
            "yref": "paper",
            "xanchor": "left",
            "yanchor": "bottom",
            "showarrow": False,
            "font": {
                "family": self.font_family,
                "size": 11,
                "color": "#555555",
            },
        }

    def _apply_world_map_layout(self, figure):
        figure.update_layout(
            title=self._world_map_title(),
            geo=self._world_map_geo(),
            font=dict(family=self.font_family),
            legend=dict(
                title="Cluster",
                bgcolor="rgba(255,255,255,0.85)",
                bordercolor="#cccccc",
                borderwidth=1,
            ),
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=60, b=40),
            annotations=[self._world_map_annotation()],
        )

    def _plot_cluster_world_map(self, cluster_result, output_path):
        assignments = cluster_result["assignments"]
        countries = sorted(assignments)
        figure = go.Figure()
        self._add_world_map_cluster_series(
            figure,
            countries,
            assignments,
            cluster_result,
            cluster_result["k"],
        )
        self._apply_world_map_layout(figure)
        figure.write_image(output_path, width=1600, height=900, scale=2)

    def save_chart_world_map(self, cluster_result):
        self._plot_cluster_world_map(
            cluster_result,
            os.path.join(self.images_dir, "world-map-by-cluster.png"),
        )
