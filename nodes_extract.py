# encoding: utf-8
"""Nodes to extract individual items from a dict (``Extract`` category)."""

from inspect import cleandoc as _cleandoc

from comfy_api.latest import io as _io, ui as _ui

from .__meta import (
	category_extract as _category_extract,
	category_extract_adv as _category_extract_adv,
	category_extract_mdl as _category_extract_mdl,
	pack_id_suffix as _pack_id
)
from .__typing import (
	_t, _A, _O, _U,
	_validate_type_factory, _validate_required_dict, _validate_str_key,
	T as _T, DictMap as _DictMap, NoiseProtocol as _NoiseProtocol,
	_ClipVisionModel, _ControlNet, _ModelPatcher, _CFGGuider, _Sampler,
	_CLIP, _VAE, _ImageModelDescriptor
)
from ._io_custom import (
	_BaseNode, _T_BaseNode,
	_DICT_INPUT_REQUIRED, _KEY_CLEANUP_INPUT, _KEY_INPUT_EXTRACT,
	_InputsConverter, _schema_old_node, _attach_execute_method
)
from .docstring_formatter import format_docstring as _format_docstring

# ----------------------------------------------------------

# noinspection PyShadowingBuiltins
def _get_key(dict: _DictMap, key: _A) -> _A:
	try:
		return dict[key]
	except KeyError:
		raise KeyError(f"No such key in Dict: {key!r}")

# ----------------------------------------------------------

def _extracting_node(
	type_name: str,
	value_type: _t.Type[_T],
	value_output_cls: _t.Type[_io.Output],
	suffix: str = '',
	a='a',  # a/an <type> for docstring
	convert_type: bool = False,
	category=_category_extract,
	**output_kwargs
):
	"""Get class decorator building a ``DictExtract*`` node for a specific type."""
	type_name = str(type_name)
	assert issubclass(value_output_cls, _io.Output)
	if not suffix:
		suffix = ''
	if not a:
		a = 'a'

	def class_decorator(cls: _t.Type[_T_BaseNode]):
		docstring = f"Extract {a} {type_name} item from a Dict."
		if not cls.__doc__:
			cls.__doc__ = docstring

		class_name = str(cls.__name__).split('.')[-1]
		tooltip = f"The actual {type_name}-type item extracted from the Dict."
		cls._schema = _io.Schema(
			node_id=f'{class_name}{_pack_id}',
			display_name=f'🗂️Dict → {type_name}{suffix}',
			category=category,
			description=_format_docstring(_cleandoc(cls.__doc__)),
			inputs=[
				_DICT_INPUT_REQUIRED,
				_KEY_INPUT_EXTRACT,
				_KEY_CLEANUP_INPUT,
			],
			outputs=[
				value_output_cls('value', tooltip=tooltip, **output_kwargs),
			],
		)

		_type_convert = value_type if convert_type else _validate_type_factory(type=value_type, type_name=type_name, a=a)

		# noinspection PyShadowingBuiltins
		def execute(
			cls: _t.Type[_T_BaseNode],
			dict: _DictMap, key: str, cleanup_key: bool = True,
		) -> _io.NodeOutput:
			dict = _validate_required_dict(dict)
			key = _validate_str_key(key, strip=cleanup_key)
			value = _get_key(dict, key)
			value = _type_convert(value)
			return _io.NodeOutput(value)

		cls = _attach_execute_method(cls, execute, docstring)

		return cls

	return class_decorator


# ----------------------------------------------------------
# Basic types


# noinspection PyAbstractClass
@_extracting_node(
	'bool', _io.Boolean.Type, _io.Boolean.Output, convert_type=True,
)
class DictExtractBool(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'float', _io.Float.Type, _io.Float.Output, convert_type=True,
)
class DictExtractFloat(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'int', _io.Int.Type, _io.Int.Output, a='an',convert_type=True,
)
class DictExtractInt(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'Cond', list, _io.Conditioning.Output, suffix='🟠',
)
class DictExtractCond(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'Image', _io.Image.Type, _io.Image.Output, a='an', suffix='🔵',
)
class DictExtractImage(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'Latent', _U[_t.Dict, _t.Mapping], _io.Latent.Output, suffix='🟣',
)
class DictExtractLatent(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'Mask', _io.Mask.Type, _io.Mask.Output, suffix='🟢',
)
class DictExtractMask(_BaseNode): pass


# ----------------------------------------------------------
# Advanced types


# noinspection PyAbstractClass
@_extracting_node(
	'Guider', _CFGGuider, _io.Guider.Output,
	category=_category_extract_adv,
)
class DictExtractGuider(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'Noise', _NoiseProtocol, _io.Noise.Output,
	category=_category_extract_adv,
)
class DictExtractNoise(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'Sampler', _Sampler, _io.Sampler.Output,
	category=_category_extract_adv,
)
class DictExtractSampler(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'Sigmas', _io.Sigmas.Type, _io.Sigmas.Output,
	category=_category_extract_adv,
)
class DictExtractSigmas(_BaseNode): pass


# ----------------------------------------------------------
# Model types


# noinspection PyAbstractClass
@_extracting_node(
	'CLIP', _CLIP, _io.Clip.Output, suffix='🟡',
	category=_category_extract_mdl,
)
class DictExtractClip(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'CLIP-vision', _ClipVisionModel, _io.ClipVision.Output, suffix='🔵',
	category=_category_extract_mdl,
)
class DictExtractClipVision(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'ControlNet', _ControlNet, _io.ControlNet.Output, suffix='🟢',
	category=_category_extract_mdl,
)
class DictExtractControlNet(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'GLIGEN', _ModelPatcher, _io.Gligen.Output, suffix='🟤',
	category=_category_extract_mdl,
)
class DictExtractGligen(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'LoRA', _io.LoraModel.Type, _io.LoraModel.Output, suffix='⚪',
	category=_category_extract_mdl,
)
class DictExtractLora(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'Model', _ModelPatcher, _io.Model.Output, suffix='🟣',
	category=_category_extract_mdl,
)
class DictExtractModel(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'Upscale', _ImageModelDescriptor, _io.UpscaleModel.Output, a='an', suffix='🟢',
	category=_category_extract_mdl,
)
class DictExtractUpscale(_BaseNode): pass


# noinspection PyAbstractClass
@_extracting_node(
	'VAE', _VAE, _io.Vae.Output, suffix='🔴',
	category=_category_extract_mdl,
)
class DictExtractVae(_BaseNode): pass


# ==========================================================
# Nodes with custom implementation


class DictExtractAny(_BaseNode):
	"""Extract any-type item from a Dict."""
	_schema = _io.Schema(
		node_id=f'DictExtractAny{_pack_id}',
		display_name='🗂️Dict → ANY◯',
		category=_category_extract,
		description=_format_docstring(_cleandoc(__doc__)),
		inputs=[
			_DICT_INPUT_REQUIRED,
			_KEY_INPUT_EXTRACT,
			_KEY_CLEANUP_INPUT,
		],
		outputs=[
			_io.AnyType.Output(
				'value',
				tooltip="The actual any-type item extracted from the Dict."
			),
		],
		# hidden=[_io.Hidden.unique_id],
	)

	# noinspection PyShadowingBuiltins
	@classmethod
	def execute(cls,
		dict: _DictMap, key: str, cleanup_key: bool = True,
	) -> _io.NodeOutput:
		"""Extract any-type item from a Dict."""
		dict = _validate_required_dict(dict)
		key = _validate_str_key(key, strip=cleanup_key)
		value = _get_key(dict, key)
		# No output-type check
		return _io.NodeOutput(value)


class DictExtractString(_BaseNode):
	"""Extract a string item from a Dict."""
	_schema = _io.Schema(
		node_id=f'DictExtractString{_pack_id}',
		display_name='🗂️Dict → string',
		category=_category_extract,
		description=_format_docstring(_cleandoc(__doc__)),
		inputs=[
			_DICT_INPUT_REQUIRED,
			_io.String.Input(
				'key',
				tooltip=(
					"Key (unique name) of a string to extract from dictionary.\n"
					"If the element with such key isn't a string, it will be turned to one.\n"
					"If no such key exists in the dict, an empty string returned."
				),
			),
			_KEY_CLEANUP_INPUT,
			_io.Boolean.Input(
				'show_status',
				tooltip="Show the extracted string on the node itself?",
				default=False,
				label_on='value',
				label_off='no',
			),
		],
		outputs=[
			_io.String.Output(
				'value',
				tooltip="The actual string item extracted from the Dict."
			)
		],
		# hidden=[_io.Hidden.unique_id],
	)

	@classmethod
	def execute(cls,
		dict: _DictMap, key: str,
		cleanup_key: bool = True, show_status: bool = False,
	) -> _io.NodeOutput:
		"""Extract a string item from a Dict."""
		dict = _validate_required_dict(dict)
		key = _validate_str_key(key, strip=cleanup_key)
		value = _get_key(dict, key)

		if value is None:
			value = ''
		elif not isinstance(value, str):
			value = repr(value)

		return _io.NodeOutput(
			value,
			ui=_ui.PreviewText(value) if show_status else None
		)


# ==========================================================
# Deprecated nodes with old IDs (for backwards compatibility)


class DictExtractStringOld1(_BaseNode):
	# noinspection PyProtectedMember
	_schema = _schema_old_node(
		DictExtractString._schema,
		'StringConstructorDictExtractString',
		inputs_converter=_InputsConverter(
			preserved=('key', 'show_status', 'dict'),
			renames={'key': 'name'},
		),
	)

	@classmethod
	def execute(cls,
		name: str, show_status: bool = False,
		dict: _O[_DictMap] = None
	) -> _io.NodeOutput:
		return DictExtractString.execute(
			dict=dict, key=name, cleanup_key=False, show_status=show_status
		)
