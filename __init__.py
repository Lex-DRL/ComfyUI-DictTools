# encoding: utf-8
"""
"""

from comfy_api.latest import ComfyExtension as _ComfyExtension, io as _io

from .node_dict_from_text import *
from .nodes_add import *
from .nodes_extract import *

class DictToolsExtension(_ComfyExtension):
	async def get_node_list(self) -> list[type[_io.ComfyNode]]:
		return [
			DictAddAny,
			DictAddBool, DictAddFloat, DictAddInt, DictAddString,
			DictAddCond, DictAddImage, DictAddLatent, DictAddMask,
			DictAddGuider, DictAddNoise, DictAddSampler, DictAddSigmas,
			DictAddClip, DictAddClipVision, DictAddControlNet, DictAddGligen, DictAddLora, DictAddModel, DictAddUpscale, DictAddVae,
			DictAddAnyOld1, DictAddStringOld1,

			DictExtractAny,
			DictExtractBool, DictExtractFloat, DictExtractInt, DictExtractString,
			DictExtractCond, DictExtractImage, DictExtractLatent, DictExtractMask,
			DictExtractGuider, DictExtractNoise, DictExtractSampler, DictExtractSigmas,
			DictExtractClip, DictExtractClipVision, DictExtractControlNet, DictExtractGligen, DictExtractLora, DictExtractModel, DictExtractUpscale, DictExtractVae,
			DictExtractStringOld1,

			TextToDict, TextToDictOld1, TextToDictOld2,
		]

async def comfy_entrypoint() -> _ComfyExtension:
	return DictToolsExtension()
