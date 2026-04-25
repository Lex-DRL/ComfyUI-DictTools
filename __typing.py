# encoding: utf-8
"""
"""

import typing as _t
from typing import (
	Any as _A, Callable as _C, Optional as _O, Union as _U,
	TypeVar as _TypeVar
)

from sys import float_info as _float_info

from frozendict import frozendict as _frozendict

from comfy_api.latest import io as _io
# Not used in this module per se, but used for input-type checking:
from comfy.clip_vision import ClipVisionModel as _ClipVisionModel
from comfy.controlnet import ControlNet as _ControlNet
from comfy.model_patcher import ModelPatcher as _ModelPatcher
from comfy.samplers import CFGGuider as _CFGGuider, Sampler as _Sampler
from comfy.sd import CLIP as _CLIP, VAE as _VAE
from spandrel import ImageModelDescriptor as _ImageModelDescriptor

T = _TypeVar('T')
T2 = _TypeVar('T2')
DictMap = _TypeVar('DictMap', bound=_U[_t.Dict, _t.Mapping])
T_ComfyNode = _TypeVar('T_ComfyNode', bound=_io.ComfyNode)

INT_MAX: int = 9223372036854775807
FLOAT_MAX: float = _float_info.max


@_t.runtime_checkable
class NoiseProtocol(_t.Protocol):
	"""The expected type of ``Noise`` input."""
	# Seed should be only an int - but just to be safe:
	seed: _U[int, float, str]

	def generate_noise(self, *args, **kwargs) -> _A: pass


# noinspection PyShadowingBuiltins
def _validate_type_factory(
	type: _t.Type[T], type_name: str = None, what: str = 'Value', a='a'
) -> _C[[_A], T]:
	"""Build a function to type-check an input against a specific type."""
	if not what:
		what = 'Value'
	what = str(what)
	what = what[0].upper() + what[1:]  # Make the first letter uppercase

	if not a:
		a = 'a'
	a = str(a)

	if not type_name:
		type_name = type.__name__
	type_name = str(type_name)

	error_template = f"{what} isn't {a} <{type_name}> instance: {{}}"

	def validate_type(value: _A) -> T:
		"""Type-check an input."""
		if not isinstance(value, type):
			raise TypeError(error_template.format(repr(value)))
		return value

	return validate_type


def _validate_required_dict(dict: _A) -> DictMap:
	if dict is None:
		raise ValueError("No Dict provided.")
	if not isinstance(dict, (_t.Dict, _frozendict, _t.Mapping)):
		raise TypeError(f"Not a Dict: {dict!r}")
	if not dict:
		raise ValueError("Dict is empty.")
	return dict


def _validate_str_key(key: _A, strip: bool = False) -> str:
	if key is None:
		raise ValueError("No key provided.")
	key = str(key)

	if not strip:
		return key

	key_raw = key
	key = ''
	for line in key_raw.split():
		line = line.strip()  # just in case \r is left
		if line:
			key = line
			break
	return key


_validate_str_value = _validate_type_factory(str, type_name='string')
