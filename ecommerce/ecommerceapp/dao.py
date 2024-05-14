from django.db.models import Sum, F

from ecommerceapp.models import OrderDetail

def stat_products(type, value):
    filter_kwargs = {}
    # Thiết lập bộ lọc tùy thuộc vào kiểu (tháng, quý hoặc năm)
    if type == 'month':
        filter_kwargs['created_date__month'] = value
    elif type == 'quarter':
        # Tính toán quý từ tháng
        quarter = (value - 1) // 3 + 1
        filter_kwargs['created_date__quarter'] = quarter
    elif type == 'year':
        filter_kwargs['created_date__year'] = value

    # Tạo queryset để lấy tổng số lượng sản phẩm đã bán
    queryset = OrderDetail.objects.filter(**filter_kwargs).annotate(
        total_quantity=Sum('quantity')
    ).values(name=F('product__name'), count=F('total_quantity')).order_by('product__name')

    # Trả về danh sách các sản phẩm và số lượng đã bán
    return queryset