import os
import smtplib
import tkinter as tk
from email.message import EmailMessage
from tkinter import filedialog, messagebox

from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv
from PIL import Image, ImageTk

load_dotenv()

DELIMITER = "1111111111111110"


def text_to_binary(text: str) -> str:
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_text(binary: str) -> str:
    chars = [binary[i:i + 8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars if len(char) == 8)


def encrypt_message_with_key(message: str, key: bytes) -> str:
    return Fernet(key).encrypt(message.encode()).decode()


def decrypt_message_with_key(encrypted_message: str, key_text: str) -> str:
    key = key_text.strip().encode()
    return Fernet(key).decrypt(encrypted_message.encode()).decode()


def hide_data_in_image(input_image_path: str, secret_text: str, output_image_path: str) -> str:
    secret_key = Fernet.generate_key()
    encrypted_text = encrypt_message_with_key(secret_text, secret_key)
    binary_data = text_to_binary(encrypted_text) + DELIMITER

    image = Image.open(input_image_path).convert("RGB")
    pixels = list(image.getdata())

    max_capacity = len(pixels) * 3
    if len(binary_data) > max_capacity:
        raise ValueError("Secret message is too large for this image. Please choose a bigger image or shorter message.")

    new_pixels = []
    data_index = 0

    for pixel in pixels:
        r, g, b = pixel
        if data_index < len(binary_data):
            r = (r & ~1) | int(binary_data[data_index])
            data_index += 1
        if data_index < len(binary_data):
            g = (g & ~1) | int(binary_data[data_index])
            data_index += 1
        if data_index < len(binary_data):
            b = (b & ~1) | int(binary_data[data_index])
            data_index += 1
        new_pixels.append((r, g, b))

    image.putdata(new_pixels)
    image.save(output_image_path, "PNG")
    return secret_key.decode()


def extract_data_from_image(stego_image_path: str, secret_key: str) -> str:
    image = Image.open(stego_image_path).convert("RGB")
    pixels = list(image.getdata())

    binary_data = ""
    for pixel in pixels:
        for color in pixel[:3]:
            binary_data += str(color & 1)
            if binary_data.endswith(DELIMITER):
                encrypted_binary = binary_data[:-len(DELIMITER)]
                encrypted_text = binary_to_text(encrypted_binary)
                return decrypt_message_with_key(encrypted_text, secret_key)

    raise ValueError("No hidden message found in this image.")


def send_key_email(receiver_email: str, secret_key: str) -> None:
    sender_email = os.getenv("SENDER_EMAIL")
    sender_app_password = os.getenv("SENDER_APP_PASSWORD")

    if not sender_email or not sender_app_password:
        raise ValueError("Email is not configured. Add SENDER_EMAIL and SENDER_APP_PASSWORD in the .env file.")

    msg = EmailMessage()
    msg["Subject"] = "Secret Key for Excellence of Steganography"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(
        f"Your secret key for extracting the hidden message is:\n\n{secret_key}\n\nKeep this key private."
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_app_password)
        server.send_message(msg)


class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excellence of Steganography")
        self.root.geometry("920x780")
        self.root.configure(bg="#121212")
        self.selected_image_path = ""

        tk.Label(
            root,
            text="Excellence of Steganography",
            font=("Times New Roman", 28, "bold"),
            bg="#121212",
            fg="#ffffff"
        ).pack(pady=12)

        tk.Label(
            root,
            text="AES/Fernet Encryption + LSB Image Steganography + Email Key Distribution",
            font=("Times New Roman", 14),
            bg="#121212",
            fg="#bdbdbd"
        ).pack(pady=4)

        main_frame = tk.Frame(root, bg="#1f1f2e", padx=25, pady=18)
        main_frame.pack(pady=12)

        tk.Button(
            main_frame,
            text="Select Cover / Stego Image",
            command=self.select_image,
            bg="#4CAF50",
            fg="white",
            font=("Times New Roman", 13, "bold"),
            width=25
        ).grid(row=0, column=0, padx=10, pady=8)

        self.image_label = tk.Label(main_frame, text="No image selected", bg="#1f1f2e", fg="white")
        self.image_label.grid(row=0, column=1, padx=10, pady=8)

        self.preview_label = tk.Label(main_frame, bg="#1f1f2e")
        self.preview_label.grid(row=1, column=0, columnspan=2, pady=8)

        tk.Label(
            main_frame,
            text="Secret Message to Hide",
            bg="#1f1f2e",
            fg="white",
            font=("Times New Roman", 13)
        ).grid(row=2, column=0, sticky="w", pady=4)

        # Hidden input: message appears as ****** while typing
        self.message_box = tk.Entry(
            main_frame,
            font=("Times New Roman", 14),
            width=70,
            show="*"
        )
        self.message_box.grid(row=3, column=0, columnspan=2, pady=4)

        tk.Label(
            main_frame,
            text="Receiver Email for Secret Key",
            bg="#1f1f2e",
            fg="white",
            font=("Times New Roman", 13)
        ).grid(row=4, column=0, sticky="w", pady=4)

        self.email_entry = tk.Entry(main_frame, font=("Times New Roman", 12), width=60)
        self.email_entry.grid(row=5, column=0, columnspan=2, pady=4)

        tk.Label(
            main_frame,
            text="Secret Key for Extraction",
            bg="#1f1f2e",
            fg="white",
            font=("Times New Roman", 13)
        ).grid(row=6, column=0, sticky="w", pady=4)

        self.key_entry = tk.Entry(main_frame, show="*", font=("Times New Roman", 12), width=60)
        self.key_entry.grid(row=7, column=0, columnspan=2, pady=4)

        button_frame = tk.Frame(main_frame, bg="#1f1f2e")
        button_frame.grid(row=8, column=0, columnspan=2, pady=18)

        tk.Button(
            button_frame,
            text="Hide Message + Generate Key",
            command=self.hide_message,
            bg="#008CBA",
            fg="white",
            font=("Times New Roman", 13, "bold"),
            width=24
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            button_frame,
            text="Extract Message Using Key",
            command=self.extract_message,
            bg="#FF9800",
            fg="white",
            font=("Times New Roman", 13, "bold"),
            width=24
        ).grid(row=0, column=1, padx=8)

        tk.Label(
            main_frame,
            text="Output / Extracted Message",
            bg="#1f1f2e",
            fg="white",
            font=("Times New Roman", 13)
        ).grid(row=9, column=0, sticky="w", pady=4)

        self.result_box = tk.Text(main_frame, height=7, width=60, font=("Times New Roman", 12))
        self.result_box.grid(row=10, column=0, columnspan=2, pady=4)
        self.result_box.insert(
            tk.END,
            "After hiding, the generated key appears here. After extraction, the hidden message appears here."
        )

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.selected_image_path = file_path
            self.image_label.config(text=os.path.basename(file_path))

            # Clear old output when user selects a new image
            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, "Image selected successfully. Now hide or extract a message.")

            img = Image.open(file_path)
            img.thumbnail((330, 250))
            photo = ImageTk.PhotoImage(img)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo

    def hide_message(self):
        if not self.selected_image_path:
            messagebox.showerror("Error", "Please select a cover image first.")
            return

        secret_message = self.message_box.get().strip()
        receiver_email = self.email_entry.get().strip()

        if not secret_message:
            messagebox.showerror("Error", "Please enter a secret message.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialfile="stego_image.png"
        )

        if not output_path:
            return

        try:
            secret_key = hide_data_in_image(self.selected_image_path, secret_message, output_path)
            email_status = ""

            if receiver_email:
                try:
                    send_key_email(receiver_email, secret_key)
                    email_status = f"\nSecret key sent to: {receiver_email}"
                except Exception as email_error:
                    email_status = f"\nEmail not sent: {email_error}"

            # Clear secret message input after hiding
            self.message_box.delete(0, tk.END)

            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END,
            f"Stego image saved successfully:\n{output_path}\n\nSecret key delivered successfully to:\n{receiver_email}"
   )
            messagebox.showinfo("Success", f"Message hidden successfully!{email_status}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_message(self):
        if not self.selected_image_path:
            messagebox.showerror("Error", "Please select a stego image first.")
            return

        secret_key = self.key_entry.get().strip()
        if not secret_key:
            messagebox.showerror("Error", "Please enter the secret key before extraction.")
            return

        try:
            hidden_message = extract_data_from_image(self.selected_image_path, secret_key)

            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, hidden_message)

            # Clear key after successful extraction
            self.key_entry.delete(0, tk.END)

            messagebox.showinfo("Success", "Hidden message extracted successfully!")
        except InvalidToken:
            messagebox.showerror("Error", "Wrong secret key! Unable to decrypt hidden message.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()