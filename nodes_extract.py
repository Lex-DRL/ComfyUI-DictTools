# encoding: utf-8
"""Nodes to extract individual items from a dict (``Extract`` category)."""

from inspect import cleandoc as _cleandoc

from comfy_api.latest import io as _io, ui as _ui

from .__meta import (
	category_extract as _category_extract,
	pack_id_suffix as _pack_id
)
from .__typing import _A, _U, _O, _t, T as _T, DictMap as _DictMap
from ._io_custom import (
	_BaseNode,
	_DICT_INPUT_OPTIONAL,
	_InputsConverter, _schema_old_node
)
from .docstring_formatter import format_docstring as _format_docstring

# ----------------------------------------------------------

class DictExtractString(_BaseNode):
	"""Extract a single string from a Format-Dict."""
	_schema = _io.Schema(
		node_id=f'DictExtractString{_pack_id}',
		display_name='STRING from Dict',
		category=_category_extract,
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
			cleanup_key=False, key=name, show_status=show_status, dict=dict
		)
