import os
import tempfile

from openpyxl import load_workbook

from .worker import celery_app
from .database import SessionLocal
from .models import Trade
from .storage import download_file_from_r2


@celery_app.task
def process_excel(object_key: str):

    db = SessionLocal()

    # Create temporary local file
    temp_file = tempfile.NamedTemporaryFile(
        suffix=".xlsx",
        delete=False
    )

    local_file_path = temp_file.name

    temp_file.close()

    try:

        # Download Excel from R2
        download_file_from_r2(
            object_key,
            local_file_path
        )

        print(
            f"Downloaded file from R2: {object_key}"
        )

        workbook = load_workbook(
            local_file_path,
            read_only=True
        )

        worksheet = workbook.active

        batch = []

        batch_size = 1000

        processed_rows = 0

        # Skip header row
        for row in worksheet.iter_rows(
            min_row=2,
            values_only=True
        ):

            employee = row[0]
            location = row[1]
            sex = row[2]
            salary = row[3]
            date_hired = row[4]

            trade_record = Trade(
                client_id=row[0],
                client_name=row[1],
                account_code=row[2],
                scrip_id=row[3],
                scrip_name=row[4],
                isin_code=row[5],
                trade_type=row[6],
                trade_number=row[7],
                trade_on=row[8],
                credit_date=row[9],
                rate=row[10],
                quantity=row[11],
                amount=row[12],
                net_amount=row[13],
                stamp_duty_amount=row[14],
                stt=row[15]
            )

            batch.append(trade_record)

            # Insert every 1000 rows
            if len(batch) >= batch_size:

                db.add_all(batch)
                db.commit()

                processed_rows += len(batch)

                print(
                    f"Processed {processed_rows} rows"
                )

                batch.clear()

        # Insert remaining rows
        if batch:

            db.add_all(batch)
            db.commit()

            processed_rows += len(batch)

        workbook.close()

        print(
            f"Excel processing completed. "
            f"Total rows: {processed_rows}"
        )

        return {
            "status": "completed",
            "rows_processed": processed_rows
        }

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()

        # Delete temporary downloaded file
        if os.path.exists(local_file_path):

            os.remove(local_file_path)