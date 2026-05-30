# Excellence of Steganography

A cybersecurity project that hides encrypted secret messages inside images using Fernet encryption and LSB image steganography.

## Features

- Select a cover image
- Hide a secret message inside the image
- Generate a secure secret key
- Optional email key distribution
- Extract the hidden message only with the correct key
- Saves output as PNG to protect hidden data

## Installation

```bash
pip install -r requirements.txt
python app.py
```

## Email Setup

To send the secret key through Gmail, create a `.env` file from `.env.example`:

```text
SENDER_EMAIL=yourgmail@gmail.com
SENDER_APP_PASSWORD=your_16_digit_gmail_app_password
```

Do not upload `.env` to GitHub.

## Workflow

1. Select a cover image.
2. Enter the secret message.
3. Optionally enter receiver email.
4. Click **Hide Message + Generate Key**.
5. Save the stego image as PNG.
6. Copy the generated secret key or send it by email.
7. Select the stego image.
8. Paste the key in **Secret Key for Extraction**.
9. Click **Extract Message Using Key**.

## Important

Use PNG for the stego image. JPG compression can destroy hidden data.

## Author

Srija Bojja
B.Tech Information Technology
Cybersecurity & Data Analytics Enthusiast

GitHub: github.com/srijabojja-07
