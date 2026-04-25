# encoding: utf-8
"""Code for the ``Dict from Text`` node."""

from inspect import cleandoc as _cleandoc

from frozendict import frozendict as _frozendict

from comfy_api.latest import io as _io, ui as _ui

from .__meta import (
	category as _category,
	pack_id_suffix as _pack_id
)
from .__typing import _A, _U, _O, _t, T as _T, DictMap as _DictMap
from ._dict_funcs import _new_updated_dict
from ._io_custom import (
	_BaseNode,
	_DICT_INPUT_OPTIONAL, _DICT_OUTPUT,
	_InputsConverter, _schema_old_node
)
from .docstring_formatter import format_docstring as _format_docstring

# ----------------------------------------------------------

def __return_line_raw(line_raw: str, line_stripped:str) -> str:
	return line_raw


def __return_line_stripped(line_raw: str, line_stripped:str) -> str:
	return line_stripped


def _parsed_kv_pairs_gen(
	multiline_str: _O[str], pre_strip_lines=True
) -> _t.Generator[_t.Tuple[str, str], _A, None]:
	"""Parse the "dict text" into sequence of key-value pairs:
	Given a multiline string, extract keywords (first non-empty line in each chunk)
	and their substrings (all the following non-empty lines).
	"""
	if not multiline_str:
		return
	multiline_str = str(multiline_str)

	choose_appended_line = __return_line_raw
	if pre_strip_lines:
		multiline_str = multiline_str.strip()
		choose_appended_line = __return_line_stripped

	if not multiline_str:
		return

	cur_chunk: _t.List[str] = list()

	def dump_chunk():
		cur_chunk_iter = iter(cur_chunk)  # It's more backwards-compatible than `a, *b = x`
		chunk_key = next(cur_chunk_iter)  # Might have just whitespaces when no strip
		cur_chunk_lines = list(cur_chunk_iter)
		# If there are no actual lines, join() would return an empty string:
		return chunk_key, '\n'.join(cur_chunk_lines)

	for line in multiline_str.splitlines():
		line_stripped: str = line.strip()
		line = choose_appended_line(line, line_stripped)
		if (
			line_stripped
			# Even if we don't strip,
			# whitespace-only lines are included only for keys:
			or (line and not cur_chunk)
		):
			cur_chunk.append(line)
			continue

		assert not line_stripped
		if cur_chunk:
			yield dump_chunk()
			cur_chunk = list()

		# We simply skip all the empty lines between blocks

	if cur_chunk:
		yield dump_chunk()

# ----------------------------------------------------------

class TextToDict(_BaseNode):
	"""Parse raw text into key-value pairs."""
	_schema = _io.Schema(
		node_id=f'TextToDict{_pack_id}',
		display_name='📃Text → Dict🗂️',
		category=_category,
		description=_format_docstring(_cleandoc(__doc__)),
		inputs=[
			_io.Boolean.Input(
				'pre_cleanup', display_name='cleanup',
				tooltip=(
					"When enabled, each line is individually pre-stripped "
					"of any leading/trailing spaces before parsing the text."
				),
				default=True,
				label_on='strip spaces',
				label_off='no',
			),
			_io.String.Input(
				'dict_text', display_name='dict-items text',
				tooltip=(
					"A wall of key-value pairs:\n"
					"• keys (item names) on their own line,\n"
					"• followed by their text.\n\n"
					"Different items are separated by empty lines."
				),
				placeholder=(
					"Example:\n\n"
					"char1_short\n1boy, blond, short hair\n\n"
					"char1_long\n1boy, smiling, blue eyes, blond, short hair,\nwearing a leather jacket, sitting on a bike"
				),
				multiline=True,
			),
			_io.Boolean.Input(
				'show_status',
				tooltip="Show detected string names on the node itself?",
				default=False,
				label_on='detected keys',
				label_off='no',
			),

			_DICT_INPUT_OPTIONAL,
		],
		outputs=[_DICT_OUTPUT],
		# hidden=[_io.Hidden.unique_id],
		is_output_node=True,  # Just to show the status message even if not connected to anything
	)

	@classmethod
	def execute(cls,
		pre_cleanup: bool, dict_text: _O[str],
		show_status: bool = False,
		dict: _O[_DictMap] = None
	) -> _io.NodeOutput:
		"""Parse raw text into key-value pairs."""
		parsed_items = _parsed_kv_pairs_gen(dict_text, pre_strip_lines=pre_cleanup)
		new_dict = {k: v for k, v in parsed_items}

		if not new_dict:
			# No need to create another dict instance if we add nothing:
			out_dict = _frozendict() if dict is None else dict
			out_ui = _ui.PreviewText('') if show_status else None
			return _io.NodeOutput(out_dict, ui=out_ui)

		out_dict = _new_updated_dict(dict, new_dict)
		# These two ↑↓ must be in this specific order:
		# `_new_updated_dict()` also checks both dicts and might throw an error
		out_ui = None
		if show_status:
			status_text = ','.join(new_dict.keys()) if new_dict else ''
			out_ui = _ui.PreviewText(status_text)

		return _io.NodeOutput(out_dict, ui=out_ui)

# ==========================================================
# Deprecated node with old ID (for backwards compatibility)

class TextToDictOld1(_BaseNode):
	# noinspection PyProtectedMember
	_schema = _schema_old_node(
		TextToDict._schema,
		'StringConstructorDictFromText',
		inputs_converter=_InputsConverter(
			preserved=('pre_cleanup', 'dict_text', 'show_status', 'dict'),
			renames={
				'pre_cleanup': 'cleanup',
				'dict_text': 'strings',
			},
		),
	)

	@classmethod
	def execute(cls,
		cleanup: bool, strings: str, show_status: bool = False,
		dict: _O[_DictMap] = None
	) -> _io.NodeOutput:
		return TextToDict.execute(
			pre_cleanup=cleanup, dict_text=strings, show_status=show_status,
			dict=dict
		)

class TextToDictOld2(TextToDict):
	_schema = _schema_old_node(
		TextToDict._schema,
		f'DictFromText{_pack_id}',
	)
