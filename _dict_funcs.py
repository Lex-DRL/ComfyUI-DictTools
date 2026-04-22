# encoding: utf-8
"""
Shared low-level utility functions for dicts.
"""

from frozendict import frozendict as _frozendict

from .__typing import _t, _A, _O, _U, DictMap as _DictMap


def __verify_input_dict_into_new(input_dict: _O[_DictMap], error_if_none=False) -> dict:
	"""
	Verify input dict.
	Always returns a new dict instance (shallow copy if non-empty dict passed).
	"""
	if input_dict is None:
		if error_if_none:
			raise TypeError("No input-dict")
		return dict()

	# In py3.10, frozendict isn't a dict, but is a `typing.Mapping`.
	# So, this many types to check against:
	if not isinstance(input_dict, (dict, _frozendict, _t.Mapping)):
		raise TypeError(f"Input-dict isn't a dict. Got: {input_dict!r}")
	return dict(input_dict)

# ----------------------------------------------------------

def _new_updated_dict(
	input_dict: _O[_DictMap], *updating_dicts: _DictMap,
	sort=True, frozen=True
) -> _U[dict, _frozendict]:
	"""Return a new dict being a union of the input one and the new (updating) ones."""
	out_dict = __verify_input_dict_into_new(input_dict)

	for upd_d in updating_dicts:
		out_dict.update(upd_d)

	if sort:
		out_dict = {k: v for k, v in sorted(out_dict.items())}  # rely on implied ordered dicts in newer py3 versions
	return _frozendict(out_dict) if frozen else out_dict
