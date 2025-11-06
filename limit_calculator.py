"""
Limit Calculator - Tính toán hạn mức khả dụng
Hỗ trợ cấu trúc phân cấp, CCR, và TSĐB liên thông
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class LimitInfo:
    """Thông tin hạn mức"""
    limit_id: str
    limit_name: str
    approved_limit: Decimal  # Hạn mức được cấp
    outstanding_amount: Decimal  # Dư nợ hiện tại
    ccr: Decimal  # Credit Conversion Rate (0-1)
    parent_limit_id: Optional[str] = None
    
    
@dataclass
class CollateralInfo:
    """Thông tin tài sản đảm bảo"""
    total_collateral: Decimal  # Tổng TSĐB
    unsecured_ratio: Decimal  # Tỷ lệ tín chấp (0-1)
    max_unsecured: Decimal  # Hạn mức tín chấp tối đa


@dataclass
class LimitResult:
    """Kết quả tính toán hạn mức"""
    limit_id: str
    limit_name: str
    approved_limit: Decimal
    outstanding_nominal: Decimal  # Dư nợ danh nghĩa
    outstanding_weighted: Decimal  # Dư nợ quy đổi (theo CCR)
    ccr: Decimal
    collateral_allocated: Decimal  # TSĐB được phân bổ
    collateral_available: Decimal  # TSĐB khả dụng
    unsecured_limit: Decimal  # Hạn mức tín chấp
    available_limit_weighted: Decimal  # Hạn mức khả dụng (quy đổi)
    available_limit_nominal: Decimal  # Hạn mức khả dụng (danh nghĩa)
    utilization_ratio: Decimal  # Tỷ lệ sử dụng (%)


class LimitCalculator:
    """Class tính toán hạn mức khả dụng"""
    
    def __init__(self, collateral_info: CollateralInfo):
        """
        Khởi tạo calculator
        
        Args:
            collateral_info: Thông tin TSĐB và tín chấp
        """
        self.collateral_info = collateral_info
        
    def calculate_unsecured_limit(self, approved_limit: Decimal) -> Decimal:
        """
        Tính hạn mức tín chấp
        
        Args:
            approved_limit: Hạn mức được cấp
            
        Returns:
            Hạn mức tín chấp
        """
        return min(
            approved_limit * self.collateral_info.unsecured_ratio,
            self.collateral_info.max_unsecured
        )
    
    def allocate_collateral_by_ccr(
        self, 
        limits: List[LimitInfo]
    ) -> Dict[str, Decimal]:
        """
        Phân bổ TSĐB theo tỷ lệ CCR (Pari-passu)
        
        Args:
            limits: Danh sách các hạn mức con
            
        Returns:
            Dictionary {limit_id: TSĐB được phân bổ}
        """
        # Tính tổng dư nợ quy đổi
        total_weighted_outstanding = Decimal('0')
        for limit in limits:
            weighted = limit.outstanding_amount * limit.ccr
            total_weighted_outstanding += weighted
        
        # Phân bổ TSĐB theo tỷ lệ
        allocation = {}
        if total_weighted_outstanding > 0:
            for limit in limits:
                weighted = limit.outstanding_amount * limit.ccr
                ratio = weighted / total_weighted_outstanding
                allocated = self.collateral_info.total_collateral * ratio
                allocation[limit.limit_id] = allocated
        else:
            # Nếu chưa có dư nợ, phân bổ đều hoặc theo chính sách
            for limit in limits:
                allocation[limit.limit_id] = Decimal('0')
        
        return allocation
    
    def allocate_collateral_by_priority(
        self,
        limits: List[LimitInfo],
        priority_order: List[str]
    ) -> Dict[str, Decimal]:
        """
        Phân bổ TSĐB theo thứ tự ưu tiên
        
        Args:
            limits: Danh sách các hạn mức con
            priority_order: Thứ tự ưu tiên (list các limit_id)
            
        Returns:
            Dictionary {limit_id: TSĐB được phân bổ}
        """
        allocation = {}
        remaining_collateral = self.collateral_info.total_collateral
        
        # Tạo dict để tra cứu nhanh
        limit_dict = {limit.limit_id: limit for limit in limits}
        
        # Phân bổ theo thứ tự ưu tiên
        for limit_id in priority_order:
            if limit_id in limit_dict:
                limit = limit_dict[limit_id]
                allocated = min(limit.outstanding_amount, remaining_collateral)
                allocation[limit_id] = allocated
                remaining_collateral -= allocated
        
        # Các hạn mức không có trong priority_order
        for limit in limits:
            if limit.limit_id not in allocation:
                allocation[limit.limit_id] = Decimal('0')
        
        return allocation
    
    def calculate_single_limit(
        self,
        limit_info: LimitInfo,
        collateral_allocated: Decimal = None
    ) -> LimitResult:
        """
        Tính hạn mức khả dụng cho một hạn mức đơn
        
        Args:
            limit_info: Thông tin hạn mức
            collateral_allocated: TSĐB được phân bổ (None = dùng toàn bộ)
            
        Returns:
            Kết quả tính toán
        """
        if collateral_allocated is None:
            collateral_allocated = self.collateral_info.total_collateral
        
        # Tính hạn mức tín chấp
        unsecured_limit = self.calculate_unsecured_limit(limit_info.approved_limit)
        
        # Tính hạn mức tối đa theo TSĐB
        max_limit_by_collateral = collateral_allocated + unsecured_limit
        
        # Tính dư nợ quy đổi
        outstanding_weighted = limit_info.outstanding_amount * limit_info.ccr
        
        # TSĐB khả dụng
        collateral_available = max(Decimal('0'), collateral_allocated - limit_info.outstanding_amount)
        
        # Hạn mức khả dụng (quy đổi rủi ro)
        available_weighted = min(
            limit_info.approved_limit,
            max_limit_by_collateral
        ) - outstanding_weighted
        available_weighted = max(Decimal('0'), available_weighted)
        
        # Hạn mức khả dụng (danh nghĩa)
        available_by_approved = limit_info.approved_limit - limit_info.outstanding_amount
        available_by_collateral = collateral_available + unsecured_limit
        
        available_nominal = min(available_by_approved, available_by_collateral)
        available_nominal = max(Decimal('0'), available_nominal)
        
        # Tỷ lệ sử dụng
        utilization = (outstanding_weighted / limit_info.approved_limit * 100) \
            if limit_info.approved_limit > 0 else Decimal('0')
        
        return LimitResult(
            limit_id=limit_info.limit_id,
            limit_name=limit_info.limit_name,
            approved_limit=limit_info.approved_limit,
            outstanding_nominal=limit_info.outstanding_amount,
            outstanding_weighted=outstanding_weighted,
            ccr=limit_info.ccr,
            collateral_allocated=collateral_allocated,
            collateral_available=collateral_available,
            unsecured_limit=unsecured_limit,
            available_limit_weighted=available_weighted,
            available_limit_nominal=available_nominal,
            utilization_ratio=utilization
        )
    
    def calculate_hierarchical_limits(
        self,
        master_limit: LimitInfo,
        child_limits: List[LimitInfo],
        allocation_method: str = 'ccr'  # 'ccr' hoặc 'priority'
    ) -> Tuple[LimitResult, List[LimitResult]]:
        """
        Tính hạn mức cho cấu trúc phân cấp với TSĐB liên thông
        
        Args:
            master_limit: Hạn mức tổng
            child_limits: Danh sách hạn mức con
            allocation_method: Phương pháp phân bổ TSĐB
            
        Returns:
            Tuple (Kết quả hạn mức tổng, Danh sách kết quả hạn mức con)
        """
        # Bước 1: Tính tổng dư nợ quy đổi từ các hạn mức con
        total_child_outstanding_weighted = Decimal('0')
        total_child_outstanding_nominal = Decimal('0')
        
        for child in child_limits:
            total_child_outstanding_weighted += child.outstanding_amount * child.ccr
            total_child_outstanding_nominal += child.outstanding_amount
        
        # Bước 2: Phân bổ TSĐB cho các hạn mức con
        if allocation_method == 'ccr':
            collateral_allocation = self.allocate_collateral_by_ccr(child_limits)
        else:  # priority
            # Thứ tự ưu tiên: CCR cao → thấp (Vay → BL → L/C)
            sorted_limits = sorted(child_limits, key=lambda x: x.ccr, reverse=True)
            priority_order = [limit.limit_id for limit in sorted_limits]
            collateral_allocation = self.allocate_collateral_by_priority(
                child_limits, priority_order
            )
        
        # Bước 3: Tính hạn mức tổng
        unsecured_limit_master = self.calculate_unsecured_limit(master_limit.approved_limit)
        max_limit_by_collateral = self.collateral_info.total_collateral + unsecured_limit_master
        
        available_master_weighted = min(
            master_limit.approved_limit,
            max_limit_by_collateral
        ) - total_child_outstanding_weighted
        available_master_weighted = max(Decimal('0'), available_master_weighted)
        
        utilization_master = (total_child_outstanding_weighted / master_limit.approved_limit * 100) \
            if master_limit.approved_limit > 0 else Decimal('0')
        
        master_result = LimitResult(
            limit_id=master_limit.limit_id,
            limit_name=master_limit.limit_name,
            approved_limit=master_limit.approved_limit,
            outstanding_nominal=total_child_outstanding_nominal,
            outstanding_weighted=total_child_outstanding_weighted,
            ccr=Decimal('1.0'),  # Master luôn có CCR = 1
            collateral_allocated=self.collateral_info.total_collateral,
            collateral_available=self.collateral_info.total_collateral - total_child_outstanding_nominal,
            unsecured_limit=unsecured_limit_master,
            available_limit_weighted=available_master_weighted,
            available_limit_nominal=None,  # Không tính danh nghĩa cho master
            utilization_ratio=utilization_master
        )
        
        # Bước 4: Tính hạn mức khả dụng cho từng hạn mức con
        child_results = []
        
        for child in child_limits:
            # TSĐB được phân bổ cho hạn mức con này
            collateral_for_child = collateral_allocation[child.limit_id]
            
            # Tính hạn mức tín chấp cho hạn mức con
            unsecured_for_child = self.calculate_unsecured_limit(child.approved_limit)
            
            # TSĐB khả dụng (đã trừ dư nợ)
            collateral_available = max(Decimal('0'), collateral_for_child - child.outstanding_amount)
            
            # Dư nợ quy đổi
            outstanding_weighted = child.outstanding_amount * child.ccr
            
            # Hạn mức khả dụng (quy đổi) - xét 3 giới hạn
            # 1. Theo hạn mức con được cấp
            available_by_approved = child.approved_limit - child.outstanding_amount
            
            # 2. Theo hạn mức tổng
            available_by_master = available_master_weighted / child.ccr if child.ccr > 0 else Decimal('0')
            
            # 3. Theo TSĐB + tín chấp
            available_by_collateral = collateral_available + unsecured_for_child
            
            # Lấy MIN
            available_nominal = min(
                available_by_approved,
                available_by_master,
                available_by_collateral
            )
            available_nominal = max(Decimal('0'), available_nominal)
            
            # Hạn mức quy đổi
            available_weighted = available_nominal * child.ccr
            
            # Tỷ lệ sử dụng
            utilization = (outstanding_weighted / child.approved_limit * 100) \
                if child.approved_limit > 0 else Decimal('0')
            
            child_result = LimitResult(
                limit_id=child.limit_id,
                limit_name=child.limit_name,
                approved_limit=child.approved_limit,
                outstanding_nominal=child.outstanding_amount,
                outstanding_weighted=outstanding_weighted,
                ccr=child.ccr,
                collateral_allocated=collateral_for_child,
                collateral_available=collateral_available,
                unsecured_limit=unsecured_for_child,
                available_limit_weighted=available_weighted,
                available_limit_nominal=available_nominal,
                utilization_ratio=utilization
            )
            
            child_results.append(child_result)
        
        return master_result, child_results


def format_currency(amount: Decimal, currency: str = 'VNĐ') -> str:
    """Format số tiền"""
    return f"{amount:,.0f} {currency}"


def format_percentage(value: Decimal) -> str:
    """Format phần trăm"""
    return f"{value:.2f}%"


def print_limit_result(result: LimitResult, indent: int = 0):
    """
    In kết quả tính toán hạn mức
    
    Args:
        result: Kết quả tính toán
        indent: Số lượng space thụt đầu dòng
    """
    prefix = " " * indent
    print(f"{prefix}{'='*60}")
    print(f"{prefix}Hạn mức: {result.limit_name} (ID: {result.limit_id})")
    print(f"{prefix}{'='*60}")
    print(f"{prefix}Hạn mức được cấp:           {format_currency(result.approved_limit)}")
    print(f"{prefix}CCR:                         {format_percentage(result.ccr * 100)}")
    print(f"{prefix}")
    print(f"{prefix}Dư nợ danh nghĩa:           {format_currency(result.outstanding_nominal)}")
    print(f"{prefix}Dư nợ quy đổi:              {format_currency(result.outstanding_weighted)}")
    print(f"{prefix}Tỷ lệ sử dụng:              {format_percentage(result.utilization_ratio)}")
    print(f"{prefix}")
    print(f"{prefix}TSĐB được phân bổ:          {format_currency(result.collateral_allocated)}")
    print(f"{prefix}TSĐB khả dụng:              {format_currency(result.collateral_available)}")
    print(f"{prefix}Hạn mức tín chấp:           {format_currency(result.unsecured_limit)}")
    print(f"{prefix}")
    print(f"{prefix}Hạn mức khả dụng (quy đổi): {format_currency(result.available_limit_weighted)}")
    if result.available_limit_nominal is not None:
        print(f"{prefix}Hạn mức khả dụng (danh nghĩa): {format_currency(result.available_limit_nominal)}")
    print(f"{prefix}{'='*60}\n")
