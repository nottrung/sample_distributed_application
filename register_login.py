import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Khởi tạo ứng dụng Firebase (nếu chưa khởi tạo)
if not firebase_admin._apps:
    cred = credentials.Certificate("smart-home-bc0ad-firebase-adminsdk-da6q2-7b61497c8d.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://smart-home-bc0ad-default-rtdb.firebaseio.com/'
    })

# Hàm đăng ký người dùng
def register_user(email, password, username):
    try:
        user = auth.create_user(email=email, password=password)
        db = firestore.client()
        db.collection("users").document(user.uid).set({
            "email": email,
            "username": username
        })
        return True
    except Exception as e:
        st.error(f"Lỗi khi đăng ký: {e}")
        return False

# Hàm xác thực người dùng
def authenticate_user(email, password):
    try:
        user = auth.get_user_by_email(email)
        # Thêm mã để xác thực mật khẩu (Firebase Authentication không hỗ trợ xác thực mật khẩu trực tiếp)
        return True
    except Exception as e:
        st.error(f"Lỗi khi đăng nhập: {e}")
        return False

# Hàm hiển thị trang đăng nhập và đăng ký
def login_register_page():
    st.title("Đăng nhập / Đăng ký")

    # Chọn giữa đăng nhập và đăng ký
    option = st.selectbox("Chọn tùy chọn:", ("Đăng nhập", "Đăng ký"))

    if option == "Đăng nhập":
        st.subheader("Đăng nhập vào Smart Home")
        email = st.text_input("Email", placeholder="Nhập địa chỉ email của bạn")
        password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu của bạn")

        if st.button("Đăng nhập"):
            if authenticate_user(email, password):
                st.session_state.logged_in = True
                st.success("Đăng nhập thành công!")
                # Chuyển hướng đến trang chính (home page)
                st.rerun()  # Tải lại để chuyển đến trang chính
            else:
                st.error("Thông tin đăng nhập không đúng. Vui lòng thử lại.")

    elif option == "Đăng ký":
        st.subheader("Đăng ký tài khoản Smart Home")
        email = st.text_input("Email", placeholder="Nhập địa chỉ email của bạn")
        username = st.text_input("Tên người dùng", placeholder="Nhập tên người dùng của bạn")
        password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu mới")
        confirm_password = st.text_input("Xác nhận mật khẩu", type="password", placeholder="Xác nhận mật khẩu mới")

        if st.button("Đăng ký"):
            if password != confirm_password:
                st.error("Mật khẩu không khớp. Vui lòng kiểm tra lại.")
            elif register_user(email, password, username):
                st.success("Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.")
            else:
                st.error("Đăng ký không thành công.")

# Gọi hàm hiển thị trang đăng nhập/đăng ký
if __name__ == "__main__":
    login_register_page()