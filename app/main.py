import requests

import sqlite3

import telebot as telebot
from bs4 import BeautifulSoup
BOT_TOKEN = ""
bot = telebot.TeleBot(BOT_TOKEN)

def obtener_contenido(url):
    response = requests.get(url)
    return response.content


def scrap_y_guardar(url, db_path='productos.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT
        )
    ''')

    contenido = obtener_contenido(url)

    soup = BeautifulSoup(contenido, 'html.parser')

    productos = soup.find_all(class_='product_name')

    for producto in productos:
        nombre_producto = producto.get_text(strip=True)

        cursor.execute("SELECT id FROM productos WHERE nombre=?", (nombre_producto,))
        existe = cursor.fetchone()

        if not existe:
            cursor.execute("INSERT INTO productos (nombre) VALUES (?)", (nombre_producto,))
            conn.commit()

            print(f"Nuevo producto añadido: {nombre_producto}")
        else:
            print("Nada nuevo")
    conn.close()

def receiver_messages():
    bot.infinity_polling()

url_a_scrapear = 'https://trashoramadvd.bigcartel.com/'

scrap_y_guardar(url_a_scrapear)
