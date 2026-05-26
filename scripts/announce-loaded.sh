#!/usr/bin/env bash
# version: 1.0.0
#
# SessionStart hook for the market-research-skills Claude Code plugin (v0.6.0+).
# Emits hookSpecificOutput JSON with additionalContext describing what
# the plugin provides in this session.
#
# Bash 3.2 compatible (runs on macOS stock /bin/bash without `brew install bash`).

set -euo pipefail

INPUT=""
if [[ ! -t 0 ]]; then
  INPUT=$(cat)
fi

SOURCE="startup"
if [[ -n "${INPUT}" ]]; then
  if [[ "${INPUT}" =~ \"source\"[[:space:]]*:[[:space:]]*\"([a-z]+)\" ]]; then
    SOURCE="${BASH_REMATCH[1]}"
  fi
fi

case "${SOURCE}" in
  compact|resume)
    ANNOUNCE="market-research-skills plugin still loaded after ${SOURCE}. Skills available: verifying / topic-brief / analyst-research (3 modes: light / medium / heavy)."
    ;;
  startup|clear|*)
    ANNOUNCE="market-research-skills plugin loaded (v0.6.0).

Three skills available — trigger by typing the skill name or describing the task:

  verifying            Trace any statement back to whitelisted primary sources.
                       Triggers: \"verify X\", \"is this true\", \"find the original source\".

  topic-brief          Generate a thematic observation briefing (HTML, paste-into-WeChat-ready).
                       Triggers: \"topic brief on Y\", \"做一份 XX 观察\", \"/topic-brief\".

  analyst-research     End-to-end research workflow. THREE MODES — picked at trigger time:
                       - light    5-page memo, 0 charts, 60-80 min, single LLM
                       - medium   10-15p analysis, 3-8 charts, half-day budget
                       - heavy    Flagship 15k+ word report, 20-35+ charts, multi-LLM optional
                       Triggers: \"research report\", \"投研报告\", \"深度分析\", \"5-page memo\".

After triggering analyst-research without specifying a mode, the skill will
present the three options and let you pick. If your trigger message contains
explicit hints (page count, time budget, chart count), the skill infers and
asks one-line confirmation.

Battle-tested on the Saudi Vision 2030 economic diversification deep-dive
(heavy mode, 41 figures, 15k+ words). Source + CHANGELOG:
https://github.com/reagan475614947/market-research-skills"
    ;;
esac

# Escape JSON
escape_json() {
  local raw="$1"
  raw="${raw//\\/\\\\}"
  raw="${raw//\"/\\\"}"
  raw="${raw//$'\n'/\\n}"
  printf '%s' "${raw}"
}

ESCAPED=$(escape_json "${ANNOUNCE}")

cat <<JSON
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"${ESCAPED}"}}
JSON

exit 0
