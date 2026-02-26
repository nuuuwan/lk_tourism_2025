from .TourismSeasonsChartCentroidsMixin import (
    TourismSeasonsChartCentroidsMixin,
)
from .TourismSeasonsChartClusterArrivalsByYearCoreMixin import (
    TourismSeasonsChartClusterArrivalsByYearCoreMixin,
)
from .TourismSeasonsChartClusterArrivalsByYearMixin import (
    TourismSeasonsChartClusterArrivalsByYearMixin,
)
from .TourismSeasonsChartClusterShapesCoreMixin import (
    TourismSeasonsChartClusterShapesCoreMixin,
)
from .TourismSeasonsChartClusterShapesMixin import (
    TourismSeasonsChartClusterShapesMixin,
)
from .TourismSeasonsChartHeatmapCoreMixin import (
    TourismSeasonsChartHeatmapCoreMixin,
)
from .TourismSeasonsChartHeatmapMixin import TourismSeasonsChartHeatmapMixin
from .TourismSeasonsChartTotalArrivalsByMonthMixin import (
    TourismSeasonsChartTotalArrivalsByMonthMixin,
)
from .TourismSeasonsChartUtilsMixin import TourismSeasonsChartUtilsMixin
from .TourismSeasonsChartWorldMapCoreMixin import (
    TourismSeasonsChartWorldMapCoreMixin,
)
from .TourismSeasonsChartWorldMapMixin import TourismSeasonsChartWorldMapMixin
from .TourismSeasonsClusterCoreMixin import TourismSeasonsClusterCoreMixin
from .TourismSeasonsClusterKMeansMixin import TourismSeasonsClusterKMeansMixin
from .TourismSeasonsConfigMixin import TourismSeasonsConfigMixin
from .TourismSeasonsDataTsvMixin import TourismSeasonsDataTsvMixin
from .TourismSeasonsExcelAggregateMixin import (
    TourismSeasonsExcelAggregateMixin,
)
from .TourismSeasonsExcelPipelineMixin import TourismSeasonsExcelPipelineMixin
from .TourismSeasonsExcelRowParseMixin import TourismSeasonsExcelRowParseMixin
from .TourismSeasonsExcelSchemaMixin import TourismSeasonsExcelSchemaMixin
from .TourismSeasonsWorkflowMixin import TourismSeasonsWorkflowMixin


class TourismSeasons(
    TourismSeasonsConfigMixin,
    TourismSeasonsExcelSchemaMixin,
    TourismSeasonsExcelRowParseMixin,
    TourismSeasonsExcelAggregateMixin,
    TourismSeasonsExcelPipelineMixin,
    TourismSeasonsDataTsvMixin,
    TourismSeasonsChartUtilsMixin,
    TourismSeasonsChartClusterShapesCoreMixin,
    TourismSeasonsChartClusterShapesMixin,
    TourismSeasonsChartCentroidsMixin,
    TourismSeasonsChartHeatmapCoreMixin,
    TourismSeasonsChartHeatmapMixin,
    TourismSeasonsChartTotalArrivalsByMonthMixin,
    TourismSeasonsChartClusterArrivalsByYearCoreMixin,
    TourismSeasonsChartClusterArrivalsByYearMixin,
    TourismSeasonsChartWorldMapCoreMixin,
    TourismSeasonsChartWorldMapMixin,
    TourismSeasonsClusterCoreMixin,
    TourismSeasonsClusterKMeansMixin,
    TourismSeasonsWorkflowMixin,
):
    def __init__(
        self,
        analysis_years=None,
        n_clusters=None,
        min_annual_arrivals=None,
        cluster_random_seed=None,
    ):
        TourismSeasonsConfigMixin.__init__(
            self,
            analysis_years=analysis_years,
            n_clusters=n_clusters,
            min_annual_arrivals=min_annual_arrivals,
            cluster_random_seed=cluster_random_seed,
        )
