# encoding: utf-8
"""The main module for simple dict nodes."""

from inspect import cleandoc as _cleandoc

from frozendict import frozendict as _frozendict

from comfy_api.latest import io as _io, ui as _ui

from .__meta import (
	category as _category,
	pack_id_suffix as _pack_id
)
from .__typing import _A, _U, _O, _t, T as _T, DictMap as _DictMap
from ._dict_funcs import _new_dict_with_updated_key
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
		category=_category,
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
		name: str, dict: _O[_DictMap] = None, value: _A = None
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
		category=_category,
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
		dict: _O[_DictMap] = None,
	) -> _io.NodeOutput:
		"""Update/append a string to the dict."""
		string = '' if string is None else str(string)
		if cleanup:
			string = '\n'.join(
				x.strip() for x in string.splitlines()
			)
		result= _new_dict_with_updated_key(dict, name, string)
		return _io.NodeOutput(result)

# ----------------------------------------------------------

class DictExtractString(_BaseNode):
	"""Extract a single string from a Format-Dict."""
	_schema = _io.Schema(
		node_id=f'DictExtractString{_pack_id}',
		display_name='Extract String from Dict',
		category=_category,
		description=_format_docstring(_cleandoc(__doc__)),
		inputs=[
			_io.Boolean.Input(
				'cleanup_key', display_name='cleanup',
				tooltip=(
					"Automatically remove leading/trailing spaces and newlines from the key."
				),
				default=True,
				label_on='leading/trailing spaces',
				label_off='no',
			),
			_io.String.Input(
				'key',
				tooltip=(
					"Key (unique name) of a string to extract from dictionary.\n"
					"If the element with such key isn't a string, it will be turned to one.\n"
					"If no such key exists in the dict, an empty string returned."
				),
			),
			_io.Boolean.Input(
				'show_status',
				tooltip="Show the extracted string on the node itself?",
				default=False,
				label_on='value',
				label_off='no',
			),

			_DICT_INPUT_OPTIONAL,
		],
		outputs=[_io.String.Output('string')],
		# hidden=[_io.Hidden.unique_id],
	)

	@classmethod
	def execute(cls,
		cleanup_key: bool, key: str, show_status: bool = False,
		dict: _O[_DictMap] = None
	) -> _io.NodeOutput:
		"""Extract a single string from the Format-Dict."""
		if cleanup_key:
			for line in key.split():
				line = line.strip()  # just in case \r is left
				if line:
					key = line
					break

		# The passed dict might not actually be a dict but ANY mapping,
		# which doesn't have a `get()` method.
		# So direct key access is better:
		string: str = ''
		# noinspection PyBroadException
		try:
			string = dict[key]
		except Exception:
			pass

		if string is None:
			string = ''
		elif not isinstance(string, str):
			string = repr(string)

		return _io.NodeOutput(
			string,
			ui=_ui.PreviewText(string) if show_status else None
		)


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


class DictExtractStringOld1(_BaseNode):
	# noinspection PyProtectedMember
	_schema = _schema_old_name(
		DictExtractString._schema,
		'StringConstructorDictExtractString',
		inputs=[
			_input_override(x, id='name') if x.id == 'key' else x
			for x in DictExtractString._schema.inputs
			if x.id != 'cleanup_key'
		],
	)

	@classmethod
	def execute(cls,
		name: str, show_status: bool = False,
		dict: _O[_DictMap] = None
	) -> _io.NodeOutput:
		return DictExtractString.execute(
			cleanup_key=False, key=name, show_status=show_status, dict=dict
		)
