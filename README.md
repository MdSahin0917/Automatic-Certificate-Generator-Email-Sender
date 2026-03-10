# Automatic Certificate Generator & Email Sender

This project automatically:

1. Generates **personalized certificates** from a template image.
2. Reads participant data from a **CSV file**.
3. Creates certificates as **PDF files**.
4. Optionally **emails the certificates automatically** to each participant.

The system supports **Participants and Presenters** and highlights important text such as **names and presentation types** on the certificate.

It works on **Linux, Windows, and macOS**.

---

# Project Structure

Your project should contain the following files:

```
project-folder/
│
├── main.py            # Main script to run the program
├── certificate.py     # Handles certificate generation
├── Email.py           # Handles email sending
├── students.csv       # Participant data
├── cer1.png           # Certificate template image
└── output/            # Generated certificates
```

---

# Requirements

Python **3.8 or higher** is recommended.

### Required Python Libraries

* pandas
* pillow

Install them using:

```
pip install pandas pillow
```

If you use **Linux or macOS**, you may need:

```
pip3 install pandas pillow
```

---

# CSV File Format

The CSV file must contain the following columns:

```
Name,Email,PresentationType,PresentationTitle,partiType
```

Example:

```
Name,Email,PresentationType,PresentationTitle,partiType
John Doe,john@email.com,Oral,Quantum Entanglement,Presenter
Jane Smith,jane@email.com,, ,Participant
```

Explanation:

| Column            | Description                             |
| ----------------- | --------------------------------------- |
| Name              | Full name of participant                |
| Email             | Email where certificate will be sent    |
| PresentationType  | Oral / Poster etc.                      |
| PresentationTitle | Title of presentation                   |
| partiType         | Either **Participant** or **Presenter** |

Important:

* `Participant` → Only participation certificate generated
* `Presenter` → Presentation certificate generated

---

# Certificate Template

You must provide a **certificate template image**.

Supported formats:

```
PNG
JPG
```

Example:

```
cer1.png
```

The script writes text **on top of this image**.

---

# Gmail Setup (Required for Email Sending)

If you want to send certificates automatically through Gmail:

### Step 1 — Enable 2-Factor Authentication

Go to:

```
Google Account → Security → 2-Step Verification
```

Enable it.

---

### Step 2 — Generate an App Password

Go to:

```
Google Account → Security → App Passwords
```

Create a password for:

```
Mail → Other Device
```

Example:

```
abcd efgh ijkl mnop
```

---

### Step 3 — Add it to `Email.py`

Replace:

```
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"
```

Example:

```
SENDER_EMAIL = "example@gmail.com"
SENDER_PASSWORD = "abcd efgh ijkl mnop"
```

Never use your real Gmail password.

---

# Running the Program

Run the main script:

```
python main.py
```

The program will ask for:

```
Enter the path to your CSV file:
Enter the path to your certificate template file:
Enter the output folder path:
```

Example:

```
Enter the path to your CSV file: students.csv
Enter the path to your certificate template file: cer1.png
Enter the output folder path: output
```

---

# What Happens Next

For each row in the CSV:

1. Data is read
2. Certificate text is generated
3. Certificate is created as **PDF**
4. The certificate is saved to the **output folder**
5. The certificate can be **emailed automatically**

Example output:

```
Processing: John Doe
Certificate generated for John Doe
Certificate sent to John Doe (john@email.com)
```

---

# Output Example

Generated files:

```
output/
│
├── John Doe.pdf
├── Jane Smith.pdf
```

---

# Supported Operating Systems

This project works on:

### Linux

```
Ubuntu
Debian
Arch
Fedora
```

Run:

```
python3 main.py
```

---

### Windows

Install Python from:

```
https://python.org
```

Then run:

```
python main.py
```

---

### macOS

Install Python using:

```
brew install python
```

Then run:

```
python3 main.py
```

---

# Customization

You can easily modify:

### Certificate Text

Inside `main.py`:

```
paText
prText1
prText2
```

---

### Font Size

```
FONT_BODY = ImageFont.truetype(..., 35)
FONT_HIGHLIGHT = ImageFont.truetype(..., 40)
```

---

### Text Position

Inside `certificate.py`:

```
y = 400
y = 500
y = 600
```

Adjust these values to move text vertically.

---

# Debugging

The program prints debug information such as:

```
Processing Row 1
Name: John Doe
Presentation Type: Oral
Title: Quantum Entanglement
```

This helps detect issues with CSV data.

---

# Common Errors

### 1. Font Not Found

Linux fonts are located at:

```
/usr/share/fonts/truetype/dejavu/
```

If the script cannot find fonts, install:

```
sudo apt install fonts-dejavu
```

---

### 2. CSV Column Error

Make sure the CSV headers are exactly:

```
Name,Email,PresentationType,PresentationTitle,partiType
```

---

### 3. Gmail Login Failed

Use **App Password**, not your Gmail password.

---

# Security Warning

Never upload your email password to GitHub.

Always store credentials safely.

---

# Author

Md Sahin Ahamed
MSc Physics
Aliah University

---

Security Notice

If you distribute this software to clients:

• Do not include your personal Gmail credentials
• Each client should configure their own email account

License

This software is commercial software.

Unauthorized redistribution, resale, or modification without permission is strictly prohibited.

All rights reserved.

