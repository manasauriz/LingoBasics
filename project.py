import tkinter as tk

from googletrans import Translator
from googletrans import LANGUAGES

from PIL import Image, ImageTk

import os
import re
import random


DIR = "../project/assets"
ITEMS = {}
LANGS = {}


class Item:
    def __init__(self, language, category, image, text):
        """
        Initializes an Item object

        :param language: The language for translation
        :type language: str

        :param category: The category of item
        :type category: str

        :param image: The image to be displayed alongside the item
        :type image: ImageTk.PhotoImage

        :param text: The text to be displayed alongside the item
        :type text: str
        """
        self.lang = language
        self.cat = category
        self.img = image
        self.txt = text

    def set_word(self):
        """
        Sets a random word from the list of items in category, translate it, and the image and text accordingly
        """
        self.word = random.choice(ITEMS[self.cat])
        self.trans = translate_word(self.word, self.lang)
        self.img = get_img(f"{DIR}/{self.cat}/{self.word}.jpeg", (240, 360))
        self.txt = f"{self.word.capitalize()} translated in {self.lang.capitalize()}\nwas {self.trans}!"


def main():
    """
    Initializes global variables, and Tkinter window and starts the Tkinter main loop
    """
    global ITEMS, LANGS
    ITEMS = setup_items(DIR)
    LANGS = setup_langs()

    root = tk.Tk()
    root.geometry("1000x500")
    root.title("Lingo Basics")
    start_menu(root)
    root.mainloop()


def setup_items(directory):
    """
    Sets up items by reading files in the assets directory

    :return: A dictionary with category names as keys and lists of item names as values
    :rtype: dict
    """
    items = {}
    for file in os.listdir(directory):
        new_dir = os.path.join(directory, file)
        sub_items = []
        for item in os.listdir(new_dir):
            sub_items.append(re.search(r"^(.*).jpeg$", item).group(1))
        items[file] = sub_items
    return items


def setup_langs():
    """
    Sets up languages by filtering out unsupported language codes from googletrans

    :return: A dictionary with valid language codes as keys and corresponding languages as values
    :rtype: dict
    """
    langs = {}
    invalid_codes = [
        "am",
        "ar",
        "bn",
        "zh-cn",
        "zh-tw",
        "gu",
        "hi",
        "ja",
        "kn",
        "km",
        "ko",
        "ml",
        "mr",
        "my",
        "ne",
        "or",
        "pa",
        "si",
        "ta",
        "te",
        "th",
        "ur",
        "en",
    ]
    for code in LANGUAGES:
        if code not in invalid_codes:
            langs[code] = LANGUAGES[code]
    return langs


def start_menu(root):
    """
    Displays the start menu with the game logo and start button

    :param root: The root Tkinter window
    :type root: tk.Tk
    """
    window = tk.Frame(root, relief=tk.RIDGE, borderwidth=10)
    window.pack(fill=tk.BOTH, expand=True)

    window.rowconfigure([0, 1, 2], weight=1)
    window.columnconfigure(0, weight=1)

    img = get_img("logo.png", (640, 240))
    lbl_img = tk.Label(window, image=img)
    lbl_img.image = img
    lbl_img.grid(row=0, column=0, pady=20)

    label = tk.Label(window, text="A Language Learning Game", font=("Arial", 18))
    label.grid(row=1, column=0, pady=10)

    def click():
        """
        Moves to the language selection screen
        """
        window.destroy()
        language_select(root)

    button = tk.Button(
        window,
        text="Start",
        command=click,
        font=("Arial", 14),
        width=10,
        relief=tk.RAISED,
        borderwidth=5,
    )
    button.grid(row=2, column=0, pady=30)


def language_select(root):
    """
    Displays the language selection screen

    :param root: The root Tkinter window
    :type root: tk.Tk
    """
    window = tk.Frame(root, relief=tk.RIDGE, borderwidth=10)
    window.pack(fill=tk.BOTH, expand=True)

    window.rowconfigure([0, 1, 2], weight=1)
    window.columnconfigure(0, weight=1)

    lbl_txt = tk.Label(window, text="Choose a language", font=("Arial", 18))
    lbl_txt.grid(row=0, column=0, pady=10)

    frm_lang = tk.Frame(window)
    var = tk.StringVar()
    for i, ls in enumerate(formatted_list(list(LANGS.values()), 7)):
        frm_lang.rowconfigure(i, weight=1)
        for j, lang in enumerate(ls):
            frm_lang.columnconfigure(j, weight=1)
            rbtn = tk.Radiobutton(
                frm_lang,
                text=lang.capitalize(),
                variable=var,
                value=lang,
                activebackground="blue",
                activeforeground="white",
            )
            rbtn.grid(row=i, column=j, padx=2, pady=2)
    frm_lang.grid(row=1, column=0, pady=10)

    def click():
        """
        Selects the language and moves to the category selection screen
        """
        language = var.get()
        window.destroy()
        category_select(root, language)

    btn = tk.Button(
        window,
        text="Select",
        command=click,
        font=("Arial", 14),
        width=10,
        relief=tk.RAISED,
        borderwidth=5,
    )
    btn.grid(row=2, column=0, pady=30)


def category_select(root, language):
    """
    Displays the category selection screen

    :param root: The root Tkinter window
    :type root: tk.Tk

    :param language: The selected language
    :type language: str
    """
    window = tk.Frame(root, relief=tk.RIDGE, borderwidth=10)
    window.pack(fill=tk.BOTH, expand=True)

    window.rowconfigure([0, 1, 2, 3], weight=1)
    window.columnconfigure(0, weight=1)

    head = "Choose a category"
    lbl_txt = tk.Label(window, text=head, font=("Arial", 18))
    lbl_txt.grid(row=0, column=0, pady=10)

    t_head = translate_word(head, language)
    lbl_trans = tk.Label(window, text=t_head, font=("Arial", 14))
    lbl_trans.grid(row=1, column=0, pady=10)

    frm_cat = tk.Frame(window)
    var = tk.StringVar()
    for i, cat in enumerate(list(ITEMS.keys())):
        frm_cat.rowconfigure(i, weight=1)
        frm_cat.columnconfigure(i, weight=1)
        rbtn = tk.Radiobutton(
            frm_cat,
            text=cat.capitalize(),
            variable=var,
            value=cat,
            activebackground="blue",
            activeforeground="white",
            font=("Arial", 12),
        )
        rbtn.grid(row=i, column=0, padx=2, pady=2)
    frm_cat.grid(row=2, column=0, pady=10)

    def click():
        """
        Selects the category, creates an Item object and moves to the playable game screen
        """
        category = var.get()
        image = get_img("question.jpg", (240, 360))
        text = "Begin!"
        window.destroy()
        item = Item(language, category, image, text)
        play_game(root, item)

    btn = tk.Button(
        window,
        text="Select",
        command=click,
        font=("Arial", 14),
        width=10,
        relief=tk.RAISED,
        borderwidth=5,
    )
    btn.grid(row=3, column=0, pady=30)


def play_game(root, item):
    """
    Starts the game with selected item and displays the question

    :param root: The root Tkinter window
    :type root: tk.Tk

    :param item: The current game item
    :type item: Item
    """
    display = tk.Frame(root, relief=tk.RIDGE, borderwidth=10)
    display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    display.rowconfigure([0, 1], weight=1)
    display.columnconfigure(0, weight=1)

    lbl_txt = tk.Label(display, text=item.txt, font=("Arial", 18))
    lbl_txt.grid(row=0, column=0, pady=10)

    lbl_img = tk.Label(display, image=item.img, relief=tk.RIDGE, borderwidth=10)
    lbl_img.image = item.img
    lbl_img.grid(row=1, column=0, pady=30)

    window = tk.Frame(root, relief=tk.RIDGE, borderwidth=10)
    window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    item.set_word()

    window.rowconfigure([0, 1, 2], weight=1)
    window.columnconfigure(0, weight=1)

    que = f"'{item.trans}' in {item.lang.capitalize()}\nmeans what in English?"
    lbl_que = tk.Label(window, text=que, font=("Arial", 18))
    lbl_que.grid(row=0, column=0, pady=10)

    entry = tk.Entry(
        window, bg="yellow", font=("Arial", 14), relief=tk.SUNKEN, borderwidth=5
    )
    entry.grid(row=1, column=0, pady=10)

    def next():
        """
        Moves to the next game screen
        """
        display.destroy()
        window.destroy()
        play_game(root, item)

    def check():
        """
        Checks if the user answered correctly
        """
        answer = entry.get().strip().lower()
        if answer == item.word:
            next()
        else:
            lbl_que["text"] = f"{answer} is incorrect! Try Again\n{que}"

    def cat():
        """
        Moves to the category selection screen
        """
        display.destroy()
        window.destroy()
        category_select(root, item.lang)

    def lang():
        """
        Moves to the language selection screen
        """
        display.destroy()
        window.destroy()
        language_select(root)

    options = tk.Frame(window)
    options.grid(row=2, column=0, pady=10)

    options.rowconfigure([0, 1], weight=1)
    options.columnconfigure([0, 1], weight=1)

    btn_check = tk.Button(
        options,
        text="Check",
        command=check,
        font=("Arial", 14),
        width=10,
        relief=tk.RAISED,
        borderwidth=5,
    )
    btn_check.grid(row=0, column=0, pady=10)

    btn_skip = tk.Button(
        options,
        text="Reveal",
        command=next,
        font=("Arial", 14),
        width=10,
        relief=tk.RAISED,
        borderwidth=5,
    )
    btn_skip.grid(row=0, column=1, pady=10)

    btn_cat = tk.Button(
        options,
        text="Change\nCategory",
        command=cat,
        font=("Arial", 12),
        width=10,
        relief=tk.RAISED,
        borderwidth=5,
    )
    btn_cat.grid(row=1, column=0, pady=10)

    btn_lang = tk.Button(
        options,
        text="Change\nLanguage",
        command=lang,
        font=("Arial", 12),
        width=10,
        relief=tk.RAISED,
        borderwidth=5,
    )
    btn_lang.grid(row=1, column=1, pady=10)


def get_img(path, size):
    """
    Get image data resized to a specific size

    :param path: The path to the image file
    :type path: str

    :param size: The size to resize the image to (width, height)
    :type size: tuple

    :return: The resized image data
    :rtype: ImageTk.PhotoImage
    """
    with Image.open(path) as img:
        return ImageTk.PhotoImage(img.resize(size))


def formatted_list(ls, n):
    """
    Splits a list into a list of smaller lists of size n

    :param ls: The list to be formatted
    :type ls: list

    :param n: The number of items per sublist
    :type n: int

    :return: Formatted list of sublists
    :rtype: list
    """
    big_list = []
    q, r = divmod(len(ls), n)
    for i in range(q):
        small_list = []
        for j in range((n * i), (n * (i + 1))):
            small_list.append(ls[j])
        big_list.append(small_list)

    last_list = []
    for i in range((n * q), (n * q) + r):
        last_list.append(ls[i])

    if len(last_list) > 0:
        big_list.append(last_list)
    return big_list


def translate_word(word, language):
    """
    Translates word using googletrans library

    :param word: The english word to be translated
    :type word: str

    :param language: The language to be translated to
    :type language: str

    :return: The translated word from english to the language provided
    :rtype: str
    """
    translator = Translator()
    for item in LANGUAGES:
        if LANGUAGES[item] == language:
            lang_code = item
            return translator.translate(word, src="en", dest=lang_code).text


if __name__ == "__main__":
    main()
