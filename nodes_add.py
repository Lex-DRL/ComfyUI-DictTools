# encoding: utf-8
"""Nodes to add/update individual items to a dict (``Add`` category)."""

from inspect import cleandoc as _cleandoc

from frozendict import frozendict as _frozendict

from comfy_api.latest import io as _io, ui as _ui

from .__meta import (
	category_add as _category_add,
	pack_id_suffix as _pack_id
)
from .__typing import _A, _U, _O, _t, T as _T, DictMap as _DictMap
from ._dict_funcs import _new_updated_dict
from ._io_custom import (
	_BaseNode,
	_DICT_INPUT_OPTIONAL, _DICT_OUTPUT, _KEY_INPUT_ADD,
	_InputsConverter, _schema_old_node
)
from .docstring_formatter import format_docstring as _format_docstring

# ----------------------------------------------------------

class DictAddAny(_BaseNode):
	"""Add/update any-type item to a Format-Dict."""
	_schema = _io.Schema(
		node_id=f'DictAddAny{_pack_id}',
		display_name='ANY to Dict',
		category=_category_add,
		description=_format_docstring(_cleandoc(__doc__)),
		inputs=[
			_KEY_INPUT_ADD,

			_io.AnyType.Input(
				'value',
				optional=True,
				tooltip="The actual any-type item to add into the dict."
			),
			_DICT_INPUT_OPTIONAL,
		],
		outputs=[_DICT_OUTPUT],
	)

	@classmethod
	def execute(cls,
		key: _O[str], value: _A = None, dict: _O[_DictMap] = None,
	) -> _io.NodeOutput:
		"""Update/append an item of any type to the dict."""
		if key is None:
			if dict is None:
				dict = _frozendict()
			# No need to create another dict instance if we add nothing:
			result = dict
		else:
			result = _new_updated_dict(dict, {key: value})
		return _io.NodeOutput(result)

# ----------------------------------------------------------

class DictAddString(_BaseNode):
	"""Add/update a string to a Format-Dict."""
	_schema = _io.Schema(
		node_id=f'DictAddString{_pack_id}',
		display_name='STRING to Dict',
		category=_category_add,
		description=_format_docstring(_cleandoc(__doc__)),
		inputs=[
			_KEY_INPUT_ADD,
			_io.Boolean.Input(
				'cleanup_value',
				tooltip=(
					"When enabled, each line in the sub-string is stripped "
					"from any spaces at its start and end."
				),
				default=True,
				label_on='leading/trailing spaces',
				label_off='no',
			),
			_io.String.Input(
				'value',
				tooltip="The actual string to add into the dict.",
				multiline=True,
			),

			_DICT_INPUT_OPTIONAL,
		],
		outputs=[_DICT_OUTPUT],
	)

	@classmethod
	def execute(cls,
		key: str, cleanup_value: bool, value: str = None,
		dict: _O[_DictMap] = None,
	) -> _io.NodeOutput:
		"""Update/append a string to the dict."""
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
			key=name, cleanup_value=cleanup, value=string, dict=dict
		)
