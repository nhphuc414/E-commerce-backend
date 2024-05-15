# E-commerce-backend

### Bước 1: Cài đặt môi trường

- **Cài đặt MySQL Community Server:** tải và cài đặt MySQL Community Server [tại đây](https://dev.mysql.com/downloads/mysql/).
- - **Cài đặt MySQL Workbench:** tải và cài đặt MySQL Workbench [tại đây](https://dev.mysql.com/downloads/workbench/).
- **Cài đặt Pycharm:** tải và cài đặt Pycharm [tại đây](https://www.jetbrains.com/pycharm/download/).

### Bước 2: Lấy mã nguồn

Mở command line hoặc git bash và gõ lệnh sau để tải mã nguồn về máy tính.

```bash
git clone https://github.com/nhphuc414/E-commerce-backend.git
```

### Bước 3: Tạo Database

Mở **MySQL Workbench**,chọn connection &#8594; New Schema &#8594;

### Bước 4: Cấu hình

Vào file

```bash
E-commerce-backend\ecommerce\ecommerce\setting.py
```

Chỉnh các thông số sau

```properties
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'Tên Schema',
       'USER': 'tên Username Mysql',
       'PASSWORD': 'Mật khẩu Mysql',
       'HOST': ''  # mặc định localhost
   }
}
```

### Bước 5: Tạo môi trường ảo

Mở project bằng pycharm &#8594; File &#8594; Settings &#8594; Project &#8594; Python Interpreter &#8594; add Interpreter

### Bước 5: Khởi chạy

bật Terminal ở pycharm và gõ

```properties
pip install -r requirements.txt
```

```properties
python manage.py makemigrations ecommerceapp
```

```properties
python manage.py migrate
```

```properties
python manage.py createsuperuser
```

```properties
python manage.py runserver
```
