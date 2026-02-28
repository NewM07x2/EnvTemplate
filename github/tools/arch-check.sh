#!/bin/bash

# =================================================================
# Project Architecture & Governance Checker
# -----------------------------------------------------------------
# このスクリプトは structure.md および paths.md に定義された
# 物理的・論理的な制約を自動チェックします。
# =================================================================

EXIT_CODE=0

# 色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "--- Architecture Audit Starting ---"

# 1. レイヤー違反チェック: ServiceからMapperを直接呼んでいないか
# (Service -> Repository -> Mapper の順序を守る)
echo "[Check 1] Layer Dependency: Service -> Mapper direct access..."
VIOLATIONS=$(grep -r "import.*\.mapper\." src/main/java/**/service/ | grep -v "Test")
if [ ! -z "$VIOLATIONS" ]; then
    echo -e "${RED}FAIL: Service layer must NOT import Mapper directly.${NC}"
    echo "$VIOLATIONS"
    EXIT_CODE=1
else
    echo -e "${GREEN}PASS${NC}"
fi

# 2. トランザクション境界チェック: Service層以外で @Transactional を使っていないか
echo "[Check 2] Transaction Boundary: @Transactional location..."
TRANS_VIOLATIONS=$(grep -r "@Transactional" src/main/java/ | grep -v "/service/" | grep -v "Test")
if [ ! -z "$TRANS_VIOLATIONS" ]; then
    echo -e "${RED}FAIL: @Transactional is only allowed in the Service layer.${NC}"
    echo "$TRANS_VIOLATIONS"
    EXIT_CODE=1
else
    echo -e "${GREEN}PASS${NC}"
fi

# 3. SQLのJava埋め込みチェック: Javaファイル内に直接SQLキーワードがないか
# (SQLはすべて MyBatis XML に集約する)
echo "[Check 3] SQL in Java: Inline SQL keywords..."
SQL_VIOLATIONS=$(grep -rE "SELECT |INSERT INTO |UPDATE |DELETE FROM " src/main/java/ | grep -v "Test")
if [ ! -z "$SQL_VIOLATIONS" ]; then
    echo -e "${RED}FAIL: Inline SQL detected in Java. Move to MyBatis XML.${NC}"
    echo "$SQL_VIOLATIONS"
    EXIT_CODE=1
else
    echo -e "${GREEN}PASS${NC}"
fi

# 4. パッケージ構成チェック: paths.md に定めたベースパッケージを遵守しているか
echo "[Check 4] Base Package Adherence: jp.co.softbank.duke.fd..."
INVALID_PACKAGES=$(find src/main/java -name "*.java" | xargs grep -L "package jp.co.softbank.duke.fd")
if [ ! -z "$INVALID_PACKAGES" ]; then
    echo -e "${RED}FAIL: Files found outside the mandatory base package.${NC}"
    echo "$INVALID_PACKAGES"
    EXIT_CODE=1
else
    echo -e "${GREEN}PASS${NC}"
fi

# 5. 完全修飾クラス名（FQCN）の禁止チェック
# (import文以外でパッケージ名を含むクラス参照を禁止する)
echo "[Check 5] Prohibit Fully Qualified Class Names (FQCN)..."
# 正規表現の説明: 行頭が import/package ではなく、小文字のパッケージパスの後に大文字で始まるクラス名が続く箇所を探す
FQCN_VIOLATIONS=$(grep -rE "(^|[^a-zA-Z0-9.])([a-z0-9]+\.)+[A-Z][a-zA-Z0-9]*" src/main/java/ | grep -vE "^import|^package|/src/test/" | grep -v "java.lang.")

if [ ! -z "$FQCN_VIOLATIONS" ]; then
    echo -e "${RED}FAIL: Fully Qualified Class Names (FQCN) detected. Use imports instead.${NC}"
    echo "$FQCN_VIOLATIONS"
    EXIT_CODE=1
else
    echo -e "${GREEN}PASS${NC}"
fi


# --- 結果判定 ---
echo "-----------------------------------"
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}RESULT: AUDIT PASSED${NC}"
else
    echo -e "${RED}RESULT: AUDIT FAILED${NC}"
fi

exit $EXIT_CODE