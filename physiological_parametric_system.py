"""
毛茸茸机器人男性模型 生理参数化系统
可实时调整勃起程度、性兴奋水平，计算所有生理反应参数
"""

import bpy
import math
from mathutils import Vector

# ========== 生理参数常量定义 ==========

# 基础尺寸
SCALE = 0.01
HEIGHT = 185 * SCALE
PENIS_SOFT_LENGTH = 9 * SCALE  # 软化状态平均长度(厘米)
PENIS_ERECT_LENGTH = 13 * SCALE  # 勃起状态长度(厘米)
PENIS_SOFT_DIAMETER = 2.75 * SCALE  # 软化直径(厘米)
PENIS_ERECT_DIAMETER = 3.5 * SCALE  # 勃起直径(厘米)
PENIS_HEAD_SOFT_DIAMETER = 3.25 * SCALE  # 龟头软化直径(厘米)
PENIS_HEAD_ERECT_DIAMETER = 4.55 * SCALE  # 龟头勃起直径(厘米)

# 基础分泌液体
SEMINAL_FLUID_TOTAL_MIN = 2 * 0.001  # 最少精液体积(升)
SEMINAL_FLUID_TOTAL_MAX = 5 * 0.001  # 最多精液体积(升)
PROSTATIC_FLUID_RATIO = 0.27  # 前列腺液占比
SEMINAL_VESICLE_FLUID_RATIO = 0.70  # 精囊液占比
COWPER_FLUID_VOLUME = 0.0001  # 尿道球腺液体积(升)

# ========== 生理参数化类 ==========

class PhysiologicalSystem:
    def __init__(self):
        # 主要控制参数
        self.arousal_level = 0.0  # 性兴奋水平 0-100
        self.erection_level = 0.0  # 勃起程度 0-100
        self.time_elapsed = 0.0  # 经过时间(秒)
        
        # 生成的生理参数
        self.penis_length = PENIS_SOFT_LENGTH
        self.penis_diameter = PENIS_SOFT_DIAMETER
        self.penis_head_diameter = PENIS_HEAD_SOFT_DIAMETER
        self.penis_erection_angle = 0  # 度数
        self.foreskin_coverage = 100  # 包皮覆盖比例 0-100%
        
        # 身体反应参数
        self.heart_rate = 70  # 心率 次/分钟
        self.breathing_rate = 14  # 呼吸频率 次/分钟
        self.systolic_pressure = 120  # 收缩压 mmHg
        self.blood_flow_rate = 1.0  # 血流相对速度倍数
        self.skin_flush_intensity = 0.0  # 皮肤潮红强度 0-100
        self.scrotum_contraction = 0.0  # 阴囊收缩程度 0-100
        self.testicle_elevation = 0.0  # 睾丸上升程度 0-100
        
        # 体液分泌参数
        self.pre_ejaculatory_fluid = 0.0  # 尿道球腺液 毫升
        self.prostatic_fluid = 0.0  # 前列腺液 毫升
        self.seminal_vesicle_fluid = 0.0  # 精囊液 毫升
        self.total_seminal_fluid = 0.0  # 总精液量 毫升
        self.seminal_fluid_viscosity = 0.0  # 精液粘度 0-100
        self.seminal_fluid_liquefaction = 0.0  # 精液液化程度 0-100
        
        # 精子参数
        self.sperm_count = 0  # 精子总数 百万
        self.sperm_motility = 0  # 精子活动力 %
        self.sperm_morphology = 0  # 精子正常形态 %
        
        # 射精相关
        self.ejaculation_readiness = 0.0  # 射精准备度 0-100
        self.ejaculation_force = 0.0  # 射精强度 0-100
        self.ejaculation_distance = 0.0  # 射程 厘米
        self.post_ejaculation_recovery = 0.0  # 射精后恢复程度 0-100
    
    def calculate_from_arousal(self, arousal_value):
        """根据性兴奋水平计算所有生理参数"""
        self.arousal_level = max(0, min(100, arousal_value))
        
        # 性兴奋水平 0-30: 兴奋期
        # 性兴奋水平 30-70: 平台期
        # 性兴奋水平 70-95: 射精期
        # 性兴奋水平 95-100: 完全射精
        
        self._calculate_erection_level()
        self._calculate_penis_dimensions()
        self._calculate_body_responses()
        self._calculate_fluid_secretion()
        self._calculate_ejaculation_parameters()
    
    def _calculate_erection_level(self):
        """计算勃起程度"""
        if self.arousal_level < 10:
            self.erection_level = 0
        elif self.arousal_level < 30:
            # 兴奋期：勃起逐渐增加
            self.erection_level = (self.arousal_level - 10) / 20 * 50
        elif self.arousal_level < 70:
            # 平台期：勃起快速增加到完全
            self.erection_level = 50 + (self.arousal_level - 30) / 40 * 50
        else:
            # 射精期及之后：完全勃起
            self.erection_level = 100
        
        self.erection_level = max(0, min(100, self.erection_level))
    
    def _calculate_penis_dimensions(self):
        """根据勃起程度计算阴茎尺寸"""
        erect_ratio = self.erection_level / 100.0
        
        # 长度变化(厘米)
        self.penis_length = PENIS_SOFT_LENGTH + (PENIS_ERECT_LENGTH - PENIS_SOFT_LENGTH) * erect_ratio
        
        # 直径变化(厘米)
        self.penis_diameter = PENIS_SOFT_DIAMETER + (PENIS_ERECT_DIAMETER - PENIS_SOFT_DIAMETER) * erect_ratio
        
        # 龟头直径变化(厘米)
        self.penis_head_diameter = PENIS_HEAD_SOFT_DIAMETER + (PENIS_HEAD_ERECT_DIAMETER - PENIS_HEAD_SOFT_DIAMETER) * erect_ratio
        
        # 勃起角度(度数)
        # 软化：向下 45-60 度 → 勃起：向上 30-45 度
        min_angle = -52.5  # 平均下垂角度
        max_angle = 37.5   # 平均勃起角度
        self.penis_erection_angle = min_angle + (max_angle - min_angle) * erect_ratio
        
        # 包皮覆盖比例
        # 软化状态：覆盖 50-70% → 勃起状态：覆盖 0-20%
        if erect_ratio < 0.3:
            self.foreskin_coverage = 60 - erect_ratio * 30
        elif erect_ratio < 0.7:
            self.foreskin_coverage = 50 - (erect_ratio - 0.3) * 25
        else:
            self.foreskin_coverage = 45 - (erect_ratio - 0.7) * 45
        
        self.foreskin_coverage = max(0, min(100, self.foreskin_coverage))
    
    def _calculate_body_responses(self):
        """计算身体的全身反应"""
        arousal_ratio = self.arousal_level / 100.0
        
        # 心率变化
        # 静息 70 → 兴奋 100-150 → 平台期 120-160 → 射精 150-180
        if self.arousal_level < 30:
            self.heart_rate = 70 + arousal_ratio * 30
        elif self.arousal_level < 70:
            self.heart_rate = 100 + (arousal_ratio - 0.3) / 0.4 * 50
        else:
            self.heart_rate = 150 + (arousal_ratio - 0.7) / 0.3 * 30
        
        # 呼吸频率
        # 静息 14 → 兴奋 20 → 平台期 30-40 → 射精 40
        if self.arousal_level < 30:
            self.breathing_rate = 14 + arousal_ratio * 6
        elif self.arousal_level < 70:
            self.breathing_rate = 20 + (arousal_ratio - 0.3) / 0.4 * 15
        else:
            self.breathing_rate = 35 + (arousal_ratio - 0.7) / 0.3 * 5
        
        # 血压变化(收缩压)
        # 静息 120 → 兴奋 140-180 → 射精 180-200
        if self.arousal_level < 30:
            self.systolic_pressure = 120 + arousal_ratio * 20
        elif self.arousal_level < 70:
            self.systolic_pressure = 140 + (arousal_ratio - 0.3) / 0.4 * 40
        else:
            self.systolic_pressure = 180 + (arousal_ratio - 0.7) / 0.3 * 20
        
        # 血流速度倍数
        # 静息 1x → 兴奋 20x → 射精 40-60x
        if self.arousal_level < 30:
            self.blood_flow_rate = 1 + arousal_ratio * 19
        elif self.arousal_level < 70:
            self.blood_flow_rate = 20 + (arousal_ratio - 0.3) / 0.4 * 20
        else:
            self.blood_flow_rate = 40 + (arousal_ratio - 0.7) / 0.3 * 20
        
        # 皮肤潮红强度
        # 0% → 兴奋期30% → 平台期 60% → 射精期 100%
        self.skin_flush_intensity = min(100, arousal_ratio * 120)
        
        # 阴囊收缩程度
        # 0% → 兴奋期 20% → 平台期 60% → 射精期 100%
        if self.arousal_level < 30:
            self.scrotum_contraction = arousal_ratio * 20 / 0.3
        elif self.arousal_level < 70:
            self.scrotum_contraction = 20 + (arousal_ratio - 0.3) / 0.4 * 40
        else:
            self.scrotum_contraction = 60 + (arousal_ratio - 0.7) / 0.3 * 40
        
        self.scrotum_contraction = min(100, self.scrotum_contraction)
        
        # 睾丸上升程度
        # 0% → 兴奋期 30% → 平台期 70% → 射精期 100%
        if self.arousal_level < 30:
            self.testicle_elevation = arousal_ratio * 30 / 0.3
        elif self.arousal_level < 70:
            self.testicle_elevation = 30 + (arousal_ratio - 0.3) / 0.4 * 40
        else:
            self.testicle_elevation = 70 + (arousal_ratio - 0.7) / 0.3 * 30
        
        self.testicle_elevation = min(100, self.testicle_elevation)
    
    def _calculate_fluid_secretion(self):
        """计算体液分泌"""
        arousal_ratio = self.arousal_level / 100.0
        
        # 尿道球腺液(库珀腺)
        # 兴奋期开始分泌，逐渐增加
        if self.arousal_level > 15:
            self.pre_ejaculatory_fluid = (arousal_ratio - 0.15) / 0.85 * 0.2
        else:
            self.pre_ejaculatory_fluid = 0
        
        self.pre_ejaculatory_fluid = min(0.2, self.pre_ejaculatory_fluid)
        
        # 前列腺液
        # 兴奋期开始，平台期达到峰值
        if self.arousal_level > 20:
            if self.arousal_level < 70:
                self.prostatic_fluid = (arousal_ratio - 0.2) / 0.5 * 2.0
            else:
                self.prostatic_fluid = 2.0
        else:
            self.prostatic_fluid = 0
        
        self.prostatic_fluid = min(2.5, self.prostatic_fluid)
        
        # 精囊液
        # 兴奋期开始，平台期达到峰值
        if self.arousal_level > 25:
            if self.arousal_level < 70:
                self.seminal_vesicle_fluid = (arousal_ratio - 0.25) / 0.45 * 3.0
            else:
                self.seminal_vesicle_fluid = 3.0
        else:
            self.seminal_vesicle_fluid = 0
        
        self.seminal_vesicle_fluid = min(3.5, self.seminal_vesicle_fluid)
        
        # 总精液量
        self.total_seminal_fluid = (self.pre_ejaculatory_fluid + self.prostatic_fluid + self.seminal_vesicle_fluid)
        self.total_seminal_fluid = min(5.0, self.total_seminal_fluid)
        
        # 精液粘度
        # 新鲜精液：粘稠(80) → 液化(20)
        # 随时间液化，30分钟完全液化
        if self.arousal_level > 25:
            self.seminal_fluid_viscosity = 80 - (self.arousal_level - 25) / 75 * 30
        else:
            self.seminal_fluid_viscosity = 80
        
        self.seminal_fluid_viscosity = max(20, min(100, self.seminal_fluid_viscosity))
        
        # 精液液化程度
        if self.arousal_level > 25:
            self.seminal_fluid_liquefaction = (self.arousal_level - 25) / 75 * 80
        else:
            self.seminal_fluid_liquefaction = 0
        
        self.seminal_fluid_liquefaction = min(80, self.seminal_fluid_liquefaction)
    
    def _calculate_ejaculation_parameters(self):
        """计算射精相关参数"""
        arousal_ratio = self.arousal_level / 100.0
        
        # 射精准备度(0-70%兴奋度时准备，70%开始射精)
        if self.arousal_level < 70:
            self.ejaculation_readiness = min(90, arousal_ratio / 0.7 * 90)
        else:
            self.ejaculation_readiness = 90 + (arousal_ratio - 0.7) / 0.3 * 10
        
        # 射精强度(70%才开始，95%达到峰值)
        if self.arousal_level >= 70:
            self.ejaculation_force = (arousal_ratio - 0.7) / 0.25 * 100
        else:
            self.ejaculation_force = 0
        
        self.ejaculation_force = min(100, self.ejaculation_force)
        
        # 射程(厘米)
        # 平均 12 厘米，强射 25-30 厘米
        if self.ejaculation_force > 0:
            self.ejaculation_distance = 12 + self.ejaculation_force / 100 * 18
        else:
            self.ejaculation_distance = 0
        
        # 射精后恢复程度(0-100，用于计算不应期)
        # 假设完成射精后进入消退期
        if self.arousal_level >= 95:
            # 射精后逐渐下降
            self.post_ejaculation_recovery = max(0, 100 - (arousal_ratio - 0.95) / 0.05 * 100)
        else:
            self.post_ejaculation_recovery = 100
    
    def _calculate_sperm_parameters(self):
        """计算精子参数"""
        arousal_ratio = self.arousal_level / 100.0
        
        # 精子总数(百万)
        # 3.9-928 百万，正常 150-250
        if self.arousal_level > 50:
            base_count = 150 + (arousal_ratio - 0.5) / 0.5 * 100
        else:
            base_count = 50 + arousal_ratio / 0.5 * 100
        
        self.sperm_count = int(base_count)
        
        # 精子活动力(%，正常 >40%)
        if self.arousal_level > 30:
            self.sperm_motility = 40 + (arousal_ratio - 0.3) / 0.7 * 50
        else:
            self.sperm_motility = 20 + arousal_ratio / 0.3 * 20
        
        self.sperm_motility = min(90, self.sperm_motility)
        
        # 精子正常形态(%，正常 >4%)
        if self.arousal_level > 40:
            self.sperm_morphology = 4 + (arousal_ratio - 0.4) / 0.6 * 12
        else:
            self.sperm_morphology = 2 + arousal_ratio / 0.4 * 2
        
        self.sperm_morphology = min(16, self.sperm_morphology)
    
    def get_all_parameters(self):
        """返回所有生理参数字典"""
        return {
            "arousal_level": round(self.arousal_level, 2),
            "erection_level": round(self.erection_level, 2),
            "penis_length_cm": round(self.penis_length / SCALE, 2),
            "penis_diameter_cm": round(self.penis_diameter / SCALE, 2),
            "penis_head_diameter_cm": round(self.penis_head_diameter / SCALE, 2),
            "penis_erection_angle_deg": round(self.penis_erection_angle, 1),
            "foreskin_coverage_percent": round(self.foreskin_coverage, 1),
            "heart_rate_bpm": round(self.heart_rate, 1),
            "breathing_rate_rpm": round(self.breathing_rate, 1),
            "systolic_pressure_mmhg": round(self.systolic_pressure, 1),
            "blood_flow_multiplier": round(self.blood_flow_rate, 1),
            "skin_flush_intensity_percent": round(self.skin_flush_intensity, 1),
            "scrotum_contraction_percent": round(self.scrotum_contraction, 1),
            "testicle_elevation_percent": round(self.testicle_elevation, 1),
            "pre_ejaculatory_fluid_ml": round(self.pre_ejaculatory_fluid, 3),
            "prostatic_fluid_ml": round(self.prostatic_fluid, 2),
            "seminal_vesicle_fluid_ml": round(self.seminal_vesicle_fluid, 2),
            "total_seminal_fluid_ml": round(self.total_seminal_fluid, 2),
            "seminal_fluid_viscosity_percent": round(self.seminal_fluid_viscosity, 1),
            "seminal_fluid_liquefaction_percent": round(self.seminal_fluid_liquefaction, 1),
            "ejaculation_readiness_percent": round(self.ejaculation_readiness, 1),
            "ejaculation_force_percent": round(self.ejaculation_force, 1),
            "ejaculation_distance_cm": round(self.ejaculation_distance, 1),
        }
    
    def print_report(self):
        """打印详细报告"""
        params = self.get_all_parameters()
        
        print("\n" + "="*70)
        print("性生理参数计算报告")
        print("="*70)
        print(f"\n【控制参数】")
        print(f"性兴奋水平: {params['arousal_level']}%")
        print(f"勃起程度: {params['erection_level']}%")
        
        print(f"\n【阴茎参数】")
        print(f"长度: {params['penis_length_cm']} cm")
        print(f"直径: {params['penis_diameter_cm']} cm")
        print(f"龟头直径: {params['penis_head_diameter_cm']} cm")
        print(f"勃起角度: {params['penis_erection_angle_deg']}°")
        print(f"包皮覆盖: {params['foreskin_coverage_percent']}%")
        
        print(f"\n【心血管参数】")
        print(f"心率: {params['heart_rate_bpm']} 次/分")
        print(f"呼吸频率: {params['breathing_rate_rpm']} 次/分")
        print(f"收缩压: {params['systolic_pressure_mmhg']} mmHg")
        print(f"血流倍数: {params['blood_flow_multiplier']}x")
        
        print(f"\n【生理反应】")
        print(f"皮肤潮红: {params['skin_flush_intensity_percent']}%")
        print(f"阴囊收缩: {params['scrotum_contraction_percent']}%")
        print(f"睾丸上升: {params['testicle_elevation_percent']}%")
        
        print(f"\n【体液分泌】")
        print(f"尿道球腺液: {params['pre_ejaculatory_fluid_ml']} ml")
        print(f"前列腺液: {params['prostatic_fluid_ml']} ml")
        print(f"精囊液: {params['seminal_vesicle_fluid_ml']} ml")
        print(f"总精液: {params['total_seminal_fluid_ml']} ml")
        print(f"粘度: {params['seminal_fluid_viscosity_percent']}%")
        print(f"液化: {params['seminal_fluid_liquefaction_percent']}%")
        
        print(f"\n【射精参数】")
        print(f"准备度: {params['ejaculation_readiness_percent']}%")
        print(f"射精强度: {params['ejaculation_force_percent']}%")
        print(f"射程: {params['ejaculation_distance_cm']} cm")
        print("\n" + "="*70)


# ========== 使用示例 ==========

if __name__ == "__main__":
    phys_sys = PhysiologicalSystem()
    
    # 演示不同性兴奋水平的生理参数
    test_arousal_levels = [0, 15, 30, 50, 70, 85, 100]
    
    print("\n演示性兴奋水平对生理参数的影响")
    print("="*70)
    
    for arousal in test_arousal_levels:
        phys_sys.calculate_from_arousal(arousal)
        phys_sys.print_report()
        print("\n")

