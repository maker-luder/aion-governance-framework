"""
毛茸茸机器人男性模型 手部刺激系统
支持交互式输入手部动作参数，计算刺激强度和生理反应
"""

import math

SCALE = 0.01
PENIS_SOFT_LENGTH = 9 * SCALE
PENIS_ERECT_LENGTH = 13 * SCALE

# ========== 手部动作类型定义 ==========

HAND_TECHNIQUES = {
    "基础套弄": {
        "grip_range": (40, 70),
        "speed_range": (5, 15),
        "frequency_range": (40, 80),
        "stimulation_focus": "整体",
        "description": "全长上下运动，握力中等"
    },
    "快速套弄": {
        "grip_range": (60, 80),
        "speed_range": (15, 25),
        "frequency_range": (80, 120),
        "stimulation_focus": "整体",
        "description": "快速上下运动，握力较强"
    },
    "紧握": {
        "grip_range": (80, 100),
        "speed_range": (5, 10),
        "frequency_range": (20, 40),
        "stimulation_focus": "整体",
        "description": "握力最强，运动缓慢"
    },
    "龟头刺激": {
        "grip_range": (30, 50),
        "speed_range": (8, 15),
        "frequency_range": (60, 100),
        "stimulation_focus": "龟头",
        "description": "专注龟头区域的刺激"
    },
    "系带按摩": {
        "grip_range": (20, 40),
        "speed_range": (5, 12),
        "frequency_range": (50, 80),
        "stimulation_focus": "系带",
        "description": "刺激阴茎下方系带区域"
    },
    "两手交替": {
        "grip_range": (50, 70),
        "speed_range": (10, 20),
        "frequency_range": (60, 100),
        "stimulation_focus": "交替",
        "description": "两只手交替上下运动"
    },
    "旋转运动": {
        "grip_range": (40, 60),
        "speed_range": (8, 15),
        "frequency_range": (30, 60),
        "stimulation_focus": "旋转",
        "description": "手部旋转运动刺激"
    },
    "按压按摩": {
        "grip_range": (50, 70),
        "speed_range": (2, 8),
        "frequency_range": (20, 40),
        "stimulation_focus": "按压",
        "description": "以按压和揉搓为主"
    }
}

# ========== 手部动作过程类 ==========

class HandStimulationProcess:
    def __init__(self):
        self.motion_history = []
        self.timeline_data = []
    
    def add_motion_phase(self, phase_name, technique, start_time, duration, 
                        grip_strength, speed, frequency, stimulation_focus):
        """添加一个手部动作阶段"""
        motion_record = {
            "phase": phase_name,
            "technique": technique,
            "start_time_second": start_time,
            "duration_second": duration,
            "end_time_second": start_time + duration,
            "grip_strength_percent": grip_strength,
            "speed_cm_per_second": speed,
            "frequency_per_minute": frequency,
            "stimulation_focus": stimulation_focus,
            "description": HAND_TECHNIQUES[technique]["description"]
        }
        self.motion_history.append(motion_record)
        return motion_record
    
    def generate_motion_timeline(self, total_seconds):
        """生成手部动作时间轴"""
        self.timeline_data = []
        interval = 0.5  # 每 0.5 秒记录一次
        
        for time_sec in [x * interval for x in range(0, int(total_seconds / interval) + 1)]:
            motion_params = self._get_motion_at_time(time_sec)
            stimulation = self._calculate_stimulation_intensity(motion_params)
            
            timeline_entry = {
                "time_second": round(time_sec, 1),
                "grip_strength": motion_params["grip_strength"],
                "speed": motion_params["speed"],
                "frequency": motion_params["frequency"],
                "stimulation_intensity": stimulation,
                "technique": motion_params["technique"],
                "hand_position": motion_params["position"]
            }
            self.timeline_data.append(timeline_entry)
    
    def _get_motion_at_time(self, time_second):
        """根据时间获取手部动作参数"""
        for motion_record in self.motion_history:
            if motion_record["start_time_second"] <= time_second <= motion_record["end_time_second"]:
                return {
                    "grip_strength": motion_record["grip_strength_percent"],
                    "speed": motion_record["speed_cm_per_second"],
                    "frequency": motion_record["frequency_per_minute"],
                    "technique": motion_record["technique"],
                    "position": motion_record["stimulation_focus"]
                }
        
        return {
            "grip_strength": 0,
            "speed": 0,
            "frequency": 0,
            "technique": "停止",
            "position": "无"
        }
    
    def _calculate_stimulation_intensity(self, motion_params):
        """计算刺激强度(0-100)"""
        grip = motion_params["grip_strength"]
        speed = motion_params["speed"]
        frequency = motion_params["frequency"]
        
        if grip == 0 or speed == 0:
            return 0
        
        # 基础刺激强度 = (握力 + 速度归一化 + 频率归一化) / 3
        speed_normalized = min(100, (speed / 25) * 100)
        frequency_normalized = min(100, (frequency / 120) * 100)
        
        base_stimulation = (grip + speed_normalized + frequency_normalized) / 3
        
        return round(base_stimulation, 1)

# ========== 手部刺激系统类 ==========

class HandStimulationSystem:
    def __init__(self):
        self.grip_strength = 0.0
        self.movement_speed = 0.0
        self.movement_frequency = 0.0
        self.current_technique = "无"
        self.stimulation_focus = "无"
        
        # 手部位置参数
        self.hand_position = 0.0  # 0: 基部, 0.5: 中部, 1.0: 龟头
        self.hand_position_height = 0.0  # 0-13cm 范围
        self.hand_contact_area = 0.0  # 接触面积百分比
        
        # 动作方向
        self.motion_direction = "停止"  # 上升、下降、旋转、按压
        self.motion_angle = 0  # 度数
        self.pressure_applied = 0.0  # 施加压力强度
        
        # 刺激效果
        self.stimulation_intensity = 0.0  # 总刺激强度 0-100
        self.pleasure_sensation = 0.0  # 快感指数 0-100
        self.arousal_contribution = 0.0  # 对兴奋度的贡献
        
        # 过程记录
        self.process_record = HandStimulationProcess()
        self.current_time = 0.0
    
    def set_hand_motion(self, technique, grip_strength, speed, frequency, focus):
        """设置手部动作参数"""
        self.current_technique = technique
        self.grip_strength = max(0, min(100, grip_strength))
        self.movement_speed = max(0, min(30, speed))
        self.movement_frequency = max(0, min(180, frequency))
        self.stimulation_focus = focus
        
        # 根据技巧更新参数
        if technique in HAND_TECHNIQUES:
            tech_info = HAND_TECHNIQUES[technique]
            grip_range = tech_info["grip_range"]
            speed_range = tech_info["speed_range"]
            freq_range = tech_info["frequency_range"]
            
            # 确保参数在技巧范围内
            self.grip_strength = max(grip_range[0], min(grip_range[1], grip_strength))
            self.movement_speed = max(speed_range[0], min(speed_range[1], speed))
            self.movement_frequency = max(freq_range[0], min(freq_range[1], frequency))
        
        self._calculate_hand_parameters()
    
    def _calculate_hand_parameters(self):
        """计算手部参数"""
        if self.grip_strength == 0:
            self.stimulation_intensity = 0
            return
        
        # 计算刺激强度
        grip_factor = self.grip_strength / 100.0
        speed_factor = self.movement_speed / 25.0
        frequency_factor = self.movement_frequency / 120.0
        
        # 综合刺激强度
        self.stimulation_intensity = min(100, 
            (grip_factor * 40 + speed_factor * 30 + frequency_factor * 30))
        
        # 快感指数（受刺激位置影响）
        if self.stimulation_focus == "龟头":
            self.pleasure_sensation = self.stimulation_intensity * 1.2
        elif self.stimulation_focus == "系带":
            self.pleasure_sensation = self.stimulation_intensity * 1.15
        else:
            self.pleasure_sensation = self.stimulation_intensity * 1.0
        
        self.pleasure_sensation = min(100, self.pleasure_sensation)
        
        # 对兴奋度的贡献
        self.arousal_contribution = self.stimulation_intensity * 0.6
        
        # 手部接触面积
        if self.grip_strength < 30:
            self.hand_contact_area = 30
        elif self.grip_strength < 60:
            self.hand_contact_area = 50
        else:
            self.hand_contact_area = 70
        
        # 施加压力强度
        self.pressure_applied = self.grip_strength * 0.8
    
    def set_hand_position(self, position_percent):
        """设置手部位置(0-100, 0=基部, 100=龟头)"""
        self.hand_position = max(0, min(100, position_percent)) / 100.0
        self.hand_position_height = self.hand_position * (PENIS_ERECT_LENGTH / SCALE)
    
    def set_motion_direction(self, direction):
        """设置运动方向"""
        valid_directions = ["上升", "下降", "旋转", "按压", "停止"]
        if direction in valid_directions:
            self.motion_direction = direction
        else:
            self.motion_direction = "停止"
        
        # 根据方向设置角度
        if direction == "旋转":
            self.motion_angle = 90
        elif direction in ["上升", "下降"]:
            self.motion_angle = 180
        else:
            self.motion_angle = 0
    
    def get_hand_parameters(self):
        """获取手部参数字典"""
        return {
            "current_technique": self.current_technique,
            "grip_strength_percent": round(self.grip_strength, 1),
            "movement_speed_cm_per_sec": round(self.movement_speed, 1),
            "movement_frequency_per_min": round(self.movement_frequency, 1),
            "stimulation_focus": self.stimulation_focus,
            "hand_position_percent": round(self.hand_position * 100, 1),
            "hand_position_height_cm": round(self.hand_position_height, 2),
            "motion_direction": self.motion_direction,
            "motion_angle_deg": round(self.motion_angle, 1),
            "hand_contact_area_percent": round(self.hand_contact_area, 1),
            "pressure_applied_percent": round(self.pressure_applied, 1),
            "stimulation_intensity_percent": round(self.stimulation_intensity, 1),
            "pleasure_sensation_percent": round(self.pleasure_sensation, 1),
            "arousal_contribution_percent": round(self.arousal_contribution, 1),
        }
    
    def print_hand_parameters(self):
        """打印手部参数"""
        params = self.get_hand_parameters()
        
        print("\n" + "="*70)
        print("手部刺激系统参数报告")
        print("="*70)
        print(f"\n【当前技巧】")
        print(f"技巧名称: {params['current_technique']}")
        print(f"刺激位置: {params['stimulation_focus']}")
        print(f"\n【手部运动参数】")
        print(f"握力强度: {params['grip_strength_percent']}%")
        print(f"运动速度: {params['movement_speed_cm_per_sec']} cm/秒")
        print(f"运动频率: {params['movement_frequency_per_min']} 次/分")
        print(f"运动方向: {params['motion_direction']}")
        print(f"运动角度: {params['motion_angle_deg']}°")
        print(f"\n【手部位置】")
        print(f"位置百分比: {params['hand_position_percent']}% (0=基部, 100=龟头)")
        print(f"位置高度: {params['hand_position_height_cm']} cm")
        print(f"\n【接触参数】")
        print(f"接触面积: {params['hand_contact_area_percent']}%")
        print(f"施加压力: {params['pressure_applied_percent']}%")
        print(f"\n【刺激效果】")
        print(f"刺激强度: {params['stimulation_intensity_percent']}%")
        print(f"快感指数: {params['pleasure_sensation_percent']}%")
        print(f"对兴奋度贡献: {params['arousal_contribution_percent']}%")
        print("="*70 + "\n")


# ========== 交互式界面 ==========

def interactive_hand_mode():
    """交互式手部动作模式"""
    hand_sys = HandStimulationSystem()
    
    print("\n" + "="*70)
    print("毛茸茸机器人男性模型 手部刺激系统 - 交互模式")
    print("="*70)
    print("\n命令:")
    print("  technique [名称] [握力] [速度] [频率] [位置]")
    print("    选择技巧，例: technique 龟头刺激 45 12 80 龟头")
    print("  position [百分比]   设置手部位置(0-100，0=基部，100=龟头)")
    print("  direction [方向]    设置运动方向(上升/下降/旋转/按压/停止)")
    print("  list               显示所有可用技巧")
    print("  custom [握力] [速度] [频率] [位置]")
    print("    自定义参数，例: custom 65 18 95 龟头")
    print("  timeline [总时长]  生成完整动作时间轴")
    print("  export             导出过程数据")
    print("  exit              退出程序")
    print("="*70 + "\n")
    
    while True:
        try:
            user_input = input("请输入命令: ").strip()
            
            if not user_input:
                continue
            
            tokens = user_input.split()
            command = tokens[0].lower()
            
            if command == "list":
                print("\n" + "="*70)
                print("可用手部刺激技巧")
                print("="*70)
                for tech_name, tech_info in HAND_TECHNIQUES.items():
                    grip_range = tech_info["grip_range"]
                    speed_range = tech_info["speed_range"]
                    freq_range = tech_info["frequency_range"]
                    print(f"\n{tech_name}:")
                    print(f"  说明: {tech_info['description']}")
                    print(f"  握力范围: {grip_range[0]}-{grip_range[1]}%")
                    print(f"  速度范围: {speed_range[0]}-{speed_range[1]} cm/秒")
                    print(f"  频率范围: {freq_range[0]}-{freq_range[1]} 次/分")
                    print(f"  刺激位置: {tech_info['stimulation_focus']}")
                print("\n" + "="*70 + "\n")
            
            elif command == "technique":
                if len(tokens) < 6:
                    print("错误: 请输入完整参数")
                    print("用法: technique [名称] [握力] [速度] [频率] [位置]")
                    continue
                
                try:
                    tech_name = tokens[1]
                    grip = float(tokens[2])
                    speed = float(tokens[3])
                    frequency = float(tokens[4])
                    focus = tokens[5]
                    
                    if tech_name not in HAND_TECHNIQUES:
                        print(f"错误: 未知技巧 '{tech_name}'，使用 'list' 命令查看所有技巧")
                        continue
                    
                    hand_sys.set_hand_motion(tech_name, grip, speed, frequency, focus)
                    hand_sys.print_hand_parameters()
                
                except ValueError:
                    print("错误: 请输入有效的数值")
            
            elif command == "custom":
                if len(tokens) < 5:
                    print("错误: 请输入完整参数")
                    print("用法: custom [握力] [速度] [频率] [位置]")
                    continue
                
                try:
                    grip = float(tokens[1])
                    speed = float(tokens[2])
                    frequency = float(tokens[3])
                    focus = tokens[4]
                    
                    hand_sys.current_technique = "自定义"
                    hand_sys.grip_strength = grip
                    hand_sys.movement_speed = speed
                    hand_sys.movement_frequency = frequency
                    hand_sys.stimulation_focus = focus
                    hand_sys._calculate_hand_parameters()
                    hand_sys.print_hand_parameters()
                
                except ValueError:
                    print("错误: 请输入有效的数值")
            
            elif command == "position":
                if len(tokens) < 2:
                    print("错误: 请输入位置百分比(0-100)")
                    continue
                
                try:
                    position = float(tokens[1])
                    hand_sys.set_hand_position(position)
                    print(f"手部位置已设置为: {position}% (高度: {round(hand_sys.hand_position_height, 2)} cm)")
                    print(f"位置说明: 0% = 基部, 50% = 中部, 100% = 龟头\n")
                
                except ValueError:
                    print("错误: 请输入有效的位置百分比")
            
            elif command == "direction":
                if len(tokens) < 2:
                    print("错误: 请输入方向(上升/下降/旋转/按压/停止)")
                    continue
                
                direction = tokens[1]
                hand_sys.set_motion_direction(direction)
                print(f"运动方向已设置为: {direction}\n")
            
            elif command == "timeline":
                if len(tokens) < 2:
                    print("错误: 请输入总时长(秒)")
                    continue
                
                try:
                    total_duration = float(tokens[1])
                    hand_sys.process_record.generate_motion_timeline(total_duration)
                    print(f"\n生成完成! 总时长: {total_duration} 秒")
                    print(f"时间轴数据点: {len(hand_sys.process_record.timeline_data)}")
                    print("可使用其他命令继续操作\n")
                
                except ValueError:
                    print("错误: 请输入有效的时间值")
            
            elif command == "export":
                print("\n导出数据中...")
                
                # 生成示例过程
                techniques_list = list(HAND_TECHNIQUES.keys())
                current_time = 0
                
                for i, tech in enumerate(techniques_list[:4]):
                    tech_info = HAND_TECHNIQUES[tech]
                    grip = (tech_info["grip_range"][0] + tech_info["grip_range"][1]) / 2
                    speed = (tech_info["speed_range"][0] + tech_info["speed_range"][1]) / 2
                    freq = (tech_info["frequency_range"][0] + tech_info["frequency_range"][1]) / 2
                    focus = tech_info["stimulation_focus"]
                    
                    hand_sys.process_record.add_motion_phase(
                        f"阶段{i+1}",
                        tech,
                        current_time,
                        60,
                        grip,
                        speed,
                        freq,
                        focus
                    )
                    current_time += 60
                
                hand_sys.process_record.generate_motion_timeline(current_time)
                
                print(f"生成完成!")
                print(f"总时长: {current_time} 秒")
                print(f"总阶段数: {len(hand_sys.process_record.motion_history)}")
                print(f"时间轴数据点: {len(hand_sys.process_record.timeline_data)}")
                print("数据已保存\n")
            
            elif command == "exit":
                print("再见!")
                break
            
            else:
                print("未知命令。输入 'list' 查看技巧列表，或使用其他命令")
        
        except KeyboardInterrupt:
            print("\n程序已中断")
            break
        except Exception as e:
            print(f"错误: {str(e)}")


if __name__ == "__main__":
    interactive_hand_mode()
