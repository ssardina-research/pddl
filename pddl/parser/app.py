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
from lark import Lark
from pddl.app_problem import APPProblem, Transition
from pddl.parser import APP_GRAMMAR_FILE, PARSERS_DIRECTORY
from pddl.parser.problem import ProblemTransformer


class APPTransformer(ProblemTransformer):
    """Agent planning problem Transformer."""

    def __init__(self, *args, **kwargs):
        """Initialize the domain and problem transformers."""
        super().__init__(*args, **kwargs)

        self._problem_transformer = ProblemTransformer()

    def start(self, args):
        return args[0]
    
    def problem(self, args):
        return APPProblem(**dict(args[2:-1]))

    def source(self, args):
        """ Process transition source rule """
        return "source", args[0]

    def target(self, args):
        """ Process transition target rule """
        return "target", args[0]

    def transitions(self, args):
        """Process the 'transitions' rule."""
        return "transitions", args[2:-1]

    def transition(self, args):
        source = args[1][1]
        target = args[2][1]
        goal = args[3][1]
        return Transition(source=source, target=target, goal=goal)
    
    def init_app(self, args):
        """Process the 'init-app' rule."""
        return "init_app", args[2]
    
    def app_problem_def(self, args):
        """Process the 'app_problem_def' rule."""
        return "name", args[2]
    

_app_parser_lark = APP_GRAMMAR_FILE.read_text()


class APPParser:
    """APP PDDL domain parser class."""

    def __init__(self):
        """Initialize."""
        self._transformer = APPTransformer()
        # self._transformer = merge_transformers(APPTransformer(), domain=DomainTransformer(), problem=ProblemTransformer())
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
    app = APPParser()(ptext)
    print(app)