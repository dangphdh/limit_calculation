"""
Test cases cho Limit Calculator
"""

import unittest
from decimal import Decimal
from limit_calculator import (
    LimitCalculator,
    LimitInfo,
    CollateralInfo
)


class TestLimitCalculator(unittest.TestCase):
    """Test cases cho LimitCalculator"""
    
    def setUp(self):
        """Thiết lập trước mỗi test"""
        self.collateral_info = CollateralInfo(
            total_collateral=Decimal('100000000000'),  # 100 tỷ
            unsecured_ratio=Decimal('0.20'),  # 20%
            max_unsecured=Decimal('30000000000')  # 30 tỷ
        )
        self.calculator = LimitCalculator(self.collateral_info)
    
    def test_calculate_unsecured_limit(self):
        """Test tính hạn mức tín chấp"""
        # Case 1: Tín chấp < Max unsecured
        approved = Decimal('100000000000')  # 100 tỷ
        unsecured = self.calculator.calculate_unsecured_limit(approved)
        expected = Decimal('20000000000')  # 20 tỷ (20% của 100 tỷ)
        self.assertEqual(unsecured, expected)
        
        # Case 2: Tín chấp > Max unsecured
        approved = Decimal('200000000000')  # 200 tỷ
        unsecured = self.calculator.calculate_unsecured_limit(approved)
        expected = Decimal('30000000000')  # 30 tỷ (max)
        self.assertEqual(unsecured, expected)
    
    def test_allocate_collateral_by_ccr(self):
        """Test phân bổ TSĐB theo CCR"""
        limits = [
            LimitInfo('L1', 'Vay', Decimal('60000000000'), Decimal('40000000000'), Decimal('1.0')),
            LimitInfo('L2', 'BL', Decimal('30000000000'), Decimal('20000000000'), Decimal('0.5')),
            LimitInfo('L3', 'LC', Decimal('20000000000'), Decimal('10000000000'), Decimal('0.2'))
        ]
        
        allocation = self.calculator.allocate_collateral_by_ccr(limits)
        
        # Tổng dư nợ quy đổi = 40*1.0 + 20*0.5 + 10*0.2 = 52 tỷ
        # L1: 100 * (40/52) = 76.92 tỷ
        # L2: 100 * (10/52) = 19.23 tỷ
        # L3: 100 * (2/52) = 3.85 tỷ
        
        self.assertAlmostEqual(
            float(allocation['L1']), 
            76923076923.08, 
            places=0
        )
        self.assertAlmostEqual(
            float(allocation['L2']), 
            19230769230.77, 
            places=0
        )
    
    def test_allocate_collateral_by_priority(self):
        """Test phân bổ TSĐB theo ưu tiên"""
        limits = [
            LimitInfo('L1', 'Vay', Decimal('60000000000'), Decimal('40000000000'), Decimal('1.0')),
            LimitInfo('L2', 'BL', Decimal('30000000000'), Decimal('20000000000'), Decimal('0.5')),
            LimitInfo('L3', 'LC', Decimal('20000000000'), Decimal('70000000000'), Decimal('0.2'))
        ]
        
        priority = ['L1', 'L2', 'L3']
        allocation = self.calculator.allocate_collateral_by_priority(limits, priority)
        
        # L1 ưu tiên đầu: min(40, 100) = 40 tỷ
        # L2 ưu tiên 2: min(20, 100-40) = 20 tỷ
        # L3 ưu tiên 3: min(70, 100-40-20) = 40 tỷ
        
        self.assertEqual(allocation['L1'], Decimal('40000000000'))
        self.assertEqual(allocation['L2'], Decimal('20000000000'))
        self.assertEqual(allocation['L3'], Decimal('40000000000'))
    
    def test_calculate_single_limit_with_sufficient_collateral(self):
        """Test tính hạn mức đơn - Có đủ TSĐB"""
        limit = LimitInfo(
            limit_id='L1',
            limit_name='Vay VLDĐ',
            approved_limit=Decimal('80000000000'),  # 80 tỷ
            outstanding_amount=Decimal('30000000000'),  # 30 tỷ
            ccr=Decimal('1.0')
        )
        
        result = self.calculator.calculate_single_limit(limit)
        
        # Hạn mức tín chấp = min(80*20%, 30) = 16 tỷ
        # Hạn mức tối đa = 100 + 16 = 116 tỷ
        # Hạn mức khả dụng = min(80, 116) - 30 = 50 tỷ
        
        self.assertEqual(result.approved_limit, Decimal('80000000000'))
        self.assertEqual(result.outstanding_nominal, Decimal('30000000000'))
        self.assertEqual(result.unsecured_limit, Decimal('16000000000'))
        self.assertEqual(result.available_limit_nominal, Decimal('50000000000'))
    
    def test_calculate_single_limit_with_insufficient_collateral(self):
        """Test tính hạn mức đơn - Không đủ TSĐB"""
        # TSĐB chỉ 50 tỷ
        small_collateral = CollateralInfo(
            total_collateral=Decimal('50000000000'),
            unsecured_ratio=Decimal('0.15'),
            max_unsecured=Decimal('20000000000')
        )
        calculator = LimitCalculator(small_collateral)
        
        limit = LimitInfo(
            limit_id='L1',
            limit_name='Vay VLDĐ',
            approved_limit=Decimal('100000000000'),  # 100 tỷ
            outstanding_amount=Decimal('40000000000'),  # 40 tỷ
            ccr=Decimal('1.0')
        )
        
        result = calculator.calculate_single_limit(limit)
        
        # Hạn mức tín chấp = min(100*15%, 20) = 15 tỷ
        # Hạn mức tối đa = 50 + 15 = 65 tỷ
        # TSĐB khả dụng = 50 - 40 = 10 tỷ
        # Hạn mức khả dụng = min(100-40, 10+15) = min(60, 25) = 25 tỷ
        
        self.assertEqual(result.available_limit_nominal, Decimal('25000000000'))
    
    def test_calculate_hierarchical_limits(self):
        """Test tính hạn mức phân cấp"""
        master = LimitInfo(
            limit_id='M1',
            limit_name='Hạn mức tổng',
            approved_limit=Decimal('100000000000'),
            outstanding_amount=Decimal('0'),
            ccr=Decimal('1.0')
        )
        
        children = [
            LimitInfo('C1', 'Vay', Decimal('60000000000'), Decimal('40000000000'), Decimal('1.0')),
            LimitInfo('C2', 'BL', Decimal('30000000000'), Decimal('20000000000'), Decimal('0.5')),
        ]
        
        master_result, child_results = self.calculator.calculate_hierarchical_limits(
            master, children, 'ccr'
        )
        
        # Tổng dư nợ quy đổi = 40*1.0 + 20*0.5 = 50 tỷ
        # Hạn mức tín chấp = 20 tỷ
        # Hạn mức tổng khả dụng = min(100, 100+20) - 50 = 50 tỷ
        
        self.assertEqual(master_result.outstanding_weighted, Decimal('50000000000'))
        self.assertEqual(master_result.available_limit_weighted, Decimal('50000000000'))
        
        # Check các hạn mức con
        self.assertEqual(len(child_results), 2)
        
        # Vay: available = min(60-40, 50/1.0, ...) = 20 tỷ
        loan_result = [r for r in child_results if r.limit_id == 'C1'][0]
        self.assertGreater(loan_result.available_limit_nominal, Decimal('0'))
    
    def test_utilization_ratio(self):
        """Test tính tỷ lệ sử dụng"""
        limit = LimitInfo(
            limit_id='L1',
            limit_name='Test',
            approved_limit=Decimal('100000000000'),
            outstanding_amount=Decimal('60000000000'),
            ccr=Decimal('1.0')
        )
        
        result = self.calculator.calculate_single_limit(limit)
        
        # Tỷ lệ sử dụng = 60/100 * 100 = 60%
        self.assertEqual(result.utilization_ratio, Decimal('60'))
    
    def test_zero_outstanding(self):
        """Test khi chưa có dư nợ"""
        limit = LimitInfo(
            limit_id='L1',
            limit_name='Test',
            approved_limit=Decimal('100000000000'),
            outstanding_amount=Decimal('0'),
            ccr=Decimal('1.0')
        )
        
        result = self.calculator.calculate_single_limit(limit)
        
        # Hạn mức khả dụng = toàn bộ hạn mức được cấp
        self.assertEqual(result.available_limit_nominal, Decimal('100000000000'))
        self.assertEqual(result.utilization_ratio, Decimal('0'))


class TestCCRCalculation(unittest.TestCase):
    """Test cases cho tính toán CCR"""
    
    def test_ccr_loan_100_percent(self):
        """Test CCR cho vay = 100%"""
        collateral_info = CollateralInfo(
            Decimal('100000000000'),
            Decimal('0.2'),
            Decimal('30000000000')
        )
        calculator = LimitCalculator(collateral_info)
        
        loan = LimitInfo('L1', 'Vay', Decimal('50000000000'), Decimal('30000000000'), Decimal('1.0'))
        result = calculator.calculate_single_limit(loan)
        
        # Dư nợ quy đổi = Dư nợ danh nghĩa (CCR = 100%)
        self.assertEqual(result.outstanding_weighted, result.outstanding_nominal)
    
    def test_ccr_guarantee_50_percent(self):
        """Test CCR cho bảo lãnh = 50%"""
        collateral_info = CollateralInfo(
            Decimal('100000000000'),
            Decimal('0.2'),
            Decimal('30000000000')
        )
        calculator = LimitCalculator(collateral_info)
        
        guarantee = LimitInfo('G1', 'BL', Decimal('50000000000'), Decimal('30000000000'), Decimal('0.5'))
        result = calculator.calculate_single_limit(guarantee)
        
        # Dư nợ quy đổi = 30 * 50% = 15 tỷ
        self.assertEqual(result.outstanding_weighted, Decimal('15000000000'))
    
    def test_ccr_lc_20_percent(self):
        """Test CCR cho L/C = 20%"""
        collateral_info = CollateralInfo(
            Decimal('100000000000'),
            Decimal('0.2'),
            Decimal('30000000000')
        )
        calculator = LimitCalculator(collateral_info)
        
        lc = LimitInfo('LC1', 'L/C', Decimal('50000000000'), Decimal('30000000000'), Decimal('0.2'))
        result = calculator.calculate_single_limit(lc)
        
        # Dư nợ quy đổi = 30 * 20% = 6 tỷ
        self.assertEqual(result.outstanding_weighted, Decimal('6000000000'))


if __name__ == '__main__':
    unittest.main()
