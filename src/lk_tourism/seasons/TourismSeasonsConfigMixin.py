from pathlib import Path


class TourismSeasonsConfigMixin:
    def __init__(
        self,
        analysis_years=None,
        n_clusters=None,
        min_annual_arrivals=None,
        cluster_random_seed=None,
    ):
        self._init_paths()
        self._init_time_dimensions()
        self._init_parameters()
        self._apply_parameter_overrides(
            analysis_years=analysis_years,
            n_clusters=n_clusters,
            min_annual_arrivals=min_annual_arrivals,
            cluster_random_seed=cluster_random_seed,
        )
        self._init_metadata()
        self._init_files()
        self._init_month_token_map()

    def _normalized_analysis_years(self, analysis_years):
        years = sorted({int(year) for year in analysis_years})
        if not years:
            raise ValueError("analysis_years must not be empty")
        return years

    def _apply_parameter_overrides(
        self,
        analysis_years,
        n_clusters,
        min_annual_arrivals,
        cluster_random_seed,
    ):
        if analysis_years is not None:
            self.analysis_years = self._normalized_analysis_years(
                analysis_years
            )
        if n_clusters is not None:
            self.n_clusters = int(n_clusters)
        if min_annual_arrivals is not None:
            self.min_annual_arrivals = int(min_annual_arrivals)
        if cluster_random_seed is not None:
            self.cluster_random_seed = int(cluster_random_seed)

    def _init_paths(self):
        self.work_dir = Path(__file__).resolve().parents[3]
        self.data_dir = self.work_dir / "data"
        self.images_dir = self.work_dir / "images"

    def _init_time_dimensions(self):
        self.analysis_years = [2024, 2025]
        self.months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]

    def _init_parameters(self):
        self.min_annual_arrivals = 20_000
        self.n_clusters = 4
        self.cluster_random_seed = 0
        self.uniform_monthly_share = 1.0 / 12.0

    def _init_metadata(self):
        self.data_source = "SLTDA"
        self.analysis_by = "Nuwan I. Senaratna"
        years = sorted(self.analysis_years)
        self.data_year = (
            str(years[0]) if len(years) == 1 else f"{years[0]}-{years[-1]}"
        )
        self.font_family = "PT Sans"

    def _init_files(self):
        self.yearly_tsv_template = (
            "tourist-arrivals-{year}-by-country-and-month.tsv"
        )
        self.aggregated_tsv_path = self.data_dir / (
            f"tourist-arrivals-{self.data_year}-aggregated.tsv"
        )
        self.population_tsv_path = self.data_dir / "country-population.tsv"

    def _init_month_token_map(self):
        self.month_token_map = {
            "jan": "Jan",
            "january": "Jan",
            "feb": "Feb",
            "february": "Feb",
            "mar": "Mar",
            "march": "Mar",
            "apr": "Apr",
            "april": "Apr",
            "may": "May",
            "jun": "Jun",
            "june": "Jun",
            "jul": "Jul",
            "july": "Jul",
            "aug": "Aug",
            "august": "Aug",
            "sep": "Sep",
            "sept": "Sep",
            "september": "Sep",
            "oct": "Oct",
            "october": "Oct",
            "nov": "Nov",
            "november": "Nov",
            "dec": "Dec",
            "december": "Dec",
        }
