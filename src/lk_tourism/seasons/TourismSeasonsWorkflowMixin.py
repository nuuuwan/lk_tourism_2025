import json
import os

import seaborn as sns


class TourismSeasonsWorkflowMixin:
    def save_shape_visualizations(
        self,
        shape_vectors,
        annual_totals,
        monthly_totals,
        cluster_result,
        yearly_cluster_results=None,
    ):
        os.makedirs(self.images_dir, exist_ok=True)
        sns.set_theme(
            style="whitegrid",
            context="talk",
            rc={"font.family": self.font_family},
        )
        self.save_chart_cluster_shapes(
            shape_vectors, annual_totals, cluster_result
        )
        self.save_chart_centroids(cluster_result, yearly_cluster_results)
        self.save_chart_heatmap(shape_vectors, annual_totals, cluster_result)
        self.save_chart_world_map(cluster_result)
        self.save_chart_total_arrivals_by_month(monthly_totals)

    def _build_yearly_cluster_results(self, yearly_tsv_paths, population):
        results = {}
        for year in self.analysis_years:
            shape_vectors, annual_totals, _ = (
                self.extract_country_analysis_data(yearly_tsv_paths[year])
            )
            results[str(year)] = self.kmeans_cluster_shapes(
                shape_vectors,
                annual_totals,
                population,
            )
        return results

    def run_tourism_seasons_workflow(self, print_json=True):
        aggregated_path, year_totals, yearly_paths = (
            self.build_aggregated_tsv_from_excels()
        )
        shape_vectors, annual_totals, monthly_totals = (
            self.extract_country_analysis_data(aggregated_path)
        )
        population = self._load_population_by_country(self.population_tsv_path)
        cluster_result = self.kmeans_cluster_shapes(
            shape_vectors,
            annual_totals,
            population,
        )
        yearly_clusters = self._build_yearly_cluster_results(
            yearly_paths, population
        )
        self.save_shape_visualizations(
            shape_vectors,
            annual_totals,
            monthly_totals,
            cluster_result,
            yearly_cluster_results=yearly_clusters,
        )
        output = {
            "aggregated_tsv_path": str(aggregated_path),
            "yearly_tsv_paths": {
                str(year): str(path) for year, path in yearly_paths.items()
            },
            "year_totals": year_totals,
            "yearly_clusters": yearly_clusters,
            "shape_vectors": shape_vectors,
            "clusters": cluster_result,
        }
        output_json_path = self.data_dir / (
            f"tourism-seasons-{self.data_year}-output.json"
        )
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, sort_keys=True)
            f.write("\n")
        return output
