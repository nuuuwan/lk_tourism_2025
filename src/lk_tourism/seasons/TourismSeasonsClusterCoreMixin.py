import numpy as np


class TourismSeasonsClusterCoreMixin:
    def _shape_matrix(self, shape_vectors):
        countries = sorted(shape_vectors.keys())
        matrix = np.array([shape_vectors[country] for country in countries])
        return countries, matrix

    def _countries_by_cluster(self, countries, assignments, k):
        return {
            cluster_index: sorted(
                country
                for country in countries
                if assignments.get(country) == cluster_index
            )
            for cluster_index in range(k)
        }

    def _centroid_monthly_variance(self, centroid):
        centroid_arr = np.asarray(centroid, dtype=float)
        return float(np.var(centroid_arr))

    def _relabel_clusters_by_variance(self, assignments, centroids, k):
        ordered_old_labels = sorted(
            range(k),
            key=lambda label: (
                self._centroid_monthly_variance(centroids[label]),
                label,
            ),
        )
        label_map = {
            old_label: new_label
            for new_label, old_label in enumerate(ordered_old_labels)
        }
        relabeled_assignments = {
            country: label_map[cluster_index]
            for country, cluster_index in assignments.items()
        }
        relabeled_centroids = [
            centroids[label] for label in ordered_old_labels
        ]
        return relabeled_assignments, relabeled_centroids

    def _build_cluster_summary(self, assignments, annual_totals, k):
        summary = []
        for cluster_index in range(k):
            countries = sorted(
                country
                for country, assigned_cluster in assignments.items()
                if assigned_cluster == cluster_index
            )
            total_arrivals = sum(
                annual_totals[country] for country in countries
            )
            count = len(countries)
            summary.append(
                {
                    "cluster": cluster_index,
                    "total_arrivals": total_arrivals,
                    "num_countries": count,
                    "average_arrivals": (
                        total_arrivals / count if count else 0
                    ),
                    "countries": countries,
                }
            )
        return summary
