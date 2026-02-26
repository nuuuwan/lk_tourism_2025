import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np


class TourismSeasonsChartTotalArrivalsByMonthMixin:
    def _monthly_shares(self, monthly_totals):
        total_arrivals = sum(monthly_totals)
        return (
            [value / total_arrivals for value in monthly_totals]
            if total_arrivals > 0
            else [0.0 for _ in monthly_totals]
        )

    def _style_total_arrivals_axis(self, axis, x_positions):
        axis.axhline(
            y=self.uniform_monthly_share,
            color="#555555",
            linestyle=":",
            linewidth=1.5,
            label="Uniform monthly share (8.33%)",
        )
        axis.set_title(
            "Sri Lanka Tourism: Total Arrivals Share by Month",
            fontsize=16,
        )
        axis.set_xlabel("Month")
        axis.set_ylabel("Share of total arrivals (%)")
        axis.set_xticks(x_positions)
        axis.set_xticklabels(self.months)
        axis.tick_params(axis="x", rotation=45)
        axis.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
        axis.legend(frameon=False)

    def _plot_total_arrivals_by_month(self, monthly_totals, output_path):
        monthly_shares = self._monthly_shares(monthly_totals)

        x_positions = np.arange(len(self.months))
        figure, axis = plt.subplots(figsize=(12, 6))
        axis.fill_between(
            x_positions,
            monthly_shares,
            color="#2f6da1",
            alpha=0.35,
        )
        axis.plot(
            x_positions,
            monthly_shares,
            linewidth=2,
            color="#2f6da1",
        )
        self._style_total_arrivals_axis(axis, x_positions)
        self._add_source_footer(figure, include_filter=False)
        figure.tight_layout(rect=(0, 0.03, 1, 1))
        figure.savefig(output_path, dpi=220)
        plt.close(figure)

    def save_chart_total_arrivals_by_month(self, monthly_totals):
        self._plot_total_arrivals_by_month(
            monthly_totals,
            os.path.join(self.images_dir, "total-arrivals-by-month.png"),
        )
