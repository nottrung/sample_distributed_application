import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Khởi tạo ứng dụng Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("smart-home-bc0ad-firebase-adminsdk-da6q2-7b61497c8d.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Hàm đăng ký người dùng
def register_user(email, password, username):
    try:
        user = auth.create_user(email=email, password=password)
        db.collection("users").document(user.uid).set({
            "email": email,
            "username": username,
            "uid": user.uid
        })
        return True
    except Exception as e:
        st.error(f"Lỗi khi đăng ký: {e}")
        return False

# Hàm xác thực người dùng
def authenticate_user(email, password):
    try:
        user = auth.get_user_by_email(email)
        return True
    except Exception as e:
        st.error(f"Lỗi khi đăng nhập: {e}")
        return False

# CSS cho phong cách hiện đại
st.markdown("""
    <style>
    .main-container {
        background-color: #f5f5f5;
        padding: 2rem;
        border-radius: 8px;
    }
    .sidebar {
        width: 50%;
        float: left;
        text-align: center;
    }
    .form-container {
        width: 50%;
        float: right;
        background: #ffffff;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);
    }
    .smart-home {
        font-size: 1.8rem;
        color: #3366ff;
        font-weight: bold;
    }
    .button {
        color: #ffffff;
        background-color: #3366ff;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-align: center;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Giao diện Smart Home
st.markdown('<div class="smart-home">Ứng dụng Smart Home</div>', unsafe_allow_html=True)
st.subheader("Đăng ký / Đăng nhập")

# Sử dụng `st.columns` để tạo 2 nút trên cùng một hàng
col1, col2 = st.columns(2)

# Biến để xác định xem phần nào hiển thị (Đăng nhập hoặc Đăng ký)
login_button = True
register_button = False

with col1:
    if st.button("Đăng nhập"):
        login_button = True
        register_button = False

with col2:
    if st.button("Đăng ký"):
        login_button = False
        register_button = True

# Form Đăng nhập và Đăng ký
if login_button:
    st.write("### Đăng nhập vào Smart Home")
    email = st.text_input("Email")
    password = st.text_input("Mật khẩu", type="password")

    if st.button("Đăng nhập", key="login"):
        if authenticate_user(email, password):
            st.success(f"Xin chào {email}, bạn đã đăng nhập thành công!")
        else:
            st.error("Thông tin đăng nhập không đúng. Vui lòng thử lại.")

elif register_button:
    st.write("### Đăng ký tài khoản Smart Home")
    email = st.text_input("Email")
    username = st.text_input("Tên người dùng")
    password = st.text_input("Mật khẩu", type="password")
    confirm_password = st.text_input("Xác nhận mật khẩu", type="password")

    if st.button("Đăng ký", key="register"):
        if password != confirm_password:
            st.error("Mật khẩu không khớp. Vui lòng kiểm tra lại.")
        elif register_user(email, password, username):
            st.success("Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.")
        else:
            st.error("Đăng ký không thành công.")