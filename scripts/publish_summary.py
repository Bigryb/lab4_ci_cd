import os
from pathlib import Path
import xml.etree.ElementTree as ET

junit_path = Path("reports/unit-report.xml")
coverage_path = Path("reports/coverage.xml")

lines = ["## Результаты модульного тестирования", ""]

if junit_path.exists():
    root = ET.parse(junit_path).getroot()
    suite = root.find("testsuite") if root.tag == "testsuites" else root
    if suite is not None:
        tests = int(suite.get("tests", "0"))
        failures = int(suite.get("failures", "0"))
        errors = int(suite.get("errors", "0"))
        skipped = int(suite.get("skipped", "0"))
        lines += [
            f"- Всего тестов: **{tests}**",
            f"- Успешно: **{tests - failures - errors - skipped}**",
            f"- Ошибки/падения: **{failures + errors}**",
            f"- Пропущено: **{skipped}**",
        ]
else:
    lines.append("- JUnit XML не был создан: проверьте логи выполнения.")

if coverage_path.exists():
    coverage = ET.parse(coverage_path).getroot()
    percent = 100 * float(coverage.get("line-rate", "0"))
    lines.append(f"- Покрытие строк кода: **{percent:.1f}%**")
else:
    lines.append("- Coverage XML не был создан.")

lines += ["", "Полные XML- и HTML-отчёты доступны в артефакте `unit-test-reports`."]
summary = "\n".join(lines) + "\n"

summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
if summary_file:
    with open(summary_file, "a", encoding="utf-8") as output:
        output.write(summary)
else:
    print(summary)
