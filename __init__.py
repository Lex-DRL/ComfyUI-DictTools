# encoding: utf-8
"""
"""

from comfy_api.latest import ComfyExtension as _ComfyExtension, io as _io

from .node_dict_from_text import *
from .nodes_add import *

class DictToolsExtension(_ComfyExtension):
	async def get_node_list(self) -> list[type[_io.ComfyNode]]:
		return [
			DictFromText, DictFromTextOld1,
			DictAddAny, DictAddString, DictExtractString,
			DictAddAnyOld1, DictAddStringOld1, DictExtractStringOld1
		]

async def comfy_entrypoint() -> _ComfyExtension:
	return DictToolsExtension()
