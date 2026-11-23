import io
import base64
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Bắt buộc để Matplotlib chạy nền trên Django không bị lỗi giao diện
import matplotlib.pyplot as plt
from store.models import Orders, OrderDetails

def _fig_to_base64(fig):
    """Chuyển biểu đồ Matplotlib thành chuỗi ảnh base64 để hiển thị lên HTML."""
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)
    return base64.b64encode(image_png).decode('utf-8')

def get_revenue_chart():
    """Biểu đồ 1: Doanh thu theo ngày (Dùng Pandas + NumPy + Matplotlib)."""
    orders = Orders.objects.exclude(status='cancelled').values('created_at', 'total_price')
    if not orders:
        return None

    # 1. Đưa dữ liệu từ MySQL vào Pandas DataFrame
    df = pd.DataFrame(list(orders))
    df['date'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y')
    df['total_price'] = df['total_price'].astype(float)

    # 2. Gom nhóm theo ngày bằng Pandas & tính tổng bằng NumPy
    daily_rev = df.groupby('date')['total_price'].apply(np.sum)
    avg_rev = np.mean(daily_rev.values)  # Tính doanh thu trung bình bằng NumPy

    # 3. Vẽ biểu đồ cột kết hợp đường trung bình bằng Matplotlib
    fig, ax = plt.subplots(figsize=(7, 3.2))
    bars = ax.bar(daily_rev.index, daily_rev.values / 1_000_000, color='#2563eb', width=0.45, alpha=0.85, label='Doanh thu (Triệu VNĐ)')
    ax.axhline(avg_rev / 1_000_000, color='#f59e0b', linestyle='--', linewidth=1.5, label=f'Trung bình: {avg_rev/1_000_000:.1f}tr')

    ax.set_ylabel('Triệu VNĐ', fontsize=9)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(fontsize=8)

    return _fig_to_base64(fig)

def get_category_chart():
    """Biểu đồ 2: Tỷ trọng doanh thu theo danh mục (Biểu đồ tròn Donut)."""
    details = OrderDetails.objects.exclude(order__status='cancelled').values(
        'product__category__name', 'quantity', 'unit_price'
    )
    if not details:
        return None

    # 1. Đưa vào Pandas DataFrame và tính thành tiền
    df = pd.DataFrame(list(details))
    df['revenue'] = df['quantity'].astype(float) * df['unit_price'].astype(float)
    cat_rev = df.groupby('product__category__name')['revenue'].sum()

    # 2. Vẽ biểu đồ tròn dạng Donut giống giao diện mẫu
    fig, ax = plt.subplots(figsize=(4.2, 3.2))
    colors = ['#2563eb', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444']
    wedges, texts, autotexts = ax.pie(
        cat_rev.values,
        labels=cat_rev.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors[:len(cat_rev)],
        wedgeprops=dict(width=0.42, edgecolor='white')  # Tạo lỗ tròn ở giữa (Donut)
    )
    plt.setp(autotexts, size=8, weight='bold', color='white')
    plt.setp(texts, size=9)

    return _fig_to_base64(fig)