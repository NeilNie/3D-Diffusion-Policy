import numpy as np
import matplotlib.pyplot as plt
import trimesh
from PIL import Image



def assign_colors(a, b, colormap="viridis"):
    # Check if a < b
    if a >= b:
        raise ValueError("a must be less than b")

    # Create a range of values between a and b
    values = np.linspace(a, b, b - a + 1)

    # Get the viridis colormap
    if colormap == "viridis":
        colormap = plt.cm.viridis
    elif colormap == "jet":
        colormap = plt.cm.jet
    else:
        raise ValueError(f"colormap {colormap} not supported")

    # Normalize values to the range [0, 1] for colormap
    norm = plt.Normalize(a, b)

    # Assign colors to each value
    colors = [colormap(norm(value)) for value in values]
    colors = np.array(colors) * 255
    colors = colors.astype(np.uint8)
    return colors


def change_textured_mesh_color(mesh, rgba):
    assert type(mesh.visual) == trimesh.visual.texture.TextureVisuals, "mesh should be a textured mesh"
    texture_image = mesh.visual.material.image
    r, g, b, a = texture_image.split()
    # Set green and blue channels to 0 (leaving red channel as is)
    r = r.point(lambda i: rgba[0])
    g = g.point(lambda i: rgba[1])
    b = b.point(lambda i: rgba[2])
    a = a.point(lambda i: rgba[3])
    # Put channels back together, merge with image
    texture_image = Image.merge('RGBA', (r, g, b, a))
    mesh.visual.material.image = texture_image
