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
from bpy.app.handlers import persistent

from .spark_operators_export import OBJECT_OT_SparkOperator_ExportForSparkAR
from .spark_operators_optimization import (
    SparkARToolkitOptimizationSettings,
    update_sparkar_optimization_settings,

    OBJECT_OT_SparkOperator_MeshCleanUp,
    OBJECT_OT_SparkOperator_Decimation,
)
from .spark_operators_pivot import (
    OBJECT_OT_SparkOperator_PivotCenter,
    OBJECT_OT_SparkOperator_PivotBottom,
)
from .spark_operators_scale import (
    SparkARToolkitScaleSettings,
    update_sparkar_scale_settings,

    OBJECT_OT_SparkOperator_Resize,
)
from .sparkar_panel import PANEL0_PT_SparkAR_Panel

bl_info = {
    'name': 'Kivicube AR Toolkit',
    'author': 'Facebook, Inc. Translate by Wendell',
    'description': 'Kivicube AR Toolkit',
    'blender': (2, 83, 0),
    'version': (1, 2, 0),
    'location': '模型优化',
    'warning': '',
    'category': 'Import-Export',
    'wiki_url': 'https://sparkar.facebook.com/ar-studio/learn/articles/creating-and-prepping-assets/toolkit-for-blender#installing-Spark-AR-toolkit',
    'tracker_url': 'https://developer.blender.org/maniphest/task/edit/form/2/',
}

classes = (
    SparkARToolkitScaleSettings,
    SparkARToolkitOptimizationSettings,

    OBJECT_OT_SparkOperator_Decimation,
    OBJECT_OT_SparkOperator_MeshCleanUp,
    OBJECT_OT_SparkOperator_Resize,
    OBJECT_OT_SparkOperator_PivotCenter,
    OBJECT_OT_SparkOperator_PivotBottom,
    OBJECT_OT_SparkOperator_ExportForSparkAR,

    PANEL0_PT_SparkAR_Panel,
)


@persistent
def load_handler(scene):
    update_sparkar_optimization_settings(bpy.context)
    update_sparkar_scale_settings(bpy.context)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Screen.sparkar_scale = bpy.props.PointerProperty(
        type=SparkARToolkitScaleSettings)
    bpy.types.Object.sparkar_optimization = bpy.props.PointerProperty(
        type=SparkARToolkitOptimizationSettings)
    bpy.app.handlers.depsgraph_update_post.append(load_handler)
    bpy.app.handlers.load_post.append(load_handler)


def unregister():
    bpy.app.handlers.load_post.remove(load_handler)
    bpy.app.handlers.depsgraph_update_post.remove(load_handler)
    del bpy.types.Object.sparkar_optimization
    del bpy.types.Screen.sparkar_scale
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
