# encoding: utf-8
"""
Shared code to deal with dicts.
"""

import typing as _t

import re as _re

from frozendict import deepfreeze as _deepfreeze, frozendict as _frozendict

from .__typing import T as _T, T2 as _T2


_re_valid_key_match = _re.compile("[a-zA-Z_][a-zA-Z_0-9]*$").match
_re_starting_digits_match = _re.compile("[0-9]+").match


def _validate_key(key: str, errors_dict: _t.Dict[_t.Any, str]) -> _t.Union[str, None]:
	"""Verify that the given string can be a key. Otherwise, append a message to `errors_dict`."""
	if not isinstance(key, str):
		errors_dict[key] = f"Not a valid key (string name): {key!r}"
		return None
	key = str(key).strip()
	if not key:
		errors_dict[key] = f"Key (string name) can't be empty. Got: {key!r}"
		return None
	if not _re_valid_key_match(key):
		if _re_starting_digits_match(key):
			errors_dict[key] = f"Key (string name) can't start with a digit. Got: {key!r}"
		else:
			errors_dict[key] = f"Key (string name) must contain only numbers, latin letters and underscores. Got: {key!r}"
		return None
	return key


def _raise_from_errors_dict(
	errors_dict: _t.Dict[_t.Any, str],
	single_error_format: str = '{}',
	multi_errors_format: str = "Invalid keys (string names): {}",
):
	if not errors_dict:
		return

	if len(errors_dict) == 1:
		msg = single_error_format.format(next(iter(errors_dict.values())))
	else:
		msg = multi_errors_format.format(', '.join(repr(x) for x in errors_dict.keys()))
	raise KeyError(msg)


def _verify_input_dict(input_dict: _t.Dict[str, _T] = None, error_if_none=False):
	"""
	Verify input dict to have only valid keys. Raises errors if invalid ones found.
	"""
	if input_dict is None:
		if error_if_none:
			raise TypeError("No input-dict")
		return

	# In py3.10, frozendict isn't a dict, but is a `typing.Mapping`.
	# So, this many types to check against:
	if not isinstance(input_dict, (dict, _frozendict, _t.Mapping)):
		raise TypeError(f"Input-dict isn't a dict. Got: {input_dict!r}")

	errors_dict: _t.Dict[_t.Any, str] = dict()
	for key in input_dict.keys():
		_validate_key(key, errors_dict)

	_raise_from_errors_dict(
		errors_dict,
		"Invalid input-dict: {}", "Invalid keys (string names) in input-dict: {}"
	)


def _verify_input_dict_into_new(input_dict: _t.Dict[str, _T] = None) -> _t.Dict[str, _T]:
	"""
	Verify input dict to have only valid keys. Raises errors if invalid ones found.
	Always returns a new dict instance (shallow copy if non-empty dict passed).
	"""
	if input_dict is None:
		return dict()
	_verify_input_dict(input_dict)
	return dict(input_dict)


def _new_updated_dict(
	input_dict: _t.Union[_t.Dict[str, _T], None], *updating_dicts: _t.Dict[str, _T2],
	sort=True, frozen=True, validate_new_keys=True
) -> _t.Dict[str, _t.Union[_T, _T2]]:
	"""Return a new dict being a union of the input one and the new (updating) ones."""
	out_dict: _t.Dict[str, _t.Union[_T, _T2]] = _verify_input_dict_into_new(input_dict)

	if validate_new_keys:
		errors_dict: _t.Dict[_t.Any, str] = dict()
		for upd_d in updating_dicts:
			upd_d = dict(upd_d)
			for key in list(upd_d.keys()):
				val = upd_d.pop(key)
				key = _validate_key(key, errors_dict)
				upd_d[key] = val
			out_dict.update(upd_d)
		_raise_from_errors_dict(errors_dict)
	else:
		for upd_d in updating_dicts:
			out_dict.update(upd_d)

	if sort:
		out_dict = {k: v for k, v in sorted(out_dict.items())}  # rely on implied ordered dicts in newer py3 versions
	return _deepfreeze(out_dict) if frozen else out_dict


def _new_dict_with_updated_key(
	input_dict: _t.Union[_t.Dict[str, _T], None], key: str, value: _T2, sort=True, frozen=True, validate_key=True
) -> _t.Dict[str, _t.Union[_T, _T2]]:
	"""Return a new dict being a union of the input one and the new (updating) key/value."""
	return _new_updated_dict(
		input_dict, {key: value}, sort=sort, frozen=frozen, validate_new_keys=validate_key
	)
