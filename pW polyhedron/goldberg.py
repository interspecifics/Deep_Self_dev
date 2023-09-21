import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

def icosahedron_vertices():
    phi = (1 + np.sqrt(5)) / 2
    vertices = np.array([
        [-1, phi, 0],
        [1, phi, 0],
        [-1, -phi, 0],
        [1, -phi, 0],
        [0, -1, phi],
        [0, 1, phi],
        [0, -1, -phi],
        [0, 1, -phi],
        [phi, 0, -1],
        [phi, 0, 1],
        [-phi, 0, -1],
        [-phi, 0, 1]
    ])
    vertices /= np.linalg.norm(vertices, axis=1)[:, np.newaxis]
    return vertices

def subdivide_triangles(vertices, triangles):
    new_triangles = []
    new_vertices = list(vertices)
    for triangle in triangles:
        midpoints = [
            (vertices[triangle[i]] + vertices[triangle[(i + 1) % 3]]) / 2
            for i in range(3)
        ]
        midpoints = [midpoint / np.linalg.norm(midpoint) for midpoint in midpoints]
        new_vertices.extend(midpoints)
        i, j, k = triangle
        a, b, c = len(new_vertices) - 3, len(new_vertices) - 2, len(new_vertices) - 1
        new_triangles.extend([
            [i, a, c],
            [j, b, a],
            [k, c, b],
            [a, b, c]
        ])
    return np.array(new_vertices), new_triangles

def filter_top_half(vertices, triangles):
    return [triangle for triangle in triangles if all(vertices[triangle[i]][2] >= 0 for i in range(3))]

def extract_edges(triangles):
    edges = set()
    for triangle in triangles:
        for i in range(3):
            edge = tuple(sorted([triangle[i], triangle[(i + 1) % 3]]))
            edges.add(edge)
    return list(edges)

triangles = [
    [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
    [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
    [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
    [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
]

def main():
    vertices = icosahedron_vertices()
    triangles = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ]
    for _ in range(2):  # Number of subdivisions
        vertices, triangles = subdivide_triangles(vertices, triangles)
    top_half_triangles = filter_top_half(vertices, triangles)

    print(len(top_half_triangles))
    edges = extract_edges(top_half_triangles)
    edge_coords = [np.array([vertices[start], vertices[end]]) for start, end in edges]
    
    # Plot with modified grid and axis opacity
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.add_collection3d(Poly3DCollection(vertices[top_half_triangles], facecolor='cyan', edgecolor='none', alpha=0.25))
    ax.add_collection3d(Line3DCollection(edge_coords, colors='darkgray', linewidths=1))

    # Modify opacity of the grid
    ax.xaxis.pane.fill = True
    ax.yaxis.pane.fill = True
    ax.zaxis.pane.fill = True
    ax.xaxis.pane.set_alpha(0.1)  # Set opacity (0 = transparent, 1 = opaque)
    ax.yaxis.pane.set_alpha(0.1)
    ax.zaxis.pane.set_alpha(0.1)

    # Modify opacity and appearance of the axis lines
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.line.set_lw(0.0)
        axis.line.set_alpha(0.01)  # Set opacity for axis lines

    ax.set_box_aspect([1, 1, 1])
    ax.dist = 12
    plt.show()


if __name__ == "__main__":
    main()
