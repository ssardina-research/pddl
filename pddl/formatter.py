#
# Copyright 2021-2023 WhiteMech
#
# ------------------------------
#
# This file is part of pddl.
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#

"""Formatting utilities for PDDL domains and problems."""
from textwrap import indent
from typing import Callable, Collection, Dict, Optional

from pddl.core import Domain, Problem
from pddl.custom_types import name
from pddl.logic.base import TRUE


def _remove_empty_lines(s: str) -> str:
    """Remove empty lines from string."""
    return "\n".join(filter(str.strip, s.splitlines()))


def _sort_and_print_collection(
    prefix, collection: Collection, postfix, to_string: Callable = str
):
    if len(collection) > 0:
        return prefix + " ".join(sorted(map(to_string, collection))) + postfix
    else:
        return ""


def _print_predicates_with_types(predicates: Collection):
    result = ""
    for p in sorted(predicates):
        if p.arity == 0:
            result += f"({p.name})"
        else:
            result += f"({p.name}"
            for t in p.terms:
                if len(t.type_tags) > 1:
                    result += f" ?{t.name} - (either {' '.join(sorted(t.type_tags))})"
                else:
                    result += (
                        f" ?{t.name} - {sorted(t.type_tags)[0]}"
                        if t.type_tags
                        else f" ?{t.name}"
                    )
            result += ") "
        result += " "
    return result.strip()


def _print_types_with_parents(types: Dict[name, Optional[name]]):
    """
    Print types with parent types..

    :param types: the type definition in dict format.
    :return: the domain types definition in string format.
    """
    result = ""
    for t in sorted(types.keys()):
        result += f"{t} - {types[t]}" if types[t] else f"{t}"
        result += " "
    return result.strip()


def _print_objects_constants_with_types(objects: Collection):
    result = ""

    # types = set.union(*[o.type_tags for o in objects if o.type_tags])
    types_obj = {}
    for o in sorted(objects):
        if o.type_tags:
            for t in o.type_tags:
                    types_obj[t] = types_obj.get(t, []) + [o.name]
        else:
            types_obj["object"] = types_obj.get("object", []) + [o.name]
    for t in sorted(types_obj):
        result += f"\n\t{' '.join(types_obj[t])} - {t}"
        # result += "\n"


    # for o in sorted(objects):
    #     result += f"{o.name} - {' '.join(o.type_tags)}" if o.type_tags else f"{o.name}"
    #     result += " "
    return result.strip()

# def _print_objects_constants_with_types(objs_consts: Collection):
#     result = ""
#     for o in sorted(objs_consts):
#         result += f"{o.name} - {' '.join(o.type_tags)}" if o.type_tags else f"{o.name}"
#         result += " "
#     return result.strip()


def domain_to_string(domain: Domain) -> str:
    """Print a PDDL domain object."""
    result = f"(define (domain {domain.name})"
    body = ""
    indentation = " " * 4
    body += _sort_and_print_collection("(:requirements ", domain.requirements, ")\n")
    body += f"(:types {_print_types_with_parents(domain.types)})\n"
    body += f"(:constants {_print_objects_constants_with_types(domain.constants)})\n"
    body += f"(:predicates {_print_predicates_with_types(domain.predicates)})\n"
    body += _sort_and_print_collection(
        "",
        domain.derived_predicates,
        "",
        to_string=lambda obj: str(obj) + "\n",
    )
    body += _sort_and_print_collection(
        "",
        domain.actions,
        "",
        to_string=lambda obj: str(obj) + "\n",
    )
    result = result + "\n" + indent(body, indentation) + "\n)"
    result = _remove_empty_lines(result)
    return result


def problem_to_string(problem: Problem) -> str:
    """Print a PDDL problem object."""
    result = f"(define (problem {problem.name})"
    body = f"(:domain {problem.domain_name})\n"
    indentation = " " * 4
    body += _sort_and_print_collection("(:requirements ", problem.requirements, ")\n")
    body += f"(:objects {_print_objects_constants_with_types(problem.objects)})\n"
    body += _sort_and_print_collection("(:init ", problem.init, ")\n")
    body += f"{'(:goal ' + str(problem.goal) + ')'}\n" if problem.goal != TRUE else ""
    result = result + "\n" + indent(body, indentation) + "\n)"
    result = _remove_empty_lines(result)
    return result
