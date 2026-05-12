#!/usr/bin/env bash
# Package a skill as a portable .zip — works on any LLM terminal.
# Usage: ./scripts/pack.sh <skill-name>
#        ./scripts/pack.sh --all
# Output: releases/<skill-name>.zip
#
# 把指定 skill 打包为 .zip 文件，适配任意 LLM 终端。
# 用法: ./scripts/pack.sh <skill-name>
#       ./scripts/pack.sh --all
# 产物: releases/<skill-name>.zip

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
RELEASES_DIR="$REPO_ROOT/releases"

usage() {
  echo "Usage / 用法: $0 <skill-name> | --all"
  echo "Example / 示例: $0 verifying"
  exit 1
}

pack_one() {
  local name="$1"
  local src="$SKILLS_DIR/$name"

  if [[ ! -d "$src" ]]; then
    echo "Error / 错误: skills/$name does not exist / 不存在" >&2
    exit 1
  fi
  if [[ ! -f "$src/SKILL.md" ]]; then
    echo "Error / 错误: skills/$name/SKILL.md does not exist / 不存在" >&2
    exit 1
  fi

  mkdir -p "$RELEASES_DIR"
  local out="$RELEASES_DIR/$name.zip"
  rm -f "$out"

  # Pack from the skills/ directory so the zip's internal path starts at <skill-name>/.
  # Exclude SKILL.zh.md (Chinese reference only) — only ship the canonical English SKILL.md.
  # 从 skills/ 目录打包，让 zip 内层级从 <skill-name>/ 开始；
  # 排除 SKILL.zh.md（仅中文参考版），只发布权威的英文 SKILL.md。
  (cd "$SKILLS_DIR" && zip -rq "$out" "$name" \
    -x "*.DS_Store" \
    -x "$name/downloads/*" \
    -x "$name/SKILL.zh.md")

  echo "Generated / 已生成: ${out#$REPO_ROOT/}"
}

main() {
  [[ $# -lt 1 ]] && usage

  if [[ "$1" == "--all" ]]; then
    for d in "$SKILLS_DIR"/*/; do
      pack_one "$(basename "$d")"
    done
  else
    pack_one "$1"
  fi
}

main "$@"
