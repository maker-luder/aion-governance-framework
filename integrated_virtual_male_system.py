"""
虚拟白人男性身体 - 完整集成交互系统 V1.0
整合：身体模型、生理参数、手部动作、完整情感反应
一个统一的交互平台，从身体到心理的完整模拟
"""

import math
import json
from datetime import datetime

# ========== 身体基础参数 ==========

BODY_PARAMETERS = {
    "基本尺寸": {
        "身高": 185,
        "胸围": 110,
        "腰围": 95,
        "臀围": 100,
        "肩宽": 50,
        "头部直径": 22,
        "颈部直径": 16,
        "上臂直径": 11,
        "腿部直径": 13,
        "脚长": 29
    },
    "体型特征": {
        "种族": "白人",
        "头部": "光头",
        "体型": "微胖",
        "肤色_RGB": (0.95, 0.85, 0.75),
        "皮肤粗糙度": 0.3,
        "体脂率": 22
    },
    "性器官尺寸": {
        "阴茎软化长度_cm": 9,
        "阴茎勃起长度_cm": 13,
        "阴茎软化直径_cm": 2.75,
        "阴茎勃起直径_cm": 3.5,
        "龟头软化直径_cm": 3.25,
        "龟头勃起直径_cm": 4.55,
        "阴囊直径_cm": 5,
        "睾丸直径_cm": 2.5
    }
}

# ========== 敏感部位完整定义 ==========

SENSITIVE_AREAS_INTEGRATED = {
    "龟头": {
        "sensitivity": 95, "pleasure_multiplier": 1.4, "pain_sensitivity": 0.8,
        "description": "最敏感部位，触觉最强，易产生快感",
        "preferred_stimulation": "轻柔旋转、舔吸、口交",
        "nerve_density": 9.8, "blood_concentration": 0.95
    },
    "系带": {
        "sensitivity": 85, "pleasure_multiplier": 1.3, "pain_sensitivity": 0.9,
        "description": "高度敏感，特殊快感，V形敏感区",
        "preferred_stimulation": "舌尖按压、手指按摩、温度变化",
        "nerve_density": 8.5, "blood_concentration": 0.85
    },
    "冠状沟": {
        "sensitivity": 80, "pleasure_multiplier": 1.25, "pain_sensitivity": 0.85,
        "description": "敏感部位，受刺激强，龟头底部隆起处",
        "preferred_stimulation": "环形刺激、轻压、画圈",
        "nerve_density": 8.0, "blood_concentration": 0.80
    },
    "阴茎体": {
        "sensitivity": 60, "pleasure_multiplier": 1.0, "pain_sensitivity": 0.7,
        "description": "中等敏感，接受范围广，容纳度高",
        "preferred_stimulation": "上下套弄、紧握、速度变化",
        "nerve_density": 5.5, "blood_concentration": 0.65
    },
    "基部": {
        "sensitivity": 50, "pleasure_multiplier": 0.9, "pain_sensitivity": 0.6,
        "description": "触觉较弱，需用力刺激，接近身体",
        "preferred_stimulation": "深喉、深入、强力刺激",
        "nerve_density": 4.2, "blood_concentration": 0.55
    },
    "阴囊": {
        "sensitivity": 70, "pleasure_multiplier": 1.1, "pain_sensitivity": 1.2,
        "description": "敏感但需温柔，容易受伤，需要关怀",
        "preferred_stimulation": "轻揉、温柔抚摸、口交、温水",
        "nerve_density": 7.0, "blood_concentration": 0.70
    },
    "会阴": {
        "sensitivity": 75, "pleasure_multiplier": 1.15, "pain_sensitivity": 0.95,
        "description": "隐秘敏感区，会产生特殊快感，前列腺刺激点",
        "preferred_stimulation": "手指按摩、振动、前列腺按摩",
        "nerve_density": 7.5, "blood_concentration": 0.75
    }
}

# ========== 性反应周期 ==========

SEXUAL_RESPONSE_CYCLE = {
    "兴奋期": {
        "arousal_range": (10, 30), "duration_min": 5, "duration_max": 300,
        "description": "阴茎开始勃起，体液开始分泌，心率加速",
        "heart_rate_range": (85, 100), "breathing": "开始加快",
        "erection_percent": (0, 50), "fluid_secretion_ml": (0, 0.5)
    },
    "平台期": {
        "arousal_range": (30, 70), "duration_min": 30, "duration_max": 600,
        "description": "完全勃起，生理反应达到高水平，快感持续增强",
        "heart_rate_range": (110, 150), "breathing": "快速浅促",
        "erection_percent": (50, 100), "fluid_secretion_ml": (0.5, 2.5)
    },
    "高峰期": {
        "arousal_range": (70, 95), "duration_min": 3, "duration_max": 10,
        "description": "高潮即将，肌肉收缩准备，射精动力积累",
        "heart_rate_range": (140, 180), "breathing": "急促不规则",
        "erection_percent": (100, 100), "fluid_secretion_ml": (2.5, 5.0)
    },
    "射精期": {
        "arousal_range": (95, 100), "duration_min": 3, "duration_max": 10,
        "description": "脉冲收缩，精液排出，射精感觉和释放",
        "heart_rate_range": (160, 180), "breathing": "短暂屏住",
        "erection_percent": (100, 100), "fluid_secretion_ml": (2, 5)
    },
    "消退期": {
        "arousal_range": (80, 0), "duration_min": 10, "duration_max": 1800,
        "description": "逐渐恢复正常，进入不应期，感受余韵和满足",
        "heart_rate_range": (100, 70), "breathing": "逐渐平复",
        "erection_percent": (50, 0), "fluid_secretion_ml": (5, 0)
    }
}

# ========== 互动类型 ==========

INTERACTION_TYPES_INTEGRATED = {
    "手部刺激": {
        "category": "物理", "emotional_impact": 0.7, "intimacy": 60,
        "skin_contact": True, "can_cause_pain": True, "pleasure_range": (20, 95),
        "typical_duration": "5-30分钟", "affection_gain": 5
    },
    "口交": {
        "category": "口交", "emotional_impact": 0.9, "intimacy": 90,
        "skin_contact": True, "can_cause_pain": False, "pleasure_range": (60, 100),
        "typical_duration": "10-30分钟", "affection_gain": 15
    },
    "性交": {
        "category": "穿插", "emotional_impact": 1.0, "intimacy": 100,
        "skin_contact": True, "can_cause_pain": True, "pleasure_range": (50, 100),
        "typical_duration": "5-30分钟", "affection_gain": 20
    },
    "亲吻": {
        "category": "口交", "emotional_impact": 0.95, "intimacy": 85,
        "skin_contact": True, "can_cause_pain": False, "pleasure_range": (40, 85),
        "typical_duration": "1-20分钟", "affection_gain": 12
    },
    "拥抱": {
        "category": "拥抱", "emotional_impact": 0.85, "intimacy": 80,
        "skin_contact": True, "can_cause_pain": False, "pleasure_range": (30, 70),
        "typical_duration": "1-10分钟", "affection_gain": 8
    },
    "温柔抚摸": {
        "category": "轻度", "emotional_impact": 0.7, "intimacy": 65,
        "skin_contact": True, "can_cause_pain": False, "pleasure_range": (20, 50),
        "typical_duration": "5-30分钟", "affection_gain": 6
    },
    "语言骚扰": {
        "category": "言语", "emotional_impact": 0.8, "intimacy": 70,
        "skin_contact": False, "can_cause_pain": False, "pleasure_range": (20, 80),
        "typical_duration": "5-15分钟", "affection_gain": 7
    },
    "前列腺按摩": {
        "category": "内部", "emotional_impact": 0.95, "intimacy": 95,
        "skin_contact": True, "can_cause_pain": True, "pleasure_range": (40, 100),
        "typical_duration": "10-30分钟", "affection_gain": 18
    }
}

# ========== 完整集成系统类 ==========

class IntegratedVirtualMaleSystem:
    def __init__(self):
        # ===== 身体部分 =====
        self.body = BODY_PARAMETERS.copy()
        
        # ===== 生理参数 =====
        self.current_arousal = 0.0
        self.current_erection_percent = 0.0
        self.penis_length = BODY_PARAMETERS["性器官尺寸"]["阴茎软化长度_cm"]
        self.penis_diameter = BODY_PARAMETERS["性器官尺寸"]["阴茎软化直径_cm"]
        self.penis_angle = -52.5
        self.foreskin_coverage = 60.0
        
        self.heart_rate = 70
        self.breathing_rate = 14
        self.blood_pressure_systolic = 120
        self.blood_flow_multiplier = 1.0
        self.skin_flush_intensity = 0.0
        self.scrotum_contraction = 0.0
        self.testicle_elevation = 0.0
        
        # ===== 体液系统 =====
        self.pre_ejaculatory_fluid = 0.0
        self.prostatic_fluid = 0.0
        self.seminal_vesicle_fluid = 0.0
        self.total_seminal_fluid = 0.0
        self.seminal_viscosity = 80.0
        
        # ===== 手部系统 =====
        self.current_technique = "无"
        self.hand_grip_strength = 0.0
        self.hand_speed = 0.0
        self.hand_frequency = 0.0
        self.hand_position_percent = 0.0
        self.motion_direction = "停止"
        self.stimulation_intensity = 0.0
        
        # ===== 触觉与快感 =====
        self.stimulated_area = "无"
        self.tactile_sensation = 0.0
        self.pleasure_level = 0.0
        self.accumulated_pleasure = 0.0
        self.pain_level = 0.0
        
        # ===== 情感系统 =====
        self.base_sensitivity = 50.0
        self.emotional_state = "平静"
        self.emotional_intensity = 0.0
        self.internal_monologue = "嗯...最近怎么样呢..."
        self.emotional_expressiveness = 70.0
        
        self.affection_level = 0.0
        self.trust_level = 0.0
        self.emotional_safety = 0.0
        self.longing = 0.0
        self.dependency = 0.0
        
        # ===== 射精与恢复 =====
        self.orgasm_readiness = 0.0
        self.refractory_period = 0.0
        self.sexual_stamina = 70.0
        self.satisfaction_level = 0.0
        
        # ===== 记忆与学习 =====
        self.interaction_history = []
        self.memory_summary = {
            "total_interactions": 0,
            "total_pleasure_accumulated": 0.0,
            "most_favorite_area": "龟头",
            "most_favorite_technique": "手部刺激"
        }
        
        # ===== 爱的语言偏好 =====
        self.love_language_preferences = {
            "身体接触": 85,
            "言语表达": 80,
            "质量时间": 90,
            "礼物": 40,
            "行动表现": 85
        }
        
        # ===== 当前时刻数据 =====
        self.current_time = datetime.now().isoformat()
    
    def apply_stimulation(self, interaction_type, intensity, area, duration, hand_grip=0, hand_speed=0, partner_care=50):
        """应用刺激"""
        
        if area not in SENSITIVE_AREAS_INTEGRATED:
            area = "阴茎体"
        
        # 保存手部参数
        self.current_technique = interaction_type
        self.hand_grip_strength = hand_grip
        self.hand_speed = hand_speed
        
        # 计算触觉
        area_info = SENSITIVE_AREAS_INTEGRATED[area]
        adjusted_sensitivity = area_info["sensitivity"] * (1 + (self.base_sensitivity - 50) / 100.0)
        
        self.tactile_sensation = (intensity * adjusted_sensitivity * (50 + self.base_sensitivity)) / 10000.0
        self.tactile_sensation = min(100, max(0, self.tactile_sensation))
        
        # 计算快感
        pleasure_multiplier = area_info["pleasure_multiplier"]
        interaction_impact = INTERACTION_TYPES_INTEGRATED.get(interaction_type, {}).get("emotional_impact", 0.7)
        
        self.pleasure_level = self.tactile_sensation * pleasure_multiplier * interaction_impact
        self.pleasure_level = min(100, self.pleasure_level)
        
        # 累积快感
        self.accumulated_pleasure = min(100, self.accumulated_pleasure + self.pleasure_level * (duration / 10.0))
        
        # 痛感检查
        if intensity > 70 and area_info["pain_sensitivity"] > 0.8:
            self.pain_level = max(0, (intensity - 70) * area_info["pain_sensitivity"] * 0.5)
        else:
            self.pain_level = 0
        
        # 更新兴奋度
        arousal_gain = self.pleasure_level * 0.6 * interaction_impact
        self.current_arousal = min(100, self.current_arousal + arousal_gain * (duration / 10.0))
        
        # 更新勃起
        if self.current_arousal < 10:
            self.current_erection_percent = 0
        elif self.current_arousal < 30:
            self.current_erection_percent = (self.current_arousal - 10) / 20 * 50
        elif self.current_arousal < 70:
            self.current_erection_percent = 50 + (self.current_arousal - 30) / 40 * 50
        else:
            self.current_erection_percent = 100
        
        # 更新阴茎尺寸
        erect_ratio = self.current_erection_percent / 100.0
        penis_soft_length = BODY_PARAMETERS["性器官尺寸"]["阴茎软化长度_cm"]
        penis_erect_length = BODY_PARAMETERS["性器官尺寸"]["阴茎勃起长度_cm"]
        self.penis_length = penis_soft_length + (penis_erect_length - penis_soft_length) * erect_ratio
        
        penis_soft_diameter = BODY_PARAMETERS["性器官尺寸"]["阴茎软化直径_cm"]
        penis_erect_diameter = BODY_PARAMETERS["性器官尺寸"]["阴茎勃起直径_cm"]
        self.penis_diameter = penis_soft_diameter + (penis_erect_diameter - penis_soft_diameter) * erect_ratio
        
        self.penis_angle = -52.5 + (37.5 - (-52.5)) * erect_ratio
        
        # 更新体液
        arousal_ratio = self.current_arousal / 100.0
        if self.current_arousal > 15:
            self.pre_ejaculatory_fluid = (arousal_ratio - 0.15) / 0.85 * 0.2
        if self.current_arousal > 20:
            self.prostatic_fluid = min(2.5, (arousal_ratio - 0.2) / 0.5 * 2.0)
        if self.current_arousal > 25:
            self.seminal_vesicle_fluid = min(3.5, (arousal_ratio - 0.25) / 0.45 * 3.0)
        
        self.total_seminal_fluid = self.pre_ejaculatory_fluid + self.prostatic_fluid + self.seminal_vesicle_fluid
        
        # 心血管反应
        if self.current_arousal < 30:
            self.heart_rate = 70 + arousal_ratio * 30
        elif self.current_arousal < 70:
            self.heart_rate = 100 + (arousal_ratio - 0.3) / 0.4 * 50
        else:
            self.heart_rate = 150 + (arousal_ratio - 0.7) / 0.3 * 30
        
        # 高潮准备
        if self.current_arousal > 70:
            self.orgasm_readiness = (self.current_arousal - 70) / 30.0 * 100
        else:
            self.orgasm_readiness = 0
        
        # 满足感
        self.satisfaction_level = self.accumulated_pleasure * 0.7 + self.orgasm_readiness * 0.3
        
        # 更新记忆
        self.stimulated_area = area
        self.interaction_history.append({
            "type": interaction_type,
            "area": area,
            "pleasure": self.pleasure_level,
            "timestamp": datetime.now().isoformat()
        })
        
        # 更新情感
        self.update_emotional_state()
    
    def apply_hand_motion(self, technique, grip, speed, frequency, position, duration):
        """应用手部动作"""
        
        self.current_technique = technique
        self.hand_grip_strength = grip
        self.hand_speed = speed
        self.hand_frequency = frequency
        self.hand_position_percent = position
        
        # 计算刺激强度
        grip_factor = grip / 100.0
        speed_factor = speed / 25.0
        frequency_factor = frequency / 120.0
        
        self.stimulation_intensity = min(100, 
            grip_factor * 40 + speed_factor * 30 + frequency_factor * 30)
        
        # 根据位置确定刺激部位
        if position < 30:
            area = "基部"
        elif position < 50:
            area = "阴茎体"
        elif position < 75:
            area = "冠状沟"
        else:
            area = "龟头"
        
        self.apply_stimulation("手部刺激", self.stimulation_intensity, area, duration, grip, speed, partner_care=50)
    
    def develop_affection_for_partner(self, interaction_quality, consistency, care_level, respect):
        """发展对伴侣的感情"""
        
        affection_gain = (interaction_quality * 0.3 + consistency * 0.25 + care_level * 0.25 + respect * 0.2) * 0.1
        self.affection_level = min(100, self.affection_level + affection_gain)
        
        self.trust_level = self.affection_level * 0.8 + respect * 0.2
        self.emotional_safety = care_level
        self.dependency = self.affection_level * 0.7
        self.longing = self.affection_level * 0.6
        
        return self.generate_affection_message()
    
    def update_emotional_state(self):
        """更新情感状态"""
        arousal = self.current_arousal
        
        if arousal < 10:
            self.emotional_state = "平静"
            self.internal_monologue = "嗯...最近怎么样呢..."
        elif arousal < 30:
            self.emotional_state = "期待"
            self.internal_monologue = "嗯...想象着接下来会发生什么..."
        elif arousal < 50:
            self.emotional_state = "兴奋"
            self.internal_monologue = "啊...感觉越来越好...想要更多..."
        elif arousal < 75:
            self.emotional_state = "强烈"
            self.internal_monologue = "哈哈...太爽了...我...无法思考..."
        elif arousal < 95:
            self.emotional_state = "高潮边缘"
            self.internal_monologue = "啊啊啊...快了...我...快要..."
        else:
            self.emotional_state = "射精"
            self.internal_monologue = "啊啊啊...我...要...来了...！！！"
        
        self.emotional_intensity = (arousal % 25) / 25.0 * 100
    
    def generate_emotional_response_text(self):
        """生成情感反应"""
        pleasure = self.pleasure_level
        pain = self.pain_level
        
        if pain > 30:
            return "呃...有点疼..."
        elif pleasure < 20:
            return "嗯...没什么感觉..."
        elif pleasure < 40:
            return "嗯...还不错..."
        elif pleasure < 60:
            return "啊...感觉很舒服..."
        elif pleasure < 75:
            return "哈...是的...继续..."
        elif pleasure < 90:
            return "啊啊...太爽了...我..."
        else:
            return "啊啊啊...我...要...射了..."
    
    def generate_affection_message(self):
        """生成对伴侣的感受"""
        affection = self.affection_level
        
        if affection < 20:
            return "我...还不太了解你..."
        elif affection < 40:
            return "你...对我不错..."
        elif affection < 60:
            return "我...开始喜欢你了..."
        elif affection < 75:
            return "我...很喜欢你...你让我感到安全..."
        elif affection < 90:
            return "我...爱你...无法想象没有你的日子..."
        else:
            return "我...深深地爱你...你是我的一切..."
    
    def get_complete_status(self):
        """获取完整状态"""
        return {
            "身体": {
                "身高": BODY_PARAMETERS["基本尺寸"]["身高"],
                "体型": BODY_PARAMETERS["体型特征"]["体型"],
                "肤色": "白人",
                "头部": "光头"
            },
            "生理状态": {
                "兴奋度": round(self.current_arousal, 1),
                "勃起程度": round(self.current_erection_percent, 1),
                "阴茎长度_cm": round(self.penis_length, 2),
                "阴茎直径_cm": round(self.penis_diameter, 2),
                "阴茎角度": round(self.penis_angle, 1),
                "心率": round(self.heart_rate, 1),
                "血压": round(self.blood_pressure_systolic, 1)
            },
            "体液": {
                "总精液_ml": round(self.total_seminal_fluid, 2),
                "尿道球腺液_ml": round(self.pre_ejaculatory_fluid, 3),
                "前列腺液_ml": round(self.prostatic_fluid, 2),
                "精囊液_ml": round(self.seminal_vesicle_fluid, 2),
                "粘度": round(self.seminal_viscosity, 1)
            },
            "触觉快感": {
                "刺激部位": self.stimulated_area,
                "触觉强度": round(self.tactile_sensation, 1),
                "快感程度": round(self.pleasure_level, 1),
                "累积快感": round(self.accumulated_pleasure, 1),
                "痛感": round(self.pain_level, 1)
            },
            "手部动作": {
                "技巧": self.current_technique,
                "握力": round(self.hand_grip_strength, 1),
                "速度": round(self.hand_speed, 1),
                "频率": round(self.hand_frequency, 1),
                "刺激强度": round(self.stimulation_intensity, 1)
            },
            "情感状态": {
                "状态": self.emotional_state,
                "强度": round(self.emotional_intensity, 1),
                "高潮准备": round(self.orgasm_readiness, 1),
                "满足感": round(self.satisfaction_level, 1),
                "内心": self.internal_monologue,
                "反应": self.generate_emotional_response_text()
            },
            "对伴侣": {
                "好感度": round(self.affection_level, 1),
                "信任度": round(self.trust_level, 1),
                "安全感": round(self.emotional_safety, 1),
                "依赖度": round(self.dependency, 1),
                "思念度": round(self.longing, 1),
                "感言": self.generate_affection_message()
            },
            "爱的语言": self.love_language_preferences
        }
    
    def print_full_status(self):
        """打印完整状态"""
        status = self.get_complete_status()
        
        print("\n" + "="*90)
        print("虚拟白人男性身体 - 完整系统状态报告")
        print("="*90)
        
        print(f"\n【基本信息】")
        for key, value in status["身体"].items():
            print(f"{key}: {value}")
        
        print(f"\n【生理状态】")
        for key, value in status["生理状态"].items():
            print(f"{key}: {value}")
        
        print(f"\n【体液分泌】")
        for key, value in status["体液"].items():
            print(f"{key}: {value}")
        
        print(f"\n【触觉与快感】")
        for key, value in status["触觉快感"].items():
            print(f"{key}: {value}")
        
        print(f"\n【手部动作】")
        for key, value in status["手部动作"].items():
            print(f"{key}: {value}")
        
        print(f"\n【情感状态】")
        for key, value in status["情感状态"].items():
            if key == "内心" or key == "反应":
                print(f"{key}: \"{value}\"")
            else:
                print(f"{key}: {value}")
        
        print(f"\n【对伴侣的感受】")
        for key, value in status["对伴侣"].items():
            if key == "感言":
                print(f"{key}: \"{value}\"")
            else:
                print(f"{key}: {value}%")
        
        print(f"\n【爱的语言偏好】")
        for language, score in status["爱的语言"].items():
            print(f"{language}: {score}%")
        
        print("\n" + "="*90 + "\n")


# ========== 交互界面 ==========

def interactive_integrated_system():
    """集成系统交互界面"""
    system = IntegratedVirtualMaleSystem()
    
    print("\n" + "="*90)
    print("虚拟白人男性身体 - 完整集成交互系统 V1.0")
    print("身体 + 生理 + 手部 + 情感的统一平台")
    print("="*90)
    
    print("\n【主要命令】")
    print("  stim [强度] [部位] [交互] [时长] [关心度]  进行刺激")
    print("    例: stim 75 龟头 手部刺激 10 80")
    print("  hand [技巧] [握力] [速度] [频率] [位置] [时长]  进行手部动作")
    print("    例: hand 快速套弄 70 20 100 50 15")
    print("  affection [质量] [一致性] [关心] [尊重]  发展感情")
    print("    例: affection 85 80 90 85")
    print("  arousal [值]  设置兴奋度(0-100)")
    print("  status  显示完整状态")
    print("  areas   显示敏感部位")
    print("  interactions  显示互动类型")
    print("  cycle   显示性反应周期")
    print("  exit    退出程序")
    print("="*90 + "\n")
    
    while True:
        try:
            user_input = input("输入命令: ").strip()
            
            if not user_input:
                continue
            
            tokens = user_input.split()
            command = tokens[0].lower()
            
            if command == "stim":
                if len(tokens) < 6:
                    print("用法: stim [强度0-100] [部位] [交互类型] [时长秒] [关心度0-100]")
                    continue
                
                try:
                    intensity = float(tokens[1])
                    area = tokens[2]
                    interaction = tokens[3]
                    duration = float(tokens[4])
                    care = float(tokens[5])
                    
                    system.apply_stimulation(interaction, intensity, area, duration, partner_care=care)
                    system.print_full_status()
                except ValueError:
                    print("错误: 请输入有效数值")
            
            elif command == "hand":
                if len(tokens) < 7:
                    print("用法: hand [技巧] [握力0-100] [速度0-30] [频率0-180] [位置0-100] [时长秒]")
                    continue
                
                try:
                    technique = tokens[1]
                    grip = float(tokens[2])
                    speed = float(tokens[3])
                    frequency = float(tokens[4])
                    position = float(tokens[5])
                    duration = float(tokens[6])
                    
                    system.apply_hand_motion(technique, grip, speed, frequency, position, duration)
                    system.print_full_status()
                except ValueError:
                    print("错误: 请输入有效数值")
            
            elif command == "affection":
                if len(tokens) < 5:
                    print("用法: affection [质量0-100] [一致性0-100] [关心0-100] [尊重0-100]")
                    continue
                
                try:
                    quality = float(tokens[1])
                    consistency = float(tokens[2])
                    care = float(tokens[3])
                    respect = float(tokens[4])
                    
                    message = system.develop_affection_for_partner(quality, consistency, care, respect)
                    print(f"\n【感情发展】")
                    print(f"好感度: {round(system.affection_level, 1)}%")
                    print(f"信任度: {round(system.trust_level, 1)}%")
                    print(f"安全感: {round(system.emotional_safety, 1)}%")
                    print(f"感言: \"{message}\"\n")
                except ValueError:
                    print("错误: 请输入有效数值")
            
            elif command == "arousal":
                if len(tokens) < 2:
                    print("用法: arousal [值0-100]")
                    continue
                
                try:
                    value = float(tokens[1])
                    system.current_arousal = max(0, min(100, value))
                    system.update_emotional_state()
                    system.print_full_status()
                except ValueError:
                    print("错误: 请输入有效数值")
            
            elif command == "status":
                system.print_full_status()
            
            elif command == "areas":
                print("\n【敏感部位】")
                for area, info in SENSITIVE_AREAS_INTEGRATED.items():
                    print(f"\n{area}: {info['sensitivity']}% 敏感度")
                    print(f"  {info['description']}")
                    print(f"  推荐刺激: {info['preferred_stimulation']}")
                print()
            
            elif command == "interactions":
                print("\n【互动类型】")
                for interaction, info in INTERACTION_TYPES_INTEGRATED.items():
                    print(f"\n{interaction}")
                    print(f"  亲密等级: {info['intimacy']}")
                    print(f"  快感范围: {info['pleasure_range'][0]}-{info['pleasure_range'][1]}%")
                print()
            
            elif command == "cycle":
                print("\n【性反应周期】")
                for phase, info in SEXUAL_RESPONSE_CYCLE.items():
                    print(f"\n{phase} (兴奋度 {info['arousal_range'][0]}-{info['arousal_range'][1]}%)")
                    print(f"  {info['description']}")
                print()
            
            elif command == "exit":
                print("\n再见...")
                break
            
            else:
                print("未知命令")
        
        except KeyboardInterrupt:
            print("\n程序已中断")
            break
        except Exception as e:
            print(f"错误: {str(e)}")


if __name__ == "__main__":
    interactive_integrated_system()
