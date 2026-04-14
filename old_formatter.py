# encoding: utf-8
"""
Code for ``StringConstructorFormatter`` node.
"""

import typing as _t

from inspect import cleandoc as _cleandoc

from frozendict import deepfreeze as _deepfreeze

from comfy.comfy_types.node_typing import IO as _IO

from .__meta import category
from ._dict import _show_text_on_node
from ._formatter_class import Formatter as _Formatter
from .docstring_formatter import format_docstring as _format_docstring
from .enums import DataTypes as _DataTypes

# --------------------------------------

_input_types = _deepfreeze({
	'required': {
		'template': (_IO.STRING, {'multiline': True, 'tooltip': (
			"Type the text template. "
			"To reference named substrings from format-dictionary, use this syntax: {substring_name}. For example:\n\n"
			"score_9, score_8_up, score_7_up, {char1_short}, standing next to {char2_short},\n"
			"{char1_long}\n{char2_long}"
		)}),
		'recursive_format': (_IO.BOOLEAN, {'default': False, 'label_on': '❗ yes', 'label_off': 'no', 'tooltip': (
			"Do recursive format - i.e., allow the chunks from the dictionary to reference other chunks."
		)}),
		'safe_format': (_IO.BOOLEAN, {'default': True, 'label_on': 'yes', 'label_off': 'no', 'tooltip': (
			"If template contains an invalid {text pattern} which can't be formatted - leave it as-is "
			"(instead of throwing an error).\n"
			"Safe mode is recommended for templates with JSON, CSS, or other literal curly brackets."
		)}),
		'show_status': (_IO.BOOLEAN, {'default': True, 'label_on': 'formatted string', 'label_off': 'no', 'tooltip': (
			"Show the final string constructed from the text-template and format-dictionary?"
		)}),
	},
	'optional': {
		'dict': _DataTypes.input_dict(tooltip=(  # It's not actually optional, but is here since there's no dict-widget
			"The dictionary to take named sub-strings from. It could be left unconnected, if the pattern doesn't reference "
			"any sub-strings - then, this node acts exactly the same as a regular string-primitive node."
		)),
	},
	'hidden': {
		'unique_id': 'UNIQUE_ID',  # used for text display at the bottom of the node
	},
})


class StringConstructorFormatter:
	"""
	Construct the formatted string from template and format-dictionary.
	"""
	NODE_NAME = 'StringConstructorFormatter'
	CATEGORY = category
	DESCRIPTION = _format_docstring(_cleandoc(__doc__))

	OUTPUT_NODE = True

	FUNCTION = 'main'
	RETURN_TYPES = (_IO.STRING, )
	RETURN_NAMES = ('string', )
	# OUTPUT_TOOLTIPS = tuple()

	@classmethod
	def INPUT_TYPES(cls):
		return _input_types

	@staticmethod
	def main(
		template: str,
		recursive_format: bool = False,
		safe_format: bool = True,
		show_status: bool = False,
		dict: _t.Dict[str, _t.Any] = None,  #actually, required - but it's here to keep the declared params order
		unique_id: str = None
	) -> _t.Tuple[str]:
		formatter = _Formatter(
			format_dict=dict,
			recursive=recursive_format, safe=safe_format,
		)
		out_text = formatter(template)
		if show_status and unique_id:
			_show_text_on_node(out_text, unique_id)
		return (out_text, )
