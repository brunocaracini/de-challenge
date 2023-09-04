"-------------------------------Imports Section-------------------------------"

# Libraries
import io
import csv


class Controller:

    @staticmethod
    async def read_csv_reader(file, headers: list[str] = None):
        if not file.filename.lower().endswith(".csv"):
            raise Exception("File is not in CSV format")
        file_content = await file.read()
        csv_reader = csv.DictReader(
            io.StringIO(file_content.decode("utf-8")), fieldnames=headers
        )

        # Use a dictionary comprehension to replace empty strings with None
        csv_content = [
            {key: (None if value == "" else value) for key, value in row.items()}
            for row in csv_reader
        ]
        return csv_content
