import altair as alt
import numpy as np
import pandas as pd

def create_speed_graph(
    val: float,
    start_val: float,
    end_val: float,
    color: str,
    color_bg: str = "lightgray",
    width: int = 250,
    height: int = 250,
) -> alt.LayerChart:
    if val < start_val:
        val = start_val

    if val > end_val:
        val = end_val

    start_angle = -np.pi / 2
    total_span = np.pi

    percent_complete = (val - start_val) / (end_val - start_val)
    percent_remaining = 1.0 - percent_complete

    source = pd.DataFrame(
        [
            {"category": "Actual", "value": percent_complete, "color": color},
            {
                "category": "Remaining",
                "value": percent_remaining,
                "color": color_bg,
            },
        ]
    )

    background_chart = (
        alt.Chart(source)
        .mark_arc(
            innerRadius=70,  # Adjust to make the donut thicker or thinner
            outerRadius=100,
            cornerRadius=5,  # Slightly rounds the corners of the arc
            color=color_bg,
        )
        .encode(
            theta=alt.value(start_angle), theta2=alt.value(start_angle + total_span)
        )
    )

    end_angle = start_angle + (percent_complete * total_span)

    progress_chart = (
        alt.Chart(source)
        .mark_arc(innerRadius=70, outerRadius=100, cornerRadius=5, color=color)
        .encode(
            # The progress bar goes from the start angle to its calculated end angle
            theta=alt.value(start_angle),
            theta2=alt.value(end_angle),
        )
    )

    final_chart = (
        (background_chart + progress_chart)
        .properties(width=width, height=height)
        .configure_view(stroke=None)
    )

    return final_chart
