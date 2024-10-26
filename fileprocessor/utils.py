import pandas as pd
from django.conf import settings
from django.core.mail import send_mail


def process_file(file_path):
    """Process the uploaded file and generate summary statistics."""
    # Read the file (handles both Excel and CSV)
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # Ensure required columns exist
    required_columns = ["Cust State", "Cust Pin", "DPD"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError("File must contain columns: Cust State, Cust Pin, DPD")

    # Group by State and PIN
    summary = df.groupby(["Cust State", "Cust Pin"])["DPD"].agg(list).reset_index()

    # Format the summary data
    formatted_data = []
    for _, row in summary.iterrows():
        formatted_data.append(
            {
                "state": row["Cust State"],
                "pin": str(row["Cust Pin"]),
                "dpd": row["DPD"][0] if len(row["DPD"]) > 0 else 0,
            }
        )

    return formatted_data


def send_summary_email(summary, user_name):
    """Send summary report via email."""
    print("send_summary_email called successfully")
    subject = f"Python Assignment - {user_name}"

    body = "Delivery Performance Summary:\n\n"
    body += "Cust State\t\tCust Pin\t\tDPD\n"
    body += "-" * 50 + "\n"

    for entry in summary:
        body += f"{entry['state']}\t\t{entry['pin']}\t\t{entry['dpd']}\n"

    send_mail(
        subject=subject,
        message=body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["mybillions@protonmail.com"],
        fail_silently=False,
    )
