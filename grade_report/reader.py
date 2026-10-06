import csv
from pathlib import Path


REQUIRED_COLUMNS = {"student", "group", "score"}


class DataValidationError(Exception):
    """Ошибка проверки входных данных."""


def read_students(file_path: str) -> list[dict]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Входной файл не найден: {file_path}"
        )

    if not path.is_file():
        raise DataValidationError(
            f"Указанный путь не является файлом: {file_path}"
        )

    students = []

    try:
        with path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise DataValidationError(
                    "CSV-файл не содержит заголовка."
                )

            actual_columns = set(reader.fieldnames)
            missing_columns = REQUIRED_COLUMNS - actual_columns

            if missing_columns:
                missing = ", ".join(sorted(missing_columns))
                raise DataValidationError(
                    f"Отсутствуют обязательные столбцы: {missing}"
                )

            for line_number, row in enumerate(reader, start=2):
                student = (row.get("student") or "").strip()
                group = (row.get("group") or "").strip()
                score_text = (row.get("score") or "").strip()

                if not student:
                    raise DataValidationError(
                        f"Строка {line_number}: пустое поле student."
                    )

                if not group:
                    raise DataValidationError(
                        f"Строка {line_number}: пустое поле group."
                    )

                if not score_text:
                    raise DataValidationError(
                        f"Строка {line_number}: пустое поле score."
                    )

                try:
                    score = int(score_text)
                except ValueError:
                    raise DataValidationError(
                        f"Строка {line_number}: балл должен быть целым числом."
                    )

                if not 0 <= score <= 100:
                    raise DataValidationError(
                        f"Строка {line_number}: балл должен быть от 0 до 100."
                    )

                students.append(
                    {
                        "student": student,
                        "group": group,
                        "score": score,
                    }
                )

    except UnicodeDecodeError:
        raise DataValidationError(
            "Не удалось прочитать файл. Используйте кодировку UTF-8."
        )

    return students
