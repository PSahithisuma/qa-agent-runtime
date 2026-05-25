# src/formatter/error_analyzer.py

from src.fixer.auto_fixer import AutoFixer


def analyze_error(output: str):

    fixer = AutoFixer()

    fixes = fixer.suggest_fix(output)

    return fixes