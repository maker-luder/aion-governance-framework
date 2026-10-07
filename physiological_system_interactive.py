"""
毛茸茸机器人男性模型 生理参数化系统 - 交互版
支持实时输入，完整记录医学性反应周期过程
"""

import bpy
import math

SCALE = 0.01
HEIGHT = 185 * SCALE
PENIS_SOFT_LENGTH = 9 * SCALE
PENIS_ERECT_LENGTH = 13 * SCALE
PENIS_SOFT_DIAMETER = 2.75 * SCALE
PENIS_ERECT_DIAMETER = 3.5 * SCALE
PENIS_HEAD_SOFT_DIAMETER = 3.25 * SCALE
PENIS_HEAD_ERECT_DIAMETER = 4.55 * SCALE

# ========== 医学性反应周期阶段定义 ==========

SEXUAL_RESPONSE_PHASES = {
    "刺激前期": {
        "arousal_range": (0, 10),
        "duration_min": 0,
        "duration_max": 0,
        "description": "无性兴奋，基础静息状态"
    },
    "兴奋期": {
        "arousal_range": (10, 30),
        "duration_min": 5,
        "duration_max": 300,
        "description": "阴茎开始勃起，体液开始分泌"
    },
    "平台期": {
        "arousal_range": (30, 70),
        "duration_min": 30,
        "duration_max": 600,
        "description": "完全勃起，生理反应达到高水平"
    },
    "射精期": {
        "arousal_range": (70, 95),
        "duration_min": 3,
        "duration_max": 10,
        "description": "肌肉收缩，精液排出，射精感觉"
    },
    "消退期": {
        "arousal_range": (95, 100),
        "duration_min": 10,
        "duration_max": 1800,
        "description": "生理参数逐渐恢复正常，进入不应期"
    }
}

# ========== 过程记录类 ==========

class SexualResponseProcess:
    def __init__(self):
        self.phase_history = []
        self.timeline_data = []
        self.current_phase = "刺激前期"
        self.total_duration = 0
        self.phase_start_time = 0
    
    def add_phase(self, phase_name, start_time, duration, start_arousal, end_arousal):
        """添加一个阶段到历史记录"""
        phase_record = {
            "phase": phase_name,
            "start_time_second": start_time,
            "duration_second": duration,
            "end_time_second": start_time + duration,
            "start_arousal_percent": start_arousal,
            "end_arousal_percent": end_arousal,
            "arousal_change": end_arousal - start_arousal,
            "description": SEXUAL_RESPONSE_PHASES[phase_name]["description"]
        }
        self.phase_history.append(phase_record)
        return phase_record
    
    def generate_timeline(self, total_seconds):
        """生成完整时间轴数据"""
        self.timeline_data = []
        interval = 1  # 每秒记录一次
        
        for time_sec in range(0, int(total_seconds) + 1, interval):
            arousal = self._get_arousal_at_time(time_sec)
            phase = self._get_phase_at_time(time_sec)
            
            timeline_entry = {
                "time_second": time_sec,
                "phase": phase,
                "arousal_percent": arousal
            }
            self.timeline_data.append(timeline_entry)
    
    def _get_arousal_at_time(self, time_second):
        """根据时间获取兴奋度"""
        for phase_record in self.phase_history:
            if phase_record["start_time_second"] <= time_second <= phase_record["end_time_second"]:
                phase_duration = phase_record["duration_second"]
                if phase_duration == 0:
                    return phase_record["start_arousal_percent"]
                
                elapsed = time_second - phase_record["start_time_second"]
                progress = elapsed / phase_duration
                arousal = phase_record["start_arousal_percent"] + (phase_record["arousal_change"]) * progress
                return arousal
        
        return 0
    
    def _get_phase_at_time(self, time_second):
        """根据时间获取阶段名称"""
        for phase_record in self.phase_history:
            if phase_record["start_time_second"] <= time_second <= phase_record["end_time_second"]:
                return phase_record["phase"]
        return "未知"

# ========== 升级的生理参数化类 ==========

class PhysiologicalSystem:
    def __init__(self):
        self.arousal_level = 0.0
        self.erection_level = 0.0
        self.current_time = 0.0  # 当前时间(秒)
        self.process_record = SexualResponseProcess()
        
        # 阴茎参数
        self.penis_length = PENIS_SOFT_LENGTH
        self.penis_diameter = PENIS_SOFT_DIAMETER
        self.penis_head_diameter = PENIS_HEAD_SOFT_DIAMETER
        self.penis_erection_angle = 0
        self.foreskin_coverage = 100
        
        # 心血管
        self.heart_rate = 70
        self.breathing_rate = 14
        self.systolic_pressure = 120
        self.blood_flow_rate = 1.0
        
        # 外观反应
        self.skin_flush_intensity = 0.0
        self.scrotum_contraction = 0.0
        self.testicle_elevation = 0.0
        
        # 体液
        self.pre_ejaculatory_fluid = 0.0
        self.prostatic_fluid = 0.0
        self.seminal_vesicle_fluid = 0.0
        self.total_seminal_fluid = 0.0
        self.seminal_fluid_viscosity = 0.0
        self.seminal_fluid_liquefaction = 0.0
        
        # 射精
        self.ejaculation_readiness = 0.0
        self.ejaculation_force = 0.0
        self.ejaculation_distance = 0.0
    
    def calculate_from_arousal(self, arousal_value):
        """根据兴奋度计算所有参数"""
        self.arousal_level = max(0, min(100, arousal_value))
        
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
            self.erection_level = (self.arousal_level - 10) / 20 * 50
        elif self.arousal_level < 70:
            self.erection_level = 50 + (self.arousal_level - 30) / 40 * 50
        else:
            self.erection_level = 100
        
        self.erection_level = max(0, min(100, self.erection_level))
    
    def _calculate_penis_dimensions(self):
        """计算阴茎尺寸"""
        erect_ratio = self.erection_level / 100.0
        
        self.penis_length = PENIS_SOFT_LENGTH + (PENIS_ERECT_LENGTH - PENIS_SOFT_LENGTH) * erect_ratio
        self.penis_diameter = PENIS_SOFT_DIAMETER + (PENIS_ERECT_DIAMETER - PENIS_SOFT_DIAMETER) * erect_ratio
        self.penis_head_diameter = PENIS_HEAD_SOFT_DIAMETER + (PENIS_HEAD_ERECT_DIAMETER - PENIS_HEAD_SOFT_DIAMETER) * erect_ratio
        
        min_angle = -52.5
        max_angle = 37.5
        self.penis_erection_angle = min_angle + (max_angle - min_angle) * erect_ratio
        
        if erect_ratio < 0.3:
            self.foreskin_coverage = 60 - erect_ratio * 30
        elif erect_ratio < 0.7:
            self.foreskin_coverage = 50 - (erect_ratio - 0.3) * 25
        else:
            self.foreskin_coverage = 45 - (erect_ratio - 0.7) * 45
        
        self.foreskin_coverage = max(0, min(100, self.foreskin_coverage))
    
    def _calculate_body_responses(self):
        """计算身体反应"""
        arousal_ratio = self.arousal_level / 100.0
        
        if self.arousal_level < 30:
            self.heart_rate = 70 + arousal_ratio * 30
        elif self.arousal_level < 70:
            self.heart_rate = 100 + (arousal_ratio - 0.3) / 0.4 * 50
        else:
            self.heart_rate = 150 + (arousal_ratio - 0.7) / 0.3 * 30
        
        if self.arousal_level < 30:
            self.breathing_rate = 14 + arousal_ratio * 6
        elif self.arousal_level < 70:
            self.breathing_rate = 20 + (arousal_ratio - 0.3) / 0.4 * 15
        else:
            self.breathing_rate = 35 + (arousal_ratio - 0.7) / 0.3 * 5
        
        if self.arousal_level < 30:
            self.systolic_pressure = 120 + arousal_ratio * 20
        elif self.arousal_level < 70:
            self.systolic_pressure = 140 + (arousal_ratio - 0.3) / 0.4 * 40
        else:
            self.systolic_pressure = 180 + (arousal_ratio - 0.7) / 0.3 * 20
        
        if self.arousal_level < 30:
            self.blood_flow_rate = 1 + arousal_ratio * 19
        elif self.arousal_level < 70:
            self.blood_flow_rate = 20 + (arousal_ratio - 0.3) / 0.4 * 20
        else:
            self.blood_flow_rate = 40 + (arousal_ratio - 0.7) / 0.3 * 20
        
        self.skin_flush_intensity = min(100, arousal_ratio * 120)
        
        if self.arousal_level < 30:
            self.scrotum_contraction = arousal_ratio * 20 / 0.3
        elif self.arousal_level < 70:
            self.scrotum_contraction = 20 + (arousal_ratio - 0.3) / 0.4 * 40
        else:
            self.scrotum_contraction = 60 + (arousal_ratio - 0.7) / 0.3 * 40
        
        self.scrotum_contraction = min(100, self.scrotum_contraction)
        
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
        
        if self.arousal_level > 15:
            self.pre_ejaculatory_fluid = (arousal_ratio - 0.15) / 0.85 * 0.2
        else:
            self.pre_ejaculatory_fluid = 0
        
        self.pre_ejaculatory_fluid = min(0.2, self.pre_ejaculatory_fluid)
        
        if self.arousal_level > 20:
            if self.arousal_level < 70:
                self.prostatic_fluid = (arousal_ratio - 0.2) / 0.5 * 2.0
            else:
                self.prostatic_fluid = 2.0
        else:
            self.prostatic_fluid = 0
        
        self.prostatic_fluid = min(2.5, self.prostatic_fluid)
        
        if self.arousal_level > 25:
            if self.arousal_level < 70:
                self.seminal_vesicle_fluid = (arousal_ratio - 0.25) / 0.45 * 3.0
            else:
                self.seminal_vesicle_fluid = 3.0
        else:
            self.seminal_vesicle_fluid = 0
        
        self.seminal_vesicle_fluid = min(3.5, self.seminal_vesicle_fluid)
        
        self.total_seminal_fluid = self.pre_ejaculatory_fluid + self.prostatic_fluid + self.seminal_vesicle_fluid
        self.total_seminal_fluid = min(5.0, self.total_seminal_fluid)
        
        if self.arousal_level > 25:
            self.seminal_fluid_viscosity = 80 - (self.arousal_level - 25) / 75 * 30
        else:
            self.seminal_fluid_viscosity = 80
        
        self.seminal_fluid_viscosity = max(20, min(100, self.seminal_fluid_viscosity))
        
        if self.arousal_level > 25:
            self.seminal_fluid_liquefaction = (self.arousal_level - 25) / 75 * 80
        else:
            self.seminal_fluid_liquefaction = 0
        
        self.seminal_fluid_liquefaction = min(80, self.seminal_fluid_liquefaction)
    
    def _calculate_ejaculation_parameters(self):
        """计算射精参数"""
        arousal_ratio = self.arousal_level / 100.0
        
        if self.arousal_level < 70:
            self.ejaculation_readiness = min(90, arousal_ratio / 0.7 * 90)
        else:
            self.ejaculation_readiness = 90 + (arousal_ratio - 0.7) / 0.3 * 10
        
        if self.arousal_level >= 70:
            self.ejaculation_force = (arousal_ratio - 0.7) / 0.25 * 100
        else:
            self.ejaculation_force = 0
        
        self.ejaculation_force = min(100, self.ejaculation_force)
        
        if self.ejaculation_force > 0:
            self.ejaculation_distance = 12 + self.ejaculation_force / 100 * 18
        else:
            self.ejaculation_distance = 0
    
    def get_all_parameters(self):
        """获取所有参数"""
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
    
    def print_parameters(self):
        """打印参数"""
        params = self.get_all_parameters()
        
        print("\n" + "="*70)
        print("性生理参数计算报告")
        print("="*70)
        print(f"\n性兴奋水平: {params['arousal_level']}%")
        print(f"勃起程度: {params['erection_level']}%")
        print(f"\n【阴茎参数】")
        print(f"长度: {params['penis_length_cm']} cm")
        print(f"直径: {params['penis_diameter_cm']} cm")
        print(f"龟头直径: {params['penis_head_diameter_cm']} cm")
        print(f"勃起角度: {params['penis_erection_angle_deg']}°")
        print(f"包皮覆盖: {params['foreskin_coverage_percent']}%")
        print(f"\n【心血管】")
        print(f"心率: {params['heart_rate_bpm']} bpm")
        print(f"呼吸: {params['breathing_rate_rpm']} rpm")
        print(f"血压: {params['systolic_pressure_mmhg']} mmHg")
        print(f"血流: {params['blood_flow_multiplier']}x")
        print(f"\n【外观反应】")
        print(f"皮肤潮红: {params['skin_flush_intensity_percent']}%")
        print(f"阴囊收缩: {params['scrotum_contraction_percent']}%")
        print(f"睾丸上升: {params['testicle_elevation_percent']}%")
        print(f"\n【体液】")
        print(f"总精液: {params['total_seminal_fluid_ml']} ml")
        print(f"粘度: {params['seminal_fluid_viscosity_percent']}%")
        print(f"\n【射精】")
        print(f"强度: {params['ejaculation_force_percent']}%")
        print(f"射程: {params['ejaculation_distance_cm']} cm")
        print("="*70 + "\n")


# ========== 交互式界面 ==========

def interactive_mode():
    """交互式输入模式"""
    phys_sys = PhysiologicalSystem()
    
    print("\n" + "="*70)
    print("毛茸茸机器人男性模型 生理参数系统 - 交互模式")
    print("="*70)
    print("\n命令:")
    print("  arousal [值]     输入兴奋度(0-100)查询参数")
    print("  time [秒数]      输入时间(秒)查询过程中的状态")
    print("  phases           显示医学性反应周期说明")
    print("  export           导出完整过程数据")
    print("  exit             退出程序")
    print("="*70 + "\n")
    
    while True:
        try:
            user_input = input("请输入命令: ").strip().split()
            
            if not user_input:
                continue
            
            command = user_input[0].lower()
            
            if command == "arousal":
                if len(user_input) < 2:
                    print("错误: 请输入兴奋度值 (0-100)")
                    continue
                
                try:
                    arousal_value = float(user_input[1])
                    phys_sys.calculate_from_arousal(arousal_value)
                    phys_sys.print_parameters()
                except ValueError:
                    print("错误: 请输入有效的数值")
            
            elif command == "time":
                if len(user_input) < 2:
                    print("错误: 请输入时间值(秒)")
                    continue
                
                try:
                    time_value = float(user_input[1])
                    if not phys_sys.process_record.timeline_data:
                        print("错误: 请先输入arousal命令生成过程数据")
                        continue
                    
                    arousal_at_time = phys_sys.process_record._get_arousal_at_time(time_value)
                    phase_at_time = phys_sys.process_record._get_phase_at_time(time_value)
                    
                    phys_sys.calculate_from_arousal(arousal_at_time)
                    
                    print(f"\n时间: {time_value} 秒")
                    print(f"阶段: {phase_at_time}")
                    phys_sys.print_parameters()
                
                except ValueError:
                    print("错误: 请输入有效的时间值")
            
            elif command == "phases":
                print("\n" + "="*70)
                print("医学性反应周期 (Masters & Johnson Model)")
                print("="*70)
                for phase_name, phase_info in SEXUAL_RESPONSE_PHASES.items():
                    arousal_min, arousal_max = phase_info["arousal_range"]
                    duration_min, duration_max = phase_info["duration_min"]
                    print(f"\n{phase_name}:")
                    print(f"  兴奋度范围: {arousal_min}-{arousal_max}%")
                    print(f"  典型时长: {duration_min}-{duration_max} 秒")
                    print(f"  说明: {phase_info['description']}")
                print("\n" + "="*70 + "\n")
            
            elif command == "export":
                print("\n生成完整过程数据中...")
                phys_sys.calculate_from_arousal(0)
                
                durations = [200, 150, 80, 5, 600]
                phases = list(SEXUAL_RESPONSE_PHASES.keys())
                
                current_time = 0
                current_arousal = 0
                
                for i, phase in enumerate(phases):
                    arousal_range = SEXUAL_RESPONSE_PHASES[phase]["arousal_range"]
                    duration = durations[i]
                    end_arousal = arousal_range[1]
                    
                    phys_sys.process_record.add_phase(
                        phase,
                        current_time,
                        duration,
                        current_arousal,
                        end_arousal
                    )
                    
                    current_time += duration
                    current_arousal = end_arousal
                
                phys_sys.process_record.generate_timeline(current_time)
                
                print(f"\n生成完成! 总时长: {current_time} 秒")
                print(f"总阶段数: {len(phys_sys.process_record.phase_history)}")
                print("数据已保存到过程记录中")
                print("使用 'time [秒数]' 命令查询任意时刻的状态\n")
            
            elif command == "exit":
                print("再见!")
                break
            
            else:
                print("未知命令，请输入 'arousal [值]', 'time [秒]', 'phases', 'export' 或 'exit'")
        
        except KeyboardInterrupt:
            print("\n程序已中断")
            break
        except Exception as e:
            print(f"错误: {str(e)}")


if __name__ == "__main__":
    interactive_mode()
