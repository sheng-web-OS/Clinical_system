"""Turn authored TeX delimiters into native, static MathML before Mistune escapes them.

The site is intentionally usable without a remote renderer or JavaScript.
Malformed TeX is a build error instead of silently leaking LaTeX commands.
"""
import html
import re
from latex2mathml.converter import convert


DISPLAY_BRACKETS = re.compile(
    r"(?m)^[ \t]*\\\[[ \t]*\r?\n(?P<tex>[\s\S]*?)\r?\n[ \t]*\\\][ \t]*(?=\r?\n|$)"
)
DISPLAY_DOLLARS = re.compile(
    r"(?m)^[ \t]*\$\$[ \t]*\r?\n(?P<tex>[\s\S]*?)\r?\n[ \t]*\$\$[ \t]*(?=\r?\n|$)"
)
INLINE_PARENS = re.compile(r"(?<!\\)\\\((?P<tex>.+?)\\\)")
FENCED_CODE = re.compile(
    r"(?m)^[ \t]*(?P<fence>\`{3,}|~{3,})[^\n]*\n[\s\S]*?^[ \t]*(?P=fence)[ \t]*(?=\r?\n|$)"
)


def _mathml(latex: str, *, block: bool) -> str:
    try:
        result = convert(latex.strip(), display="block" if block else "inline")
    except Exception as exc:
        raise ValueError("Cannot render TeX expression: " + repr(latex[:140])) from exc
    if "<math " not in result or "</math>" not in result:
        raise ValueError("Math converter did not produce a MathML element")
    # Native MathML remains selectable, scalable, and accessible without network JS.
    if block:
        return '<div class="math-display" role="group" aria-label="數學公式">' + result + "</div>"
    return '<span class="math-inline">' + result + "</span>"


def compile_math(raw: str) -> str:
    """Handle \[...\], $$...$$ and \(...\) while preserving fenced source code.

    Preprocessing must occur BEFORE Markdown parsing: Mistune legitimately turns
    backslash-escaped square brackets into visible brackets, losing TeX delimiters.
    """
    fences: list[str] = []

    def keep_fence(m):
        fences.append(m.group(0))
        return "@@XIAOMA_CODE_FENCE_" + str(len(fences) - 1) + "@@"

    text = FENCED_CODE.sub(keep_fence, raw)
    blocks: list[str] = []

    def block(m):
        blocks.append(_mathml(m.group("tex"), block=True))
        return "\n\n@@XIAOMA_MATH_BLOCK_" + str(len(blocks) - 1) + "@@\n\n"

    text = DISPLAY_BRACKETS.sub(block, text)
    text = DISPLAY_DOLLARS.sub(block, text)
    text = INLINE_PARENS.sub(lambda m: _mathml(m.group("tex"), block=False), text)
    # Restore unmodified fences only after inline conversion.
    for i, chunk in enumerate(fences):
        text = text.replace("@@XIAOMA_CODE_FENCE_" + str(i) + "@@", chunk)
    for i, chunk in enumerate(blocks):
        text = text.replace("@@XIAOMA_MATH_BLOCK_" + str(i) + "@@", chunk)

    # Broken source delimiters should never reappear as unreadable raw commands.
    if re.search(r"(?m)^[ \t]*\\[\[\]][ \t]*$", text):
        raise ValueError("Unmatched display-math delimiter in article")
    return text
