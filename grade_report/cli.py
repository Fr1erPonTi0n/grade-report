import argparse
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .reader import DataValidationError, read_students
from .statistics import calculate_statistics


console = Console()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Анализатор успеваемости студентов"
    )

    parser.add_argument(
        "input_file",
        help="Путь к входному CSV-файлу",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Путь к выходному JSON-файлу",
    )

    return parser.parse_args()


def print_statistics(statistics: dict) -> None:
    table = Table(title="Анализ успеваемости")

    table.add_column("Показатель", style="cyan")
    table.add_column("Значение", style="green")

    table.add_row(
        "Количество студентов",
        str(statistics["student_count"]),
    )
    table.add_row(
        "Средний балл",
        f'{statistics["average_score"]:.2f}',
    )
    table.add_row(
        "Минимальный балл",
        str(statistics["minimum_score"]),
    )
    table.add_row(
        "Максимальный балл",
        str(statistics["maximum_score"]),
    )

    console.print(table)

    groups_table = Table(title="Средний балл по группам")
    groups_table.add_column("Группа", style="cyan")
    groups_table.add_column("Средний балл", style="green")

    for group, average in statistics["groups"].items():
        groups_table.add_row(group, f"{average:.2f}")

    if statistics["groups"]:
        console.print(groups_table)


def save_report(statistics: dict, output_path: str) -> None:
    output = Path(output_path)

    if output.parent != Path("."):
        output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as file:
        json.dump(
            statistics,
            file,
            ensure_ascii=False,
            indent=4,
        )


def main() -> int:
    args = parse_arguments()

    try:
        students = read_students(args.input_file)
    except FileNotFoundError as error:
        console.print(f"[red]Ошибка:[/red] {error}")
        return 1
    except DataValidationError as error:
        console.print(f"[red]Ошибка проверки данных:[/red] {error}")
        return 1

    if not students:
        console.print(
            "[yellow]Файл содержит только заголовок. "
            "Данные отсутствуют.[/yellow]"
        )
        return 0

    statistics = calculate_statistics(students)
    print_statistics(statistics)
    save_report(statistics, args.output)

    console.print(
        f"[green]Отчёт сохранён в файл:[/green] {args.output}"
    )

    return 0
