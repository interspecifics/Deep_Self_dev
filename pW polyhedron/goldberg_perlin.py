import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise3
from goldberg import icosahedron_vertices, subdivide_triangles, filter_top_half, triangles
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation

# Generate the icosahedron and subdivide its triangles
vertices = icosahedron_vertices()
for _ in range(2):
    vertices, triangles = subdivide_triangles(vertices, triangles)
triangles = filter_top_half(vertices, triangles)

# Function to generate a Perlin noise map
# Create two side-by-side 3D plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), subplot_kw=dict(projection="3d"))

fig.patch.set_facecolor('#f2f2f2')

fig.suptitle('pulseWidth polyhedron   \n  perlin modulation  \n  152 faces ', fontsize=20, horizontalalignment='right', name='Monospace')


# Function to generate a Perlin noise map
def generate_noise_map(base, num_points=152, octaves=1, persistence=0.1, repeatx=1024, repeaty=1024, repeatz=1024):
    """Generate a Perlin noise map based on the generate_terrain logic."""
    noise_values = []
    x_step = 100.0 / num_points
    y_step = 100.0 / num_points

    for i in range(num_points):
        # Simulating a 2D grid using single loop
        x_val = i * x_step
        y_val = i * y_step
        noise_values.append(pnoise3(x_val, y_val, base, octaves=octaves, persistence=persistence,
                                    # repeatx=repeatx, repeaty=repeaty, repeatz=repeatz
                                    ))
    
    return noise_values

# Custom function to style the axes
def style_axes(ax):
    # Adjusting the alpha and making the labels bold
    ax.xaxis.label.set_alpha(0.1)
    ax.yaxis.label.set_alpha(0.1)
    ax.zaxis.label.set_alpha(0.1)
    ax.xaxis.label.set_weight('bold')
    ax.yaxis.label.set_weight('bold')
    ax.zaxis.label.set_weight('bold')

    # Adjusting the alpha and making the tick labels bold
    for label in ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels():
        label.set_alpha(0.4)
        label.set_weight('bold')

    # Adjusting the alpha for the axes lines
    ax.xaxis.line.set_alpha(0.4)
    ax.yaxis.line.set_alpha(0.4)
    ax.zaxis.line.set_alpha(0.4)

    # Adjusting the alpha for the tick lines
    for line in ax.xaxis.get_ticklines() + ax.yaxis.get_ticklines() + ax.zaxis.get_ticklines():
        line.set_alpha(0.4)

    # Set the background color of the 3D axes (the panes) to light gray
    ax.xaxis.set_pane_color((0.8, 0.8, 0.8, .4))
    ax.yaxis.set_pane_color((0.8, 0.8, 0.8, .4))
    ax.zaxis.set_pane_color((0.8, 0.8, 0.8, .4))

    # Remove the white frame around the subplot
    ax.set_frame_on(False)

    ax.set_facecolor('#f2f2f2')




def update(frame):
    # Update the Goldberg polyhedron
    ax1.clear()
    ax1.view_init(elev=35, azim=25)
    
    noise_values = generate_noise_map(frame * 0.1)
    norm = plt.Normalize(min(noise_values), max(noise_values))
    colors = plt.cm.cividis(norm(noise_values))

    for triangle, color in zip(triangles, colors):
        polygon = [vertices[v] for v in triangle]
        ax1.add_collection3d(Poly3DCollection([polygon], color=color, alpha=0.5))
    
    # Set limits for the Goldberg polyhedron
    ax1.set_xlim([-0.7, 0.7])
    ax1.set_ylim([-0.7, 0.7])
    ax1.set_zlim([-0.7, 0.7])

    # Update the Perlin blanket
    ax2.clear()
    ax2.view_init(elev=35, azim=25)
    
    x = np.linspace(0, 5, 12)
    y = np.linspace(0, 5, 12)
    x, y = np.meshgrid(x, y)
    z = generate_noise_map(frame * 0.01, num_points=12*12)
    z = np.array(z).reshape(12, 12)
    ax2.plot_surface(x, y, z, cmap="cividis", edgecolor='none', rstride=1, cstride=1)
    
    # Set limits for the Perlin blanket
    ax2.set_xlim([0, 5])
    ax2.set_ylim([0, 5])
    ax2.set_zlim([-0.1, 1])
    
    # Apply the custom style to both ax1 and ax2
    style_axes(ax1)
    style_axes(ax2)

    return ax1.collections + ax2.collections

ani = FuncAnimation(fig, update, frames=1000, interval=10)

plt.show()

