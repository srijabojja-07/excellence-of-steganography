# 🔐 Excellence of Steganography

## 📌 Project Overview

**Excellence of Steganography** is a cybersecurity project designed to securely hide confidential messages inside digital images using a combination of **Fernet Encryption** and **Least Significant Bit (LSB) Image Steganography**.

The system encrypts the secret message before embedding it into an image, providing two layers of security:

1. **Encryption** – Protects the message content.
2. **Steganography** – Conceals the existence of the message.

This ensures that sensitive information can be transmitted securely without attracting attention.

---

## 🎯 Problem Statement

Traditional communication methods expose sensitive information to interception and unauthorized access. To enhance confidentiality, this project combines cryptography and steganography techniques to securely transmit secret messages hidden within images.

---

## 🚀 Key Features

* Hide confidential messages inside images
* Fernet-based message encryption
* LSB (Least Significant Bit) image steganography
* Secure secret key generation
* Optional email-based key distribution
* Extraction only with the correct secret key
* PNG image support to preserve hidden data
* User-friendly graphical interface

---

## 🛠️ Technologies Used

### Programming Language

* Python

### Libraries & Frameworks

* Cryptography (Fernet)
* OpenCV
* Pillow (PIL)
* NumPy
* Tkinter / GUI Framework
* Python-dotenv
* SMTP (Email Integration)

### Security Techniques

* Fernet Symmetric Encryption
* Least Significant Bit (LSB) Steganography

---

## 🔒 Security Workflow

### Message Hiding Process

1. Select a cover image.
2. Enter the secret message.
3. Generate a secure encryption key.
4. Encrypt the message using Fernet encryption.
5. Embed the encrypted message into the image using LSB steganography.
6. Save the output image in PNG format.
7. Optionally send the secret key via email.

### Message Extraction Process

1. Select the stego image.
2. Enter the correct secret key.
3. Extract the hidden encrypted message.
4. Decrypt the message using Fernet.
5. Display the original secret message.

---

## 📂 Project Structure

```text
Excellence-of-Steganography/
│
├── images/                 # Cover and stego images
├── output/                 # Generated stego images
├── app.py                  # Main application
├── requirements.txt        # Dependencies
├── .env.example            # Environment variables template
├── README.md
└── .gitignore
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/srijabojja-07/excellence-of-steganography.git
```

### 2️⃣ Navigate to Project Directory

```bash
cd excellence-of-steganography
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python app.py
```

---

## 📧 Email Configuration (Optional)

To enable automatic secret key sharing through Gmail:

Create a `.env` file using `.env.example`.

```env
SENDER_EMAIL=yourgmail@gmail.com
SENDER_APP_PASSWORD=your_16_digit_gmail_app_password
```

### Important

* Enable Two-Factor Authentication (2FA) on Gmail.
* Generate a Gmail App Password.
* Never upload your `.env` file to GitHub.

---

## 🖼️ Supported Image Formats

### Recommended Format

```text
PNG
```

PNG preserves image quality and hidden data integrity.

### Not Recommended

```text
JPG / JPEG
```

JPEG compression may alter hidden bits and destroy embedded messages.

---

## 🔐 Security Advantages

* Dual-layer security through encryption and steganography
* Hidden communication channel
* Protection against unauthorized access
* Secure key-based message recovery
* Reduced risk of message interception

---

## 📊 Project Applications

* Secure communication
* Confidential data sharing
* Military and defense communications
* Digital forensics
* Cybersecurity research
* Information protection systems

---

## 🔮 Future Enhancements

* Audio Steganography
* Video Steganography
* AES-256 Encryption Integration
* Multi-file Secret Embedding
* Cloud-based Secure Message Sharing
* Advanced Image Analysis Resistance

---

## 👩‍💻 Author

**Srija Bojja**

B.Tech – Information Technology

Cybersecurity & Machine Learning Enthusiast

GitHub: https://github.com/srijabojja-07
