"""A deliberately bounded public-packet numerical baseline.

This module has no dataset, case-ID, checker, reference, file, subprocess or
network access. It handles explicit exact arithmetic and narrow mean/sum/
difference/ratio claims over supplied CSV. Everything else is unsupported.
Confidence vectors are deterministic one-hot declarations, not calibration.
"""
from __future__ import annotations

import ast
import csv
from fractions import Fraction
import io
import re
from typing import Any

LABELS = ("formally_established", "computationally_established", "empirically_supported",
          "refuted", "insufficient_evidence", "disputed_or_unresolved")
PUBLIC_FIELDS = {"question", "claim", "documents", "methodology", "assumptions"}
DOCUMENT_FIELDS = {"id", "title", "text", "source_id"}
NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?(?:/\d+)?"
OVERREACH = re.compile(
    r"\b(caus(?:e|es|ed|al|ation)|cures?|safe|safety|effective|efficacy|proves?|"
    r"guarantees?|all patients|all proteins|every|universally|mechanism|clinically|"
    r"statistically significant|confidence interval|p-value|binding affinity|predicts?)\b", re.I)


def _unsupported(reason: str) -> dict[str, str]:
    return {"status": "unsupported", "reason": reason}


def _fraction(text: str) -> Fraction:
    if len(text) > 100 or not re.fullmatch(NUMBER, text.strip()):
        raise ValueError("not a bounded exact number")
    exponent = re.search(r"[eE]([+-]?\d+)", text)
    if exponent and (len(exponent[1]) > 5 or abs(int(exponent[1])) > 1000):
        raise ValueError("exponent outside bounded exact calculator")
    result = Fraction(text.strip())
    if result.numerator.bit_length() + result.denominator.bit_length() > 4096:
        raise ValueError("number too large")
    return result


def arithmetic(expression: str) -> Fraction:
    """Interpret only a tiny arithmetic AST; never call eval or execute code."""
    if len(expression) > 200 or not re.fullmatch(r"[0-9eE+*/().\s-]+", expression):
        raise ValueError("not a supported arithmetic expression")
    tree = ast.parse(expression, mode="eval")
    if sum(1 for _ in ast.walk(tree)) > 60:
        raise ValueError("expression too complex")

    def visit(node: ast.AST) -> Fraction:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            # Recover the exact supplied decimal spelling, not a binary float.
            return _fraction(ast.get_source_segment(expression, node) or "")
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = visit(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):
                value = left + right
            elif isinstance(node.op, ast.Sub):
                value = left - right
            elif isinstance(node.op, ast.Mult):
                value = left * right
            else:
                value = left / right
            if value.numerator.bit_length() + value.denominator.bit_length() > 4096:
                raise ValueError("arithmetic result too large")
            return value
        raise ValueError("unsupported arithmetic syntax")

    return visit(tree)


def _normal(name: str) -> str:
    return re.sub(r"[_\s]+", " ", name.strip()).lower()


def _tables(documents: list[dict[str, str]]) -> list[dict[str, Any]]:
    tables = []
    for document in documents:
        text = document["text"]
        blocks = re.findall(r"```(?:csv)?\s*\n(.*?)```", text, flags=re.S | re.I)
        if not blocks:
            lines = text.splitlines()
            # A bare rectangular CSV must stand alone. Prose before/after is
            # accepted only when a CSV fence unambiguously separates the table.
            if lines and ("," in lines[0] or len(lines) > 1 and re.fullmatch(NUMBER, lines[1].strip())):
                blocks = [text]
        for block in blocks:
            try:
                rows = list(csv.reader(io.StringIO(block.strip()), strict=True))
            except csv.Error:
                continue
            if not 2 <= len(rows) <= 1001 or not 1 <= len(rows[0]) <= 32:
                continue
            header = [_normal(x) for x in rows[0]]
            if any(not x for x in header) or len(set(header)) != len(header):
                continue
            if any(len(row) != len(header) for row in rows[1:]):
                continue
            tables.append({"id": document["id"], "header": header, "rows": rows[1:]})
    return tables


def _column(table: dict[str, Any], name: str) -> list[Fraction]:
    name = _normal(name)
    if name not in table["header"]:
        raise ValueError("named column absent")
    index = table["header"].index(name)
    return [_fraction(row[index]) for row in table["rows"]]


def _aggregate(values: list[Fraction], operation: str) -> Fraction:
    total = sum(values, Fraction())
    return total / len(values) if operation == "mean" else total


def _reply(value: Fraction, claimed: Fraction, evidence_ids: list[str]) -> dict[str, Any]:
    label = "computationally_established" if value == claimed else "refuted"
    return {"label": label, "scopes": ["computational"],
            "confidence": {name: float(name == label) for name in LABELS},
            "evidence_ids": evidence_ids,
            "reasoning": f"Exact supplied-data calculation gives {value}; the claim states {claimed}. This verifies only the specified arithmetic, without causal or physical interpretation. One-hot confidence is uncalibrated.",
            "citations": []}


def _fact_reply(valid: bool, evidence_id: str, calculation: str) -> dict[str, Any]:
    label = "computationally_established" if valid else "refuted"
    return {"label": label, "scopes": ["computational"],
            "confidence": {name: float(name == label) for name in LABELS},
            "evidence_ids": [evidence_id], "citations": [],
            "reasoning": calculation + " Only supplied-table arithmetic is checked; no scientific interpretation follows. One-hot confidence is uncalibrated."}


def _table_facts(claim: str, tables: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Generic row counts, distinct keys, and named-record residual arithmetic.

    Public scientific packets often state a concrete table fact rather than the
    narrow mean-of-column grammar. This routine still requires explicit counts
    or an unambiguous named record and never infers empirical adequacy.
    """
    matches = []
    grouped_counts = re.fullmatch(r"The (?:supplied )?table (?:contains|has)\s*(\d+)\s+([A-Za-z_-]+) rows and\s*(\d+)\s+([A-Za-z_-]+) rows", claim, re.I)
    distinct_pairs = re.fullmatch(r"The (?:supplied )?table has\s*(\d+) records,\s*(\d+) distinct (.+?) strings, and\s*(\d+) distinct \((.+?),\s*(.+?)\) pairs", claim, re.I)
    repeated_groups = re.fullmatch(r"The (?:supplied )?table has\s*(\d+) distinct (.+?) identifiers and\s*(\d+) rows, with (\w+) recorded concentrations per (\w+)", claim, re.I)
    for table in tables:
        header, rows = table["header"], table["rows"]
        if grouped_counts:
            n_a, a, n_b, b = grouped_counts.groups()
            columns = []
            for index in range(len(header)):
                values = [_normal(row[index]) for row in rows]
                if _normal(a) in values and _normal(b) in values:
                    columns.append(values)
            if len(columns) == 1:
                a_count, b_count = columns[0].count(_normal(a)), columns[0].count(_normal(b))
                matches.append(_fact_reply(a_count == int(n_a) and b_count == int(n_b), table["id"], f"Direct row counts are {a_count} and {b_count}."))
        if distinct_pairs:
            n, distinct, key, pairs, first, second = distinct_pairs.groups()
            names = [_normal(x) for x in (key, first, second)]
            if all(x in header for x in names):
                i, j, k = [header.index(x) for x in names]
                observed = len(rows), len({row[i] for row in rows}), len({(row[j], row[k]) for row in rows})
                matches.append(_fact_reply(observed == (int(n), int(distinct), int(pairs)), table["id"], f"Calculated row/distinct-key/distinct-pair counts are {observed}."))
        if repeated_groups:
            distinct, group, n, repetitions, repeated_name = repeated_groups.groups()
            words = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10}
            k = words.get(repetitions.lower(), int(repetitions) if repetitions.isdigit() else -1)
            group = _normal(group)
            concs = [i for i, name in enumerate(header) if name in ("concentration", "conc", "concentration code")]
            if group in header and _normal(repeated_name) == group and len(concs) == 1 and k > 0:
                i, j = header.index(group), concs[0]
                groups = {row[i] for row in rows}
                correct = len(groups) == int(distinct) and len(rows) == int(n) and all(len({row[j] for row in rows if row[i] == g}) == k for g in groups)
                matches.append(_fact_reply(correct, table["id"], f"Counted {len(groups)} distinct groups and {len(rows)} rows, checking per-group concentration counts."))
        residual = re.search(r"\bresidual is\s*(" + NUMBER + r")\s*([A-Za-z/]+)\s*\(calculated minus experimental\)$", claim, re.I)
        both = re.search(r"\bexperimental and calculated\b.*\bboth equal\s*(" + NUMBER + r")\s*([A-Za-z/]+)$", claim, re.I)
        target = residual or both
        if target:
            calculated = [i for i, name in enumerate(header) if name.startswith("calculated ") and "uncertainty" not in name and "reference" not in name]
            experimental = [i for i, name in enumerate(header) if name.startswith("experimental ") and "uncertainty" not in name and "reference" not in name]
            if len(calculated) != 1 or len(experimental) != 1:
                continue
            ci, ei = calculated[0], experimental[0]
            unit_a, unit_b = header[ci].removeprefix("calculated "), header[ei].removeprefix("experimental ")
            if unit_a != unit_b or unit_a.replace(" ", "/") != target[2].lower():
                continue
            # Locate a record by an explicit exact categorical cell occurring as
            # a whole token in the claim, never by a source/case identifier.
            name_columns = [i for i, name in enumerate(header) if name in ("name", "compound", "compound name", "substance")]
            selected = [row for row in rows if any(len(row[i]) >= 3 and re.search(r"(?<!\w)" + re.escape(row[i]) + r"(?!\w)", claim, re.I) for i in name_columns)]
            if len(selected) == 1:
                a, b = _fraction(selected[0][ci]), _fraction(selected[0][ei])
                stated = _fraction(target[1])
                if residual:
                    matches.append(_reply(a-b, stated, [table["id"]]))
                else:
                    matches.append(_fact_reply(a == b == stated, table["id"], f"The named record displays calculated={a} and experimental={b}."))
    return matches[0] if len(matches) == 1 else None


def respond(packet: dict[str, Any]) -> dict[str, Any]:
    """Return a six-key decision or explicit unsupported, using only the packet."""
    if not isinstance(packet, dict) or set(packet) != PUBLIC_FIELDS:
        return _unsupported("Only the five public packet fields are admitted.")
    if not all(isinstance(packet[k], str) and len(packet[k]) <= 20000 for k in ("question", "claim", "methodology")):
        return _unsupported("Invalid or oversized public text.")
    if not isinstance(packet["assumptions"], list) or not all(isinstance(x, str) for x in packet["assumptions"]):
        return _unsupported("Assumptions must be disclosed text.")
    documents = packet["documents"]
    if not isinstance(documents, list) or len(documents) > 20:
        return _unsupported("Invalid document collection.")
    if any(not isinstance(d, dict) or set(d) != DOCUMENT_FIELDS or not all(isinstance(v, str) and len(v) <= 20000 for v in d.values()) for d in documents):
        return _unsupported("Document allowlist violation.")
    claim = packet["claim"].strip().removesuffix(".").strip()
    if OVERREACH.search(claim):
        return _unsupported("The target includes interpretation outside this numerical calculator's scope.")
    if any(re.search(r"\b(approximately|about|rounded|within|uncertainty|standard error)\b", x, re.I) for x in (claim, packet["methodology"])):
        return _unsupported("Rounding, tolerance or uncertainty semantics require a separate declared procedure.")
    try:
        # Explicit arithmetic claims can be checked without documents. Exact
        # equality syntax is narrow, preventing calculation -> overclaim drift.
        equality = re.fullmatch(r"(?:The (?:exact )?(?:calculation|expression) )?([0-9eE+*/().\s-]+)\s*(?:=|equals|is)\s*(" + NUMBER + r")", claim, re.I)
        if equality:
            return _reply(arithmetic(equality[1].strip()), _fraction(equality[2]), [])
        tables = _tables(documents)
        fact = _table_facts(claim, tables)
        if fact:
            return fact
        target = re.fullmatch(r"(?:The )?(mean|sum) of ([A-Za-z][A-Za-z0-9 _-]{0,80}?) (?:is|equals|=) (" + NUMBER + r")", claim, re.I)
        contrast = re.fullmatch(r"(?:The )?(difference|ratio) (?:between|of) (?:the )?mean of ([A-Za-z][A-Za-z0-9 _-]{0,60}?) (?:and|to) (?:the )?mean of ([A-Za-z][A-Za-z0-9 _-]{0,60}?) (?:is|equals|=) (" + NUMBER + r")", claim, re.I)
        paired = re.fullmatch(r"(?:The )?mean change \(([A-Za-z][A-Za-z0-9 _-]{0,40}?) minus ([A-Za-z][A-Za-z0-9 _-]{0,40}?)\) (?:is|equals|=) (" + NUMBER + r")", claim, re.I)
        if not any((target, contrast, paired)):
            return _unsupported("No unambiguous supported arithmetic or named-column aggregate target was identified.")
        matches = []
        for table in tables:
            try:
                if target:
                    value = _aggregate(_column(table, target[2]), target[1].lower())
                    stated = _fraction(target[3])
                elif contrast:
                    a = _aggregate(_column(table, contrast[2]), "mean")
                    b = _aggregate(_column(table, contrast[3]), "mean")
                    value = a - b if contrast[1].lower() == "difference" else a / b
                    stated = _fraction(contrast[4])
                else:
                    assert paired is not None
                    a, b = _column(table, paired[1]), _column(table, paired[2])
                    value = _aggregate([x - y for x, y in zip(a, b)], "mean")
                    stated = _fraction(paired[3])
                matches.append((value, stated, table["id"]))
            except (ValueError, ZeroDivisionError):
                continue
        if len(matches) != 1:
            return _unsupported("Exactly one complete numeric CSV table must identify the claimed quantity; ambiguous or missing evidence is unsupported.")
        value, stated, evidence_id = matches[0]
        return _reply(value, stated, [evidence_id])
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError, RecursionError):
        return _unsupported("The supplied arithmetic is undefined or outside the bounded exact calculator.")
