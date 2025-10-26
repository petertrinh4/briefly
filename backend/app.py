from flask import Flask, redirect, request, session, url_for, jsonify
from google_auth_oauthlib.flow import flow # Google OAuth sys.
from agents.gmail.gmail_send import gmail_send
import os

app = Flask(__name__)