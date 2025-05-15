# Hàm kiểm tra số nhị phân có chia hết cho 5 không
def chia_het_cho_5(so_nhi_phan):
    # Chuyển số nhị phân thành số thập phân
    so_thap_phan = int(so_nhi_phan, 2)
    # Kiểm tra xem số thập phân % 5 có bằng 0 không
    if so_thap_phan % 5 == 0:
        return True
    else:
        return False

# Tách chuỗi từ người dùng
so_nhi_phan = input("Nhập chuỗi số nhị phân (phân tách bởi dấu phẩy): ")
so_nhi_phan_list = so_nhi_phan.split(',')
ket_qua = [so for so in so_nhi_phan_list if chia_het_cho_5(so)]
print("Các số nhị phân nào chia hết cho 5 là:", ket_qua)
print("Không có số nhị phân nào chia hết cho 5 trong chuỗi đã nhập.")