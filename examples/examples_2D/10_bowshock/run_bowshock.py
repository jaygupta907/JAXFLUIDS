import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import numpy as np

from jaxfluids import InputManager, InitializationManager, SimulationManager
from jaxfluids_postprocess import load_data, create_2D_animation, create_2D_figure

# SETUP SIMULATION
input_manager = InputManager("bowshock.json", "numerical_setup.json")
initialization_manager = InitializationManager(input_manager)
sim_manager = SimulationManager(input_manager)

# RUN SIMULATION
jxf_buffers = initialization_manager.initialization()
sim_manager.simulate(jxf_buffers)

# LOAD DATA
path = sim_manager.output_writer.save_path_domain
quantities = [
    "density", "schlieren", "mach_number", 
    "levelset", "volume_fraction", "pressure"
]
jxf_data = load_data(path, quantities)

cell_centers = jxf_data.cell_centers
data = jxf_data.data
times = jxf_data.times

mask_real = data["volume_fraction"] > 0.0

# PLOT
nrows_ncols = (1,4)
plot_dict = {
    "density"       : data["density"]* mask_real,
    "pressure"      : data["pressure"]* mask_real,
    "mach_number"   : np.clip(data["mach_number"] * mask_real, 0.0, 3.0),
    "schlieren"     : np.clip(data["schlieren"] * mask_real, 1e0, 5e2)
}

# CREATE ANIMATION
create_2D_animation(
    plot_dict, 
    cell_centers, 
    times, 
    nrows_ncols=nrows_ncols, 
    plane="xy", plane_value=0.0,
    interval=100)

# CREATE FIGURE
create_2D_figure(
    plot_dict,
    nrows_ncols=nrows_ncols,
    cell_centers=cell_centers, 
    plane="xy", plane_value=0.0, 
    save_fig="bowshock.png")
