import argparse
import sys
from pathlib import Path

WORK_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = WORK_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--analysis-years",
        nargs="+",
        type=int,
        help="Years to include (e.g. --analysis-years 2024 2025)",
    )
    parser.add_argument(
        "--n-clusters",
        type=int,
        help="Number of k-means clusters",
    )
    parser.add_argument(
        "--min-annual-arrivals",
        type=int,
        help="Annual arrivals cutoff for country filtering",
    )
    parser.add_argument(
        "--cluster-random-seed",
        type=int,
        help="Random seed for clustering",
    )
    return parser.parse_args()


if __name__ == "__main__":
    from lk_tourism.seasons import TourismSeasons

    args = _parse_args()
    TourismSeasons(
        analysis_years=args.analysis_years,
        n_clusters=args.n_clusters,
        min_annual_arrivals=args.min_annual_arrivals,
        cluster_random_seed=args.cluster_random_seed,
    ).run_tourism_seasons_workflow(print_json=True)
