# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from . geometry import DSC_geometry

from mathutils import Vector, Matrix
from math import cos, sin, pi, degrees


class Arc():

    def __init__(self, point_end):
        valid, self.radius, self.angle, self.determinant = \
            self.get_radius_angle_det(Vector((0.0, 0.0, 0.0)), point_end)
        if valid:
            if self.determinant > 0:
                self.offset_angle = 0
                self.curvature = 1/self.radius
                self.offset_y = self.radius
                if self.angle < 0:
                    # Limit angle to 180 degrees
                    self.heading_end  = pi
                    self.angle = pi
                else:
                    self.heading_end  = self.angle
            else:
                self.offset_angle = pi
                self.curvature = -1/self.radius
                self.offset_y = -self.radius
                if self.angle > 0:
                    # Limit angle to 180 degrees
                    self.heading_end = pi
                    self.angle = -pi
                else:
                    self.heading_end = self.angle
        else:
            self.radius = 1
            self.curvature = 1
            self.offset_y = self.radius
            self.angle = 0
            self.offset_angle = 0
            self.heading_end = 0
        self.length = self.radius * abs(self.angle)

    def get_radius_angle_det(self, point_start, point_end):
        '''
            Calculate center and radius of the arc that is defined by the
            starting point (predecessor connection point), the start heading
            (heading of the connected road) and the end point. Also return
            determinant that tells us if point end is left or right of heading
            direction.
        '''
        # The center of the arc is the crossing point of line orthogonal to the
        # predecessor road in the connection point and the perpendicular
        # bisector of the connection between start and end point.
        p = point_start.to_2d()
        a = Vector((0.0, 1.0))
        q = 0.5 * (point_start + point_end).to_2d()
        b_normal = (point_start - point_end)
        b = Vector((-b_normal[1], b_normal[0]))
        if a.orthogonal() @ b != 0:
            # See https://mathepedia.de/Schnittpunkt.html for crossing point equation
            center = 1 / (a @ b.orthogonal()) * ((q @ b.orthogonal()) * a - (p @ a.orthogonal()) * b)
            radius = (center - p).length
            # Calculate determinant to know where to start drawing the arc {0, pi}
            vec_hdg = Vector((1.0, 0.0, 0.0))
            determinant = Matrix([vec_hdg.to_2d(), (point_end - point_start).to_2d()]).transposed().determinant()
            angle = (point_end.to_2d() - center).angle_signed(point_start.to_2d() - center)
            return True, radius, angle, determinant
        else:
            return False, 0, 0, 0

class DSC_geometry_arc(DSC_geometry):

    def update(self, point_start, heading_start, point_end, heading_end):
        # Calculate transform between global and local coordinates
        self.update_local_to_global(point_start, heading_start)

        # Transform end point to local coordinates, constrain and transform back
        point_end_local = self.matrix_world.inverted() @ point_end
        if point_end_local.x < 0:
            point_end_local.x = 0
        point_end_global = self.matrix_world @ point_end_local

        # Calculate geometry
        self.geometry_base = Arc(point_end_local)

        # Remember geometry parameters
        self.params = {'curve': 'arc',
                       'point_start': point_start,
                       'heading_start': heading_start,
                       'point_end': point_end_global,
                       'heading_end': heading_start + self.geometry_base.heading_end,
                       'angle': self.geometry_base.angle,
                       'curvature': self.geometry_base.curvature,
                       'length': self.geometry_base.length}

    def sample_local(self, s, t_vec):
        angle_s = s / self.geometry_base.radius
        if self.geometry_base.determinant > 0:
            x_s_0 = cos(angle_s + self.geometry_base.offset_angle - pi/2) \
                    * self.geometry_base.radius
            y_s_0 = sin(angle_s + self.geometry_base.offset_angle - pi/2) \
                    * self.geometry_base.radius + self.geometry_base.offset_y
            hdg_t = angle_s + pi/2
        else:
            x_s_0 = cos(-angle_s + self.geometry_base.offset_angle - pi/2) \
                    * self.geometry_base.radius
            y_s_0 = sin(-angle_s + self.geometry_base.offset_angle - pi/2) \
                    * self.geometry_base.radius + self.geometry_base.offset_y
            hdg_t = -angle_s + pi/2
        vector_hdg_t = Vector((1.0, 0.0))
        vector_hdg_t.rotate(Matrix.Rotation(hdg_t, 2))
        xyz = []
        for t in t_vec:
            xy_vec = Vector((x_s_0, y_s_0)) + t * vector_hdg_t
            xyz += [(xy_vec.x, xy_vec.y, 0)]
        return xyz, self.geometry_base.curvature
