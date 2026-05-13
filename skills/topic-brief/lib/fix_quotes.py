"""修复 seed JSON 里中文双引号未配对的问题。

常见症状：手写 JSON 时把 "X" 错写成 "X"（都是左引号），导致 JSON 解析失败
或视觉异常。本脚本：
  1. 把字符串值里嵌入的英文直引号 " 转为 " （配对的 " "）
  2. 把已存在的非配对 " 与下一个 " 配对，第 2 个换成 "

用法：
  python3 -m lib.fix_quotes <seed.json>
"""
from __future__ import annotations
import sys, json, re
from pathlib import Path


def fix_inline_straight_quotes(content: str) -> str:
    """状态机扫描：把 JSON 字符串内部的 \" 替换为中文左引号 "（后面再做配对）。"""
    out = []
    i, n = 0, len(content)
    in_str = False
    while i < n:
        c = content[i]
        if c == "\\" and in_str and i + 1 < n:
            out.append(c); out.append(content[i + 1]); i += 2; continue
        if c == '"':
            if not in_str:
                in_str = True
                out.append(c); i += 1; continue
            else:
                j = i + 1
                while j < n and content[j] in " \t":
                    j += 1
                nxt = content[j] if j < n else ""
                if nxt in (":", ",", "}", "]", "\n", "\r", ""):
                    in_str = False
                    out.append(c); i += 1; continue
                else:
                    out.append("“"); i += 1; continue
        out.append(c); i += 1
    return "".join(out)


def pair_chinese_quotes(s: str) -> str:
    """把 "X" 形式中第 2 个 " 换成 " （成对）。"""
    if not isinstance(s, str) or "“" not in s:
        return s
    return re.sub(r"“([^“”]*?)“", r"“\1”", s)


def walk(obj):
    if isinstance(obj, dict):
        return {k: walk(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk(x) for x in obj]
    if isinstance(obj, str):
        return pair_chinese_quotes(obj)
    return obj


def fix_file(path: Path) -> None:
    """读 JSON、修引号、写回。"""
    raw = path.read_text(encoding="utf-8")
    try:
        json.loads(raw)
    except json.JSONDecodeError:
        raw = fix_inline_straight_quotes(raw)
    data = json.loads(raw)
    fixed = walk(data)
    path.write_text(json.dumps(fixed, ensure_ascii=False, indent=2), encoding="utf-8")
    json.load(open(path, encoding="utf-8"))  # 自检


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python3 fix_quotes.py <seed.json>")
    fix_file(Path(sys.argv[1]))
    print(f"OK: {sys.argv[1]}")


if __name__ == "__main__":
    main()
