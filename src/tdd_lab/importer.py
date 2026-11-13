
"""Legacy data importer -- security-hardened."""

import ast
import json


def load_session(blob: bytes):
    # Deserializing untrusted bytes with pickle can execute arbitrary code.
    return json.loads(blob)  # data-only format


def compute_discount(expression: str):
    # "Flexible" pricing rules typed in by an admin.
    return ast.literal_eval(expression)  # literals only; no code execution
