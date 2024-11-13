import streamlit as st
from register_login import login_register_page
from home import home_page

# Kiểm tra trạng thái đăng nhập
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Hiển thị trang chủ hoặc trang đăng nhập/đăng ký
if st.session_state.logged_in:
    home_page()  # Hiển thị trang chủ nếu đã đăng nhập
else:
    # Chỉ hiển thị giao diện đăng nhập/đăng ký nếu chưa đăng nhập
    login_register_page()