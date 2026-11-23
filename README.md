# Tech Store Manager (ElectroAdmin)

Hệ thống quản trị cửa hàng thiết bị điện tử xây dựng bằng **Django**, kết hợp cơ sở dữ liệu **MySQL**, phân tích dữ liệu với **Pandas / NumPy / Matplotlib**, giao diện **Bootstrap 5** và gửi email thông báo đơn hàng qua **Gmail SMTP**.

## Tính năng chính

- **Tổng quan (Dashboard)** (`/dashboard/`):
  - Hiển thị 4 thẻ thống kê KPI: Tổng sản phẩm, Tổng đơn hàng, Doanh thu (tính trên các đơn `completed`), Khách hàng.
  - Trực quan hóa **Doanh thu theo ngày** (biểu đồ cột kèm đường doanh thu trung bình) và **Tỷ trọng doanh thu theo danh mục** (biểu đồ Donut).
- **Quản lý sản phẩm** (`/dashboard/products/`, `/dashboard/product/add/`, `/dashboard/product/edit/<id>/`, `/dashboard/product/delete/<id>/`):
  - Tìm kiếm sản phẩm theo tên.
  - Thêm, chỉnh sửa, xóa sản phẩm, quản lý giá nhập, giá bán, tồn kho và tải ảnh sản phẩm lên thư mục `media/products/`.
- **Quản lý đơn hàng & Gửi Email SMTP** (`/dashboard/orders/`, `/dashboard/orders/update/<id>/`):
  - Theo dõi danh sách đơn hàng và cập nhật trạng thái (`pending`, `shipping`, `completed`, `cancelled`).
  - Tự động gửi email thông báo trạng thái đơn hàng tới khách hàng qua giao thức SMTP SSL (`smtp.gmail.com:465`).
- **Quản lý khách hàng** (`/dashboard/customers/`):
  - Xem danh sách tài khoản người dùng từ bảng `users`.
- **Báo cáo & Xuất CSV** (`/dashboard/reports/`, `/dashboard/reports/export-csv/`):
  - Thống kê giá trị đơn hàng trung bình, lớn nhất, nhỏ nhất bằng **Pandas**.
  - Hiển thị biểu đồ doanh thu, danh mục và xuất danh sách đơn hàng ra tệp `bao_cao_don_hang.csv`.
- **Cài đặt & Django Admin** (`/dashboard/settings/`, `/admin/`):
  - Xem thông tin cấu hình SMTP / MySQL và truy cập trang quản trị Django mặc định.

## Công nghệ sử dụng

- **Backend**: Python 3.13, Django
- **Database**: MySQL (`electronics_store`), kết nối qua `PyMySQL`
- **Phân tích & Biểu đồ**: `pandas`, `numpy`, `matplotlib`, `pillow`
- **Frontend**: HTML5, Bootstrap 5.3.2, Bootstrap Icons 1.11.1
- **Email**: Python `smtplib` (SMTP SSL cổng 465)

## Cấu trúc thư mục

```text
electronics_project/
├── config/                     # Cấu hình Django (settings, urls, wsgi, asgi, PyMySQL)
├── dashboard/                  # Ứng dụng quản trị cửa hàng
│   ├── templates/dashboard/    # Giao diện HTML (base, index, products, orders, customers, reports, settings)
│   ├── urls.py                 # Định tuyến các trang trong dashboard
│   ├── views.py                # Xử lý nghiệp vụ CRUD, báo cáo, xuất CSV và gọi gửi email
│   ├── utils_charts.py         # Tạo biểu đồ Matplotlib dạng base64 từ dữ liệu Pandas/NumPy
│   └── utils_email.py          # Hàm gửi email cập nhật trạng thái đơn hàng qua Gmail SMTP
├── store/                      # Ứng dụng chứa models ánh xạ CSDL MySQL
│   └── models.py               # Categories, Products, Users, Orders, OrderDetails (managed = False)
├── manage.py                   # Công cụ dòng lệnh quản trị Django
├── .gitignore                  # Danh sách tệp/thư mục bỏ qua khi dùng Git
└── README.md                   # Tài liệu mô tả dự án
```

## Cơ sở dữ liệu

Dự án cấu hình kết nối MySQL tới database `electronics_store` trong `config/settings.py`. Các model trong `store/models.py` sử dụng `managed = False` để ánh xạ với các bảng đã có trong MySQL:

- `categories` (`Categories`)
- `products` (`Products`)
- `users` (`Users`)
- `orders` (`Orders`)
- `order_details` (`OrderDetails`)

## Hướng dẫn cài đặt và chạy dự án

1. **Tạo và kích hoạt môi trường ảo**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Cài đặt các thư viện phụ thuộc**:
   ```powershell
   pip install django pymysql pandas numpy matplotlib pillow
   ```

3. **Cấu hình cơ sở dữ liệu MySQL**:
   - Khởi động MySQL (ví dụ qua XAMPP/Laragon hoặc MySQL Server) và tạo database `electronics_store` cùng các bảng tương ứng.
   - Kiểm tra thông số kết nối (`NAME`, `USER`, `PASSWORD`, `HOST`, `PORT`) trong `config/settings.py`.

4. **Cấu hình gửi Email SMTP (tùy chọn)**:
   - Mở `dashboard/utils_email.py` và điền `SENDER_EMAIL` cùng `SENDER_PASSWORD` (Gmail App Password 16 ký tự) nếu muốn gửi email thật.

5. **Chạy server phát triển**:
   ```powershell
   python manage.py runserver
   ```
   Sau đó truy cập `http://127.0.0.1:8000/dashboard/` trên trình duyệt.
