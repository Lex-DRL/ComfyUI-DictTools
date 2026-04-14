# encoding: utf-8
"""Service nodes for dict preparation."""

from inspect import cleandoc as _cleandoc

from frozendict import frozendict as _frozendict

from comfy_api.latest import io as _io, ui as _ui

from .__meta import (
	category_dict as _category_dict,
	pack_id_suffix as _pack_id
)
from .__typing import _A, _U, _O, _t, T as _T, FormatDict as _FormatDict
from ._dict import _new_dict_with_updated_key
from ._io_custom import (
	_BaseNode,
	_DICT_INPUT_OPTIONAL, _DICT_OUTPUT,
	_input_override, _schema_old_name
)
from .docstring_formatter import format_docstring as _format_docstring

_dict = dict

# ----------------------------------------------------------

class DictAddAny(_BaseNode):
	"""Add/update any-type item to a Format-Dict."""
	_schema = _io.Schema(
		node_id=f'DictAddAny{_pack_id}',
		display_name='Add ANY to Dict',
		category=_category_dict,
		description=_format_docstring(_cleandoc(__doc__)),
		inputs=[
			_io.String.Input(
				'name',
				tooltip=(
					"Name (key) of the item inserted into the dict. "
					"It must comprise only of latin letters, digits and underscores + it can't start with a digit."
				),
			),

			_DICT_INPUT_OPTIONAL,
			_io.AnyType.Input(
				'value',
				optional=True,
				tooltip="The actual any-type item to add into the dict."
			),
		],
		outputs=[_DICT_OUTPUT],
	)

	@classmethod
	def execute(cls,
		name: str, dict: _O[_FormatDict] = None, value: _A = None
	) -> _io.NodeOutput:
		"""Update/append an item of any type to the dict."""
		if value is None:
			if dict is None:
				dict = _frozendict()
			# No need to create another dict instance if we add nothing:
			result = dict
		else:
			result = _new_dict_with_updated_key(dict, name, value)
		return _io.NodeOutput(result)

# ----------------------------------------------------------

class DictAddString(_BaseNode):
	"""Add/update a string to a Format-Dict."""
	_schema = _io.Schema(
		node_id=f'DictAddString{_pack_id}',
		display_name='Add String to Dict',
		category=_category_dict,
		description=_format_docstring(_cleandoc(__doc__)),
		inputs=[
			_io.String.Input(
				'name',
				tooltip=(
					"Name (key) of the string inserted into the dict. "
					"It must comprise only of latin letters, digits and underscores + it can't start with a digit."
				),
			),
			_io.Boolean.Input(
				'cleanup',
				tooltip=(
					"When enabled, each line in the sub-string is stripped "
					"from any spaces at its start and end."
				),
				default=True,
				label_on='leading/trailing spaces',
				label_off='no',
			),
			_io.String.Input(
				'string',
				tooltip="The actual string to add into the dict.",
				multiline=True,
			),

			_DICT_INPUT_OPTIONAL,
		],
		outputs=[_DICT_OUTPUT],
	)

	@classmethod
	def execute(cls,
		name: str, cleanup: bool, string: str,
		dict: _O[_FormatDict] = None,
	) -> _io.NodeOutput:
		"""Update/append a string to the dict."""
		string = '' if string is None else str(string)
		if cleanup:
			string = '\n'.join(
				x.strip() for x in string.splitlines()
			)
		result= _new_dict_with_updated_key(dict, name, string)
		return _io.NodeOutput(result)


# ==========================================================
# Deprecated nodes with old IDs (for backwards compatibility)


class DictAddAnyOld1(DictAddAny):
	_schema = _schema_old_name(
		DictAddAny._schema,
		'StringConstructorDictAddAny'
	)


class DictAddStringOld1(DictAddString):
	_schema = _schema_old_name(
		DictAddString._schema,
		'StringConstructorDictAddString'
	)
