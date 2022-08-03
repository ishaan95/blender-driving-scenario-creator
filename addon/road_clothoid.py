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

from . road_base import DSC_OT_road
from . geometry_clothoid import DSC_geometry_clothoid


class DSC_OT_road_clothoid(DSC_OT_road):
    bl_idname = "dsc.road_clothoid"
    bl_label = "Clothoid"
    bl_description = "Create a clothoid (Euler spiral) road"
    bl_options = {'REGISTER', 'UNDO'}

    object_type = 'road_clothoid'
    snap_filter = 'OpenDRIVE'

    geometry = DSC_geometry_clothoid()
