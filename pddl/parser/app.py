# Parser for Agent Planning Programs, based on pddl
#
# This file is part of app-pddl.
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#

"""Implementation of the PDDL domain parser."""
import sys
from typing import AbstractSet, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from lark import Lark, ParseError, Transformer
from lark.visitors import merge_transformers
from pddl.constants import EITHER
from pddl.core import Action, Domain, Requirements
from pddl.exceptions import PDDLMissingRequirementError, PDDLParsingError
from pddl.helpers.base import assert_, safe_index
from pddl.logic.base import (
    And,
    ExistsCondition,
    FalseFormula,
    ForallCondition,
    Imply,
    Not,
    OneOf,
    Or,
)
from pddl.logic.effects import AndEffect, Forall, When
from pddl.logic.predicates import DerivedPredicate, EqualTo, Predicate
from pddl.logic.terms import Constant, Variable
from pddl.parser import APP_GRAMMAR_FILE, PARSERS_DIRECTORY
from pddl.parser.domain import DomainParser, DomainTransformer
from pddl.parser.problem import ProblemParser, ProblemTransformer
from pddl.parser.symbols import Symbols


class APPTransformer(ProblemTransformer):
    """Agent planning problem Transformer."""

    def __init__(self, *args, **kwargs):
        """Initialize the domain and problem transformers."""
        super().__init__(*args, **kwargs)

        self._problem_transformer = ProblemTransformer()

    def start(self, args):
        return args[0]
    
    def problem(self, args):
        pass

    def transitions(self, args):
        """Process the 'object' rule."""
        pass
    
    def init_app(self, args):
        """Process the 'init' rule."""
        return "init_app", args[2]
    


_app_parser_lark = APP_GRAMMAR_FILE.read_text()


class APPParser:
    """APP PDDL domain parser class."""

    def __init__(self):
        """Initialize."""
        self._transformer = merge_transformers(APPTransformer(), domain=DomainTransformer(), problem=ProblemTransformer())
        self._parser = Lark(
            _app_parser_lark, parser="lalr", import_paths=[PARSERS_DIRECTORY]
        )

    def __call__(self, text):
        """Call."""
        sys.tracebacklimit = 0  # noqa
        tree = self._parser.parse(text)
        sys.tracebacklimit = None  # noqa
        formula = self._transformer.transform(tree)
        return formula


if __name__ == "__main__":
    file = sys.argv[1]
    with open(file, "r") as f:
        ptext = f.read()
    # app = DomainParser()(ptext)
    app = APPParser()(ptext)
    print(app)
    # ProblemParser()(ptext)