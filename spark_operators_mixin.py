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

SPARK_ADDON_TAG = 'spark_blender_addon'


def is_context_valid(context):
    return (len(context.selected_objects) == 1
            and context.active_object is not None
            and context.active_object.type == 'MESH')


class SparkOperatorsMixin(object):
    @classmethod
    def poll(cls, context):
        return is_context_valid(context)

    def tag_from_plugin(self, context):
        context.active_object[SPARK_ADDON_TAG] = 1
