import csv
import os

import numpy as np
from sklearn.cluster import KMeans


class TourismSeasonsClusterKMeansMixin:
    def _load_population_by_country(self, population_tsv_path):
        if not os.path.exists(population_tsv_path):
            return {}
        population_by_country = {}
        with open(population_tsv_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter="\t")
            for row in reader:
                country = row.get("Country", "").strip()
                if country:
                    population_by_country[country] = int(row["Population"])
        return population_by_country

    def _build_country_weights(
        self,
        countries,
        annual_totals,
        population_by_country,
    ):
        raw_weights = np.array(
            [
                float(
                    population_by_country.get(country, annual_totals[country])
                )
                for country in countries
            ],
            dtype=float,
        )
        if np.any(raw_weights <= 0):
            raise ValueError("All sample weights must be positive")
        return raw_weights / raw_weights.mean()

    def _fit_kmeans(self, matrix, k, seed, sample_weights):
        model = KMeans(
            n_clusters=k,
            max_iter=100,
            random_state=seed,
            n_init=10,
        )
        labels = model.fit_predict(matrix, sample_weight=sample_weights)
        return labels, model.cluster_centers_.tolist()

    def kmeans_cluster_shapes(
        self,
        shape_vectors,
        annual_totals,
        population_by_country,
        k=None,
        seed=None,
    ):
        k = self.n_clusters if k is None else k
        seed = self.cluster_random_seed if seed is None else seed
        countries, matrix = self._shape_matrix(shape_vectors)
        if len(countries) < k:
            raise ValueError(
                f"k={k} is larger than number of countries={len(countries)}"
            )

        weights = self._build_country_weights(
            countries, annual_totals, population_by_country
        )
        labels, centroids = self._fit_kmeans(matrix, k, seed, weights)
        assignments = {
            country: int(label) for country, label in zip(countries, labels)
        }
        assignments, centroids = self._relabel_clusters_by_variance(
            assignments,
            centroids,
            k,
        )
        return {
            "k": k,
            "centroids": centroids,
            "assignments": assignments,
            "countries_by_cluster": self._countries_by_cluster(
                countries, assignments, k
            ),
            "summary": self._build_cluster_summary(
                assignments, annual_totals, k
            ),
        }
