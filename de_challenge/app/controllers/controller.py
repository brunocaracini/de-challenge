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
        return [row for row in csv_reader]
