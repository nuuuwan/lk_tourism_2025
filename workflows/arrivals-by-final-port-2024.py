import json
import os

import plotly.graph_objects as go

DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "arrivals-by-final-port-2024.json"
)
OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "images",
    "arrivals-by-final-port-2024-world-map.png",
)

FONT_FAMILY = "Arial"

MIDDLE_EAST_COUNTRIES = {
    "United Arab Emirates",
    "Qatar",
    "Oman",
    "Kuwait",
    "Bahrain",
    "Saudi Arabia",
}

CIRCLE_COLOR = "rgba(220, 50, 50, 0.2)"
CIRCLE_BORDER_COLOR = "rgba(180, 20, 20, 0.5)"
MAP_BGCOLOR = "#c8dff5"
LAND_COLOR = "#f5f0e8"
BORDER_COLOR = "#aaaaaa"


def load_data(path):
    with open(path, "r") as f:
        return json.load(f)


def _is_middle_east(entry):
    country = entry["Country"]
    return any(me in country for me in MIDDLE_EAST_COUNTRIES)


def build_figure(data):
    lats = [d["latlng"][0] for d in data]
    lons = [d["latlng"][1] for d in data]
    arrivals = [d["Number of tourists"] for d in data]
    max_arrivals = max(arrivals)

    total_arrivals = sum(arrivals)
    me_arrivals = sum(
        d["Number of tourists"] for d in data if _is_middle_east(d)
    )
    me_ports = sorted(
        [
            f"{d['Final Port by Air']} ({d['IATA']})"
            for d in data
            if _is_middle_east(d)
        ]
    )
    me_pct = 100 * me_arrivals / total_arrivals

    # Scale so that the largest circle has a reference size of 200 (area units).
    # sizemode="area" means plotly treats size as the marker area, so
    # visual area is proportional to the value.
    sizes = [400 * (v / max_arrivals) for v in arrivals]

    hover_texts = [
        (
            f"<b>{d['Final Port by Air']} ({d['IATA']})</b><br>"
            f"Airport | {d['Country']}<br>"
            f"Arrivals: {d['Number of tourists']:,}<br>"
            f"Share: {d['% Share']:.2f}%"
        )
        for d in data
    ]

    fig = go.Figure()

    # All-airport bubble layer
    fig.add_trace(
        go.Scattergeo(
            lat=lats,
            lon=lons,
            mode="markers",
            marker=dict(
                size=sizes,
                sizemode="area",
                sizeref=1,
                color=CIRCLE_COLOR,
                line=dict(width=1, color=CIRCLE_BORDER_COLOR),
            ),
            text=hover_texts,
            hovertemplate="%{text}<extra></extra>",
            name="Arrivals",
            showlegend=False,
        )
    )

    fig.update_layout(
        title=dict(
            text=(
                "Sri Lanka Tourist Arrivals 2024 — Top 40 Final Airports of Embarkation<br>"
                "<sup>Circle area proportional to number of arrivals</sup>"
            ),
            x=0.5,
            xanchor="center",
            font=dict(family=FONT_FAMILY, size=16),
        ),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor=BORDER_COLOR,
            showland=True,
            landcolor=LAND_COLOR,
            showocean=True,
            oceancolor=MAP_BGCOLOR,
            showlakes=True,
            lakecolor=MAP_BGCOLOR,
            showcountries=True,
            countrycolor=BORDER_COLOR,
            countrywidth=0.5,
            projection_type="natural earth",
            lonaxis=dict(range=[-25, 175]),
            lataxis=dict(range=[-50, 75]),
        ),
        font=dict(family=FONT_FAMILY),
        paper_bgcolor="white",
        margin=dict(l=10, r=10, t=80, b=40),
        annotations=[
            dict(
                text=(
                    "Data Source: Sri Lanka Tourism Development Authority (SLTDA) 2024 |"
                    " Circle area ∝ arrivals"
                ),
                x=0,
                y=0,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="bottom",
                showarrow=False,
                font=dict(family=FONT_FAMILY, size=10, color="#666666"),
            ),
            dict(
                text=(
                    f"<b>Middle East</b><br>"
                    f"{me_pct:.1f}% of arrivals<br>"
                    f"{me_arrivals:,} tourists<br>"
                    f"via {len(me_ports)} airports"
                ),
                # Arrow tip points at the Gulf region (approx paper coords for
                # lon≈53, lat≈24 on the cropped natural-earth projection)
                x=0.37,
                y=0.46,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="bottom",
                ax=0,
                ay=80,
                axref="pixel",
                ayref="pixel",
                showarrow=True,
                arrowhead=2,
                arrowsize=1.2,
                arrowwidth=2,
                arrowcolor="#cc3333",
                bgcolor="rgba(255,255,255,0.92)",
                bordercolor="#cc3333",
                borderwidth=2,
                borderpad=10,
                font=dict(family=FONT_FAMILY, size=12, color="#333333"),
            ),
        ],
    )

    # Top-10 ranked labels with connector lines — added AFTER update_layout so
    # they are not overwritten by the annotations= list in update_layout.
    top10 = sorted(data, key=lambda d: d["Number of tourists"], reverse=True)[
        :10
    ]

    # Manually offset label positions (lat, lon) spread to avoid overlap.
    LABEL_POSITIONS = [
        (38, 58),  # 1  Dubai
        (34, 40),  # 2  Doha
        (10, 88),  # 3  Chennai
        (16, 58),  # 4  Abu Dhabi
        (20, 65),  # 5  Mumbai
        (34, 84),  # 6  Delhi
        (8, 71),  # 7  Bangalore
        (10, 108),  # 8  Kuala Lumpur
        (64, 25),  # 9  Moscow
        (-5, 113),  # 10 Singapore
    ]

    # Dotted connector lines: airport → label
    conn_lats, conn_lons = [], []
    for d, (lbl_lat, lbl_lon) in zip(top10, LABEL_POSITIONS):
        conn_lats += [d["latlng"][0], lbl_lat, None]
        conn_lons += [d["latlng"][1], lbl_lon, None]
    fig.add_trace(
        go.Scattergeo(
            lat=conn_lats,
            lon=conn_lons,
            mode="lines",
            line=dict(color="#888888", width=1, dash="dot"),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # Text labels at offset positions
    fig.add_trace(
        go.Scattergeo(
            lat=[pos[0] for pos in LABEL_POSITIONS],
            lon=[pos[1] for pos in LABEL_POSITIONS],
            mode="text",
            text=[
                f"<b>#{i} {d['Final Port by Air']} ({d['IATA']})</b><br>{d['Number of tourists']:,}"
                for i, d in enumerate(top10, start=1)
            ],
            textfont=dict(size=9, color="#222222", family=FONT_FAMILY),
            textposition="middle center",
            hoverinfo="skip",
            showlegend=False,
        )
    )

    return fig


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    data = load_data(DATA_PATH)
    fig = build_figure(data)
    fig.write_image(OUTPUT_PATH, width=1400, height=800, scale=2)
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
