#!/auto/vestec1-elixir/home/manishkumar/.conda/envs/kpython310/bin/python3.1
import numpy as np
import sys
from ase.io import read,write


atoms = read(sys.argv[1])
rotated_atoms = atoms.copy()
coordinate = rotated_atoms.positions

def fit_plane(points):
    # Center the points to improve accuracy
    centroid = np.mean(points, axis=0)
    centered_points = points - centroid
    # Perform SVD to find the normal vector
    _, _, Vt = np.linalg.svd(centered_points)
    normal_vector = Vt[-1]
    return normal_vector

def get_rotation_matrix(normal_vector):
    z_axis = np.array([0, 0, 1])
    v = np.cross(normal_vector, z_axis)
    s = np.linalg.norm(v)
    c = np.dot(normal_vector, z_axis)
    v_cross = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.identity(3) + v_cross + np.dot(v_cross, v_cross) * ((1 - c) / (s ** 2))
    return rotation_matrix

# Rotate points to make the normal vector perpendicular to the XY plane while preserving bond lengths
def rotate_to_perpendicular_with_preservation(points, normal_vector):
    rotation_matrix = get_rotation_matrix(normal_vector)
    rotated_points = np.dot(points, rotation_matrix.T)
    return rotated_points

norm_vec = fit_plane(coordinate)
rotated_points = rotate_to_perpendicular_with_preservation(coordinate, norm_vec)
rotated_atoms.positions = rotated_points - np.mean(rotated_points, axis=0)
if len(sys.argv)>2:
    write(sys.argv[2],rotated_atoms)
else:
    write('rotated_geom.xyz',rotated_atoms)



