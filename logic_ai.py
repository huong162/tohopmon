# logic.py

# ==============================================================================
#  ĐỊNH NGHĨA CÁC TỔ HỢP MÔN VÀ CÁC CẤU TRÚC DỮ LIỆU CƠ BẢN
# ==============================================================================

# Danh sách các tổ hợp môn được xét duyệt. Tên key là mã tổ hợp.
SUBJECT_COMBINATIONS = {
    "KHTN_1": {
        "name": "Toán - Lý - Hóa",
        "subjects": ["Toán", "Lý", "Hóa"],
        "description": "Phù hợp với khối ngành kỹ thuật, công nghệ, khoa học tự nhiên.",
    },
    "KHTN_2": {
        "name": "Toán - Hóa - Sinh",
        "subjects": ["Toán", "Hóa", "Sinh"],
        "description": "Phù hợp với khối ngành Y - Dược, công nghệ sinh học, hóa học.",
    },
    "KHTN_3": {
        "name": "Toán - Lý - Tin",
        "subjects": ["Toán", "Lý", "Tin học"],
        "description": "Phù hợp với khối ngành Công nghệ thông tin, Tự động hóa, AI.",
    },
    "KHXH_1": {
        "name": "Văn - Sử - Địa",
        "subjects": ["Ngữ văn", "Lịch sử", "Địa lí"],
        "description": "Phù hợp với khối ngành khoa học xã hội, báo chí, du lịch, sư phạm.",
    },
    "KHXH_2": {
        "name": "Văn - Anh - GD KT&PL",
        "subjects": ["Ngữ văn", "Ngoại ngữ", "GD Kinh tế & Pháp luật"],
        "description": "Phù hợp với khối ngành Luật, Quan hệ công chúng, Truyền thông.",
    },
    "COBAN_1": {
        "name": "Toán - Văn - Anh",
        "subjects": ["Toán", "Ngữ văn", "Ngoại ngữ"],
        "description": "Tổ hợp có tính ứng dụng rộng, phù hợp với các ngành Kinh tế, Quản trị, Marketing.",
    },
}

# Ánh xạ giữa câu trả lời khảo sát và mã Holland
HOLLAND_MAPPING = {
    "cau2": {
        "Sửa chữa đồ đạc, lắp ráp mô hình, làm vườn.": "R",
        "Đọc sách khoa học, xem phim tài liệu, tìm hiểu cách mọi thứ hoạt động.": "I",
        "Vẽ, hát, viết truyện hoặc chơi một loại nhạc cụ.": "A",
        "Tham gia hoạt động tình nguyện, trò chuyện, giúp đỡ bạn bè.": "S",
        "Lên kế hoạch kinh doanh nhỏ, tổ chức một sự kiện cho lớp.": "E",
        "Sắp xếp lại góc học tập, tạo một bảng kế hoạch chi tiết.": "C",
    },
    "cau3": {
        "Ngoài trời, trong xưởng, nơi có thể dùng tay và công cụ.": "R",
        "Trong phòng thí nghiệm, thư viện, nơi có thể tập trung nghiên cứu.": "I",
        "Một không gian sáng tạo, linh hoạt, không gò bó.": "A",
        "Nơi có nhiều người, có thể hợp tác và hỗ trợ lẫn nhau.": "S",
        "Môi trường năng động, có cơ hội thể hiện khả năng lãnh đạo.": "E",
        "Văn phòng có trật tự, quy trình làm việc rõ ràng, ổn định.": "C",
    },
    "cau4": {
        "Bắt tay vào làm thử ngay để xem kết quả.": "R",
        "Phân tích kỹ lưỡng các dữ liệu và thông tin.": "I",
        "Tìm một giải pháp mới lạ, độc đáo không giống ai.": "A",
        "Thảo luận với mọi người để tìm hướng giải quyết chung.": "S",
        "Thuyết phục người khác làm theo phương án của mình.": "E",
        "Làm theo các bước đã được hướng dẫn một cách cẩn thận.": "C",
    },
}

# ==============================================================================
#  CÁC HÀM XỬ LÝ LOGIC
# ==============================================================================

def analyze_survey_results(survey_data):
    """
    Hàm chính để phân tích toàn bộ kết quả khảo sát và trả về gợi ý.
    
    Args:
        survey_data (dict): Dữ liệu kết quả khảo sát của học sinh.
        
    Returns:
        str: Chuỗi văn bản chứa các gợi ý và giải thích.
    """
    # Bước 1: Phân tích và chấm điểm
    strong_subjects = _identify_strong_subjects(survey_data["part_a"])
    holland_codes = _calculate_holland_scores(survey_data["part_b"])
    career_orientation = survey_data["part_c"]["cau5"]

    # Bước 2: Áp dụng bộ luật IF-THEN để tính điểm
    combination_scores = _apply_rules(strong_subjects, holland_codes, career_orientation)

    # Bước 3: Xếp hạng và tạo kết quả trả về
    recommendations = _generate_recommendations(combination_scores, holland_codes, strong_subjects, career_orientation)
    
    return recommendations

def _identify_strong_subjects(part_a_data, threshold=4):
    """Xác định các môn học mạnh dựa trên điểm tự đánh giá."""
    return [subject for subject, score in part_a_data.items() if score >= threshold]

def _calculate_holland_scores(part_b_data):
    """Tính điểm và xác định mã Holland chính và phụ."""
    scores = {'R': 0, 'I': 0, 'A': 0, 'S': 0, 'E': 0, 'C': 0}
    
    for question, answers in part_b_data.items():
        for answer in answers:
            code = HOLLAND_MAPPING[question].get(answer)
            if code:
                scores[code] += 1
    
    # Sắp xếp để tìm ra mã có điểm cao nhất và cao nhì
    sorted_codes = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    return {
        "primary": sorted_codes[0][0],
        "secondary": sorted_codes[1][0],
        "scores": scores
    }

def _apply_rules(strong_subjects, holland_codes, career_orientation):
    """Áp dụng bộ luật IF-THEN để chấm điểm cho từng tổ hợp."""
    scores = {code: 0 for code in SUBJECT_COMBINATIONS.keys()}

    # --- Luật 1: Dựa trên Mã Holland (Trọng số: chính +4, phụ +2) ---
    primary_code = holland_codes["primary"]
    secondary_code = holland_codes["secondary"]
    
    holland_rules = {
        'I': ["KHTN_1", "KHTN_2"],
        'R': ["KHTN_1", "KHTN_3"],
        'S': ["KHXH_1", "KHXH_2"],
        'A': ["KHXH_1"],
        'E': ["COBAN_1", "KHXH_2"],
        'C': ["KHTN_3", "COBAN_1"],
    }
    
    if primary_code in holland_rules:
        for combo in holland_rules[primary_code]:
            scores[combo] += 4
    if secondary_code in holland_rules:
        for combo in holland_rules[secondary_code]:
            scores[combo] += 2

    # --- Luật 2: Dựa trên Năng lực (Trọng số: +3 cho mỗi môn mạnh) ---
    for combo_code, combo_info in SUBJECT_COMBINATIONS.items():
        for subject in strong_subjects:
            if subject in combo_info["subjects"]:
                scores[combo_code] += 3

    # --- Luật 3: Dựa trên Định hướng Nghề nghiệp (Trọng số: +6 - cao nhất) ---
    career_rules = {
        "Kỹ thuật - Công nghệ": ["KHTN_1", "KHTN_3"],
        "Công nghệ thông tin": ["KHTN_3"],
        "Y - Dược - Sinh học": ["KHTN_2"],
        "Kinh tế - Quản trị - Marketing": ["COBAN_1"],
        "Khoa học Xã hội": ["KHXH_1"],
        "Sư phạm": ["KHXH_1", "COBAN_1"],
        "Luật sư, Nhà báo, Chuyên gia tâm lý": ["KHXH_1", "KHXH_2"],
        "Nghệ thuật - Thiết kế": ["KHXH_1"]
    }

    for career in career_orientation:
        if career in career_rules:
            for combo in career_rules[career]:
                scores[combo] += 6
                
    # --- Luật 4: Luật kết hợp đặc biệt (Thưởng điểm cho sự trùng khớp hoàn hảo) ---
    if primary_code == 'I' and "Y - Dược - Sinh học" in career_orientation and "Sinh" in strong_subjects:
        scores["KHTN_2"] += 4 # Bonus
    if primary_code == 'R' and "Công nghệ thông tin" in career_orientation and "Tin học" in strong_subjects:
        scores["KHTN_3"] += 4 # Bonus

    return scores

# Thay thế hàm này trong file logic_ai.py
def _generate_recommendations(scores, holland_codes, strong_subjects, career_orientation):
    """Tạo dữ liệu gợi ý có cấu trúc để hiển thị trên trang web."""
    sorted_combinations = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    analysis_lines = [
        f"Nhóm tính cách nổi bật (Holland): {holland_codes['primary']} (Chính) và {holland_codes['secondary']} (Phụ).",
        f"Các môn học có thế mạnh: {', '.join(strong_subjects) if strong_subjects else 'Chưa xác định rõ'}.",
        f"Định hướng nghề nghiệp quan tâm: {', '.join(career_orientation)}."
    ]

    recommendations_list = []
    for i, (combo_code, score) in enumerate(sorted_combinations[:3]):
        combo_info = SUBJECT_COMBINATIONS[combo_code]
        
        reasons = []
        if holland_codes['primary'] in 'IR' and combo_code in ['KHTN_1', 'KHTN_2', 'KHTN_3']:
            reasons.append("rất phù hợp với thiên hướng tính cách của bạn")
        if holland_codes['primary'] in 'ASEC' and combo_code in ['KHXH_1', 'KHXH_2', 'COBAN_1']:
             reasons.append("rất phù hợp với thiên hướng tính cách của bạn")
        
        strong_matches = [s for s in strong_subjects if s in combo_info['subjects']]
        if len(strong_matches) > 0:
            reasons.append(f"khớp với các môn bạn học tốt là {', '.join(strong_matches)}")
        
        is_career_match = False
        for career in career_orientation:
            if "Kỹ thuật" in career and combo_code in ["KHTN_1", "KHTN_3"]: is_career_match = True
            if "Y - Dược" in career and combo_code == "KHTN_2": is_career_match = True
            if "Kinh tế" in career and combo_code == "COBAN_1": is_career_match = True
            if "Xã hội" in career and combo_code in ["KHXH_1", "KHXH_2"]: is_career_match = True
        
        if is_career_match:
            reasons.append(f"hỗ trợ mạnh mẽ cho định hướng nghề nghiệp bạn đã chọn")

        if not reasons:
            reasons.append("đây là một lựa chọn cân bằng giữa các yếu tố")

        recommendations_list.append({
            "rank": f"{i+1}. Lựa chọn hàng đầu",
            "name": combo_info['name'],
            "score": score,
            "subjects": ', '.join(combo_info['subjects']),
            "reason": f"Tổ hợp này {', và '.join(reasons)}."
        })

    return {
        "analysis": analysis_lines,
        "recommendations": recommendations_list
    }