import streamlit as st
import sqlite3
import hashlib

# Kết nối với cơ sở dữ liệu
def get_db_connection():
    conn = sqlite3.connect('users.db')
    return conn

# Hàm băm mật khẩu
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Hàm đăng ký người dùng
def register_user(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Hàm kiểm tra đăng nhập
def login_user(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
              (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user is not None

# Hàm quản lý tài khoản
def manage_account(username):
    st.subheader('Quản lý Tài khoản')
    new_password = st.text_input('Nhập mật khẩu mới:', type='password')
    
    if st.button('Cập nhật mật khẩu'):
        if new_password:
            update_password(username, new_password)
            st.success('Mật khẩu đã được cập nhật.')
        else:
            st.error('Vui lòng nhập mật khẩu mới.')

# Hàm cập nhật mật khẩu
def update_password(username, new_password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE username = ?", 
              (hash_password(new_password), username))
    conn.commit()
    conn.close()

# Hàm đăng ký lịch khám
def register_appointment():
    st.subheader('Đăng ký Lịch Khám')
    appointment_date = st.date_input('Chọn ngày khám:')
    appointment_time = st.time_input('Chọn giờ khám:')
    reason = st.text_area('Lý do khám:')
    
    if st.button('Đăng ký lịch khám'):
        if appointment_date and appointment_time and reason:
            st.success(f'Lịch khám đã được đăng ký vào {appointment_date} lúc {appointment_time}.')
        else:
            st.error('Vui lòng điền đầy đủ thông tin.')

# Tiêu đề ứng dụng
st.set_page_config(page_title='Lịch Khám Sức Khỏe', layout='wide')
st.title('🏥 Ứng dụng Cá nhân hóa Lịch Khám Sức Khỏe')
st.write("Chào mừng bạn đến với ứng dụng của chúng tôi! Hãy đăng ký hoặc đăng nhập để bắt đầu.")

# Khởi tạo session state cho tên người dùng và mật khẩu
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'password' not in st.session_state:
    st.session_state.password = ''
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Tạo menu chọn chức năng ở thanh bên trái
menu_option = st.sidebar.selectbox('Chọn chức năng:', ['Đăng ký', 'Đăng nhập', 'Quản lý tài khoản', 'Đăng ký Lịch Khám'])

# Cải thiện giao diện cho phần đăng ký
if menu_option == 'Đăng ký':
    st.subheader('Đăng ký Tài khoản')
    st.session_state.username = st.text_input('Tên người dùng:', value=st.session_state.username)
    st.session_state.password = st.text_input('Mật khẩu:', type='password', value=st.session_state.password)

    # Kiểm tra điều kiện trước khi đăng ký
    if st.button('Đăng ký', key='register'):
        if st.session_state.username and st.session_state.password:
            if register_user(st.session_state.username, st.session_state.password):
                st.success('Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.')
                # Reset các giá trị sau khi đăng ký
                st.session_state.username = ''
                st.session_state.password = ''
            else:
                st.error('Tên người dùng đã tồn tại. Vui lòng chọn tên khác.')
        else:
            st.error('Vui lòng nhập cả tên người dùng và mật khẩu.')

# Cải thiện giao diện cho phần đăng nhập
elif menu_option == 'Đăng nhập':
    st.subheader('Đăng nhập vào Tài khoản')
    st.session_state.username = st.text_input('Tên người dùng:', value=st.session_state.username)
    st.session_state.password = st.text_input('Mật khẩu:', type='password', value=st.session_state.password)

    if st.button('Đăng nhập', key='login'):
        if login_user(st.session_state.username, st.session_state.password):
            st.success('Đăng nhập thành công! Chào mừng bạn!')
            st.session_state.logged_in = True
            # Reset các giá trị sau khi đăng nhập
            st.session_state.username = ''
            st.session_state.password = ''
            # Chuyển đến trang đăng ký lịch khám
            st.experimental_rerun()  # Tải lại trang để chuyển đến trang đăng ký lịch khám
        else:
            st.error('Tên người dùng hoặc mật khẩu không đúng. Vui lòng thử lại.')

# Quản lý tài khoản
elif menu_option == 'Quản lý tài khoản' and st.session_state.logged_in:
    manage_account(st.session_state.username)

# Đăng ký lịch khám
elif menu_option == 'Đăng ký Lịch Khám' and st.session_state.logged_in:
    register_appointment()

# Thêm một số hướng dẫn
st.markdown("""
### Hướng dẫn sử dụng:
- Để đăng ký, hãy điền tên người dùng và mật khẩu của bạn.
- Để đăng nhập, sử dụng tên người dùng và mật khẩu bạn đã đăng ký.
- Sau khi đăng nhập, bạn có thể đăng ký lịch khám của mình.
""")