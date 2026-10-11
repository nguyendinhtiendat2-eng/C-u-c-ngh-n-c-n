import streamlit as st
import random
import time

# --- CONFIG PAGE ---
st.set_page_config(
    page_title="Game Câu Cá May Mắn",
    page_icon="🎣",
    layout="centered"
)

# --- KHỞI TẠO STATE ---
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "money" not in st.session_state:
    st.session_state.money = 100
if "rod_level" not in st.session_state:
    st.session_state.rod_level = 1
if "inventory" not in st.session_state:
    st.session_state.inventory = {}
if "total_catches" not in st.session_state:
    st.session_state.total_catches = 0
if "logs" not in st.session_state:
    st.session_state.logs = []
if "last_catch" not in st.session_state:
    st.session_state.last_catch = {
        "name": "Chưa có cá nào", 
        "price": 0, 
        "rarity": "Bắt đầu", 
        "img": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300"
    }

# --- DỮ LIỆU CÁ ---
FISH_TYPES = [
    {
        "name": "Rác / Giày cũ", 
        "price": 0, 
        "rarity": "Rác", 
        "weight": 35, 
        "img": "https://images.unsplash.com/photo-1621451537084-482c73073a0f?w=300"
    },
    {
        "name": "Cá Chép", 
        "price": 20, 
        "rarity": "Phổ thông", 
        "weight": 35, 
        "img": "https://images.unsplash.com/photo-1522069169874-c58ec4b76be5?w=300"
    },
    {
        "name": "Cá Hồi", 
        "price": 50, 
        "rarity": "Hiếm", 
        "weight": 18, 
        "img": "https://images.unsplash.com/photo-1534567153574-2b12153a87f0?w=300"
    },
    {
        "name": "Cá Ngừ", 
        "price": 120, 
        "rarity": "Cực hiếm", 
        "weight": 9, 
        "img": "https://images.unsplash.com/photo-1509356843152-d0d466f22588?w=300"
    },
    {
        "name": "Cá Mập Vàng", 
        "price": 500, 
        "rarity": "Huyền thoại", 
        "weight": 3, 
        "img": "https://images.unsplash.com/photo-1560275619-4662e36fa65c?w=300"
    },
]

ROD_UPGRADES = {
    1: {"name": "Cần Trúc", "cost": 0, "luck_bonus": 0},
    2: {"name": "Cần Máy", "cost": 200, "luck_bonus": 5},
    3: {"name":
        
