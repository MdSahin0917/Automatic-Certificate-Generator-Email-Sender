import certificate
import Email
from PIL import Image, ImageDraw, ImageFont
import os
import pandas as pd

# =============== CONFIGURATION =============== #
CSV_FILE = input("Enter the path to your CSV file: ")   # Your CSV file (Name,Email,PresentationType,PresentationTitle)
TEMPLATE_FILE = input("Enter the path to your certificate template file: ")   # Certificate template
OUTPUT_FOLDER = input("Enter the output folder path: ")   # Output folder

# =======================================================================================
FONT_BODY = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 35)
FONT_HIGHLIGHT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 40)
#===========================================================================================

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load student data
df = pd.read_csv(CSV_FILE)
df.columns = df.columns.str.strip()
print("\n=== CSV Data Loaded ===")
print(f"Columns: {list(df.columns)}")
print(f"First few rows:")
print(df.head())
print("=======================\n")

for index, row in df.iterrows():
    # Convert all values to strings and handle NaN
    name = str(row["Name"]).strip() if pd.notna(row["Name"]) else ""
    ptype = str(row["PresentationType"]).strip() if pd.notna(row["PresentationType"]) else ""
    title = str(row["PresentationTitle"]).strip() if pd.notna(row["PresentationTitle"]) else ""
    partiType = str(row["partiType"]).strip() if pd.notna(row["partiType"]) else ""
    email = str(row["Email"]).strip() if pd.notna(row["Email"]) else ""

    print(f"\n--- Processing Row {index+1} ---")
    print(f"Name: '{name}'")
    print(f"Presentation Type: '{ptype}'")
    print(f"Title: '{title}'")
    print(f"partiType: '{partiType}'")
    print(f"Email: '{email}'")

    # email texts
    email_content = f"Please find attached your E-certificate for attending the 'National Seminar on the Occasion of National Science Day' held at the Department of Physics, Aliah University, Newtown, Kolkata 700160, on 28th February 2026.\n\nPlease acknowledge the receipt of this mail. With best wishes,\nOrganizing Committee"

    # Certificate texts with placeholders for dynamic content
    paText = 'This is to certify that Mr. {name} participated in the "National Seminar on the Occasion of National Science Day" held at the Department of Physics, Aliah University, Newtown, Kolkata 700160, on 28th February 2026'
    
    prText1 = 'This is to certify that Mr. {name} has given an {ptype} presentation titled '
    
    prText2 = 'in the "National Seminar on the Occasion of National Science Day" held at the Department of Physics, Aliah University, Newtown, Kolkata 700160, on 28th February 2026'

    # Replace {ptype} with actual presentation type in prText1
    prText1 = prText1.replace("{ptype}", ptype)
    print(f"prText1 after ptype replacement: '{prText1}'")
    
    # Note: {name} will be replaced in the certificate.py file

    cert_path = certificate.generate_certificate(
        name, 
        partiType, 
        title, 
        TEMPLATE_FILE, 
        OUTPUT_FOLDER, 
        FONT_BODY, 
        FONT_HIGHLIGHT, 
        paText, 
        prText1, 
        prText2
    )

    Email.send_email(email, name, cert_path, email_content)
