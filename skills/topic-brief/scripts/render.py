"""render.py —— CLI 入口

把一个 seed JSON 渲染成 HTML。

用法：
  python3 scripts/render.py <seed.json> [--out <output_dir>] [--open]

例：
  python3 scripts/render.py reference/region_middle_east.example.json --out output --open
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

# 让 lib 包能被导入（无论从哪里调用 render.py）
SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from lib.writer import write_briefing_mock
from lib.renderer import save_briefing
from lib.fix_quotes import fix_file


def main():
    p = argparse.ArgumentParser()
    p.add_argument("seed", help="种子 JSON 路径")
    p.add_argument("--out", default="output", help="输出目录（默认 output/）")
    p.add_argument("--open", action="store_true", help="生成后自动在浏览器打开")
    p.add_argument("--skip-fix-quotes", action="store_true",
                   help="跳过自动修引号步骤")
    args = p.parse_args()

    seed_path = Path(args.seed)
    if not seed_path.exists():
        sys.exit(f"seed not found: {seed_path}")

    # 自动修中文引号配对
    if not args.skip_fix_quotes:
        try:
            fix_file(seed_path)
        except Exception as e:
            print(f"[warn] fix_quotes failed: {e}", file=sys.stderr)

    seed = json.loads(seed_path.read_text(encoding="utf-8"))
    briefing = write_briefing_mock(seed)
    out_path = save_briefing(briefing, args.out)
    print(f"OK: {out_path}")

    if args.open:
        import subprocess
        subprocess.run(["open", str(out_path)])


if __name__ == "__main__":
    main()
