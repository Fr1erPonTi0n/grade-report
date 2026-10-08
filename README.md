### Larper Alex Ivanovich 4SPI

## Description

Develop a console application called "Academic Performance Analyzer." The program accepts the path to a CSV file as a command-line argument and saves the result to a JSON file at a user-specified path.
The input CSV contains the columns `student`, `group`, and `score`. For each student, the data includes a surname, a group, and an integer score ranging from 0 to 100. Use UTF-8 encoding.
Example execution: `python main.py data/students.csv --output report.json`

## Requirements

- Python 3.14.4
- Poetry

## Installation

```bash
poetry install
```

## Launch
```bash
poetry run python main.py data/students.csv --output report.json
```

Processing all CSV files in the data folder:

```bash
for file in data/*.csv; do
    [ -f "\$file" ] || continue
    name=\$(basename "\$file" .csv)
    echo "Файл: \$(basename "\$file")"
    poetry run python main.py "\$file" --output "report-\${name}.json"
done
```

## Build

```bash
poetry build
```

To build an executable application on Linux:

```bash
sudo apt install binutils
poetry run pyinstaller --name grade-report --onedir main.py
```
