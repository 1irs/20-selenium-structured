#!/usr/bin/env bash
# Ожидание того, что browserless готов принимать команды
pytest test --html=/test-reports/report.html --self-contained-html
