# encoding: utf-8
"""
"""

import typing as _t

from ._formatter_class import Formatter
from .old_dict_add_any import StringConstructorDictAddAny
from .old_dict_add_string import StringConstructorDictAddString
from .old_dict_key_extract import StringConstructorDictExtractString
from .old_dict_from_text import StringConstructorDictFromText
from .old_dict_preview import StringConstructorDictPreview
from .old_formatter import StringConstructorFormatter
from .old_validate_keys import StringConstructorValidateKeys

NODE_CLASS_MAPPINGS: _t.Dict[str, type] = {
	'StringConstructorDictAddAny': StringConstructorDictAddAny,
	'StringConstructorDictAddString': StringConstructorDictAddString,
	'StringConstructorDictExtractString': StringConstructorDictExtractString,
	'StringConstructorDictFromText': StringConstructorDictFromText,
	'StringConstructorDictPreview': StringConstructorDictPreview,
	'StringConstructorFormatter': StringConstructorFormatter,
	'StringConstructorValidateKeys': StringConstructorValidateKeys,
}
NODE_DISPLAY_NAME_MAPPINGS: _t.Dict[str, str] = {
	'StringConstructorDictAddAny': "Add ANY to Dict",
	'StringConstructorDictAddString': "Add String to Dict",
	'StringConstructorDictExtractString': "Extract String from Dict",
	'StringConstructorDictFromText': "Dict from Text",
	'StringConstructorDictPreview': "Preview Dict",
	'StringConstructorFormatter': "String Formatter",
	'StringConstructorValidateKeys': "Validate Dict",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
