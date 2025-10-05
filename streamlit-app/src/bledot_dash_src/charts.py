import altair as alt
import numpy as np
import pandas as pd


default_colors = {
    "background": "lightgray",
    "val": "#5fadde",
    "avg": "#007fcf"
}

def get_colors(label: str, issues: set[str]) -> tuple[str, str]:
    colors = {
        "val_good": "#68e39c",
        "avg_good": "#02ad4a",
        "val_bad": "#ff6759",
        "avg_bad": "#d41604",
    }

    if label in issues:
        return colors["val_bad"], colors["avg_bad"]
    return colors["val_good"], colors["avg_good"]


def frac_val(val: float, start_val: float, end_val: float) -> float:
    if start_val == end_val:
        return 0

    return (val - start_val) / (end_val - start_val)


def create_speed_chart(
    val: float,
    start_val: float,
    end_val: float,
    min_val: float,
    max_val: float,
    format_str: str,
    title: str,
    color_val: str = default_colors["val"],
    color_avg: str = default_colors["avg"],
    color_bg: str = default_colors["background"],
    inner_radius: float = 70.0,
    outer_radius: float = 100.0,
    corner_radius: float = 5.0,
    width: int = 250,
    height: int = 280,
) -> alt.LayerChart:
    val = min(max(val, start_val), end_val)
    min_val = min(max(min_val, start_val), end_val)
    max_val = min(max(max_val, start_val), end_val)

    start_angle = -np.pi / 2
    total_span = np.pi

    frac_min = frac_val(min_val, start_val, end_val)
    frac_avg = frac_val(val, start_val, end_val)
    frac_max = frac_val(max_val, start_val, end_val)

    source = pd.DataFrame(
        [
            {"category": "range", "value": frac_max - frac_min, "color": color_val},
            {"category": "average", "value": 0.06, "color": color_avg},
            {"category": "background", "value": 1, "color": color_bg},
        ]
    )

    text = pd.DataFrame([{"label": format_str.format(val), "title": title}])

    background_chart = (
        alt.Chart(source)
        .mark_arc(
            innerRadius=inner_radius,
            outerRadius=outer_radius,
            cornerRadius=corner_radius,
            color=color_bg,
        )
        .encode(
            theta=alt.value(start_angle), theta2=alt.value(start_angle + total_span)
        )
    )

    min_angle = total_span * frac_min
    avg_angle = total_span * frac_avg
    max_angle = total_span * frac_max

    progress_chart = (
        alt.Chart(source)
        .mark_arc(
            innerRadius=inner_radius,
            outerRadius=outer_radius,
            cornerRadius=corner_radius,
            color=color_val,
        )
        .encode(
            theta=alt.value(start_angle + min_angle),
            theta2=alt.value(start_angle + max_angle),
        )
    )

    avg_chart = (
        alt.Chart(source)
        .mark_arc(
            innerRadius=inner_radius,
            outerRadius=outer_radius,
            cornerRadius=corner_radius / 4,
            color=color_avg,
        )
        .encode(
            theta=alt.value(start_angle + avg_angle - 0.03),
            theta2=alt.value(start_angle + avg_angle + 0.03),
        )
    )

    label = (
        alt.Chart(text)
        .mark_text(
            align="center", baseline="middle", fontSize=28, fontWeight="bold", dy=-20
        )
        .encode(text="label:N")
    )

    title_label = (
        alt.Chart(text)
        .mark_text(
            align="center", baseline="middle", fontSize=22, fontWeight="bold", dy=-120
        )
        .encode(text="title:N")
    )

    final_chart = (
        (background_chart + progress_chart + avg_chart + label + title_label)
        .properties(width=width, height=height)
        .configure_view(stroke=None)
    )

    return final_chart


def create_hsbar_chart(
    val: float,
    min_val: float,
    max_val: float,
    format_str: str,
    title: str,
    start_val: float = 0,
    end_val: float = 100,
    color_val: str = default_colors["val"],
    color_avg: str = default_colors["avg"],
    color_bg: str = default_colors["background"],
    corner_radius: float = 5.0,
    width: int = 250,
    height: int = 280,
):
    val = min(max(val, start_val), end_val)
    min_val = min(max(min_val, start_val), end_val)
    max_val = min(max(max_val, start_val), end_val)

    df = pd.DataFrame(
        [
            {"category": "value", "start": 0, "end": max_val, "color": color_bg},
            {"category": "value", "start": min_val, "end": max_val, "color": color_val},
            {
                "category": "value",
                "start": val - 0.5,
                "end": val + 0.5,
                "color": color_avg,
            },
        ]
    )

    text = pd.DataFrame([{"label": format_str.format(val), "title": title}])

    bar_chart = (
        alt.Chart(df)
        .mark_bar(height=0.6 * height, cornerRadius=corner_radius)
        .encode(
            x=alt.X(
                "start:Q",
                scale=alt.Scale(domain=[0, 100]),
                axis=alt.Axis(title=None),
            ),
            x2=alt.X2("end:Q"),
            y=alt.Y("category:N", title=None, axis=alt.Axis(labels=False, ticks=False)),
            color=alt.Color("color:N", scale=None),
            # order=alt.Order("order_column", sort="ascending"),
            tooltip=alt.value(None),
        )
        .properties(title=title, width=0.75 * width, height=height)
    )

    text_label = (
        alt.Chart(text)
        .mark_text(
            align="left", baseline="middle", fontSize=28, fontWeight="bold", dx=10
        )
        .encode(text=alt.Text("label"))
        .properties(height=height)
    )

    final_chart = alt.hconcat(bar_chart, text_label).configure_view(stroke=None)

    return final_chart


def create_card_chart(
    val: float,
    format_str: str,
    title: str,
    color: str = default_colors["avg"],
    width: int = 250,
    height: int = 280,
):
    text = pd.DataFrame([{"label": format_str.format(val), "title": title}])

    label = (
        alt.Chart(text)
        .mark_text(
            align="center", baseline="middle", fontSize=56, fontWeight="bold", dy=40, color=color
        )
        .encode(text=alt.Text("label"))
    )

    title_label = (
        alt.Chart(text)
        .mark_text(
            align="center", baseline="middle", fontSize=30, fontWeight="bold", dy=-60
        )
        .encode(text=alt.Text("title"))
    )

    final_chart = (
        (label + title_label)
        .properties(width=width, height=height)
        .configure_view(stroke=None)
    )

    return final_chart
