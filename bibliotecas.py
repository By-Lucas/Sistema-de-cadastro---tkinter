#SISTEMA DE LOJA
from tkinter import *
from tkinter import ttk, messagebox
import os
import time
import datetime

#biblioteca para salver relatorio em pdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

#Mysql Cloud Cloutes
from psycopg2 import connect
import mysql.connector
from mysql.connector import errorcode

