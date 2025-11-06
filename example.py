"""
Example: Ví dụ tính toán hạn mức theo tài liệu
Minh họa Ví dụ 1 và 1A từ tài liệu
"""

from decimal import Decimal
from limit_calculator import (
    LimitCalculator,
    LimitInfo,
    CollateralInfo,
    print_limit_result,
    format_currency
)


def example_1_hierarchical_with_shared_collateral():
    """
    Ví dụ 1: Hạn mức phân cấp với CCR khác nhau và TSĐB liên thông
    
    Dữ liệu:
    - Hạn mức tổng: 100 tỷ
    - TSĐB: 80 tỷ (chia sẻ cho tất cả hạn mức con)
    - Tỷ lệ tín chấp: 20%
    - Max Unsecured: 30 tỷ
    
    Hạn mức con:
    - Vay vốn lưu động: 60 tỷ, CCR 100%, Dư nợ: 40 tỷ
    - Bảo lãnh: 30 tỷ, CCR 50%, Dư nợ: 20 tỷ
    - L/C trả ngay: 20 tỷ, CCR 20%, Dư nợ: 10 tỷ
    """
    print("\n" + "="*70)
    print("VÍ DỤ 1: HẠN MỨC PHÂN CẤP VỚI CCR VÀ TSĐB LIÊN THÔNG")
    print("="*70 + "\n")
    
    # Thiết lập thông tin TSĐB và tín chấp
    collateral_info = CollateralInfo(
        total_collateral=Decimal('80000000000'),  # 80 tỷ
        unsecured_ratio=Decimal('0.20'),  # 20%
        max_unsecured=Decimal('30000000000')  # 30 tỷ
    )
    
    # Khởi tạo calculator
    calculator = LimitCalculator(collateral_info)
    
    # Hạn mức tổng
    master_limit = LimitInfo(
        limit_id='MASTER_001',
        limit_name='Hạn mức tổng',
        approved_limit=Decimal('100000000000'),  # 100 tỷ
        outstanding_amount=Decimal('0'),  # Không tính trực tiếp
        ccr=Decimal('1.0')
    )
    
    # Các hạn mức con
    child_limits = [
        LimitInfo(
            limit_id='LOAN_001',
            limit_name='Vay vốn lưu động',
            approved_limit=Decimal('60000000000'),  # 60 tỷ
            outstanding_amount=Decimal('40000000000'),  # 40 tỷ
            ccr=Decimal('1.0'),  # 100%
            parent_limit_id='MASTER_001'
        ),
        LimitInfo(
            limit_id='GUARANTEE_001',
            limit_name='Bảo lãnh',
            approved_limit=Decimal('30000000000'),  # 30 tỷ
            outstanding_amount=Decimal('20000000000'),  # 20 tỷ
            ccr=Decimal('0.5'),  # 50%
            parent_limit_id='MASTER_001'
        ),
        LimitInfo(
            limit_id='LC_001',
            limit_name='L/C trả ngay',
            approved_limit=Decimal('20000000000'),  # 20 tỷ
            outstanding_amount=Decimal('10000000000'),  # 10 tỷ
            ccr=Decimal('0.2'),  # 20%
            parent_limit_id='MASTER_001'
        )
    ]
    
    # Tính toán với phương pháp phân bổ TSĐB theo CCR
    master_result, child_results = calculator.calculate_hierarchical_limits(
        master_limit=master_limit,
        child_limits=child_limits,
        allocation_method='ccr'
    )
    
    # In kết quả
    print("PHÂN BỔ TSĐB THEO TỶ LỆ CCR (Pari-passu)\n")
    
    # In kết quả hạn mức tổng
    print_limit_result(master_result)
    
    # In phân bổ TSĐB
    print("PHÂN BỔ TSĐB CHO CÁC HẠN MỨC CON:")
    print("-" * 70)
    total_weighted = Decimal('0')
    for result in child_results:
        weighted = result.outstanding_nominal * result.ccr
        total_weighted += weighted
        print(f"{result.limit_name:20} - Dư nợ quy đổi: {format_currency(weighted)}")
    
    print(f"{'Tổng dư nợ quy đổi':20} - {format_currency(total_weighted)}")
    print()
    
    for result in child_results:
        ratio = (result.outstanding_nominal * result.ccr) / total_weighted * 100
        print(f"{result.limit_name:20} - TSĐB phân bổ: {format_currency(result.collateral_allocated)} ({ratio:.2f}%)")
    print("-" * 70)
    print()
    
    # In kết quả các hạn mức con
    for result in child_results:
        print_limit_result(result, indent=2)
    
    return master_result, child_results


def example_1a_impact_of_additional_loan():
    """
    Ví dụ 1A: Tác động khi vay thêm
    
    Tiếp tục từ Ví dụ 1, giả sử khách hàng vay thêm 15 tỷ
    """
    print("\n" + "="*70)
    print("VÍ DỤ 1A: TÁC ĐỘNG CỦA TSĐB LIÊN THÔNG KHI VAY THÊM")
    print("="*70 + "\n")
    
    print("TÌNH HUỐNG: Khách hàng vay thêm 15 tỷ VNĐ")
    print("Dư nợ vay mới: 40 + 15 = 55 tỷ\n")
    
    # Thiết lập giống Ví dụ 1
    collateral_info = CollateralInfo(
        total_collateral=Decimal('80000000000'),
        unsecured_ratio=Decimal('0.20'),
        max_unsecured=Decimal('30000000000')
    )
    
    calculator = LimitCalculator(collateral_info)
    
    master_limit = LimitInfo(
        limit_id='MASTER_001',
        limit_name='Hạn mức tổng',
        approved_limit=Decimal('100000000000'),
        outstanding_amount=Decimal('0'),
        ccr=Decimal('1.0')
    )
    
    # Các hạn mức con - Dư nợ vay tăng lên
    child_limits = [
        LimitInfo(
            limit_id='LOAN_001',
            limit_name='Vay vốn lưu động',
            approved_limit=Decimal('60000000000'),
            outstanding_amount=Decimal('55000000000'),  # 55 tỷ (tăng 15 tỷ)
            ccr=Decimal('1.0'),
            parent_limit_id='MASTER_001'
        ),
        LimitInfo(
            limit_id='GUARANTEE_001',
            limit_name='Bảo lãnh',
            approved_limit=Decimal('30000000000'),
            outstanding_amount=Decimal('20000000000'),  # Không đổi
            ccr=Decimal('0.5'),
            parent_limit_id='MASTER_001'
        ),
        LimitInfo(
            limit_id='LC_001',
            limit_name='L/C trả ngay',
            approved_limit=Decimal('20000000000'),
            outstanding_amount=Decimal('10000000000'),  # Không đổi
            ccr=Decimal('0.2'),
            parent_limit_id='MASTER_001'
        )
    ]
    
    # Tính toán
    master_result, child_results = calculator.calculate_hierarchical_limits(
        master_limit=master_limit,
        child_limits=child_limits,
        allocation_method='ccr'
    )
    
    # In kết quả
    print_limit_result(master_result)
    
    # So sánh phân bổ TSĐB
    print("SO SÁNH PHÂN BỔ TSĐB TRƯỚC VÀ SAU KHI VAY THÊM:")
    print("-" * 70)
    
    # TSĐB cũ (từ Ví dụ 1)
    old_allocation = {
        'Vay vốn lưu động': Decimal('61540000000'),  # 61.54 tỷ
        'Bảo lãnh': Decimal('15380000000'),  # 15.38 tỷ
        'L/C trả ngay': Decimal('3080000000')  # 3.08 tỷ
    }
    
    print(f"{'Hạn mức':20} | {'TSĐB cũ':>15} | {'TSĐB mới':>15} | {'Thay đổi':>15}")
    print("-" * 70)
    
    for result in child_results:
        old_val = old_allocation.get(result.limit_name, Decimal('0'))
        new_val = result.collateral_allocated
        change = new_val - old_val
        sign = '+' if change >= 0 else ''
        
        print(f"{result.limit_name:20} | {old_val/1e9:>13.2f} tỷ | {new_val/1e9:>13.2f} tỷ | {sign}{change/1e9:>13.2f} tỷ")
    
    print("-" * 70)
    print()
    
    # In chi tiết các hạn mức
    for result in child_results:
        print_limit_result(result, indent=2)
    
    # Phân tích tác động
    print("\nPHÂN TÍCH TÁC ĐỘNG:")
    print("-" * 70)
    print("✓ Hạn mức tổng khả dụng giảm từ 48 tỷ xuống 33 tỷ")
    print("✓ TSĐB phân bổ cho vay tăng → TSĐB cho BL/LC giảm")
    print("✓ Do BL/LC vẫn còn dư TSĐB nên chưa bị ảnh hưởng ngay")
    print("✓ Nếu tiếp tục vay thêm, BL/LC sẽ phải chuyển sang dùng tín chấp")
    print("-" * 70)
    

def example_simple_loan_limit():
    """
    Ví dụ đơn giản: Tính hạn mức vay không phân cấp
    """
    print("\n" + "="*70)
    print("VÍ DỤ ĐƠN GIẢN: HẠN MỨC VAY KHÔNG PHÂN CẤP")
    print("="*70 + "\n")
    
    # Thông tin TSĐB
    collateral_info = CollateralInfo(
        total_collateral=Decimal('50000000000'),  # 50 tỷ
        unsecured_ratio=Decimal('0.15'),  # 15%
        max_unsecured=Decimal('20000000000')  # 20 tỷ
    )
    
    calculator = LimitCalculator(collateral_info)
    
    # Hạn mức vay
    loan_limit = LimitInfo(
        limit_id='LOAN_001',
        limit_name='Hạn mức vay vốn lưu động',
        approved_limit=Decimal('80000000000'),  # 80 tỷ
        outstanding_amount=Decimal('30000000000'),  # 30 tỷ
        ccr=Decimal('1.0')  # 100%
    )
    
    # Tính toán
    result = calculator.calculate_single_limit(loan_limit)
    
    # In kết quả
    print_limit_result(result)


if __name__ == '__main__':
    # Chạy các ví dụ
    
    # Ví dụ đơn giản
    example_simple_loan_limit()
    
    # Ví dụ 1: Hạn mức phân cấp với TSĐB liên thông
    example_1_hierarchical_with_shared_collateral()
    
    # Ví dụ 1A: Tác động khi vay thêm
    example_1a_impact_of_additional_loan()
    
    print("\n" + "="*70)
    print("HOÀN THÀNH CÁC VÍ DỤ TÍNH TOÁN")
    print("="*70 + "\n")
