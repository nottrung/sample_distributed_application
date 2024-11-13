import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# Initialize Firebase app if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("smart-home-bc0ad-firebase-adminsdk-da6q2-7b61497c8d.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://smart-home-bc0ad-default-rtdb.firebaseio.com/'
    })

# Function to get door status and card list from Realtime Database
def get_door_status_and_cards():
    door_ref = db.reference('door')
    status = door_ref.child('status').get()
    cards = door_ref.child('cards').get() or []
    password = door_ref.child('password').get()
    return status, cards, password

# Function to update door status
def update_door_status(new_status):
    db.reference('door/status').set(new_status)

# Function to update password
def update_password(new_password):
    db.reference('door/password').set(new_password)

# Function to display the home page
def home_page():
    st.title("Trang Chủ Smart Home")

    # Retrieve door status and card list
    door_status, card_ids, current_password = get_door_status_and_cards()

    # Use session_state to track door status
    st.session_state.door_status = door_status

    # Display the door status
    if st.session_state.door_status:
        st.markdown("### 🚪 Trạng thái cửa: Mở")  # "Open" when true
        button_label = "Đóng cửa"  # Label for closing the door
    else:
        st.markdown("### 🚪 Trạng thái cửa: Đóng")  # "Close" when false
        button_label = "Mở cửa"  # Label for opening the door

    # Button to toggle the door status
    if st.button(button_label, key="toggle_door"):
        new_status = not st.session_state.door_status
        update_door_status(new_status)  # Update the status in Firebase
        st.session_state.door_status = new_status  # Update status in session_state
        st.success(f"Trạng thái cửa đã được cập nhật thành công: {'Mở' if new_status else 'Đóng'}.")

    # Password change section in an expander
    with st.expander("Đổi mật khẩu", expanded=False):
        old_password = st.text_input("Mật khẩu cũ", type="password", key="old_password")
        new_password = st.text_input("Mật khẩu mới", type="password", key="new_password")
        confirm_new_password = st.text_input("Xác nhận mật khẩu mới", type="password", key="confirm_new_password")

        if st.button("Cập nhật mật khẩu", key="update_password"):
            if old_password != current_password:
                st.error("Mật khẩu cũ không đúng.")
            elif new_password == old_password:
                st.error("Mật khẩu mới không được trùng với mật khẩu cũ.")
            elif new_password != confirm_new_password:
                st.error("Mật khẩu mới không khớp.")
            else:
                update_password(new_password)
                st.success("Mật khẩu đã được cập nhật thành công.")

    # Display list of card IDs
    st.subheader("Danh sách thẻ")
    if card_ids:
        for card in card_ids:
            st.write(f"- {card}")
    else:
        st.write("Không có thẻ nào được lưu trữ.")

# Function to refresh data from Firebase periodically
def refresh_data():
    while True:
        door_status, card_ids, current_password = get_door_status_and_cards()
        st.session_state.door_status = door_status  # Update door status in session state
        st.session_state.card_ids = card_ids  # Update card IDs in session state
        st.session_state.current_password = current_password  # Update current password
        time.sleep(5)  # Adjust the refresh interval as needed

# Call the function to display the home page
if __name__ == "__main__":
    home_page()
    refresh_data()  # Start the data refresh process