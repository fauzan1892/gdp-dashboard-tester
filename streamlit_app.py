import mysql.connector
from mysql.connector import Error
import streamlit as st

def get_connection():
    """Membuat koneksi ke database MariaDB menggunakan mysql.connector."""
    try:
        # Membuat koneksi ke database
        conn = mysql.connector.connect(
            host=st.secrets["DB_HOST"],
            database=st.secrets["DB_DATABASE"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"]
        )
        if conn.is_connected():
            st.success("Berhasil terhubung ke database!")
        return conn
    except Error as e:
        st.error(f"Error saat menyambungkan ke database: {e}")
        st.write("Pastikan pengaturan koneksi Anda benar.")
        return None

def fetch_data(conn, table_name):
    """Mengambil data dari tabel tertentu dalam database."""
    try:
        # Membuat kursor untuk mengeksekusi query
        cursor = conn.cursor(dictionary=True)
        # Query untuk mengambil data dari tabel
        query = f"SELECT * FROM {table_name} LIMIT 10"
        cursor.execute(query)
        # Mengambil hasil query
        result = cursor.fetchall()
        return result
    except Error as e:
        st.error(f"Error saat mengambil data dari tabel {table_name}: {e}")
        return None
    finally:
        # Menutup kursor
        if cursor:
            cursor.close()

def main():
    st.title("Uji Koneksi Streamlit ke Database MariaDB")

    # Menguji koneksi ke database
    conn = get_connection()
    if conn:
        # Input untuk nama tabel
        table_name = 'databersih'
        if st.button("Tampilkan Data"):
            # Mengambil data dari tabel
            data = fetch_data(conn, table_name)
            if data:
                # Menampilkan data dalam bentuk DataFrame
                st.write(f"Data dari tabel {table_name}:")
                st.dataframe(data)
        # Menutup koneksi setelah selesai
        conn.close()
        st.success("Koneksi ke database ditutup.")
    else:
        st.error("Koneksi ke database gagal. Pastikan pengaturan koneksi Anda benar.")

if __name__ == "__main__":
    main()
