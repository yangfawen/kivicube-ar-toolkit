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

import bpy

from .spark_operators_mixin import (
    is_context_valid,
    SparkOperatorsMixin,
)

SPARK_DECIMATE_MODIFIER_NAME = 'SparkDecimateModifier'


def update_sparkar_optimization_settings(context):
    if not is_context_valid(context):
        return
    settings = context.active_object.sparkar_optimization
    percentage = settings.InvertedReducePercentage
    if context.object.modifiers.find(SPARK_DECIMATE_MODIFIER_NAME) != -1:
        ratio_field = (100 - percentage) / 100
        ratio_modifier = context.object.modifiers[
            SPARK_DECIMATE_MODIFIER_NAME].ratio
        if ratio_field != ratio_modifier:
            settings.InvertedReducePercentage = (1 - ratio_modifier) * 100


def update_spark_decimation_ratio(self, context):
    if not is_context_valid(context):
        return
    percentage = context.active_object.sparkar_optimization\
        .InvertedReducePercentage
    if percentage != 0:
        if context.object.modifiers.find(SPARK_DECIMATE_MODIFIER_NAME) == -1:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.modifier_add(type='DECIMATE')
            context.object.modifiers[-1].name = SPARK_DECIMATE_MODIFIER_NAME
            context.object.modifiers[
                SPARK_DECIMATE_MODIFIER_NAME].decimate_type = 'COLLAPSE'
        ratio = (100 - percentage) / 100
        context.object.modifiers[SPARK_DECIMATE_MODIFIER_NAME].ratio = ratio


class SparkARToolkitOptimizationSettings(bpy.types.PropertyGroup):
    InvertedReducePercentage: bpy.props.FloatProperty(
        subtype='PERCENTAGE',
        update=update_spark_decimation_ratio,
        default=0, min=0, precision=0, name='',
    )


class OBJECT_OT_SparkOperator_MeshCleanUp(bpy.types.Operator,
                                          SparkOperatorsMixin):
    bl_idname = 'object.spark_mesh_cleanup'
    bl_label = 'Clean up mesh'
    bl_description = 'Clean up mesh'
    bl_options = {'REGISTER', 'UNDO'}

    TEXTURE_MAX_SIZE = 1024
    REMOVE_DOUBLES_THRESHOLD = 0.0001
    NONPLANAR_ANGLE_LIMIT = 0.0872665

    def _cleanup_textures(self, context):
        textures_list = []
        for material_slot in bpy.context.active_object.material_slots:
            if material_slot.material and material_slot.material.node_tree:
                nodes = material_slot.material.node_tree.nodes
                images = [node for node in nodes if node.type == 'TEX_IMAGE']
                textures_list.extend(images)

        for texture in textures_list:
            if texture.image and texture.image.size[0] > self.TEXTURE_MAX_SIZE:
                name = texture.image.name
                bpy.data.images[name].scale(self.TEXTURE_MAX_SIZE,
                                            self.TEXTURE_MAX_SIZE)
                bpy.data.images[name].save()
                bpy.data.images[name].reload()

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.delete_loose()
        bpy.ops.mesh.dissolve_degenerate()
        bpy.ops.mesh.remove_doubles(threshold=self.REMOVE_DOUBLES_THRESHOLD)
        bpy.ops.mesh.face_make_planar()
        bpy.ops.mesh.vert_connect_nonplanar(
            angle_limit=self.NONPLANAR_ANGLE_LIMIT)
        bpy.ops.mesh.vert_connect_concave()

        self._cleanup_textures(context)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=True,
                                       rotation=True,
                                       scale=True)

        return {'FINISHED'}


class OBJECT_OT_SparkOperator_Decimation(bpy.types.Operator,
                                         SparkOperatorsMixin):
    bl_idname = 'object.spark_decimation'
    bl_label = 'Reduce triangles'
    bl_description = 'Reduce triangles'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.modifier_apply(modifier=SPARK_DECIMATE_MODIFIER_NAME)
        context.active_object.sparkar_optimization.InvertedReducePercentage = 0

        return {'FINISHED'}
