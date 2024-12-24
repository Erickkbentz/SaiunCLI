#!/bin/bash
set -e

echo "Installing Git hooks..."

cp .githooks/pre-commit .git/hooks/pre-commit
cp .githooks/pre-push .git/hooks/pre-push

chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push

echo "Pre-commit hook installed!"
