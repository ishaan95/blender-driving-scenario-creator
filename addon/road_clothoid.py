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

import bpy
from mathutils import Vector, Matrix

from . road_base import DSC_OT_road
from . geometry_clothoid import DSC_geometry_clothoid
from . import helpers

from math import pi, sin, cos, acos, ceil


class DSC_OT_road_clothoid(DSC_OT_road):
    bl_idname = "dsc.road_clothoid"
    bl_label = "Clothoid"
    bl_description = "Create a clothoid (Euler spiral) road"
    bl_options = {'REGISTER', 'UNDO'}

    object_type = 'road_clothoid'
    snap_filter = 'OpenDRIVE'

    geometry = DSC_geometry_clothoid()

    def constrain_point_end(self, point_start, heading_start, point_selected_end):
        '''
            Constrain the endpoint if necessary.
        '''
        return point_selected_end