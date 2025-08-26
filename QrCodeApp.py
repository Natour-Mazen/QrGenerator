import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import qrcode
from PIL import Image, ImageTk

class QrCodeApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Générateur de QR Code")
        self.geometry("500x500")
        self.configure(bg="#f5f5f5")

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=5)
        self.style.configure("TLabel", font=("Arial", 12))

        self.qr_color = "black"
        self.bg_color = "white"

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True, fill="both")

        # Entrée du lien
        ttk.Label(frame, text="Lien :").grid(row=0, column=0, sticky="w", pady=5)
        self.lien_entry = ttk.Entry(frame, width=40)
        self.lien_entry.grid(row=0, column=1, pady=5)

        # Couleur QR Code
        ttk.Label(frame, text="Couleur QR Code :").grid(row=1, column=0, sticky="w", pady=5)
        self.qr_color_btn = ttk.Button(frame, text="Choisir", command=lambda: self.choisir_couleur("qr"))
        self.qr_color_btn.grid(row=1, column=1, sticky="w")
        self.qr_color_preview = tk.Label(frame, width=3, height=1, bg=self.qr_color)
        self.qr_color_preview.grid(row=1, column=2, padx=5)

        # Couleur arrière-plan
        self.bg_label = ttk.Label(frame, text="Couleur Fond :")
        self.bg_label.grid(row=2, column=0, sticky="w", pady=5)
        self.bg_color_btn = ttk.Button(frame, text="Choisir", command=lambda: self.choisir_couleur("bg"))
        self.bg_color_btn.grid(row=2, column=1, sticky="w")
        self.bg_color_preview = tk.Label(frame, width=3, height=1, bg=self.bg_color)
        self.bg_color_preview.grid(row=2, column=2, padx=5)

        # Checkbox fond transparent
        self.transparent_var = tk.BooleanVar()
        self.transparent_check = ttk.Checkbutton(frame, text="Fond transparent", variable=self.transparent_var,
                                                 command=self.toggle_bg_option)
        self.transparent_check.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

        # Nom du fichier
        ttk.Label(frame, text="Nom du fichier :").grid(row=4, column=0, sticky="w", pady=5)
        self.nom_fichier_entry = ttk.Entry(frame, width=40)
        self.nom_fichier_entry.grid(row=4, column=1, pady=5)

        # Bouton de génération
        self.generate_btn = ttk.Button(frame, text="Générer QR Code", command=self.generer_qr_code)
        self.generate_btn.grid(row=5, column=0, columnspan=2, pady=20)

    def choisir_couleur(self, type_couleur):
        color = colorchooser.askcolor()[1]
        if color:
            if type_couleur == "qr":
                self.qr_color = color
                self.qr_color_preview.config(bg=color)
            elif not self.transparent_var.get():
                self.bg_color = color
                self.bg_color_preview.config(bg=color)

    def toggle_bg_option(self):
        if self.transparent_var.get():
            self.bg_color_btn.state(["disabled"])
            self.bg_color_preview.config(bg="#f5f5f5")
        else:
            self.bg_color_btn.state(["!disabled"])
            self.bg_color_preview.config(bg=self.bg_color)

    def generer_qr_code(self):
        lien = self.lien_entry.get().strip()
        nom_fichier = self.nom_fichier_entry.get().strip()

        if not lien or not nom_fichier:
            messagebox.showerror("Erreur", "Tous les champs sont requis.")
            return

        couleur_bg = self.bg_color if not self.transparent_var.get() else (255, 255, 255)
        # white color

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(lien)
        qr.make(fit=True)

        img = qr.make_image(fill=self.qr_color, back_color=couleur_bg)

        if self.transparent_var.get():
            print("Fond transparent")
            img = img.convert("RGBA")
            datas = img.getdata()
            new_data = []
            for item in datas:
                if item[:3] == (255, 255, 255):  # Fond blanc détecté
                    new_data.append((255, 255, 255, 0))  # Rendre transparent
                else:
                    new_data.append(item)
            img.putdata(new_data)

        fichier_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")],
                                                    initialfile=nom_fichier)
        if fichier_path:
            img.save(fichier_path, "PNG")
            messagebox.showinfo("Succès", "Le QR code a été généré avec succès.")

