"-------------------------------Imports Section-------------------------------"

# Libraries
import io
import csv
from fastapi import HTTPException

class Controller:

    @staticmethod
    async def read_csv_reader(file, headers: list[str] = None, allowed_headers: list[str] = None):
        if not file.filename.lower().endswith(".csv"):
            raise Exception("File is not in CSV format")
        file_content = await file.read()
        csv_reader = csv.DictReader(
            io.StringIO(file_content.decode("utf-8")), fieldnames=headers
        )
        if allowed_headers:
            print(allowed_headers, csv_reader.fieldnames)
            if set(allowed_headers) != set(csv_reader.fieldnames):
                raise HTTPException(
                    status_code=400,
                    detail=f"CSV headers do not match the allowed header combination. CSV headers must be: {allowed_headers}",
                )
        # Use a dictionary comprehension to replace empty strings with None
        csv_content = [
            {key: (None if value == "" else value) for key, value in row.items()}
            for row in csv_reader
        ]
        return csv_content
