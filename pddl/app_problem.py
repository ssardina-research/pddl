from ctypes import cast
from textwrap import indent
from typing import AbstractSet, Collection, Optional
from pddl.core import Domain, Problem, Requirements
from pddl.custom_types import namelike
from pddl.formatter import _print_objects_constants_with_types, _remove_empty_lines, _sort_and_print_collection
from pddl.helpers.base import ensure, ensure_set
from pddl.logic.base import Formula, TrueFormula
from pddl.logic.terms import Constant
from pddl.custom_types import name as name_type


class APPProblem(Problem):
    def __init__(
        self,
        name: namelike,
        domain: Optional[Domain] = None,
        domain_name: Optional[str] = None,
        requirements: Optional[Collection["Requirements"]] = None,
        objects: Optional[Collection["Constant"]] = None,
        init: Optional[Collection[Formula]] = None,
        init_app: Optional[str] = None,
        transitions: Optional[Collection["Transition"]] = None,
    ):
        """
        Initialize the PDDL problem.

        :param name: the name of the PDDL problem.
        :param domain: the PDDL domain.
        :param domain_name: the domain name. Must match with the domain object.
        :param requirements: the set of PDDL requirements.
        :param objects: the set of objects.
        :param init: the initial condition.
        :param init_app: the start node
        :param transitions: transitions for the agent planning problem
        """
        planning_goal = None
        super().__init__(name, domain, domain_name, requirements, objects, init, planning_goal)
        self._transitions = ensure_set(transitions)
        self._init_app = name_type(init_app)

    @property
    def init_app(self) -> str:
        """Get the initial node."""
        return self._init_app
    
    @property
    def transitions(self) -> AbstractSet["Transition"]:
        """Get the Transitions."""
        return self._transitions
    
    def __str__(self) -> str:
        """String representation for APP problem."""
        result = f"(define (planprog {self.name})"
        body = f"(:domain {self.domain_name})\n"
        indentation = " " * 4
        body += f"(:objects {_print_objects_constants_with_types(self.objects)})\n"
        body += _sort_and_print_collection("(:init ", self.init, ")\n")
        body += f"(:init-app {self.init_app})\n"
        body += f"(:transitions \n" 
        for _t in self._transitions:
            body += f"{indentation}{_t}\n"
        body += ")\n" 
        result = result + "\n" + indent(body, indentation) + "\n)"
        result = _remove_empty_lines(result)
        return result

class Transition:
    def __init__(
        self,
        source: namelike,
        target: namelike,
        goal: Optional[Formula] = None,
    ):
        """
        Initialize the action.

        :param name: the action name.
        :param parameters: the action parameters.
        :param precondition: the action precondition.
        :param effect: the action effect.
        """
        self._source: str = name_type(source)
        self._goal: Formula = ensure(goal, TrueFormula())
        self._target: str = name_type(target)
   
    @property
    def goal(self) -> Formula:
        """Get the goal."""
        return self._goal
    
    @property
    def source(self) -> str:
        """Get the source node."""
        return self._source
    
    @property
    def target(self) -> str:
        """Get the target node."""
        return self._target
    
    def __str__(self) -> str:
        return f"{self.source}--{str(self.goal)}-->{self.target}"