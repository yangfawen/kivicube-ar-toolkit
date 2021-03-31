# Copyright (C) Facebook, Inc. and its affiliates
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Copyright (C) 2021 Wendell.Yang

import bpy
from bpy_extras.io_utils import ExportHelper

from .spark_operators_mixin import SparkOperatorsMixin


class OBJECT_OT_SparkOperator_ExportForSparkAR(bpy.types.Operator,
                                               SparkOperatorsMixin,
                                               ExportHelper):
    bl_idname = 'object.export_for_spark_ar'
    bl_label = '导出网格'
    bl_description = 'Export optimized mesh'
    bl_options = {'PRESET'}

    filename_ext = '.glb'
    hide_props_region = True

    filter_glob: bpy.props.StringProperty(
        default='*.glb',
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        if bpy.ops.object.spark_decimation.poll():
            bpy.ops.object.spark_decimation()

        self.tag_from_plugin(context)
        self._export_mesh()

        self.report({'INFO'}, '导出成功')

        return {'FINISHED'}

    def _export_mesh(self):
        bpy.ops.export_scene.gltf(
            # Format
            export_format='GLB',
            filepath=self.filepath,
            check_existing=False,

            # Setup
            export_cameras=False,
            export_lights=False,
            export_yup=True,
            use_selection=True,
            export_extras=True,
            will_save_settings=True,

            # Materials and Textures
            export_texcoords=True,
            export_image_format='AUTO',

            # Mesh Data
            export_normals=True,
            export_colors=True,

            # Deformers
            export_skins=True,
            export_morph=True,

            # Animation
            export_animations=True,
            export_force_sampling=False
        )
