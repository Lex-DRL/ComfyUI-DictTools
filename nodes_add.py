# encoding: utf-8
"""Nodes to add/update individual items to a dict (``Add`` category)."""

from inspect import cleandoc as _cleandoc

from frozendict import frozendict as _frozendict

from comfy_api.latest import io as _io, ui as _ui

from .__meta import (
	category_add as _category_add,
	category_add_adv as _category_add_adv,
	category_add_mdl as _category_add_mdl,
	pack_id_suffix as _pack_id
)
from .__typing import (
	_t, _A, _O, _U, _validate_type_factory, _validate_str_key,
	T as _T, INT_MAX as _INT_MAX, FLOAT_MAX as _FLOAT_MAX,
	DictMap as _DictMap, NoiseProtocol as _NoiseProtocol,
	_ClipVisionModel, _ControlNet, _ModelPatcher, _CFGGuider, _Sampler,
	_CLIP, _VAE, _ImageModelDescriptor
)
from ._dict_funcs import _new_updated_dict
from ._io_custom import (
	_BaseNode, _T_BaseNode,
	_DICT_INPUT_OPTIONAL, _DICT_OUTPUT, _KEY_CLEANUP_INPUT, _KEY_INPUT_ADD,
	_InputsConverter, _schema_old_node, _attach_execute_method
)
from .docstring_formatter import format_docstring as _format_docstring

# ----------------------------------------------------------

def _adding_node(
	type_name: str,
	value_type: _t.Type[_T],
	value_input_cls: _t.Type[_io.Input],
	prefix: str = '',
	a='a',  # a/an <type> for docstring
	convert_type: bool = False,
	category=_category_add,
	**input_kwargs
):
	"""Get class decorator building a ``DictAdd*`` node for a specific type."""
	type_name = str(type_name)
	assert issubclass(value_input_cls, _io.Input)
	if not prefix:
		prefix = ''
	if not a:
		a = 'a'

	def class_decorator(cls: _t.Type[_T_BaseNode]):
		docstring = f"Add/update {a} {type_name} item to a Dict."
		if not cls.__doc__:
			cls.__doc__ = docstring

		class_name = str(cls.__name__).split('.')[-1]
		tooltip = f"The actual {type_name}-type item to add into the Dict."
		cls._schema = _io.Schema(
			node_id=f'{class_name}{_pack_id}',
			display_name=f'{prefix}{type_name} → Dict🗂️',
			category=category,
			description=_format_docstring(_cleandoc(cls.__doc__)),
			inputs=[
				_KEY_INPUT_ADD,
				_KEY_CLEANUP_INPUT,
				_DICT_INPUT_OPTIONAL,
				value_input_cls('value', tooltip=tooltip, **input_kwargs),
			],
			outputs=[_DICT_OUTPUT],
		)

		_type_convert = value_type if convert_type else _validate_type_factory(type=value_type, type_name=type_name, a=a)

		def execute(
			cls: _t.Type[_T_BaseNode],
			key: str, value: _O[_T] = None, cleanup_key: bool = True,
			dict: _O[_DictMap] = None,
		) -> _io.NodeOutput:
			if value is None and not convert_type:
				return _io.NodeOutput(
					_frozendict() if dict is None else dict
				)
			value = _type_convert(value)
			key = _validate_str_key(key, strip=cleanup_key)
			result = _new_updated_dict(dict, {key: value})
			return _io.NodeOutput(result)

		cls = _attach_execute_method(cls, execute, docstring)

		return cls

	return class_decorator


# ----------------------------------------------------------
# Basic types


# noinspection PyAbstractClass
@_adding_node(
	'bool', _io.Boolean.Type, _io.Boolean.Input, convert_type=True,
	default=False
)
class DictAddBool(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'float', _io.Float.Type, _io.Float.Input, convert_type=True,
	default=0.0, min=-_FLOAT_MAX, max=_FLOAT_MAX, step=0.01,
)
class DictAddFloat(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'int', _io.Int.Type, _io.Int.Input, convert_type=True, a='an',
	default=0, min=-_INT_MAX, max=_INT_MAX, step=1,
	control_after_generate=False,
)
class DictAddInt(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'Cond', list, _io.Conditioning.Input, prefix='🟠',
	optional=True,
)
class DictAddCond(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'Image', _io.Image.Type, _io.Image.Input, a='an', prefix='🔵',
	optional=True,
)
class DictAddImage(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'Latent', _U[_t.Dict, _t.Mapping], _io.Latent.Input, prefix='🟣',
	optional=True,
)
class DictAddLatent(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'Mask', _io.Mask.Type, _io.Mask.Input, prefix='🟢',
	optional=True,
)
class DictAddMask(_BaseNode): pass


# ----------------------------------------------------------
# Advanced types


# noinspection PyAbstractClass
@_adding_node(
	'Guider', _CFGGuider, _io.Guider.Input,
	category=_category_add_adv,
	optional=True,
)
class DictAddGuider(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'Noise', _NoiseProtocol, _io.Noise.Input,
	category=_category_add_adv,
	optional=True,
)
class DictAddNoise(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'Sampler', _Sampler, _io.Sampler.Input,
	category=_category_add_adv,
	optional=True,
)
class DictAddSampler(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'Sigmas', _io.Sigmas.Type, _io.Sigmas.Input,
	category=_category_add_adv,
	optional=True,
)
class DictAddSigmas(_BaseNode): pass


# ----------------------------------------------------------
# Model types


# noinspection PyAbstractClass
@_adding_node(
	'CLIP', _CLIP, _io.Clip.Input, prefix='🟡',
	category=_category_add_mdl,
	optional=True,
)
class DictAddClip(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'CLIP-vision', _ClipVisionModel, _io.ClipVision.Input, prefix='🔵',
	category=_category_add_mdl,
	optional=True,
)
class DictAddClipVision(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'ControlNet', _ControlNet, _io.ControlNet.Input, prefix='🟢',
	category=_category_add_mdl,
	optional=True,
)
class DictAddControlNet(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'GLIGEN', _ModelPatcher, _io.Gligen.Input, prefix='🟤',
	category=_category_add_mdl,
	optional=True,
)
class DictAddGligen(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'LoRA', _io.LoraModel.Type, _io.LoraModel.Input, prefix='⚪',
	category=_category_add_mdl,
	optional=True,
)
class DictAddLora(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'Model', _ModelPatcher, _io.Model.Input, prefix='🟣',
	category=_category_add_mdl,
	optional=True,
)
class DictAddModel(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'Upscale', _ImageModelDescriptor, _io.UpscaleModel.Input, a='an', prefix='🟢',
	category=_category_add_mdl,
	optional=True,
)
class DictAddUpscale(_BaseNode): pass


# noinspection PyAbstractClass
@_adding_node(
	'VAE', _VAE, _io.Vae.Input, prefix='🔴',
	category=_category_add_mdl,
	optional=True,
)
class DictAddVae(_BaseNode): pass


# ==========================================================
# Nodes with custom implementation


class DictAddAny(_BaseNode):
	"""Add/update any-type item to a Dict."""
	_schema = _io.Schema(
		node_id=f'DictAddAny{_pack_id}',
		display_name='◯ANY → Dict🗂️',
		category=_category_add,
		description=_format_docstring(_cleandoc(__doc__)),
		inputs=[
			_KEY_INPUT_ADD,
			_KEY_CLEANUP_INPUT,

			_DICT_INPUT_OPTIONAL,
			_io.AnyType.Input(
				'value',
				optional=True,
				tooltip="The actual any-type item to add into the Dict."
			),
		],
		outputs=[_DICT_OUTPUT],
	)

	# noinspection PyShadowingBuiltins
	@classmethod
	def execute(cls,
		key: str, value: _A = None, cleanup_key: bool = True,
		dict: _O[_DictMap] = None,
	) -> _io.NodeOutput:
		"""Add/update any-type item to a Dict."""
		key = _validate_str_key(key, strip=cleanup_key)
		# No value-type check
		result = _new_updated_dict(dict, {key: value})
		return _io.NodeOutput(result)


# ----------------------------------------------------------


class DictAddString(_BaseNode):
	"""Add/update a string item to a Dict."""
	_schema = _io.Schema(
		node_id=f'DictAddString{_pack_id}',
		display_name='string → Dict🗂️',
		category=_category_add,
		description=_format_docstring(_cleandoc(__doc__)),
		inputs=[
			_KEY_INPUT_ADD,
			_KEY_CLEANUP_INPUT,
			_io.String.Input(
				'value',
				tooltip="The actual string to add into the Dict.",
				multiline=True,
			),
			_io.Boolean.Input(
				'cleanup_value', display_name='clean val',
				tooltip=(
					"When enabled, each line in the value-string is "
					"individually stripped of any leading/trailing spaces."
				),
				default=True,
				label_on='strip spaces',
				label_off='no',
			),

			_DICT_INPUT_OPTIONAL,
		],
		outputs=[_DICT_OUTPUT],
	)

	@classmethod
	def execute(cls,
		key: str, value: str,
		cleanup_key: bool = True, cleanup_value: bool = True,
		dict: _O[_DictMap] = None,
	) -> _io.NodeOutput:
		"""Add/update a string item to a Dict."""
		key = _validate_str_key(key, strip=cleanup_key)

		value = '' if value is None else str(value)
		if cleanup_value:
			value = '\n'.join(
				x.strip() for x in value.splitlines()
			)
		result= _new_updated_dict(dict, {key: value})
		return _io.NodeOutput(result)


# ==========================================================
# Deprecated nodes with old IDs (for backwards compatibility)


class DictAddAnyOld1(_BaseNode):
	# noinspection PyProtectedMember
	_schema = _schema_old_node(
		DictAddAny._schema,
		'StringConstructorDictAddAny',
		inputs_converter=_InputsConverter(
			preserved=('key', 'dict', 'value'),
			renames={'key': 'name'},
		),
	)

	@classmethod
	def execute(cls,
		name: _O[str], dict: _O[_DictMap] = None, value: _A = None
	) -> _io.NodeOutput:
		return DictAddAny.execute(key=name, dict=dict, value=value)


class DictAddStringOld1(_BaseNode):
	# noinspection PyProtectedMember
	_schema = _schema_old_node(
		DictAddString._schema,
		'StringConstructorDictAddString',
		inputs_converter=_InputsConverter(
			preserved=('key', 'cleanup_value', 'value', 'dict'),
			renames={
				'key': 'name',
				'cleanup_value': 'cleanup',
				'value': 'string',
			},
		),
	)

	@classmethod
	def execute(cls,
		name: str, cleanup: bool, string: str,
		dict: _O[_DictMap] = None,
	) -> _io.NodeOutput:
		return DictAddString.execute(
			key=name, value=string,
			cleanup_key=False, cleanup_value=cleanup,
			dict=dict
		)
