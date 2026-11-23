from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .utils_email import send_order_status_email, SENDER_EMAIL
# Create your views here.
from django.shortcuts import render
from django.db.models import Sum
from store.models import Products, Orders, Users
import pandas as pd

def dashboard_home(request):
    # Lấy dữ liệu cho 4 thẻ thống kê trên cùng
    total_products = Products.objects.count()
    total_orders = Orders.objects.count()
    total_revenue = Orders.objects.filter(status='completed').aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_customers = Users.objects.filter(role='customer').count()

    # Lấy danh sách sản phẩm cho bảng Quản lý sản phẩm
    products = Products.objects.select_related('category').all().order_by('-id')

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_customers': total_customers,
        'products': products,
    }
    return render(request, 'dashboard/index.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.core.files.storage import FileSystemStorage
from store.models import Products, Categories, Orders, Users

def dashboard_home(request):
    total_products = Products.objects.count()
    total_orders = Orders.objects.count()
    total_revenue = Orders.objects.filter(status='completed').aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_customers = Users.objects.filter(role='customer').count()
    products = Products.objects.select_related('category').all().order_by('-id')

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_customers': total_customers,
        'products': products,
        'chart_revenue': get_revenue_chart(),    
        'chart_category': get_category_chart(),
    }
    return render(request, 'dashboard/index.html', context)

# 1. Thêm sản phẩm
def product_add(request):
    categories = Categories.objects.all()
    if request.method == 'POST':
        image_path = None
        if request.FILES.get('image'):
            img_file = request.FILES['image']
            fs = FileSystemStorage(location='media/products/')
            filename = fs.save(img_file.name, img_file)
            image_path = f'products/{filename}'

        Products.objects.create(
            category_id=request.POST.get('category'),
            name=request.POST.get('name'),
            price=request.POST.get('price'),
            cost_price=request.POST.get('cost_price'),
            stock=request.POST.get('stock'),
            description=request.POST.get('description'),
            image=image_path
        )
        return redirect('dashboard_home')

    return render(request, 'dashboard/product_form.html', {
        'categories': categories,
        'title': 'Thêm sản phẩm mới'
    })

# 2. Sửa sản phẩm
def product_edit(request, pk):
    product = get_object_or_404(Products, pk=pk)
    categories = Categories.objects.all()
    if request.method == 'POST':
        product.category_id = request.POST.get('category')
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.cost_price = request.POST.get('cost_price')
        product.stock = request.POST.get('stock')
        product.description = request.POST.get('description')

        if request.FILES.get('image'):
            img_file = request.FILES['image']
            fs = FileSystemStorage(location='media/products/')
            filename = fs.save(img_file.name, img_file)
            product.image = f'products/{filename}'

        product.save()
        return redirect('dashboard_home')

    return render(request, 'dashboard/product_form.html', {
        'product': product,
        'categories': categories,
        'title': 'Chỉnh sửa sản phẩm'
    })

# 3. Xóa sản phẩm
def product_delete(request, pk):
    product = get_object_or_404(Products, pk=pk)
    product.delete()
    return redirect('dashboard_home')
from .utils_charts import get_revenue_chart, get_category_chart
# --- Mục: Sản phẩm ---
def product_list(request):
    q = request.GET.get('q', '')
    products = Products.objects.select_related('category').all().order_by('-id')
    if q:
        products = products.filter(name__icontains=q)
    return render(request, 'dashboard/products.html', {'products': products, 'q': q})

# --- Mục: Đơn hàng ---
def order_list(request):
    orders = Orders.objects.all().order_by('-created_at')
    return render(request, 'dashboard/orders.html', {'orders': orders})

def order_update_status(request, pk):
    order = get_object_or_404(Orders, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()

        # Gọi giao thức SMTP gửi email tự động cho khách
        ok, msg = send_order_status_email(
            order.customer_email, order.id, order.customer_name, new_status
        )
        if ok:
            messages.success(request, msg)
        else:
            messages.warning(request, msg)
    return redirect('order_list')

# --- Mục: Khách hàng ---
def customer_list(request):
    customers = Users.objects.all().order_by('-id')
    return render(request, 'dashboard/customers.html', {'customers': customers})

# --- Mục: Báo cáo & Xuất CSV (Pandas) ---
def report_view(request):
    orders = Orders.objects.all().values('id', 'customer_name', 'total_price', 'status', 'created_at')
    stats = {}
    if orders:
        df = pd.DataFrame(list(orders))
        df['total_price'] = df['total_price'].astype(float)
        stats = {
            'tong_don': len(df),
            'doanh_thu_tb': df['total_price'].mean(),
            'don_lon_nhat': df['total_price'].max(),
            'don_nho_nhat': df['total_price'].min(),
        }
    return render(request, 'dashboard/reports.html', {
        'chart_revenue': get_revenue_chart(),
        'chart_category': get_category_chart(),
        'stats': stats,
    })

def export_orders_csv(request):
    orders = Orders.objects.all().values(
        'id', 'customer_name', 'customer_email', 'customer_phone', 'total_price', 'status', 'created_at'
    )
    df = pd.DataFrame(list(orders))
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="bao_cao_don_hang.csv"'
    df.to_csv(response, index=False, encoding='utf-8-sig')
    return response

# --- Mục: Cài đặt ---
def settings_view(request):
    return render(request, 'dashboard/settings.html', {'sender_email': SENDER_EMAIL})