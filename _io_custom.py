# encoding: utf-8
"""
"""

from dataclasses import dataclass as _dataclass, fields as __dataclass_fields

from comfy_api.latest import io as _io

from .__meta import category_old as _category_old
from .__typing import (
	_t, _A, _C, _O, _U, _TypeVar,
	T as _T, T_ComfyNode as _T_ComfyNode
)


_DICT = _io.Custom("DICT")
_DICT_INPUT_OPTIONAL = _DICT.Input(
	'dict',
	optional=True,
	tooltip="An (optional) Dictionary to work with."
)
_DICT_INPUT_REQUIRED = _DICT.Input(
	'dict',
	tooltip="A Dictionary to work with."
)
_DICT_OUTPUT = _DICT.Output(
	'DICT',
	display_name='dict'
)
_KEY_CLEANUP_INPUT = _io.Boolean.Input(
	'cleanup_key', display_name='clean key',
	tooltip=(
		"Automatically remove leading/trailing spaces and extra newlines from the key."
	),
	default=True,
	label_on='strip spaces',
	label_off='no',
)
_KEY_INPUT_ADD = _io.String.Input(
	'key',
	tooltip="Key (name) of the item inserted into the dict.",
)
_KEY_INPUT_EXTRACT = _io.String.Input(
	'key',
	tooltip="Key (name) of the item extracted from the dict.",
)

_T_Input = _t.TypeVar('T_Input', bound=_io.Input)


# ----------------------------------------------------------


@_dataclass
class _InputsConverter:
	"""
	Config-like class used to rebuild schema's inputs for old version of a node.

	- Only the inputs with IDs in ``preserved`` set are kept (or all, if empty).
	- Then, they're optionally renamed according to ``renames`` dict.
	"""
	preserved: _O[_t.Sequence[str]] = None
	renames: _O[_t.Dict[str, str]] = None

	def convert(self, inputs: _t.Sequence[_T_Input]) -> _t.List[_T_Input]:
		preserved = self.preserved
		renames = self.renames
		if not(preserved or renames):
			return list(inputs)

		def _out_item_with_renames(inp: _T_Input) -> _T_Input:
			_id = inp.id
			if _id in renames:
				return _input_override(inp, id=renames[_id])
			return inp

		def _out_item_as_is(inp: _T_Input) -> _T_Input:
			return inp

		out_item = _out_item_with_renames if renames else _out_item_as_is

		if not preserved:
			# We keep all the inputs in the original order:
			return [out_item(x) for x in inputs]

		# Instead, we filter and possibly reorder them:
		orig_inputs_dict = {x.id: x for x in inputs}
		return [out_item(orig_inputs_dict[_id]) for _id in preserved]


# ----------------------------------------------------------


def __dataclass_fields_dict(obj) -> _t.Dict[str, _t.Any]:
	"""Return all the field values from a dataclass - as dict. No deep-copy."""
	field_names = (field.name for field in __dataclass_fields(obj))
	return {
		attr: getattr(obj, attr)
		for attr in field_names
	}


def _dataclass_override(obj: _T, **overrides) -> _T:
	"""Copy a dataclass instance with optional overrides."""
	obj_dict = __dataclass_fields_dict(obj)
	obj_dict.update(overrides)
	obj_type = type(obj)
	return obj_type(**obj_dict)


def _input_override(input_obj: _T_Input, **overrides) -> _T_Input:
	"""Copy an ``io.Input`` instance with optional overrides."""
	new_id = input_obj.id
	if 'id' in overrides:
		new_id = overrides.pop('id')

	input_args = input_obj.as_dict()
	if 'id' in input_args:
		del input_args['id']
	input_args.update(overrides)

	input_type: _t.Type[_T_Input] = type(input_obj)
	return input_type(new_id, **input_args)


def _schema_old_node(
	schema: _io.Schema, node_id: str,
	inputs_converter: _InputsConverter = None,
	**overrides
):
	"""Build a deprecated schema for old node-ID."""
	if inputs_converter is not None:
		inputs: _t.List[_T_Input] = overrides.get('inputs', schema.inputs)
		inputs = inputs_converter.convert(inputs)
		overrides['inputs'] = inputs

	schema_dict = __dataclass_fields_dict(schema)
	if 'node_id' in schema_dict:
		del schema_dict['node_id']
	name_old = schema_dict.pop('display_name')

	schema_dict.update(dict(
		category=_category_old,
		display_name=f"{name_old} [OLD]",
		is_deprecated=True,
		is_dev_only=True,
	))
	schema_dict.update(overrides)
	return _io.Schema(node_id, **schema_dict)


# noinspection PyAbstractClass
class _BaseNode(_io.ComfyNode):
	"""Shared base class for all the nodes in pack.
	Stores schema in internal class attribute.
	"""
	_schema: _io.Schema = None

	@classmethod
	def define_schema(cls) -> _io.Schema:
		return cls._schema


_T_BaseNode = _TypeVar('T_BaseNode', bound=_BaseNode)


def _attach_execute_method(cls: _t.Type[_T_ComfyNode], execute: _C, docstring: str = None) -> _t.Type[_T_ComfyNode]:
	"""Attach a function as ``execute`` method override."""
	if not docstring:
		try:
			docstring = execute.__doc__
		except AttributeError:
			docstring = None
	if not docstring:
		try:
			docstring = cls.execute.__doc__
		except AttributeError:
			docstring = None
	if docstring:
		execute.__doc__ = docstring

	# Mimic the func's metadata to make it look as if it was
	# actually defined as an in-class method:
	execute.__module__ = cls.__module__
	execute.__name__ = 'execute'
	execute.__qualname__ = f"{cls.__qualname__}.execute"

	# Make it a class method (has to be done after this ^)
	# and attach to the class:
	cls.execute = classmethod(execute)

	# Since any decorator works after ABCMeta has done its job,
	# and `execute` might be previously missing (kept as abstract method),
	# we need to manually exclude it:
	if getattr(cls, "__abstractmethods__", None):
		cls.__abstractmethods__ = frozenset(
			name for name in cls.__abstractmethods__
			if name != 'execute'
		)

	return cls
