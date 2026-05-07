# ── Configuration file for Gujarati Translator ────────────────────

# Tesseract OCR engine path (Backend config)
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Translation settings (Backend config)
SOURCE_LANGUAGE = 'gu'   # Gujarati
TARGET_LANGUAGE = 'en'   # English

# OCR language
OCR_LANGUAGE = 'guj'     # Gujarati for Tesseract

# GUI settings (Frontend config)
WINDOW_SIZE = '900x700'
WINDOW_TITLE = 'Gujarati to English Translator'
CANVAS_BG = '#f5f5f5'

# Colors
BTN_TRANSLATE = '#4CAF50'   # Green
BTN_UPLOAD    = '#2196F3'   # Blue
BTN_CLEAR     = '#f44336'   # Red
BTN_SAVE      = '#FF9800'   # Orange

# Font
FONT_TITLE  = ('Arial', 20, 'bold')
FONT_NORMAL = ('Arial', 13)
FONT_BTN    = ('Arial', 12)

# File save settings
SAVE_ENCODING = 'utf-8'
SAVE_EXTENSION = '.txt'