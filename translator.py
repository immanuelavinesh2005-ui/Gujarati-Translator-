import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract
from googletrans import Translator
from config import *

# ── Apply config settings ─────────────────────────────────────────
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
translator = Translator()

# ── Main App ──────────────────────────────────────────────────────
class GujaratiTranslator:
    def __init__(self, root):
        root.title('Gujarati to English Translator')
        root.configure(bg='#f5f5f5')
        root.geometry('900x700')
        root.resizable(True, True)

        # ── Title ─────────────────────────────────────────────────
        tk.Label(root,
                 text='Gujarati ↔ English Translator',
                 font=('Arial', 20, 'bold'),
                 bg='#f5f5f5',
                 fg='#333').pack(pady=15)

        # ── Buttons row ───────────────────────────────────────────
        btn_frame = tk.Frame(root, bg='#f5f5f5')
        btn_frame.pack(pady=5)

        tk.Button(btn_frame,
                  text='Translate Text',
                  font=('Arial', 12),
                  bg='#4CAF50', fg='white',
                  width=15, height=1,
                  command=self.translate_text).grid(
                  row=0, column=0, padx=10)

        tk.Button(btn_frame,
                  text='Upload Image',
                  font=('Arial', 12),
                  bg='#2196F3', fg='white',
                  width=15, height=1,
                  command=self.upload_image).grid(
                  row=0, column=1, padx=10)

        tk.Button(btn_frame,
                  text='Clear All',
                  font=('Arial', 12),
                  bg='#f44336', fg='white',
                  width=15, height=1,
                  command=self.clear_all).grid(
                  row=0, column=2, padx=10)

        tk.Button(btn_frame,
                  text='Save Translation',
                  font=('Arial', 12),
                  bg='#FF9800', fg='white',
                  width=15, height=1,
                  command=self.save_translation).grid(
                  row=0, column=3, padx=10)

        # ── Text areas side by side ───────────────────────────────
        text_frame = tk.Frame(root, bg='#f5f5f5')
        text_frame.pack(fill='both', expand=True,
                        padx=20, pady=10)

        # Left — Gujarati input
        left_frame = tk.Frame(text_frame, bg='#f5f5f5')
        left_frame.pack(side='left', fill='both',
                        expand=True, padx=(0,10))

        tk.Label(left_frame,
                 text='Gujarati Text (Input)',
                 font=('Arial', 13, 'bold'),
                 bg='#f5f5f5', fg='#333').pack(anchor='w')

        self.gujarati_text = tk.Text(left_frame,
                                     font=('Arial', 13),
                                     wrap='word',
                                     relief='solid',
                                     borderwidth=1,
                                     bg='white')
        self.gujarati_text.pack(fill='both', expand=True)

        # Right — English output
        right_frame = tk.Frame(text_frame, bg='#f5f5f5')
        right_frame.pack(side='right', fill='both',
                         expand=True, padx=(10,0))

        tk.Label(right_frame,
                 text='English Translation (Output)',
                 font=('Arial', 13, 'bold'),
                 bg='#f5f5f5', fg='#333').pack(anchor='w')

        self.english_text = tk.Text(right_frame,
                                    font=('Arial', 13),
                                    wrap='word',
                                    relief='solid',
                                    borderwidth=1,
                                    bg='#f0fff0',
                                    state='disabled')
        self.english_text.pack(fill='both', expand=True)

        # ── Image preview ─────────────────────────────────────────
        tk.Label(root,
                 text='Uploaded Image Preview:',
                 font=('Arial', 11, 'bold'),
                 bg='#f5f5f5').pack(anchor='w', padx=20)

        self.image_label = tk.Label(root,
                                    bg='#ddd',
                                    text='No image uploaded',
                                    width=80, height=8,
                                    relief='solid',
                                    borderwidth=1)
        self.image_label.pack(padx=20, pady=5, fill='x')

        # ── Status bar ────────────────────────────────────────────
        self.status = tk.Label(root,
                               text='Ready',
                               font=('Arial', 10),
                               bg='#ddd', fg='#333',
                               anchor='w')
        self.status.pack(fill='x', side='bottom',
                         padx=0, pady=0)

    # ── Translate typed text ──────────────────────────────────────
    def translate_text(self):
        gujarati = self.gujarati_text.get('1.0', 'end').strip()

        if not gujarati:
            messagebox.showwarning('Empty Input',
                'Please type or paste Gujarati text first.')
            return

        self.status.config(text='Translating...')
        try:
            result = translator.translate(gujarati,
                                          src='gu',
                                          dest='en')
            self.show_translation(result.text)
            self.status.config(text='Translation complete!')

        except Exception as e:
            messagebox.showerror('Translation Error',
                f'Could not translate.\nError: {str(e)}')
            self.status.config(text='Translation failed.')

    # ── Upload image and extract + translate ──────────────────────
    def upload_image(self):
        path = filedialog.askopenfilename(
            filetypes=[('Image files',
                        '*.png *.jpg *.jpeg *.bmp *.tiff')])
        if not path:
            return

        self.status.config(text='Reading image...')

        try:
            # Show image preview
            img = Image.open(path)
            img_preview = img.copy()
            img_preview.thumbnail((800, 150))
            self.tk_img = ImageTk.PhotoImage(img_preview)
            self.image_label.config(image=self.tk_img,
                                    text='', width=0, height=0)

            # Extract Gujarati text using OCR
            self.status.config(text='Extracting text from image...')
            extracted = pytesseract.image_to_string(
                img, lang='guj')

            if not extracted.strip():
                messagebox.showwarning('No Text Found',
                    'Could not extract any text from this image.\n'
                    'Make sure the image has clear Gujarati text.')
                self.status.config(text='No text found in image.')
                return

            # Show extracted Gujarati in left box
            self.gujarati_text.delete('1.0', 'end')
            self.gujarati_text.insert('1.0', extracted.strip())

            # Translate it
            self.status.config(text='Translating extracted text...')
            result = translator.translate(extracted.strip(),
                                          src='gu', dest='en')
            self.show_translation(result.text)
            self.status.config(
                text='Image text extracted and translated!')

        except Exception as e:
            messagebox.showerror('Error', str(e))
            self.status.config(text='Error occurred.')

    # ── Show translation in right box ─────────────────────────────
    def show_translation(self, text):
        self.english_text.config(state='normal')
        self.english_text.delete('1.0', 'end')
        self.english_text.insert('1.0', text)
        self.english_text.config(state='disabled')

    # ── Save translation to file ──────────────────────────────────
    def save_translation(self):
        gujarati = self.gujarati_text.get('1.0', 'end').strip()
        english = self.english_text.get('1.0', 'end').strip()

        if not english:
            messagebox.showwarning('Nothing to Save',
                'Please translate something first.')
            return

        path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('Text files', '*.txt')])

        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write('GUJARATI:\n')
                f.write(gujarati)
                f.write('\n\nENGLISH TRANSLATION:\n')
                f.write(english)
            messagebox.showinfo('Saved',
                'Translation saved successfully!')
            self.status.config(text=f'Saved to {path}')

    # ── Clear everything ──────────────────────────────────────────
    def clear_all(self):
        self.gujarati_text.delete('1.0', 'end')
        self.english_text.config(state='normal')
        self.english_text.delete('1.0', 'end')
        self.english_text.config(state='disabled')
        self.image_label.config(image='',
                                text='No image uploaded',
                                width=80, height=8)
        self.status.config(text='Cleared.')

# ── Run ───────────────────────────────────────────────────────────
root = tk.Tk()
app = GujaratiTranslator(root)
root.mainloop()
