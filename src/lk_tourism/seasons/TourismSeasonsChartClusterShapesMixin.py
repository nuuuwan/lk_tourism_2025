import os

import matplotlib.pyplot as plt


class TourismSeasonsChartClusterShapesMixin:
    def _plot_country_shapes_for_cluster(
        self,
        shape_vectors,
        annual_totals,
        cluster_result,
        cluster_id,
        output_path,
    ):
        assignments = cluster_result["assignments"]
        countries = self._cluster_countries_by_arrivals(
            shape_vectors,
            annual_totals,
            assignments,
            cluster_id,
        )
        cluster_label = self._cluster_label(cluster_result, cluster_id)
        cluster_color = self._cluster_palette(cluster_result["k"])[cluster_id]
        centroid = cluster_result["centroids"][cluster_id]

        figure, axis = plt.subplots(figsize=(12, 7))
        self._plot_cluster_country_lines(
            axis,
            countries,
            shape_vectors,
            annual_totals,
            cluster_color,
        )
        self._plot_cluster_reference_lines(
            axis,
            centroid,
            cluster_label,
            cluster_color,
        )
        self._style_cluster_shape_axis(axis, cluster_label)
        self._add_source_footer(figure)
        figure.tight_layout(rect=(0, 0.03, 1, 1))
        figure.savefig(output_path, dpi=200)
        plt.close(figure)

    def save_chart_cluster_shapes(
        self, shape_vectors, annual_totals, cluster_result
    ):
        for cluster_id in range(cluster_result["k"]):
            self._plot_country_shapes_for_cluster(
                shape_vectors,
                annual_totals,
                cluster_result,
                cluster_id,
                os.path.join(
                    self.images_dir,
                    f"country-shapes-by-cluster-{cluster_id}.png",
                ),
            )
