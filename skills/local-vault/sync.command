#!/bin/bash
# 双击入口：跑 local-vault 的转换管线。
# 先在 scripts/.env 里配好 KB_SOURCE_DIR / KB_TARGET_DIR（见 scripts/.env.example）。

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python3 "$DIR/scripts/sync.py"
EXIT_CODE=$?

echo ""
echo "─────── 同步结束（退出码 $EXIT_CODE），按回车关闭窗口 ───────"
read -r
exit $EXIT_CODE
