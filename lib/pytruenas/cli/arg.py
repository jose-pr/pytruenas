import argparse as _argparse
import types as _types
import typing as _ty

from ..utils import ast as _astutils

NOT_DEFINED = _astutils.NOT_DEFINED


_type = type

_T = _ty.TypeVar("_T")

Factory = _ty.Callable[[str], _T]

NS = _argparse.Namespace
Arg = _ty.Annotated


class ArgumentMeta(_ty._ProtocolMeta):

    def __instancecheck__(self, instance) -> bool:
        builder_factory = getattr(instance, "_argbuilder_", None)
        return callable(builder_factory)


@_ty.runtime_checkable
class Argument(_ty.Protocol, metaclass=ArgumentMeta):

    @classmethod
    def _argbuilder_(
        cls,
        name: str,
        decl: _astutils.ArgDeclaration,
        factory: Factory | None = None,
    ):
        help = decl.docstring or ""
        flags = next(
            filter(lambda x: isinstance(x, (list, tuple, set)), decl.exprs),
            ("--" + name.replace("_", "-"),),
        )
        required = None
        ty = decl.type
        if ty is _astutils.NOT_DEFINED:
            ty = factory if isinstance(factory, type) else cls

        if factory is None:
            _factory = decl.type if decl.type is not _astutils.NOT_DEFINED else cls
        else:
            _factory = _ty.cast(Factory, factory)

        cls = ty
        if cls is not None and cls is not Argument:
            origin = _ty.get_origin(cls)
            args = _ty.get_args(cls)
            if origin:
                if origin is _ty.Union and _types.NoneType in args:
                    args = [a for a in args if a is not _types.NoneType]
                    required = False
                    if len(args) == 1:
                        _factory = args[0]

                if origin is _ty.Union or origin is _types.UnionType and len(args) > 1:

                    def _factory(text: str, /):
                        for ty in args:
                            try:
                                return ty(text)
                            except:
                                pass
                        raise ValueError(text, args)

        return ArgumentBuilder(
            name=name,
            flags=flags,
            type=_factory,
            default=decl.default,
            help=help,
            required=required,
        )

    @classmethod
    def from_type(cls, factory: _ty.Callable[[str], _T], **kwargs):
        _factory = factory

        class Arg(cls):

            @classmethod
            def _argbuilder_(
                cls,
                name: str,
                decl: _astutils.ArgDeclaration,
                factory: Factory | None = _factory,
            ):
                builder = super()._argbuilder_(name, decl, factory or _factory)
                for k, v in kwargs.items():
                    setattr(builder, k, v)
                return builder

        return Arg


class ArgumentBuilder(_argparse.Namespace):
    name: str
    flags: list[str]
    type: Factory
    default: None | object | _astutils.NotDefined
    help: str
    required: bool | None = None
    action: str | _type[_argparse.Action] | None = None

    def _kwargs(self):
        kwargs = getattr(self, "kwargs", None) or {}
        if self.required is not None:
            kwargs["required"] = self.required

        if self.default is not _astutils.NOT_DEFINED:
            kwargs["default"] = self.default

        if self.type is bool and not self.action:
            kwargs["action"] = "store_true"
        if self.action:
            kwargs["action"] = self.action

        if kwargs.get("action") not in ["count", "store_true"]:
            kwargs["type"] = self.type

        if kwargs.get("action") == "store_true" and "default" not in kwargs:
            kwargs["default"] = False

        flags = self.flags
        dest = self.name
        if len(flags) == 1 and not flags[0].startswith("-"):
            dest = None

        if dest:
            kwargs["dest"] = dest

        return kwargs

    def add_to_parser(self, parser: _argparse.ArgumentParser):
        help = self.help
        if callable(help):  # type:ignore
            help = help()
        return parser.add_argument(
            *self.flags,
            help=help,
            **self._kwargs(),
        )


class _Parser(_argparse.ArgumentParser, _ty.Generic[_T]):
    def parse_args(self, args=None, namespace: _T | None = None) -> _T:  # type:ignore
        raise NotImplementedError()

    def parse_known_args(  # type:ignore
        self, args=None, namespace: _T | None = None
    ) -> tuple[_T, list[str]]:
        raise NotImplementedError()


class Args(_argparse.Namespace):
    @classmethod
    def _getargs_(cls):
        clsargs = _astutils.get_clsargs(cls)
        args: list[ArgumentBuilder] = []
        for name, decl in clsargs.items():
            if decl.annotations:
                if decl.annotations[0] is _argparse.SUPPRESS:
                    continue
                options = {}
                for opts in decl.annotations:
                    options.update(
                        opts if isinstance(opts, _ty.Mapping) else opts.__dict__
                    )
                builder = Argument.from_type(decl.type, **options)._argbuilder_
            elif isinstance(decl.type, Argument):
                builder = decl.type._argbuilder_
            else:
                builder = Argument.from_type(decl.type)._argbuilder_
            args.append(builder(name, decl))
        return args

    @classmethod
    def build_parser(
        cls,
        subparser: _argparse._SubParsersAction | None = None,
        name: str | None = None,  # type:ignore
        parents: _ty.Sequence[_argparse.ArgumentParser] = [],
        **kwargs,
    ):
        if subparser:
            method = subparser.add_parser
        else:
            method = _argparse.ArgumentParser

        name: str = name or getattr(cls, "_parsername_", None) or cls.__name__
        kwargs.setdefault("description", cls.__doc__ or "")
        parser = _ty.cast(
            _Parser[_ty.Self],
            method(name, parents=parents, **kwargs),
        )

        cls.initparser(parser)

        return parser

    @classmethod
    def initparser(cls, parser: _argparse.ArgumentParser):

        def parse_known_args(
            args: _ty.Sequence[str] | None = None, namespace: NS | None = None
        ):
            if namespace is None:
                namespace = _argparse.Namespace()

            setattr(namespace, "#cls", cls)

            parsed, unk = _argparse.ArgumentParser.parse_known_args(
                parser, args, namespace
            )
            _cls: "type[_ty.Self]" = getattr(parsed, "#cls")
            return _cls(**parsed.__dict__), unk

        parser.parse_known_args = parse_known_args  # type:ignore

        for arg in cls._getargs_():
            _action = None
            for action in parser._actions:
                if action.dest == arg.name:
                    _action = action
            if not _action:
                _action = arg.add_to_parser(parser)
            setattr(cls, f"_action_{_action.dest}", _action)

        return parser
