"""
Author: Murat Berk Buzluk

Plot velocity deficit profiles

This example illustrates how to plot velocity deficit profiles at several locations
downstream of a turbine. Here we use the following definition:
    velocity_deficit = (homogeneous_wind_speed - u) / homogeneous_wind_speed
        , where u is the wake velocity obtained when the incoming wind speed is the
        same at all heights and equal to `homogeneous_wind_speed`.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker

import floris.flow_visualization as flowviz
from floris import FlorisModel
from floris.flow_visualization import VelocityProfilesFigure
from floris.utilities import reverse_rotate_coordinates_rel_west


# The first two functions are just used to plot the coordinate system in which the
# profiles are sampled. Please go to the main function to begin the example.
def plot_coordinate_system(x_origin, y_origin, wind_direction):
    quiver_length = 1.4 * D
    plt.quiver(
        [x_origin, x_origin],
        [y_origin, y_origin],
        [quiver_length, quiver_length],
        [0, 0],
        angles=[270 - wind_direction, 360 - wind_direction],
        scale_units="x",
        scale=1,
    )
    annotate_coordinate_system(x_origin, y_origin, quiver_length)


def annotate_coordinate_system(x_origin, y_origin, quiver_length):
    x1 = np.array([quiver_length + 0.35 * D, 0.0])
    x2 = np.array([0.0, quiver_length + 0.35 * D])
    x3 = np.array([90.0, 90.0])
    x, y, _ = reverse_rotate_coordinates_rel_west(
        fmodel.wind_directions,
        x1[None, :],
        x2[None, :],
        x3[None, :],
        x_center_of_rotation=0.0,
        y_center_of_rotation=0.0,
    )

    # sada
    x = np.squeeze(x, axis=0) + x_origin
    y = np.squeeze(y, axis=0) + y_origin
    plt.text(x[0], y[0], "$x_1$", bbox={"facecolor": "white"})
    plt.text(x[1], y[1], "$x_2$", bbox={"facecolor": "white"})


if __name__ == "__main__":
    D = 1.1  # Turbine diameter  
    hub_height = 0.8
    homogeneous_wind_speed = 5.4

    fmodel = FlorisModel("C:/Users/Murat Berk/Desktop/24-25 Summer/Wind Turbine/floris/gch.yaml")
    # fmodel = FlorisModel("gch.yaml")
    fmodel.set(layout_x=[0.0], layout_y=[0.0])

    # ------------------------------ Single-turbine layout ------------------------------
    # We first show how to sample and plot velocity deficit profiles on a single-turbine layout.
    # Lines are drawn on a horizontal plane to indicate were the velocity is sampled.
    downstream_dists = D * np.array([2, 3, 4])
    # Sample three profiles along three corresponding lines that are all parallel to the y-axis
    # (cross-stream direction). The streamwise location of each line is given in `downstream_dists`.
    profiles = fmodel.sample_velocity_deficit_profiles(
        direction="cross-stream",
        downstream_dists=downstream_dists,
        homogeneous_wind_speed=homogeneous_wind_speed,
    )

    # Initialize a VelocityProfilesFigure. The workflow is similar to a matplotlib Figure:
    # Initialize it, plot data, and then customize it further if needed.
    print(downstream_dists)
    profiles_fig = VelocityProfilesFigure(
        downstream_dists_D=downstream_dists / D,
        layout=["cross-stream"],
        coordinate_labels=["x/D", "y/D"],
    )
    # Add profiles to the VelocityProfilesFigure. This method automatically matches the supplied
    # profiles to the initialized axes in the figure.
    profiles_fig.add_profiles(profiles, color="k")

    # The dashed reference lines show the extent of the rotor
    profiles_fig.add_ref_lines_x2([-0.5, 0.5])
    for ax in profiles_fig.axs[0]:
        ax.xaxis.set_major_locator(ticker.MultipleLocator(0.2))

    profiles_fig.axs[0, 0].legend(["gauss"], fontsize=11)
    profiles_fig.fig.suptitle(
        "Velocity deficit profiles from different gaussian model",
        fontsize=14,
    )

    plt.show()
import warnings

warnings.filterwarnings('ignore')
