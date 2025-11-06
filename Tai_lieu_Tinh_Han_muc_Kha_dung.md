# TÀI LIỆU YÊU CẦU TÍNH HẠN MỨC KHẢ DỤNG

## 1. TỔNG QUAN

Tài liệu này mô tả chi tiết cách tính toán hạn mức khả dụng (Available Limit) cho từng loại hạn mức tín dụng dựa trên các yếu tố:
- Giá trị hạn mức được cấp
- Giá trị tài sản đảm bảo (TSĐB)
- Tỷ lệ tín chấp cho vay / Hạn mức tín chấp tối đa (Max Unsecured)
- Giá trị các khoản vay đã sử dụng
- Giá trị bảo lãnh đã sử dụng
- Giá trị L/C (Letter of Credit) đã sử dụng

## 2. CÁC KHÁI NIỆM CƠ BẢN

### 2.1. Hạn mức được cấp (Approved Limit)
Giá trị tối đa mà khách hàng được phép sử dụng theo quyết định phê duyệt của ngân hàng.

### 2.2. Hạn mức khả dụng (Available Limit)
Giá trị còn lại mà khách hàng có thể sử dụng tại thời điểm hiện tại.

### 2.3. Tài sản đảm bảo (TSĐB - Collateral)
Tài sản được thế chấp/cầm cố để đảm bảo cho các khoản vay.

### 2.4. Tỷ lệ tín chấp (Unsecured Ratio)
Tỷ lệ phần trăm cho phép khách hàng vay không cần tài sản đảm bảo.

### 2.5. Hạn mức tín chấp tối đa (Max Unsecured Limit)
Giá trị tối đa mà khách hàng được phép vay không cần tài sản đảm bảo.

### 2.6. Dư nợ đã sử dụng (Outstanding)
Tổng giá trị các khoản vay, bảo lãnh, L/C mà khách hàng đã sử dụng.

### 2.7. Hạn mức phân cấp (Hierarchical Limit Structure)
Cấu trúc hạn mức gồm:
- **Hạn mức tổng (Parent/Master Limit):** Hạn mức tổng thể cấp cho khách hàng
- **Hạn mức con (Child Limit):** Hạn mức cấp 1 dưới hạn mức tổng, phục vụ các mục đích cụ thể
- **Hạn mức cháu (Sub-child Limit):** Hạn mức cấp 2 trở đi, chi tiết hơn nữa theo mục đích/sản phẩm

### 2.8. Tỷ lệ CCR (Credit Conversion Rate)
Tỷ lệ chuyển đổi rủi ro tín dụng, quy đổi các nghĩa vụ ngoại bảng (off-balance) về tương đương nợ vay:
- **Vay/Cho vay:** CCR = 100% (rủi ro đầy đủ)
- **Bảo lãnh thực hiện hợp đồng:** CCR = 50%
- **Bảo lãnh thanh toán/vay vốn:** CCR = 100%
- **L/C trả ngay (Sight L/C):** CCR = 20%
- **L/C trả chậm (Usance L/C):** CCR = 50%
- **L/C xác nhận:** CCR = 20%
- **Cam kết cho vay chưa giải ngân:** CCR = 50-75%

## 3. CẤU TRÚC PHÂN CẤP HẠN MỨC

### 3.1. Mô hình phân cấp

```
Hạn mức Tổng (Master Limit) - 100 tỷ VNĐ
│
├── Hạn mức Con 1: Vay vốn lưu động - 60 tỷ VNĐ
│   ├── Hạn mức Cháu 1.1: Vay mua nguyên liệu - 30 tỷ
│   ├── Hạn mức Cháu 1.2: Vay trả lương - 15 tỷ
│   └── Hạn mức Cháu 1.3: Vay chu chuyển - 15 tỷ
│
├── Hạn mức Con 2: Bảo lãnh - 30 tỷ VNĐ
│   ├── Hạn mức Cháu 2.1: Bảo lãnh dự thầu - 10 tỷ (CCR 50%)
│   ├── Hạn mức Cháu 2.2: Bảo lãnh thực hiện - 15 tỷ (CCR 50%)
│   └── Hạn mức Cháu 2.3: Bảo lãnh bảo hành - 5 tỷ (CCR 50%)
│
└── Hạn mức Con 3: L/C - 20 tỷ VNĐ
    ├── Hạn mức Cháu 3.1: L/C trả ngay - 10 tỷ (CCR 20%)
    └── Hạn mức Cháu 3.2: L/C trả chậm - 10 tỷ (CCR 50%)
```

### 3.2. Nguyên tắc phân cấp

1. **Nguyên tắc giới hạn tổng:**
   ```
   ∑(Hạn mức con đã sử dụng × CCR tương ứng) ≤ Hạn mức tổng
   ```

2. **Nguyên tắc giới hạn con:**
   ```
   Hạn mức con khả dụng = MIN(
       Hạn mức con được cấp - Dư nợ con,
       Hạn mức tổng khả dụng,
       TSĐB khả dụng cho hạn mức con
   )
   ```

3. **Nguyên tắc tính dồn:**
   - Dư nợ cháu được tính dồn vào dư nợ con
   - Dư nợ con được tính dồn vào dư nợ tổng
   - Áp dụng CCR tương ứng khi tính dồn

4. **Nguyên tắc ràng buộc:**
   ```
   ∑(Hạn mức con) có thể > Hạn mức tổng (overselling)
   Nhưng: ∑(Dư nợ con × CCR) ≤ Hạn mức tổng
   ```

5. **Nguyên tắc TSĐB liên thông:**
   - TSĐB được chia sẻ giữa các hạn mức con
   - TSĐB đã sử dụng cho hạn mức này không thể dùng cho hạn mức khác
   - Cần tính toán TSĐB khả dụng còn lại cho từng hạn mức con
   ```
   TSĐB khả dụng = Tổng TSĐB - ∑(TSĐB đã phân bổ cho các hạn mức con khác)
   ```

### 3.3. Công thức tính theo CCR

**Dư nợ quy đổi (Risk-Weighted Outstanding):**
```
Dư nợ quy đổi = ∑(Dư nợ từng loại × CCR tương ứng)
```

**Ví dụ:**
- Dư nợ vay: 30 tỷ × 100% = 30 tỷ
- Dư nợ bảo lãnh: 10 tỷ × 50% = 5 tỷ
- Dư nợ L/C trả ngay: 8 tỷ × 20% = 1.6 tỷ
- **Tổng dư nợ quy đổi: 36.6 tỷ**

### 3.4. Phân bổ TSĐB liên thông giữa các hạn mức con

Khi TSĐB được chia sẻ giữa các hạn mức con (Vay, Bảo lãnh, L/C), cần tính toán TSĐB khả dụng cho từng hạn mức:

**Công thức TSĐB khả dụng cho hạn mức con:**

```
TSĐB khả dụng cho hạn mức i = Tổng TSĐB - ∑(TSĐB đã sử dụng bởi hạn mức khác)
```

**Cách tính TSĐB đã sử dụng bởi hạn mức:**

Có 2 phương pháp phổ biến:

**Phương pháp 1: TSĐB bao phủ dư nợ theo thứ tự ưu tiên**

```
TSĐB đã sử dụng cho hạn mức i = MIN(Dư nợ i, TSĐB được phân bổ cho hạn mức i)
```

Thứ tự ưu tiên thường: Vay (CCR 100%) → Bảo lãnh (CCR 50%) → L/C (CCR 20%)

**Phương pháp 2: TSĐB bao phủ theo tỷ lệ CCR (Pari-passu)**

```
TSĐB sử dụng cho hạn mức i = Tổng TSĐB × (Dư nợ i × CCR i) / ∑(Dư nợ j × CCR j)
```

**Ví dụ minh họa:**

Giả sử:
- Tổng TSĐB: 100 tỷ
- Dư nợ vay: 50 tỷ (CCR 100%)
- Dư nợ bảo lãnh: 40 tỷ (CCR 50%)
- Dư nợ L/C: 30 tỷ (CCR 20%)

*Phương pháp 1 - Theo thứ tự ưu tiên:*

```
TSĐB cho vay = MIN(50, 100) = 50 tỷ
TSĐB cho bảo lãnh = MIN(40, 100-50) = 40 tỷ
TSĐB cho L/C = MIN(30, 100-50-40) = 10 tỷ
TSĐB còn lại chưa sử dụng = 100 - 50 - 40 - 10 = 0
```

*Phương pháp 2 - Theo tỷ lệ CCR:*

```
Tổng dư nợ quy đổi = 50×100% + 40×50% + 30×20% = 50 + 20 + 6 = 76 tỷ

TSĐB cho vay = 100 × (50×100%)/76 = 100 × 50/76 = 65.79 tỷ
TSĐB cho bảo lãnh = 100 × (40×50%)/76 = 100 × 20/76 = 26.32 tỷ
TSĐB cho L/C = 100 × (30×20%)/76 = 100 × 6/76 = 7.89 tỷ
```

**Hạn mức khả dụng với TSĐB liên thông:**

```
Hạn mức vay khả dụng = MIN(
    Hạn mức vay được cấp - Dư nợ vay,
    (TSĐB chưa sử dụng + Hạn mức tín chấp vay) - Dư nợ vay,
    Hạn mức tổng khả dụng / CCR vay
)
```

Trong đó:
```
TSĐB chưa sử dụng = Tổng TSĐB - TSĐB đã dùng cho BL - TSĐB đã dùng cho L/C
```

## 4. CÔNG THỨC TÍNH TỔNG QUÁT

### 4.1. Công thức cơ bản cho hạn mức đơn

```
Hạn mức khả dụng = MIN(Hạn mức được cấp, Hạn mức theo TSĐB) - Dư nợ đã sử dụng
```

Trong đó:

```
Hạn mức theo TSĐB = Giá trị TSĐB + Hạn mức tín chấp
```

### 4.2. Công thức cho hạn mức phân cấp

**A. Hạn mức tổng khả dụng:**

```
Hạn mức tổng khả dụng = MIN(
    Hạn mức tổng được cấp,
    Hạn mức tổng theo TSĐB
) - ∑(Dư nợ con × CCR tương ứng)
```

**B. Hạn mức con khả dụng:**

```
Hạn mức con khả dụng = MIN(
    Hạn mức con được cấp - Dư nợ con,
    Hạn mức tổng khả dụng / CCR của hạn mức con
)
```

**C. Hạn mức cháu khả dụng:**

```
Hạn mức cháu khả dụng = MIN(
    Hạn mức cháu được cấp - Dư nợ cháu,
    Hạn mức con khả dụng
)
```

**Lưu ý:** Khi tính hạn mức con khả dụng, cần chia hạn mức tổng khả dụng cho CCR để quy đổi ngược lại về giá trị danh nghĩa.

### 4.3. Chi tiết các thành phần

**A. Hạn mức tín chấp:**
```
Hạn mức tín chấp = MIN(
    Hạn mức được cấp × Tỷ lệ tín chấp,
    Hạn mức tín chấp tối đa
)
```

**B. Dư nợ đã sử dụng:**
```
Dư nợ đã sử dụng = Giá trị vay + Giá trị bảo lãnh + Giá trị L/C
```

## 4. CÔNG THỨC CHI TIẾT THEO TỪNG TRƯỜNG HỢP

### 4.1. Trường hợp có đầy đủ TSĐB

Khi giá trị TSĐB ≥ Hạn mức được cấp:

```
Hạn mức khả dụng = Hạn mức được cấp - Dư nợ đã sử dụng
```

**Điều kiện:**
- Hạn mức khả dụng ≥ 0
- Nếu Dư nợ đã sử dụng > Hạn mức được cấp thì Hạn mức khả dụng = 0 (quá hạn mức)

### 4.2. Trường hợp có TSĐB một phần

Khi 0 < Giá trị TSĐB < Hạn mức được cấp:

**Bước 1:** Tính hạn mức tín chấp
```
Hạn mức tín chấp = MIN(
    Hạn mức được cấp × Tỷ lệ tín chấp %,
    Max Unsecured Limit
)
```

**Bước 2:** Tính tổng hạn mức khả dụng tối đa
```
Hạn mức tối đa = Giá trị TSĐB + Hạn mức tín chấp
```

**Bước 3:** Tính hạn mức khả dụng
```
Hạn mức khả dụng = MIN(Hạn mức được cấp, Hạn mức tối đa) - Dư nợ đã sử dụng
```

### 4.3. Trường hợp không có TSĐB (Tín chấp hoàn toàn)

Khi Giá trị TSĐB = 0:

**Bước 1:** Tính hạn mức tín chấp cho phép
```
Hạn mức tín chấp = MIN(
    Hạn mức được cấp × Tỷ lệ tín chấp %,
    Max Unsecured Limit
)
```

**Bước 2:** Tính hạn mức khả dụng
```
Hạn mức khả dụng = Hạn mức tín chấp - Dư nợ đã sử dụng
```

**Lưu ý:** 
- Nếu Hạn mức tín chấp < Hạn mức được cấp, khách hàng cần bổ sung TSĐB để sử dụng đủ hạn mức được cấp.

## 5. VÍ DỤ TÍNH TOÁN

### Ví dụ 1: Hạn mức phân cấp với CCR khác nhau và TSĐB liên thông

**Dữ liệu:**

**Hạn mức tổng:**
- Hạn mức tổng được cấp: 100 tỷ VNĐ
- Giá trị TSĐB: 80 tỷ VNĐ (chia sẻ cho tất cả hạn mức con)
- Tỷ lệ tín chấp: 20%
- Max Unsecured: 30 tỷ VNĐ

**Hạn mức con và dư nợ:**

| Loại hạn mức | Hạn mức cấp | CCR | Dư nợ hiện tại |
|--------------|-------------|-----|----------------|
| Vay vốn lưu động | 60 tỷ | 100% | 40 tỷ |
| Bảo lãnh | 30 tỷ | 50% | 20 tỷ |
| L/C trả ngay | 20 tỷ | 20% | 10 tỷ |

**Tính toán:**

**Bước 1:** Tính hạn mức tín chấp tổng

```
Hạn mức tín chấp = MIN(100 × 20%, 30) = MIN(20, 30) = 20 tỷ
```

**Bước 2:** Phân bổ TSĐB đã sử dụng (Phương pháp theo tỷ lệ CCR)

```
Tổng dư nợ quy đổi = 40×100% + 20×50% + 10×20% = 40 + 10 + 2 = 52 tỷ

TSĐB đã sử dụng cho vay = 80 × (40×100%)/52 = 80 × 40/52 = 61.54 tỷ
TSĐB đã sử dụng cho BL = 80 × (20×50%)/52 = 80 × 10/52 = 15.38 tỷ
TSĐB đã sử dụng cho L/C = 80 × (10×20%)/52 = 80 × 2/52 = 3.08 tỷ

Kiểm tra: 61.54 + 15.38 + 3.08 = 80 tỷ ✓
```

**Bước 3:** Tính hạn mức tổng khả dụng

```
Hạn mức tổng theo TSĐB = 80 + 20 = 100 tỷ
Hạn mức tổng khả dụng (quy đổi) = MIN(100, 100) - 52 = 48 tỷ
```

**Bước 4:** Phân bổ TSĐB khả dụng cho từng loại (cho phần mở rộng)

```
TSĐB chưa sử dụng = 80 - 80 = 0 tỷ (đã hết TSĐB)
Hạn mức tín chấp còn lại = 20 tỷ (toàn bộ)
```

**Bước 5:** Tính hạn mức khả dụng cho từng loại

*Vay vốn lưu động (CCR 100%):*

```
TSĐB còn lại cho vay = 80 - 15.38 - 3.08 = 61.54 tỷ
Nhưng dư nợ vay đã dùng = 40 tỷ
TSĐB chưa dùng cho vay = 61.54 - 40 = 21.54 tỷ

Hạn mức vay khả dụng = MIN(
    60 - 40,                    // 20 tỷ - theo hạn mức con
    48/1.00,                    // 48 tỷ - theo hạn mức tổng
    21.54 + phần tín chấp       // theo TSĐB còn lại
) = MIN(20, 48, ...) = 20 tỷ
```

*Bảo lãnh (CCR 50%):*

```
TSĐB còn lại cho BL = 80 - 61.54 - 3.08 = 15.38 tỷ
Nhưng dư nợ BL đã dùng = 20 tỷ (vượt TSĐB được phân bổ)
→ Đang dùng tín chấp: 20 - 15.38 = 4.62 tỷ

Hạn mức BL khả dụng = MIN(
    30 - 20,                    // 10 tỷ - theo hạn mức con
    48/0.50,                    // 96 tỷ - theo hạn mức tổng
    15.38 - 15.38 + (20 - 4.62) // Cần tính TSĐB + tín chấp còn lại
) = MIN(10, 96) = 10 tỷ
```

*L/C trả ngay (CCR 20%):*

```
Hạn mức L/C khả dụng = MIN(
    20 - 10,                    // 10 tỷ - theo hạn mức con
    48/0.20                     // 240 tỷ - theo hạn mức tổng
) = MIN(10, 240) = 10 tỷ
```

**Kết luận:**
- Hạn mức tổng khả dụng: 48 tỷ (quy đổi rủi ro)
- Vay còn có thể sử dụng: 20 tỷ
- Bảo lãnh còn có thể sử dụng: 10 tỷ (tương đương 5 tỷ rủi ro)
- L/C còn có thể sử dụng: 10 tỷ (tương đương 2 tỷ rủi ro)
- **Lưu ý:** Do TSĐB liên thông, nếu sử dụng thêm vay sẽ ảnh hưởng đến khả năng sử dụng BL/L/C

### Ví dụ 1A: TSĐB liên thông - Khi vay thêm sẽ ảnh hưởng BL/LC

**Tiếp tục từ Ví dụ 1, giả sử khách hàng vay thêm 15 tỷ:**

**Trạng thái mới:**
- Dư nợ vay: 40 + 15 = 55 tỷ
- Dư nợ bảo lãnh: 20 tỷ (không đổi)
- Dư nợ L/C: 10 tỷ (không đổi)

**Tính lại TSĐB phân bổ:**

```
Tổng dư nợ quy đổi mới = 55×100% + 20×50% + 10×20% = 55 + 10 + 2 = 67 tỷ

TSĐB cho vay = 80 × 55/67 = 65.67 tỷ
TSĐB cho BL = 80 × 10/67 = 11.94 tỷ
TSĐB cho L/C = 80 × 2/67 = 2.39 tỷ
```

**Phân tích tác động:**
- TSĐB cho vay tăng từ 61.54 → 65.67 tỷ (+4.13 tỷ)
- TSĐB cho BL giảm từ 15.38 → 11.94 tỷ (-3.44 tỷ)
- TSĐB cho L/C giảm từ 3.08 → 2.39 tỷ (-0.69 tỷ)

**Hạn mức khả dụng mới:**

```
Hạn mức tổng khả dụng = MIN(100, 100) - 67 = 33 tỷ (giảm từ 48 tỷ)

Hạn mức vay khả dụng = MIN(60-55, 33/1.0) = MIN(5, 33) = 5 tỷ
Hạn mức BL khả dụng = MIN(30-20, 33/0.5) = MIN(10, 66) = 10 tỷ
Hạn mức L/C khả dụng = MIN(20-10, 33/0.2) = MIN(10, 165) = 10 tỷ
```

**Kết luận:** Việc vay thêm 15 tỷ làm giảm TSĐB khả dụng cho BL và L/C, nhưng do BL/LC vẫn còn dư TSĐB nên chưa bị ảnh hưởng ngay lập tức. Tuy nhiên, hạn mức tổng giảm từ 48 tỷ xuống 33 tỷ.

### Ví dụ 2: Hạn mức con/cháu nhiều cấp

**Cấu trúc:**
```
Hạn mức tổng: 100 tỷ
├── Vay vốn lưu động: 60 tỷ (CCR 100%)
│   ├── Vay mua nguyên liệu: 30 tỷ - Dư nợ: 25 tỷ
│   ├── Vay trả lương: 15 tỷ - Dư nợ: 10 tỷ
│   └── Vay chu chuyển: 20 tỷ - Dư nợ: 15 tỷ
└── Bảo lãnh: 50 tỷ (CCR 50%)
    ├── Bảo lãnh dự thầu: 20 tỷ - Dư nợ: 10 tỷ
    └── Bảo lãnh thực hiện: 30 tỷ - Dư nợ: 15 tỷ
```

**TSĐB:** 70 tỷ, **Hạn mức tín chấp:** 20 tỷ

**Tính toán:**

**Bước 1:** Tính dư nợ quy đổi các hạn mức cháu
```
Dư nợ vay cháu = 25 + 10 + 15 = 50 tỷ × 100% = 50 tỷ
Dư nợ bảo lãnh cháu = 10 + 15 = 25 tỷ × 50% = 12.5 tỷ
Tổng dư nợ quy đổi = 50 + 12.5 = 62.5 tỷ
```

**Bước 2:** Tính hạn mức tổng khả dụng
```
Hạn mức tổng theo TSĐB = 70 + 20 = 90 tỷ
Hạn mức tổng khả dụng = MIN(100, 90) - 62.5 = 90 - 62.5 = 27.5 tỷ
```

**Bước 3:** Tính hạn mức con khả dụng

*Vay vốn lưu động:*
```
Dư nợ con = 50 tỷ
Hạn mức con khả dụng = MIN(60 - 50, 27.5/1.00) = MIN(10, 27.5) = 10 tỷ
```

*Bảo lãnh:*
```
Dư nợ con = 25 tỷ
Hạn mức con khả dụng = MIN(50 - 25, 27.5/0.50) = MIN(25, 55) = 25 tỷ
```

**Bước 4:** Tính hạn mức cháu khả dụng

*Vay mua nguyên liệu:*
```
Hạn mức cháu khả dụng = MIN(30 - 25, 10) = MIN(5, 10) = 5 tỷ
```

*Vay trả lương:*
```
Hạn mức cháu khả dụng = MIN(15 - 10, 10) = MIN(5, 10) = 5 tỷ
```

*Vay chu chuyển:*
```
Hạn mức cháu khả dụng = MIN(20 - 15, 10) = MIN(5, 10) = 5 tỷ
```

Tổng hạn mức vay cháu khả dụng: 5 + 5 + 5 = 15 tỷ > 10 tỷ (hạn mức con)
→ Giới hạn bởi hạn mức con: chỉ có thể sử dụng tổng 10 tỷ cho các hạn mức cháu

**Kết luận:** Cơ chế phân cấp đảm bảo không vượt quá hạn mức tổng và hạn mức con.

### Ví dụ 3: Có đầy đủ TSĐB (Hạn mức đơn)

**Dữ liệu:**
- Hạn mức được cấp: 10,000,000,000 VNĐ
- Giá trị TSĐB: 12,000,000,000 VNĐ
- Tỷ lệ tín chấp: 20%
- Max Unsecured: 3,000,000,000 VNĐ
- Dư nợ vay: 3,000,000,000 VNĐ
- Dư nợ bảo lãnh: 2,000,000,000 VNĐ
- Dư nợ L/C: 1,000,000,000 VNĐ

**Tính toán:**
```
Dư nợ đã sử dụng = 3,000 + 2,000 + 1,000 = 6,000,000,000 VNĐ
Hạn mức khả dụng = 10,000,000,000 - 6,000,000,000 = 4,000,000,000 VNĐ
```

### Ví dụ 2: Có TSĐB một phần

**Dữ liệu:**
- Hạn mức được cấp: 10,000,000,000 VNĐ
- Giá trị TSĐB: 6,000,000,000 VNĐ
- Tỷ lệ tín chấp: 20%
- Max Unsecured: 3,000,000,000 VNĐ
- Dư nợ vay: 4,000,000,000 VNĐ
- Dư nợ bảo lãnh: 1,000,000,000 VNĐ
- Dư nợ L/C: 500,000,000 VNĐ

**Tính toán:**
```
Bước 1: Hạn mức tín chấp = MIN(10,000 × 20%, 3,000) = MIN(2,000, 3,000) = 2,000,000,000 VNĐ
Bước 2: Hạn mức tối đa = 6,000 + 2,000 = 8,000,000,000 VNĐ
Bước 3: Dư nợ đã sử dụng = 4,000 + 1,000 + 500 = 5,500,000,000 VNĐ
Bước 4: Hạn mức khả dụng = MIN(10,000, 8,000) - 5,500 = 8,000 - 5,500 = 2,500,000,000 VNĐ
```

**Giải thích:** Mặc dù hạn mức được cấp là 10 tỷ, nhưng do chỉ có TSĐB 6 tỷ và hạn mức tín chấp 2 tỷ, nên tổng hạn mức tối đa chỉ là 8 tỷ.

### Ví dụ 5: Không có TSĐB (Tín chấp hoàn toàn - Hạn mức đơn)

**Dữ liệu:**
- Hạn mức được cấp: 10,000,000,000 VNĐ
- Giá trị TSĐB: 0 VNĐ
- Tỷ lệ tín chấp: 20%
- Max Unsecured: 3,000,000,000 VNĐ
- Dư nợ vay: 1,500,000,000 VNĐ
- Dư nợ bảo lãnh: 500,000,000 VNĐ
- Dư nợ L/C: 0 VNĐ

**Tính toán:**
```
Bước 1: Hạn mức tín chấp = MIN(10,000 × 20%, 3,000) = MIN(2,000, 3,000) = 2,000,000,000 VNĐ
Bước 2: Dư nợ đã sử dụng = 1,500 + 500 + 0 = 2,000,000,000 VNĐ
Bước 3: Hạn mức khả dụng = 2,000 - 2,000 = 0 VNĐ
```

**Giải thích:** Khách hàng đã sử dụng hết hạn mức tín chấp cho phép. Để sử dụng thêm, cần bổ sung TSĐB.

### Ví dụ 6: Vượt hạn mức (Hạn mức đơn)

**Dữ liệu:**
- Hạn mức được cấp: 10,000,000,000 VNĐ
- Giá trị TSĐB: 8,000,000,000 VNĐ
- Tỷ lệ tín chấp: 30%
- Max Unsecured: 5,000,000,000 VNĐ
- Dư nợ vay: 12,000,000,000 VNĐ
- Dư nợ bảo lãnh: 0 VNĐ
- Dư nợ L/C: 0 VNĐ

**Tính toán:**
```
Bước 1: Hạn mức tín chấp = MIN(10,000 × 30%, 5,000) = MIN(3,000, 5,000) = 3,000,000,000 VNĐ
Bước 2: Hạn mức tối đa = 8,000 + 3,000 = 11,000,000,000 VNĐ
Bước 3: Dư nợ đã sử dụng = 12,000,000,000 VNĐ
Bước 4: Hạn mức khả dụng = MIN(10,000, 11,000) - 12,000 = 10,000 - 12,000 = -2,000,000,000 VNĐ
```

**Kết luận:** Hạn mức khả dụng = 0 (đã vượt hạn mức 2 tỷ - cần xử lý)

## 6. PHÂN TÍCH THEO TỪNG LOẠI SẢN PHẨM VÀ CẤU TRÚC PHÂN CẤP

### 6.1. Nguyên tắc chung cho hạn mức phân cấp

1. **Tính dồn từ dưới lên (Bottom-up):**
   - Dư nợ cháu → Dư nợ con
   - Dư nợ con → Dư nợ tổng
   - Áp dụng CCR khi tính dồn

2. **Kiểm soát từ trên xuống (Top-down):**
   - Hạn mức khả dụng tổng giới hạn hạn mức khả dụng con
   - Hạn mức khả dụng con giới hạn hạn mức khả dụng cháu

3. **Nguyên tắc CCR:**
   - Mỗi loại sản phẩm/mục đích có CCR riêng
   - CCR của hạn mức con kế thừa từ loại sản phẩm chính
   - Hạn mức cháu thừa kế CCR từ hạn mức con (trừ khi có quy định riêng)

4. **Nguyên tắc TSĐB liên thông:**
   - TSĐB được chia sẻ động giữa các hạn mức con dựa trên dư nợ thực tế
   - Khi hạn mức này sử dụng thêm TSĐB → TSĐB khả dụng cho hạn mức khác giảm
   - Cần tính toán lại phân bổ TSĐB sau mỗi giao dịch
   - Hạn mức có CCR cao (vay 100%) chiếm TSĐB nhiều hơn hạn mức CCR thấp (L/C 20%)

### 6.2. Hạn mức Vay (Loan Limit) - Với TSĐB liên thông

**Công thức hạn mức vay khả dụng (có xét TSĐB liên thông):**

```
Hạn mức vay khả dụng = MIN(
    Hạn mức vay được cấp - Dư nợ vay,
    (TSĐB khả dụng cho vay + Hạn mức tín chấp vay) - Dư nợ vay,
    Hạn mức tổng khả dụng / CCR vay
)
```

Trong đó:

```
TSĐB khả dụng cho vay = TSĐB được phân bổ cho vay - Dư nợ vay đã dùng TSĐB

TSĐB được phân bổ cho vay = Tổng TSĐB × (Dư nợ vay × CCR vay) / ∑(Dư nợ i × CCR i)
```

**Ví dụ cụ thể:**

Cho:
- Tổng TSĐB: 100 tỷ
- Hạn mức vay: 80 tỷ, Dư nợ vay: 50 tỷ
- Hạn mức BL: 40 tỷ, Dư nợ BL: 20 tỷ (CCR 50%)
- Hạn mức L/C: 30 tỷ, Dư nợ L/C: 15 tỷ (CCR 20%)
- Hạn mức tín chấp: 20 tỷ

```
Tổng dư nợ quy đổi = 50×100% + 20×50% + 15×20% = 50 + 10 + 3 = 63 tỷ

TSĐB phân bổ cho vay = 100 × 50/63 = 79.37 tỷ
TSĐB phân bổ cho BL = 100 × 10/63 = 15.87 tỷ
TSĐB phân bổ cho L/C = 100 × 3/63 = 4.76 tỷ

TSĐB khả dụng cho vay = 79.37 - 50 = 29.37 tỷ
TSĐB khả dụng cho BL = 15.87 - 20 = -4.13 tỷ (đang dùng tín chấp 4.13 tỷ)
TSĐB khả dụng cho L/C = 4.76 - 15 = -10.24 tỷ (đang dùng tín chấp 10.24 tỷ)

Hạn mức vay khả dụng = MIN(
    80 - 50,                    // 30 tỷ
    29.37 + 20 - 50,            // -0.63 tỷ (vì BL/LC đang dùng tín chấp)
    (100 - 63) / 1.0            // 37 tỷ
) 
```

→ **Cần điều chỉnh:** Do BL/LC đang dùng tín chấp, phần tín chấp còn lại cho vay = 20 - 4.13 - 10.24 = 5.63 tỷ

```
Hạn mức vay khả dụng thực tế = MIN(30, 29.37 + 5.63, 37) = MIN(30, 35, 37) = 30 tỷ
```

**Lưu ý quan trọng:**
- Khi vay thêm, TSĐB phân bổ cho vay sẽ tăng → TSĐB cho BL/LC giảm
- Nếu BL/LC đang dùng nhiều TSĐB, việc vay thêm có thể làm họ phải chuyển sang dùng tín chấp
- Nếu hết tín chấp, BL/LC không thể mở rộng thêm

### 6.3. Hạn mức Bảo lãnh (Guarantee Limit)

**Công thức với CCR khác nhau:**

```
Hạn mức bảo lãnh tổng khả dụng (quy đổi) = MIN(
    Hạn mức bảo lãnh tổng được cấp,
    Hạn mức theo TSĐB
) - ∑(Dư nợ bảo lãnh con × CCR tương ứng)
```

**Công thức hạn mức bảo lãnh con:**

```
Hạn mức bảo lãnh con khả dụng = MIN(
    Hạn mức bảo lãnh con được cấp - Dư nợ bảo lãnh con,
    Hạn mức bảo lãnh tổng khả dụng / CCR của hạn mức con
)
```

**Ví dụ cấu trúc với CCR:**

```
Hạn mức bảo lãnh tổng: 50 tỷ
├── Bảo lãnh dự thầu: 20 tỷ (CCR 50%)
├── Bảo lãnh thực hiện hợp đồng: 20 tỷ (CCR 50%)
├── Bảo lãnh thanh toán: 10 tỷ (CCR 100%)
└── Bảo lãnh bảo hành: 5 tỷ (CCR 50%)
```

**Ví dụ tính toán:**

Giả sử:
- Hạn mức bảo lãnh tổng: 50 tỷ
- TSĐB phân bổ cho bảo lãnh: 30 tỷ
- Hạn mức tín chấp: 10 tỷ
- Dư nợ: Dự thầu 10 tỷ, Thực hiện 15 tỷ, Thanh toán 5 tỷ

```
Dư nợ quy đổi = 10×50% + 15×50% + 5×100% = 5 + 7.5 + 5 = 17.5 tỷ
Hạn mức tổng theo TSĐB = 30 + 10 = 40 tỷ
Hạn mức tổng khả dụng (quy đổi) = MIN(50, 40) - 17.5 = 40 - 17.5 = 22.5 tỷ

Hạn mức dự thầu khả dụng = MIN(20-10, 22.5/0.5) = MIN(10, 45) = 10 tỷ
Hạn mức thực hiện khả dụng = MIN(20-15, 22.5/0.5) = MIN(5, 45) = 5 tỷ
Hạn mức thanh toán khả dụng = MIN(10-5, 22.5/1.0) = MIN(5, 22.5) = 5 tỷ
```

**Lưu ý:**
- CCR thay đổi theo loại bảo lãnh và mức độ rủi ro
- Bảo lãnh thanh toán/vay vốn có CCR cao hơn (thường 100%)
- Bảo lãnh dự thầu/thực hiện/bảo hành có CCR thấp hơn (50%)

### 6.4. Hạn mức L/C (Letter of Credit Limit)

**Công thức với CCR khác nhau:**

```
Hạn mức L/C tổng khả dụng (quy đổi) = MIN(
    Hạn mức L/C tổng được cấp,
    Hạn mức theo TSĐB
) - ∑(Dư nợ L/C con × CCR tương ứng)
```

**Ví dụ cấu trúc với CCR:**

```
Hạn mức L/C tổng: 30 tỷ
├── L/C trả ngay (Sight L/C): 15 tỷ (CCR 20%)
├── L/C trả chậm (Usance L/C): 10 tỷ (CCR 50%)
└── L/C xác nhận: 5 tỷ (CCR 20%)
```

**Ví dụ tính toán:**

Giả sử:
- Hạn mức L/C tổng: 30 tỷ
- TSĐB: 20 tỷ, Tín chấp: 8 tỷ
- Dư nợ: Sight L/C 10 tỷ, Usance L/C 5 tỷ

```
Dư nợ quy đổi = 10×20% + 5×50% = 2 + 2.5 = 4.5 tỷ
Hạn mức tổng theo TSĐB = 20 + 8 = 28 tỷ
Hạn mức tổng khả dụng (quy đổi) = MIN(30, 28) - 4.5 = 28 - 4.5 = 23.5 tỷ

Hạn mức Sight L/C khả dụng = MIN(15-10, 23.5/0.2) = MIN(5, 117.5) = 5 tỷ
Hạn mức Usance L/C khả dụng = MIN(10-5, 23.5/0.5) = MIN(5, 47) = 5 tỷ
Hạn mức L/C xác nhận khả dụng = MIN(5-0, 23.5/0.2) = MIN(5, 117.5) = 5 tỷ
```

**Lưu ý:**
- L/C trả ngay có rủi ro thấp hơn (CCR 20%)
- L/C trả chậm có rủi ro trung bình (CCR 50%)
- L/C có thể yêu cầu ký quỹ từ 0-100%

### 6.5. Hạn mức Tổng (Master/Total Limit)

**Công thức tổng hợp:**

```
Hạn mức tổng khả dụng (quy đổi) = MIN(
    Hạn mức tổng được cấp,
    Giá trị TSĐB + Hạn mức tín chấp
) - ∑(Dư nợ tất cả sản phẩm × CCR tương ứng)
```

**Ví dụ tổng hợp đầy đủ:**

**Cấu trúc:**

```
Hạn mức tổng khách hàng: 200 tỷ
│
├── Hạn mức vay: 100 tỷ (CCR 100%)
│   ├── Vay ngắn hạn: 60 tỷ
│   │   ├── Vay VLDĐ: 30 tỷ - Dư nợ: 25 tỷ
│   │   └── Vay trả lương: 15 tỷ - Dư nợ: 10 tỷ
│   └── Vay dài hạn: 50 tỷ
│       └── Vay mua TSCĐ: 40 tỷ - Dư nợ: 30 tỷ
│
├── Hạn mức bảo lãnh: 70 tỷ (CCR 50%-100%)
│   ├── BL dự thầu: 30 tỷ (CCR 50%) - Dư nợ: 15 tỷ
│   ├── BL thực hiện: 25 tỷ (CCR 50%) - Dư nợ: 10 tỷ
│   └── BL thanh toán: 15 tỷ (CCR 100%) - Dư nợ: 8 tỷ
│
└── Hạn mức L/C: 50 tỷ (CCR 20%-50%)
    ├── L/C Sight: 30 tỷ (CCR 20%) - Dư nợ: 20 tỷ
    └── L/C Usance: 20 tỷ (CCR 50%) - Dư nợ: 10 tỷ
```

**TSĐB và Tín chấp:**
- Tổng TSĐB: 150 tỷ
- Hạn mức tín chấp: 30 tỷ
- Hạn mức tổng theo TSĐB: 150 + 30 = 180 tỷ

**Tính toán:**

**Bước 1:** Tính dư nợ quy đổi từng nhóm

*Nhóm vay:*
```
Dư nợ vay = (25 + 10 + 30) × 100% = 65 tỷ
```

*Nhóm bảo lãnh:*
```
Dư nợ BL = 15×50% + 10×50% + 8×100% = 7.5 + 5 + 8 = 20.5 tỷ
```

*Nhóm L/C:*
```
Dư nợ L/C = 20×20% + 10×50% = 4 + 5 = 9 tỷ
```

**Bước 2:** Tính tổng dư nợ quy đổi
```
Tổng dư nợ quy đổi = 65 + 20.5 + 9 = 94.5 tỷ
```

**Bước 3:** Tính hạn mức tổng khả dụng
```
Hạn mức tổng khả dụng = MIN(200, 180) - 94.5 = 180 - 94.5 = 85.5 tỷ
```

**Bước 4:** Tính hạn mức khả dụng từng nhóm

*Hạn mức vay khả dụng:*
```
Dư nợ vay hiện tại = 65 tỷ
Hạn mức vay khả dụng = MIN(100-65, 85.5/1.0) = MIN(35, 85.5) = 35 tỷ
```

*Hạn mức bảo lãnh khả dụng:*
```
Dư nợ BL hiện tại = 15 + 10 + 8 = 33 tỷ (danh nghĩa)
Hạn mức BL khả dụng (cần xét từng loại do CCR khác nhau):
- BL dự thầu: MIN(30-15, 85.5/0.5) = MIN(15, 171) = 15 tỷ
- BL thực hiện: MIN(25-10, 85.5/0.5) = MIN(15, 171) = 15 tỷ
- BL thanh toán: MIN(15-8, 85.5/1.0) = MIN(7, 85.5) = 7 tỷ
```

*Hạn mức L/C khả dụng:*
```
Dư nợ L/C hiện tại = 20 + 10 = 30 tỷ (danh nghĩa)
- L/C Sight: MIN(30-20, 85.5/0.2) = MIN(10, 427.5) = 10 tỷ
- L/C Usance: MIN(20-10, 85.5/0.5) = MIN(10, 171) = 10 tỷ
```

**Kiểm tra:**
```
Nếu sử dụng hết hạn mức vay: 35 tỷ × 100% = 35 tỷ
Hạn mức còn lại cho BL và L/C: 85.5 - 35 = 50.5 tỷ
→ Vẫn đủ cho BL (15×50% + 15×50% + 7×100% = 22.5 tỷ) 
  và L/C (10×20% + 10×50% = 7 tỷ)
```

**Lưu ý:**
- Tổng hạn mức các sản phẩm con (100+70+50=220 tỷ) > Hạn mức tổng (200 tỷ) → Overselling được phép
- Nhưng tổng dư nợ quy đổi không được vượt quá hạn mức tổng theo TSĐB
- Cần theo dõi cả hạn mức danh nghĩa và hạn mức quy đổi rủi ro

## 7. CÁC TRƯỜNG HỢP ĐẶC BIỆT

### 7.1. TSĐB chia sẻ giữa nhiều hạn mức

Khi một TSĐB được sử dụng cho nhiều hạn mức:

**Cách 1: Phân bổ TSĐB theo tỷ lệ**

```
Giá trị TSĐB phân bổ cho hạn mức i = Tổng giá trị TSĐB × (Hạn mức i / Tổng hạn mức)
```

**Cách 2: Phân bổ TSĐB theo CCR (Weighted by Risk)**

```
Trọng số rủi ro i = Hạn mức i × CCR i
Tổng trọng số = ∑(Hạn mức i × CCR i)
Giá trị TSĐB phân bổ cho hạn mức i = Tổng TSĐB × (Trọng số i / Tổng trọng số)
```

**Ví dụ:**

Tổng TSĐB: 100 tỷ, phân bổ cho:
- Hạn mức vay: 60 tỷ (CCR 100%)
- Hạn mức bảo lãnh: 40 tỷ (CCR 50%)
- Hạn mức L/C: 20 tỷ (CCR 20%)

*Cách 1 - Theo tỷ lệ hạn mức:*

```
TSĐB cho vay = 100 × (60/120) = 50 tỷ
TSĐB cho BL = 100 × (40/120) = 33.33 tỷ
TSĐB cho L/C = 100 × (20/120) = 16.67 tỷ
```

*Cách 2 - Theo trọng số rủi ro:*

```
Trọng số vay = 60 × 100% = 60
Trọng số BL = 40 × 50% = 20
Trọng số L/C = 20 × 20% = 4
Tổng trọng số = 60 + 20 + 4 = 84

TSĐB cho vay = 100 × (60/84) = 71.43 tỷ
TSĐB cho BL = 100 × (20/84) = 23.81 tỷ
TSĐB cho L/C = 100 × (4/84) = 4.76 tỷ
```

**Cách 3: Ưu tiên theo thứ tự**

- Phân bổ TSĐB theo thứ tự ưu tiên đã định
- Hạn mức có ưu tiên cao hơn được phân bổ TSĐB trước
- Thường ưu tiên: Vay → Bảo lãnh → L/C

**Cách 4: Sử dụng chung (Pool)**

- Không phân bổ cố định TSĐB cho từng hạn mức
- Tính tổng thể theo công thức hạn mức tổng
- Linh hoạt hơn nhưng phức tạp trong quản lý

### 7.2. Hạn mức con vượt quá hạn mức tổng (Overselling)

**Trường hợp được phép:**

```
∑(Hạn mức con) > Hạn mức tổng
```

Nhưng phải đảm bảo:

```
∑(Dư nợ con × CCR) ≤ Hạn mức tổng
```

**Ví dụ:**

- Hạn mức tổng: 100 tỷ
- Hạn mức vay con: 70 tỷ (CCR 100%)
- Hạn mức BL con: 60 tỷ (CCR 50%)
- Hạn mức L/C con: 40 tỷ (CCR 20%)
- **Tổng hạn mức con: 170 tỷ > 100 tỷ** ✓ Được phép

Giả sử sử dụng:
- Dư nợ vay: 50 tỷ
- Dư nợ BL: 40 tỷ
- Dư nợ L/C: 30 tỷ

```
Dư nợ quy đổi = 50×100% + 40×50% + 30×20% = 50 + 20 + 6 = 76 tỷ ≤ 100 tỷ ✓
```

**Lợi ích của Overselling:**
- Tăng tính linh hoạt cho khách hàng
- Tối ưu hóa sử dụng TSĐB
- Phù hợp khi các loại sản phẩm có CCR thấp

**Rủi ro:**
- Cần giám sát chặt chẽ
- Có thể xảy ra tình trạng một số hạn mức con không sử dụng được do hạn mức tổng đã hết

### 7.2. TSĐB có nhiều mức giá trị khác nhau

```
Giá trị TSĐB hiệu dụng = MIN(Giá trị thẩm định, Giá trị thị trường, Giá trị pháp lý) × Tỷ lệ cho vay tối đa (LTV)
```

### 7.3. Hạn mức có thời hạn

```
Hạn mức khả dụng = MIN(Hạn mức còn lại theo thời hạn, Hạn mức theo TSĐB) - Dư nợ đã sử dụng
```

### 7.4. Hạn mức tuần hoàn (Revolving Limit)

Đối với hạn mức tuần hoàn (khách hàng có thể vay lại sau khi trả nợ):

```
Hạn mức khả dụng = MIN(Hạn mức được cấp, Hạn mức theo TSĐB) - Dư nợ hiện tại
```

**Lưu ý:** Dư nợ hiện tại sẽ giảm khi khách hàng trả nợ, làm tăng hạn mức khả dụng.

### 7.5. Hạn mức không tuần hoàn (Non-Revolving Limit)

```
Hạn mức khả dụng = Hạn mức ban đầu - Tổng giá trị đã giải ngân (bao gồm cả phần đã trả)
```

## 8. QUY TẮC VÀ RÀNG BUỘC

### 8.1. Ràng buộc cơ bản

1. **Ràng buộc hạn mức:**

   ```
   Hạn mức khả dụng ≥ 0
   ```

2. **Ràng buộc tín chấp:**

   ```
   Hạn mức tín chấp ≤ MIN(Hạn mức được cấp × Tỷ lệ tín chấp, Max Unsecured)
   ```

3. **Ràng buộc TSĐB:**

   ```
   Dư nợ có TSĐB ≤ Giá trị TSĐB
   Dư nợ tín chấp ≤ Hạn mức tín chấp
   ```

4. **Ràng buộc tổng:**

   ```
   Tổng dư nợ ≤ MIN(Hạn mức được cấp, Giá trị TSĐB + Hạn mức tín chấp)
   ```

5. **Ràng buộc phân cấp:**

   ```
   ∑(Dư nợ con × CCR) ≤ Hạn mức tổng
   Dư nợ cháu ≤ Hạn mức cháu
   ∑(Dư nợ cháu) ≤ Hạn mức con
   ```

6. **Ràng buộc CCR:**

   ```
   0 < CCR ≤ 1 (hoặc 0% - 100%)
   Dư nợ quy đổi = Dư nợ danh nghĩa × CCR
   ```

7. **Ràng buộc TSĐB liên thông:**

   ```
   ∑(TSĐB phân bổ cho các hạn mức con) = Tổng TSĐB
   TSĐB phân bổ cho hạn mức i ≥ MIN(Dư nợ i, TSĐB theo phân bổ)
   Khi hạn mức i tăng dư nợ → TSĐB khả dụng cho hạn mức j giảm
   ```

### 8.2. Nguyên tắc tính toán

1. **Nguyên tắc thận trọng:** Luôn chọn giá trị nhỏ hơn (MIN) khi có nhiều giới hạn
2. **Nguyên tắc ưu tiên TSĐB:** Sử dụng TSĐB trước, tín chấp sau
3. **Nguyên tắc thời gian thực:** Cập nhật ngay khi có thay đổi dư nợ hoặc TSĐB
4. **Nguyên tắc toàn vẹn:** Tổng hạn mức các sản phẩm con ≤ Hạn mức tổng (hoặc cho phép overselling có kiểm soát)
5. **Nguyên tắc CCR:** Áp dụng đúng tỷ lệ CCR cho từng loại sản phẩm/mục đích
6. **Nguyên tắc phân cấp:** Kiểm soát từ trên xuống, tính dồn từ dưới lên
7. **Nguyên tắc nhất quán:** CCR của hạn mức cháu phải nhất quán với hạn mức con (trừ khi có quy định đặc biệt)
8. **Nguyên tắc TSĐB liên thông:** 
   - TSĐB được phân bổ động theo dư nợ thực tế và CCR
   - Phải tính toán lại phân bổ TSĐB khi có thay đổi dư nợ ở bất kỳ hạn mức nào
   - Hạn mức có CCR cao chiếm TSĐB nhiều hơn (theo tỷ lệ rủi ro)
   - Khi tính hạn mức khả dụng cho vay, phải trừ đi TSĐB đã dùng cho BL/LC

### 8.3. Xử lý trường hợp đặc biệt

1. **Khi TSĐB bị phong tỏa/tranh chấp:**
   ```
   Giá trị TSĐB hiệu dụng = Giá trị TSĐB - Giá trị bị phong tỏa
   ```

2. **Khi TSĐB giảm giá:**
   - Tái thẩm định TSĐB
   - Yêu cầu bổ sung TSĐB hoặc thu hồi nợ
   - Điều chỉnh hạn mức khả dụng

3. **Khi khách hàng quá hạn:**
   ```
   Hạn mức khả dụng = 0 (tạm khóa cho đến khi xử lý xong nợ quá hạn)
   ```

## 9. CÔNG THỨC CHO HỆ THỐNG

### 9.1. Công thức tổng quát cho lập trình (có phân cấp và CCR)

```python
def calculate_available_limit_hierarchical(
    limit_id: str,
    approved_limit: float,
    collateral_value: float,
    unsecured_ratio: float,
    max_unsecured: float,
    outstanding_amount: float,
    ccr: float,
    parent_limit_id: str = None,
    child_limits: list = None,
    sibling_limits: list = None  # Thêm tham số hạn mức anh em (để tính TSĐB liên thông)
) -> dict:
    """
    Tính hạn mức khả dụng cho cấu trúc phân cấp với CCR và TSĐB liên thông
    
    Parameters:
    - limit_id: Mã hạn mức
    - approved_limit: Hạn mức được cấp
    - collateral_value: Tổng giá trị TSĐB (chia sẻ giữa các hạn mức con)
    - unsecured_ratio: Tỷ lệ tín chấp (0-1)
    - max_unsecured: Hạn mức tín chấp tối đa
    - outstanding_amount: Dư nợ danh nghĩa của hạn mức này
    - ccr: Tỷ lệ CCR của hạn mức này (0-1)
    - parent_limit_id: Mã hạn mức cha (None nếu là hạn mức tổng)
    - child_limits: Danh sách hạn mức con (None nếu là hạn mức lá)
    - sibling_limits: Danh sách hạn mức anh em (cùng cấp, chia sẻ TSĐB)
    
    Returns:
    - Dictionary chứa thông tin hạn mức khả dụng
    """
    
    # Bước 1: Tính hạn mức tín chấp
    unsecured_limit = min(
        approved_limit * unsecured_ratio,
        max_unsecured
    )
    
    # Bước 2: Tính hạn mức tối đa theo TSĐB
    max_limit_by_collateral = collateral_value + unsecured_limit
    
    # Bước 3: Tính dư nợ quy đổi từ các hạn mức con (nếu có)
    total_child_outstanding_weighted = 0
    if child_limits:
        for child in child_limits:
            child_outstanding = child['outstanding_amount']
            child_ccr = child['ccr']
            total_child_outstanding_weighted += child_outstanding * child_ccr
    
    # Bước 4: Phân bổ TSĐB liên thông (nếu có hạn mức anh em)
    collateral_allocated = collateral_value  # Mặc định: toàn bộ TSĐB
    collateral_available_for_this = collateral_value
    
    if sibling_limits and len(sibling_limits) > 0:
        # Tính tổng dư nợ quy đổi của tất cả hạn mức anh em (bao gồm cả mình)
        total_weighted_outstanding_all = outstanding_amount * ccr
        
        for sibling in sibling_limits:
            total_weighted_outstanding_all += sibling['outstanding_amount'] * sibling['ccr']
        
        if total_weighted_outstanding_all > 0:
            # Phân bổ TSĐB theo tỷ lệ dư nợ quy đổi
            my_weighted_outstanding = outstanding_amount * ccr
            collateral_allocated = collateral_value * (my_weighted_outstanding / total_weighted_outstanding_all)
            
            # TSĐB khả dụng cho hạn mức này
            collateral_available_for_this = max(0, collateral_allocated - outstanding_amount)
            
            # Tính TSĐB đã dùng bởi các hạn mức khác
            collateral_used_by_siblings = 0
            for sibling in sibling_limits:
                sibling_weighted = sibling['outstanding_amount'] * sibling['ccr']
                sibling_allocated = collateral_value * (sibling_weighted / total_weighted_outstanding_all)
                collateral_used_by_siblings += sibling_allocated
    
    # Bước 5: Tính dư nợ quy đổi của chính hạn mức này
    if child_limits:
        outstanding_weighted = total_child_outstanding_weighted
        outstanding_nominal = sum(child['outstanding_amount'] for child in child_limits)
    else:
        outstanding_weighted = outstanding_amount * ccr
        outstanding_nominal = outstanding_amount
    
    # Bước 6: Tính hạn mức khả dụng (quy đổi rủi ro)
    available_limit_weighted = min(approved_limit, max_limit_by_collateral) - outstanding_weighted
    available_limit_weighted = max(0, available_limit_weighted)
    
    # Bước 7: Tính hạn mức khả dụng danh nghĩa (có xét TSĐB liên thông)
    if child_limits is None:
        # Hạn mức lá - cần xét TSĐB liên thông
        available_by_approved = approved_limit - outstanding_amount
        available_by_collateral = collateral_available_for_this + unsecured_limit - outstanding_amount
        
        available_limit_nominal = min(
            available_by_approved,
            available_by_collateral
        )
        available_limit_nominal = max(0, available_limit_nominal)
    else:
        # Hạn mức cha - không tính trực tiếp
        available_limit_nominal = None
    
    # Bước 8: Nếu có hạn mức cha, cần kiểm tra ràng buộc từ trên xuống
    parent_constraint = None
    if parent_limit_id:
        parent_constraint = "Cần kiểm tra hạn mức cha"
    
    return {
        'limit_id': limit_id,
        'approved_limit': approved_limit,
        'outstanding_nominal': outstanding_nominal,
        'outstanding_weighted': outstanding_weighted,
        'ccr': ccr,
        'collateral_allocated': collateral_allocated,
        'collateral_available': collateral_available_for_this,
        'available_limit_weighted': available_limit_weighted,
        'available_limit_nominal': available_limit_nominal,
        'unsecured_limit': unsecured_limit,
        'max_limit_by_collateral': max_limit_by_collateral,
        'utilization_ratio': (outstanding_weighted / approved_limit * 100) if approved_limit > 0 else 0
    }


def calculate_child_limit_available_with_shared_collateral(
    child_approved_limit: float,
    child_outstanding: float,
    child_ccr: float,
    parent_available_weighted: float,
    collateral_available_for_child: float,
    unsecured_available_for_child: float
) -> float:
    """
    Tính hạn mức khả dụng danh nghĩa cho hạn mức con
    có xét TSĐB liên thông với các hạn mức anh em
    
    Parameters:
    - child_approved_limit: Hạn mức con được cấp
    - child_outstanding: Dư nợ danh nghĩa của hạn mức con
    - child_ccr: CCR của hạn mức con
    - parent_available_weighted: Hạn mức cha khả dụng (đã quy đổi rủi ro)
    - collateral_available_for_child: TSĐB khả dụng cho hạn mức con (sau khi trừ phần dùng bởi anh em)
    - unsecured_available_for_child: Hạn mức tín chấp khả dụng cho hạn mức con
    
    Returns:
    - Hạn mức con khả dụng (danh nghĩa)
    """
    
    # Giới hạn 1: Theo hạn mức con được cấp
    available_by_approved = child_approved_limit - child_outstanding
    
    # Giới hạn 2: Theo hạn mức cha (quy đổi ngược)
    available_by_parent = parent_available_weighted / child_ccr if child_ccr > 0 else 0
    
    # Giới hạn 3: Theo TSĐB + tín chấp khả dụng (TSĐB liên thông)
    available_by_collateral = collateral_available_for_child + unsecured_available_for_child
    
    # Lấy giá trị nhỏ nhất
    available_limit = min(available_by_approved, available_by_parent, available_by_collateral)
    
    return max(0, available_limit)


# Ví dụ sử dụng
if __name__ == "__main__":
    # Hạn mức tổng
    master_limit = calculate_available_limit_hierarchical(
        limit_id="MASTER_001",
        approved_limit=100_000_000_000,  # 100 tỷ
        collateral_value=80_000_000_000,  # 80 tỷ
        unsecured_ratio=0.20,
        max_unsecured=30_000_000_000,  # 30 tỷ
        outstanding_amount=0,  # Không tính trực tiếp, lấy từ con
        ccr=1.0,
        parent_limit_id=None,
        child_limits=[
            {'outstanding_amount': 40_000_000_000, 'ccr': 1.0},  # Vay
            {'outstanding_amount': 20_000_000_000, 'ccr': 0.5},  # BL
            {'outstanding_amount': 10_000_000_000, 'ccr': 0.2},  # L/C
        ]
    )
    
    print(f"Hạn mức tổng khả dụng (quy đổi): {master_limit['available_limit_weighted']:,.0f} VNĐ")
    print(f"Dư nợ quy đổi: {master_limit['outstanding_weighted']:,.0f} VNĐ")
    print(f"Tỷ lệ sử dụng: {master_limit['utilization_ratio']:.2f}%")
    
    # Hạn mức con - Vay
    loan_available = calculate_child_limit_available(
        child_approved_limit=60_000_000_000,  # 60 tỷ
        child_outstanding=40_000_000_000,  # 40 tỷ
        child_ccr=1.0,
        parent_available_weighted=master_limit['available_limit_weighted']
    )
    print(f"\nHạn mức vay khả dụng: {loan_available:,.0f} VNĐ")
    
    # Hạn mức con - Bảo lãnh
    guarantee_available = calculate_child_limit_available(
        child_approved_limit=30_000_000_000,  # 30 tỷ
        child_outstanding=20_000_000_000,  # 20 tỷ
        child_ccr=0.5,
        parent_available_weighted=master_limit['available_limit_weighted']
    )
    print(f"Hạn mức bảo lãnh khả dụng: {guarantee_available:,.0f} VNĐ")
    
    # Hạn mức con - L/C
    lc_available = calculate_child_limit_available(
        child_approved_limit=20_000_000_000,  # 20 tỷ
        child_outstanding=10_000_000_000,  # 10 tỷ
        child_ccr=0.2,
        parent_available_weighted=master_limit['available_limit_weighted']
    )
    print(f"Hạn mức L/C khả dụng: {lc_available:,.0f} VNĐ")
```

### 9.2. Công thức SQL mẫu (có phân cấp và CCR)

```sql
-- Cấu trúc bảng mẫu
CREATE TABLE credit_limits (
    limit_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    parent_limit_id VARCHAR(50),  -- NULL nếu là hạn mức tổng
    limit_type VARCHAR(50),  -- 'MASTER', 'LOAN', 'GUARANTEE', 'LC', etc.
    purpose VARCHAR(100),  -- Mục đích sử dụng
    approved_limit DECIMAL(18,2),
    collateral_value DECIMAL(18,2),
    unsecured_ratio DECIMAL(5,4),
    max_unsecured DECIMAL(18,2),
    ccr DECIMAL(5,4),  -- Credit Conversion Rate
    status VARCHAR(20),
    FOREIGN KEY (parent_limit_id) REFERENCES credit_limits(limit_id)
);

CREATE TABLE limit_outstanding (
    outstanding_id VARCHAR(50) PRIMARY KEY,
    limit_id VARCHAR(50),
    transaction_type VARCHAR(50),  -- 'LOAN', 'GUARANTEE', 'LC'
    outstanding_amount DECIMAL(18,2),
    currency VARCHAR(10),
    effective_date DATE,
    FOREIGN KEY (limit_id) REFERENCES credit_limits(limit_id)
);

-- CTE tính dư nợ quy đổi cho mỗi hạn mức
WITH outstanding_summary AS (
    SELECT 
        lo.limit_id,
        cl.ccr,
        SUM(lo.outstanding_amount) AS total_outstanding_nominal,
        SUM(lo.outstanding_amount) * cl.ccr AS total_outstanding_weighted
    FROM limit_outstanding lo
    JOIN credit_limits cl ON lo.limit_id = cl.limit_id
    WHERE cl.status = 'ACTIVE'
    GROUP BY lo.limit_id, cl.ccr
),

-- CTE tính hạn mức tín chấp
unsecured_limits AS (
    SELECT 
        limit_id,
        LEAST(
            approved_limit * unsecured_ratio,
            max_unsecured
        ) AS unsecured_limit
    FROM credit_limits
    WHERE status = 'ACTIVE'
),

-- CTE tính hạn mức tối đa theo TSĐB
max_limits AS (
    SELECT 
        cl.limit_id,
        cl.approved_limit,
        cl.collateral_value,
        ul.unsecured_limit,
        cl.collateral_value + ul.unsecured_limit AS max_limit_by_collateral
    FROM credit_limits cl
    JOIN unsecured_limits ul ON cl.limit_id = ul.limit_id
    WHERE cl.status = 'ACTIVE'
),

-- CTE tính tổng dư nợ quy đổi từ các hạn mức con
child_outstanding AS (
    SELECT 
        cl_parent.limit_id AS parent_limit_id,
        SUM(os.total_outstanding_weighted) AS total_child_outstanding_weighted,
        SUM(os.total_outstanding_nominal) AS total_child_outstanding_nominal
    FROM credit_limits cl_parent
    JOIN credit_limits cl_child ON cl_child.parent_limit_id = cl_parent.limit_id
    LEFT JOIN outstanding_summary os ON os.limit_id = cl_child.limit_id
    WHERE cl_parent.status = 'ACTIVE'
    GROUP BY cl_parent.limit_id
)

-- Truy vấn chính: Tính hạn mức khả dụng
SELECT 
    cl.limit_id,
    cl.customer_id,
    cl.parent_limit_id,
    cl.limit_type,
    cl.purpose,
    cl.approved_limit,
    cl.ccr,
    
    -- Dư nợ
    COALESCE(os.total_outstanding_nominal, 0) AS outstanding_nominal,
    COALESCE(os.total_outstanding_weighted, 0) AS outstanding_weighted,
    
    -- Dư nợ từ các hạn mức con (nếu có)
    COALESCE(co.total_child_outstanding_nominal, 0) AS child_outstanding_nominal,
    COALESCE(co.total_child_outstanding_weighted, 0) AS child_outstanding_weighted,
    
    -- Hạn mức tín chấp và theo TSĐB
    ml.unsecured_limit,
    ml.max_limit_by_collateral,
    
    -- Hạn mức khả dụng (quy đổi rủi ro)
    GREATEST(0,
        LEAST(
            cl.approved_limit,
            ml.max_limit_by_collateral
        ) - COALESCE(
            CASE 
                WHEN co.total_child_outstanding_weighted IS NOT NULL 
                THEN co.total_child_outstanding_weighted  -- Có hạn mức con
                ELSE os.total_outstanding_weighted  -- Hạn mức lá
            END, 0
        )
    ) AS available_limit_weighted,
    
    -- Hạn mức khả dụng danh nghĩa (chỉ cho hạn mức lá)
    CASE 
        WHEN co.parent_limit_id IS NULL THEN  -- Hạn mức lá
            GREATEST(0, cl.approved_limit - COALESCE(os.total_outstanding_nominal, 0))
        ELSE NULL  -- Hạn mức cha - cần tính riêng cho từng con
    END AS available_limit_nominal,
    
    -- Tỷ lệ sử dụng
    CASE 
        WHEN cl.approved_limit > 0 THEN
            (COALESCE(
                CASE 
                    WHEN co.total_child_outstanding_weighted IS NOT NULL 
                    THEN co.total_child_outstanding_weighted
                    ELSE os.total_outstanding_weighted
                END, 0
            ) / cl.approved_limit) * 100
        ELSE 0
    END AS utilization_ratio
    
FROM credit_limits cl
LEFT JOIN outstanding_summary os ON os.limit_id = cl.limit_id
LEFT JOIN max_limits ml ON ml.limit_id = cl.limit_id
LEFT JOIN child_outstanding co ON co.parent_limit_id = cl.limit_id
WHERE cl.status = 'ACTIVE'
ORDER BY cl.customer_id, cl.parent_limit_id NULLS FIRST, cl.limit_id;


-- View để tính hạn mức con khả dụng (có xét hạn mức cha)
CREATE VIEW v_child_limit_available AS
WITH parent_limits AS (
    SELECT 
        limit_id,
        GREATEST(0,
            LEAST(approved_limit, collateral_value + 
                LEAST(approved_limit * unsecured_ratio, max_unsecured)
            ) - (
                SELECT SUM(lo.outstanding_amount * cl_child.ccr)
                FROM credit_limits cl_child
                JOIN limit_outstanding lo ON lo.limit_id = cl_child.limit_id
                WHERE cl_child.parent_limit_id = credit_limits.limit_id
            )
        ) AS available_weighted
    FROM credit_limits
    WHERE parent_limit_id IS NULL
)
SELECT 
    cl.limit_id,
    cl.customer_id,
    cl.limit_type,
    cl.approved_limit,
    cl.ccr,
    COALESCE(SUM(lo.outstanding_amount), 0) AS outstanding_nominal,
    
    -- Hạn mức khả dụng theo chính hạn mức con
    cl.approved_limit - COALESCE(SUM(lo.outstanding_amount), 0) AS available_by_child,
    
    -- Hạn mức khả dụng theo hạn mức cha
    CASE 
        WHEN cl.ccr > 0 THEN pl.available_weighted / cl.ccr
        ELSE 0
    END AS available_by_parent,
    
    -- Hạn mức khả dụng cuối cùng (lấy MIN)
    GREATEST(0,
        LEAST(
            cl.approved_limit - COALESCE(SUM(lo.outstanding_amount), 0),
            CASE WHEN cl.ccr > 0 THEN pl.available_weighted / cl.ccr ELSE 0 END
        )
    ) AS available_limit
    
FROM credit_limits cl
JOIN parent_limits pl ON pl.limit_id = cl.parent_limit_id
LEFT JOIN limit_outstanding lo ON lo.limit_id = cl.limit_id
WHERE cl.status = 'ACTIVE' AND cl.parent_limit_id IS NOT NULL
GROUP BY cl.limit_id, cl.customer_id, cl.limit_type, cl.approved_limit, cl.ccr, pl.available_weighted;
```

### 9.3. Stored Procedure mẫu

```sql
CREATE PROCEDURE sp_calculate_limit_available(
    IN p_limit_id VARCHAR(50),
    OUT p_available_weighted DECIMAL(18,2),
    OUT p_available_nominal DECIMAL(18,2)
)
BEGIN
    DECLARE v_approved_limit DECIMAL(18,2);
    DECLARE v_collateral_value DECIMAL(18,2);
    DECLARE v_unsecured_limit DECIMAL(18,2);
    DECLARE v_max_limit DECIMAL(18,2);
    DECLARE v_outstanding_weighted DECIMAL(18,2);
    DECLARE v_outstanding_nominal DECIMAL(18,2);
    DECLARE v_ccr DECIMAL(5,4);
    DECLARE v_parent_id VARCHAR(50);
    DECLARE v_parent_available DECIMAL(18,2);
    
    -- Lấy thông tin hạn mức
    SELECT 
        approved_limit,
        collateral_value,
        LEAST(approved_limit * unsecured_ratio, max_unsecured),
        ccr,
        parent_limit_id
    INTO 
        v_approved_limit,
        v_collateral_value,
        v_unsecured_limit,
        v_ccr,
        v_parent_id
    FROM credit_limits
    WHERE limit_id = p_limit_id;
    
    -- Tính hạn mức tối đa theo TSĐB
    SET v_max_limit = v_collateral_value + v_unsecured_limit;
    
    -- Tính dư nợ (kiểm tra có hạn mức con không)
    IF EXISTS (SELECT 1 FROM credit_limits WHERE parent_limit_id = p_limit_id) THEN
        -- Có hạn mức con - tính tổng dư nợ quy đổi từ con
        SELECT 
            SUM(lo.outstanding_amount * cl.ccr),
            SUM(lo.outstanding_amount)
        INTO 
            v_outstanding_weighted,
            v_outstanding_nominal
        FROM credit_limits cl
        JOIN limit_outstanding lo ON lo.limit_id = cl.limit_id
        WHERE cl.parent_limit_id = p_limit_id;
    ELSE
        -- Không có hạn mức con - dùng dư nợ của chính nó
        SELECT 
            SUM(outstanding_amount) * v_ccr,
            SUM(outstanding_amount)
        INTO 
            v_outstanding_weighted,
            v_outstanding_nominal
        FROM limit_outstanding
        WHERE limit_id = p_limit_id;
    END IF;
    
    SET v_outstanding_weighted = COALESCE(v_outstanding_weighted, 0);
    SET v_outstanding_nominal = COALESCE(v_outstanding_nominal, 0);
    
    -- Tính hạn mức khả dụng quy đổi
    SET p_available_weighted = GREATEST(0,
        LEAST(v_approved_limit, v_max_limit) - v_outstanding_weighted
    );
    
    -- Tính hạn mức khả dụng danh nghĩa
    IF v_parent_id IS NULL THEN
        -- Hạn mức tổng hoặc không có cha
        SET p_available_nominal = GREATEST(0, v_approved_limit - v_outstanding_nominal);
    ELSE
        -- Hạn mức con - cần xét hạn mức cha
        CALL sp_calculate_limit_available(v_parent_id, v_parent_available, @dummy);
        
        SET p_available_nominal = GREATEST(0,
            LEAST(
                v_approved_limit - v_outstanding_nominal,
                CASE WHEN v_ccr > 0 THEN v_parent_available / v_ccr ELSE 0 END
            )
        );
    END IF;
END;
```

## 10. BẢNG TRA CỨU NHANH

### 10.1. Ma trận tình huống

| Tình huống | TSĐB | Tín chấp | Công thức áp dụng |
|-----------|------|----------|-------------------|
| 1 | Đầy đủ (≥ Hạn mức) | Có | Hạn mức khả dụng = Hạn mức được cấp - Dư nợ |
| 2 | Một phần | Có | Hạn mức khả dụng = MIN(Hạn mức, TSĐB + Tín chấp) - Dư nợ |
| 3 | Không có | Có | Hạn mức khả dụng = Hạn mức tín chấp - Dư nợ |
| 4 | Không có | Không có | Hạn mức khả dụng = 0 (không cho vay) |

### 10.2. Checklist kiểm tra

- [ ] Hạn mức được cấp có hợp lệ và còn hiệu lực?
- [ ] Giá trị TSĐB đã được thẩm định và cập nhật?
- [ ] Tỷ lệ tín chấp có phù hợp với chính sách?
- [ ] Max Unsecured đã được thiết lập đúng?
- [ ] Dư nợ vay đã được cập nhật đầy đủ?
- [ ] Dư nợ bảo lãnh đã bao gồm tất cả bảo lãnh còn hiệu lực?
- [ ] Dư nợ L/C đã bao gồm cả L/C chưa sử dụng hết?
- [ ] Có TSĐB nào bị phong tỏa/tranh chấp không?
- [ ] Khách hàng có khoản nợ quá hạn không?
- [ ] Hạn mức có điều kiện đặc biệt nào không?

## 11. CẬP NHẬT VÀ BẢO TRÌ

### 11.1. Tần suất cập nhật

1. **Thời gian thực (Real-time):**
   - Khi giải ngân mới
   - Khi trả nợ
   - Khi phát sinh bảo lãnh/L/C mới

2. **Hàng ngày:**
   - Cập nhật giá trị TSĐB (nếu có thay đổi)
   - Kiểm tra nợ quá hạn
   - Cập nhật lãi suất và phí

3. **Định kỳ:**
   - Tái thẩm định TSĐB (6 tháng/1 năm)
   - Xem xét điều chỉnh tỷ lệ tín chấp
   - Rà soát hạn mức tổng thể

### 11.2. Cảnh báo tự động

```python
def check_limit_alerts(available_limit, approved_limit):
    """Kiểm tra và tạo cảnh báo"""
    
    utilization = 1 - (available_limit / approved_limit)
    
    if available_limit <= 0:
        return "CRITICAL: Hết hạn mức hoặc vượt hạn mức"
    elif utilization >= 0.9:
        return "WARNING: Đã sử dụng 90% hạn mức"
    elif utilization >= 0.8:
        return "INFO: Đã sử dụng 80% hạn mức"
    else:
        return "OK"
```

## 12. PHỤ LỤC

### 12.1. Bảng thuật ngữ

| Thuật ngữ tiếng Việt | Thuật ngữ tiếng Anh | Viết tắt |
|---------------------|-------------------|----------|
| Hạn mức được cấp | Approved Limit | AL |
| Hạn mức khả dụng | Available Limit | AVL |
| Tài sản đảm bảo | Collateral | TSĐB |
| Tỷ lệ tín chấp | Unsecured Ratio | UR |
| Hạn mức tín chấp tối đa | Maximum Unsecured Limit | MUL |
| Dư nợ | Outstanding | OS |
| Thư tín dụng | Letter of Credit | L/C |
| Tỷ lệ cho vay trên giá trị tài sản | Loan to Value | LTV |
| Hệ số chuyển đổi tín dụng | Credit Conversion Rate/Factor | CCR/CCF |
| Hạn mức tổng | Master Limit / Parent Limit | ML |
| Hạn mức con | Child Limit | CL |
| Hạn mức cháu | Sub-child Limit / Grandchild Limit | SCL |
| Dư nợ quy đổi | Risk-Weighted Outstanding | RWO |
| Dư nợ danh nghĩa | Nominal Outstanding | NO |
| Bảo lãnh | Guarantee / Letter of Guarantee | BL / LG |

### 12.2. Tham khảo pháp lý

- Thông tư 39/2016/TT-NHNN về cho vay đối với khách hàng là tổ chức, cá nhân
- Thông tư 13/2018/TT-NHNN về tỷ lệ bảo đảm an toàn trong hoạt động của tổ chức tín dụng
- Thông tư 36/2014/TT-NHNN về giới hạn, tỷ lệ bảo đảm an toàn trong hoạt động của tổ chức tín dụng
- Quy định nội bộ của từng ngân hàng về quản lý rủi ro tín dụng

---

**Phiên bản:** 2.0  
**Ngày ban hành:** 06/11/2025  
**Người soạn thảo:** GitHub Copilot  
**Cập nhật:** Bổ sung cấu trúc phân cấp hạn mức và tỷ lệ CCR  
**Trạng thái:** Tài liệu hướng dẫn
