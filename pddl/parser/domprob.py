# Parser for Agent Planning Programs, based on pddl
#
# This file is part of app-pddl.
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#

"""Implementation of the PDDL domain parser."""
from typing import Any

import sys
import os
from lark import Lark

from pddl.parser.domain import DomainTransformer
from pddl.parser.problem import ProblemTransformer
from pddl.helpers.base import assert_

from lark.visitors import Transformer, merge_transformers

from pddl.parser import DOMPROB_GRAMMAR_FILE, PARSERS_DIRECTORY

# set the folder where the LARK grammar located (the other .lark files are the pddl project)

class DomainProblemTransformer(Transformer):
    """A transformer for domain + problems
    """

    def start(self, children):
        # print(type(children))
        print(children)
        return children

    def domain_start(self, children):
        return children[0]

    def problem_start(self, children):
        return children[0]


_parser_lark = DOMPROB_GRAMMAR_FILE.read_text()

class DomProbParser:
    """Domain and/or problem PDDL domain parser class."""

    def __init__(self):
        """Initialize."""
        self._transformer = merge_transformers(DomainProblemTransformer(), domain=DomainTransformer(), problem=ProblemTransformer())
        # self._transformer = merge_transformers(APPTransformer(), domain=DomainTransformer(), problem=ProblemTransformer())
        # print(PARSERS_DIRECTORY)
        self._parser = Lark(
            _parser_lark, parser="lalr", import_paths=[PARSERS_DIRECTORY]
        )

    def __call__(self, text):
        """Call the object as a function
        Will return the object representing the parsed text/file which is an object 
        of class pddl_parser.app_problem.APPProblem

        The call_parser() function is part of pddl package: will build a Tree from text and then an object pddl_parser.app_problem.APPProblem from the Tree
        """
        # this is OK when pddl.helpers.base provides call_parser API, but that is not in pip package 0.4.0 so we implement directly what is in that function
        # https://github.com/AI-Planning/pddl/blob/4ee8d63034a668072dd0656be1fe59d2f00804f8/pddl/helpers/base.py#L203
        # return call_parser(text, self._parser, self._transformer)

        # this was actually the code in call_parser() function
        sys.tracebacklimit = 0  # noqa
        tree = self._parser.parse(text)
        # print(tree)
        sys.tracebacklimit = None  # noqa
        formula = self._transformer.transform(tree)
        return formula



if __name__ == "__main__":
    file = sys.argv[1]
    with open(file, "r") as f:
        ptext = f.read()
    app = DomProbParser()(ptext)
    print(app)