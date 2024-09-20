import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

# Fungsi untuk Vigenere Cipher
def vigenere_encrypt(plaintext, key):
    key = key.upper()
    plaintext = plaintext.upper()
    ciphertext = ""
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            ciphertext += chr(((ord(plaintext[i]) - 65) + (ord(key[i % len(key)]) - 65)) % 26 + 65)
        else:
            ciphertext += plaintext[i]
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    key = key.upper()
    ciphertext = ciphertext.upper()
    plaintext = ""
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            plaintext += chr(((ord(ciphertext[i]) - 65) - (ord(key[i % len(key)]) - 65)) % 26 + 65)
        else:
            plaintext += ciphertext[i]
    return plaintext

# Fungsi untuk Playfair Cipher
def create_playfair_matrix(key):
    key = key.upper().replace('J', 'I')
    matrix = []
    used_chars = set()

    for char in key:
        if char not in used_chars and char.isalpha():
            matrix.append(char)
            used_chars.add(char)

    for i in range(65, 91):
        if chr(i) not in used_chars and chr(i) != 'J':
            matrix.append(chr(i))

    return [matrix[i:i + 5] for i in range(0, 25, 5)]

def prepare_text_playfair(text):
    text = text.upper().replace('J', 'I').replace(' ', '')
    prepared = ""
    i = 0
    while i < len(text):
        prepared += text[i]
        if i + 1 < len(text) and text[i] == text[i + 1]:
            prepared += 'X'
        else:
            if i + 1 < len(text):
                prepared += text[i + 1]
            else:
                prepared += 'X'
            i += 1
        i += 1
    return prepared

def playfair_encrypt(plaintext, key):
    matrix = create_playfair_matrix(key)
    plaintext = prepare_text_playfair(plaintext)
    ciphertext = ""

    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i + 1]
        row_a, col_a = divmod(find_index_playfair(matrix, a), 5)
        row_b, col_b = divmod(find_index_playfair(matrix, b), 5)

        if row_a == row_b:
            ciphertext += matrix[row_a][(col_a + 1) % 5]
            ciphertext += matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            ciphertext += matrix[(row_a + 1) % 5][col_a]
            ciphertext += matrix[(row_b + 1) % 5][col_b]
        else:
            ciphertext += matrix[row_a][col_b]
            ciphertext += matrix[row_b][col_a]

    return ciphertext

def playfair_decrypt(ciphertext, key):
    matrix = create_playfair_matrix(key)
    plaintext = ""

    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i + 1]
        row_a, col_a = divmod(find_index_playfair(matrix, a), 5)
        row_b, col_b = divmod(find_index_playfair(matrix, b), 5)

        if row_a == row_b:
            plaintext += matrix[row_a][(col_a - 1) % 5]
            plaintext += matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            plaintext += matrix[(row_a - 1) % 5][col_a]
            plaintext += matrix[(row_b - 1) % 5][col_b]
        else:
            plaintext += matrix[row_a][col_b]
            plaintext += matrix[row_b][col_a]

    return plaintext.replace('X', '')

def find_index_playfair(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i * 5 + row.index(char)
    return -1

# Fungsi Hill Cipher
def hill_encrypt(plaintext, key):
    key_matrix = np.array(key).reshape(2, 2)
    plaintext = plaintext.upper().replace(' ', '')
    
    if len(plaintext) % 2 != 0:
        plaintext += 'X'  # Tambahkan 'X' jika panjang plaintext ganjil

    ciphertext = ''
    for i in range(0, len(plaintext), 2):
        vector = np.array([ord(plaintext[i]) - 65, ord(plaintext[i + 1]) - 65])
        encrypted_vector = np.dot(key_matrix, vector) % 26
        ciphertext += chr(encrypted_vector[0] + 65) + chr(encrypted_vector[1] + 65)

    return ciphertext

def hill_decrypt(ciphertext, key):
    key_matrix = np.array(key).reshape(2, 2)
    determinant = int(np.round(np.linalg.det(key_matrix))) % 26
    
    # Mencari invers determinan modulo 26
    inv_determinant = pow(determinant, -1, 26)
    
    # Membuat matriks adjugate
    adjugate_matrix = np.round(determinant * np.linalg.inv(key_matrix)).astype(int) % 26

    # Menghitung matriks invers kunci
    inv_key_matrix = (inv_determinant * adjugate_matrix) % 26

    plaintext = ''
    for i in range(0, len(ciphertext), 2):
        vector = np.array([ord(ciphertext[i]) - 65, ord(ciphertext[i + 1]) - 65])
        decrypted_vector = np.dot(inv_key_matrix, vector) % 26
        plaintext += chr(int(decrypted_vector[0]) + 65) + chr(int(decrypted_vector[1]) + 65)

    # Jika 'X' ditambahkan saat enkripsi, hapus hanya jika ada di akhir
    if plaintext.endswith('X'):
        plaintext = plaintext[:-1]

    return plaintext


# Fungsi untuk membuka file dan mengisi input pesan
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    return ""

# Fungsi untuk menyimpan hasil ke dalam file .txt
def save_result_to_file(result):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(result)
        messagebox.showinfo("Success", "Result saved to file!")

# Fungsi untuk menampilkan hasil
def show_result(result):
    result_label.config(text="Result: " + result)

# Fungsi validasi kunci
def validate_key(key):
    if len(key) < 12:
        messagebox.showerror("Error", "Key must be at least 12 characters long!")
        return False
    return True

# Fungsi untuk memilih dan menjalankan enkripsi
def encrypt_action():
    cipher = cipher_var.get()
    message = message_input.get()
    key = key_input.get()

    if validate_key(key):
        if cipher == "Vigenere":
            result = vigenere_encrypt(message, key)
        elif cipher == "Playfair":
            result = playfair_encrypt(message, key)
        elif cipher == "Hill":
            key_matrix = [3, 3, 2, 5]  # Contoh kunci untuk Hill Cipher
            result = hill_encrypt(message, key_matrix)
        else:
            result = "Invalid cipher choice"
        show_result(result)

# Fungsi untuk memilih dan menjalankan dekripsi
def decrypt_action():
    cipher = cipher_var.get()
    message = message_input.get()
    key = key_input.get()

    if validate_key(key):
        if cipher == "Vigenere":
            result = vigenere_decrypt(message, key)
        elif cipher == "Playfair":
            result = playfair_decrypt(message, key)
        elif cipher == "Hill":
            key_matrix = [3, 3, 2, 5]  # Contoh kunci untuk Hill Cipher
            result = hill_decrypt(message, key_matrix)
        else:
            result = "Invalid cipher choice"
        show_result(result)

# Fungsi untuk mengisi input dari file
def upload_file_action():
    content = open_file()
    if content:
        message_input.delete(0, tk.END)
        message_input.insert(0, content)

# Fungsi untuk menampilkan antarmuka
def create_gui():
    global message_input, key_input, result_label, cipher_var

    root = tk.Tk()
    root.title("Cipher Tool")

    # Label dan input untuk pesan
    tk.Label(root, text="Input Message:").grid(row=0, column=0)
    message_input = tk.Entry(root, width=50)
    message_input.grid(row=0, column=1)

    # Tombol untuk upload file
    tk.Button(root, text="Upload File", command=upload_file_action).grid(row=0, column=2)

    # Label dan input untuk kunci
    tk.Label(root, text="Key:").grid(row=1, column=0)
    key_input = tk.Entry(root, width=50, show='*')  # Menambahkan show='*' untuk menyembunyikan input
    key_input.grid(row=1, column=1)


    # Opsi untuk memilih cipher
    cipher_var = tk.StringVar(root)
    cipher_var.set("Vigenere")  # Default value
    tk.Label(root, text="Choose Cipher:").grid(row=2, column=0)
    cipher_menu = tk.OptionMenu(root, cipher_var, "Vigenere", "Playfair", "Hill")
    cipher_menu.grid(row=2, column=1)

    # Tombol enkripsi dan dekripsi
    tk.Button(root, text="Encrypt", command=encrypt_action).grid(row=3, column=0)
    tk.Button(root, text="Decrypt", command=decrypt_action).grid(row=3, column=1)

    # Tombol untuk menyimpan hasil ke file
    tk.Button(root, text="Save to File", command=lambda: save_result_to_file(result_label.cget("text")[8:])).grid(row=3, column=2)

    # Label untuk menampilkan hasil
    result_label = tk.Label(root, text="Result: ")
    result_label.grid(row=4, column=0, columnspan=3)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
