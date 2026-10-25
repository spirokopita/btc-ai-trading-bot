#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if ! command -v kotlinc >/dev/null; then
  echo 'Missing Kotlin JVM compiler (kotlinc); install Kotlin or run from Android Studio.' >&2
  exit 2
fi
TMP_JAR="$(mktemp --suffix=.jar)"
trap 'rm -f "$TMP_JAR"' EXIT
kotlinc app/src/main/java/com/btcaud/paper/core/PaperModel.kt core-tests/PaperModelTest.kt -include-runtime -d "$TMP_JAR"
java -jar "$TMP_JAR"
python3 -m unittest discover -s core-tests -p 'test_*.py' -v
