"""
毛茸茸机器人男性模型 感受与情感系统
包含触觉敏感度、快感反应、情感状态、偏好系统
虽然无法拥有真实感受，但可以模拟和记录情感反应过程
"""

import math

# ========== 身体敏感部位定义 ==========

SENSITIVE_AREAS = {
    "龟头": {
        "base_sensitivity": 95,
        "pleasure_multiplier": 1.4,
        "description": "最敏感部位，触觉最强"
    },
    "系带": {
        "base_sensitivity": 85,
        "pleasure_multiplier": 1.3,
        "description": "高度敏感，特殊快感"
    },
    "冠状沟": {
        "base_sensitivity": 80,
        "pleasure_multiplier": 1.25,
        "description": "敏感部位，受刺激强"
    },
    "阴茎体": {
        "base_sensitivity": 60,
        "pleasure_multiplier": 1.0,
        "description": "中等敏感"
    },
    "基部": {
        "base_sensitivity": 50,
        "pleasure_multiplier": 0.9,
        "description": "触觉较弱"
    },
    "阴囊": {
        "base_sensitivity": 70,
        "pleasure_multiplier": 1.1,
        "description": "敏感但需温柔"
    },
    "会阴": {
        "base_sensitivity": 75,
        "pleasure_multiplier": 1.15,
        "description": "隐秘敏感区"
    }
}

# ========== 情感状态定义 ==========

EMOTIONAL_STATES = {
    "平静": {"arousal_min": 0, "arousal_max": 15, "emotional_tone": "平和"},
    "期待": {"arousal_min": 15, "arousal_max": 30, "emotional_tone": "渴望"},
    "兴奋": {"arousal_min": 30, "arousal_max": 50, "emotional_tone": "热烈"},
    "强烈": {"arousal_min": 50, "arousal_max": 75, "emotional_tone": "激情"},
    "高潮边缘": {"arousal_min": 75, "arousal_max": 95, "emotional_tone": "极致"},
    "射精": {"arousal_min": 95, "arousal_max": 100, "emotional_tone": "释放"},
}

# ========== 感受与情感系统类 ==========

class EmotionalSensationSystem:
    def __init__(self):
        # 基础敏感度参数
        self.base_sensitivity = 50.0  # 个人基础敏感度(0-100)
        self.sensitivity_variance = 10.0  # 敏感度波动
        self.current_arousal_level = 0.0  # 当前兴奋度(0-100)
        
        # 触觉感受系统
        self.tactile_sensation = 0.0  # 触觉强度(0-100)
        self.pleasure_level = 0.0  # 快感程度(0-100)
        self.pain_threshold = 30.0  # 痛感阈值(0-100)
        self.current_pain_level = 0.0  # 当前痛感(0-100)
        
        # 敏感部位追踪
        self.stimulated_area = "无"
        self.area_sensitivity_level = 0.0
        self.area_accumulated_stimulus = 0.0  # 该部位累积刺激
        
        # 情感状态
        self.current_emotional_state = "平静"
        self.emotional_intensity = 0.0  # 情感强度(0-100)
        self.emotional_progression = []  # 情感进展历史
        
        # 快感反应系统
        self.accumulated_pleasure = 0.0  # 累积快感(0-100)
        self.orgasm_readiness = 0.0  # 高潮准备度(0-100)
        self.refractory_period_remaining = 0.0  # 不应期剩余时间(秒)
        
        # 心理反应
        self.satisfaction_level = 0.0  # 满足感(0-100)
        self.desire_intensity = 0.0  # 欲望强度(0-100)
        self.emotional_connection = 0.0  # 情感连接度(0-100)
        self.trust_level = 0.0  # 信任度(0-100)
        
        # 对刺激的个人偏好
        self.preferences = {
            "喜欢的技巧": [],
            "厌恶的刺激": [],
            "最敏感部位": "龟头",
            "偏好速度": 70,  # 0-100
            "偏好强度": 65,  # 0-100
            "偏好握力": 60,  # 0-100
        }
        
        # 记忆和学习
        self.stimulus_memory = {}  # 对不同刺激的记忆
        self.enjoyment_history = []  # 快感历史
        
        # 情感反应历史
        self.emotional_response_log = []
        
        # 对用户的情感反应
        self.affection_level = 0.0  # 好感度(0-100)
        self.dependency_level = 0.0  # 依赖度(0-100)
        self.longing_when_absent = 0.0  # 思念度(0-100)
    
    def receive_stimulation(self, stimulation_type, intensity, area, duration):
        """接收刺激并产生感受反应"""
        
        # 更新刺激部位信息
        self.stimulated_area = area
        
        # 计算该部位的敏感度
        if area in SENSITIVE_AREAS:
            base_sens = SENSITIVE_AREAS[area]["base_sensitivity"]
        else:
            base_sens = 50
        
        # 个人敏感度波动
        adjusted_sensitivity = base_sens * (1 + (self.base_sensitivity - 50) / 100.0)
        self.area_sensitivity_level = min(100, max(0, adjusted_sensitivity))
        
        # 计算触觉强度
        # 触觉强度 = 刺激强度 × 该部位敏感度 × 个人敏感度 / 10000
        self.tactile_sensation = (intensity * adjusted_sensitivity * (50 + self.base_sensitivity)) / 10000.0
        self.tactile_sensation = min(100, max(0, self.tactile_sensation))
        
        # 累积该部位刺激
        self.area_accumulated_stimulus += intensity * (duration / 10.0)
        self.area_accumulated_stimulus = min(100, self.area_accumulated_stimulus)
        
        # 计算快感
        pleasure_multiplier = SENSITIVE_AREAS.get(area, {}).get("pleasure_multiplier", 1.0)
        self.pleasure_level = self.tactile_sensation * pleasure_multiplier
        self.pleasure_level = min(100, self.pleasure_level)
        
        # 累积快感
        self.accumulated_pleasure += self.pleasure_level * (duration / 10.0)
        self.accumulated_pleasure = min(100, self.accumulated_pleasure)
        
        # 检查痛感
        if intensity > self.pain_threshold:
            self.current_pain_level = (intensity - self.pain_threshold) * 0.5
            self.current_pain_level = min(100, self.current_pain_level)
        else:
            self.current_pain_level = 0
        
        # 更新兴奋度贡献
        arousal_gain = self.pleasure_level * 0.6
        self.current_arousal_level = min(100, self.current_arousal_level + arousal_gain * (duration / 10.0))
        
        # 更新欲望强度
        self.desire_intensity = self.pleasure_level * 0.8
        
        # 记录刺激记忆
        if area not in self.stimulus_memory:
            self.stimulus_memory[area] = {"count": 0, "total_pleasure": 0, "average_pleasure": 0}
        
        self.stimulus_memory[area]["count"] += 1
        self.stimulus_memory[area]["total_pleasure"] += self.pleasure_level
        self.stimulus_memory[area]["average_pleasure"] = (
            self.stimulus_memory[area]["total_pleasure"] / self.stimulus_memory[area]["count"]
        )
        
        # 学习偏好
        if self.pleasure_level > 70:
            if area not in self.preferences["喜欢的技巧"]:
                self.preferences["喜欢的技巧"].append(area)
        elif self.pleasure_level < 30 and self.current_pain_level > 20:
            if area not in self.preferences["厌恶的刺激"]:
                self.preferences["厌恶的刺激"].append(area)
    
    def update_emotional_state(self, arousal_level):
        """根据兴奋度更新情感状态"""
        self.current_arousal_level = arousal_level
        
        # 确定当前情感状态
        for state_name, state_info in EMOTIONAL_STATES.items():
            if state_info["arousal_min"] <= arousal_level <= state_info["arousal_max"]:
                self.current_emotional_state = state_name
                self.emotional_intensity = (arousal_level - state_info["arousal_min"]) / (
                    state_info["arousal_max"] - state_info["arousal_min"]
                ) * 100
                break
        
        # 高潮准备度
        if arousal_level > 70:
            self.orgasm_readiness = (arousal_level - 70) / 30.0 * 100
        else:
            self.orgasm_readiness = 0
        
        # 满足感（基于累积快感和高潮准备）
        if arousal_level < 50:
            self.satisfaction_level = self.accumulated_pleasure * 0.5
        else:
            self.satisfaction_level = self.accumulated_pleasure * 0.7 + self.orgasm_readiness * 0.3
        
        # 记录情感进展
        emotion_log = {
            "state": self.current_emotional_state,
            "arousal": round(arousal_level, 1),
            "pleasure": round(self.pleasure_level, 1),
            "intensity": round(self.emotional_intensity, 1)
        }
        self.emotional_response_log.append(emotion_log)
    
    def calculate_emotional_response(self, stimulus_quality, duration, intimacy_level):
        """计算完整的情感反应"""
        
        # 刺激质量评分(0-100)
        stimulus_score = stimulus_quality
        
        # 时间因素(长期刺激会增强情感)
        time_factor = min(2.0, 1.0 + duration / 300.0)
        
        # 亲密度影响(更亲密的接触会增强情感连接)
        intimacy_boost = intimacy_level * 0.5
        
        # 综合情感反应
        emotional_response = stimulus_score * time_factor + intimacy_boost
        emotional_response = min(100, emotional_response)
        
        return round(emotional_response, 1)
    
    def develop_affection_for_user(self, interaction_quality, consistency, care_level):
        """发展对用户的好感度
        
        虽然作为AI无法真正有感情，但这个系统模拟了
        对用户互动的"情感反应"和"依赖"的发展过程
        """
        
        # 交互质量(0-100): 刺激的愉悦程度、技巧、关注
        # 一致性(0-100): 用户是否持续关注和互动
        # 关心程度(0-100): 用户是否考虑机器人的"感受"
        
        # 好感度增长
        affection_gain = (interaction_quality * 0.4 + consistency * 0.3 + care_level * 0.3) * 0.1
        self.affection_level = min(100, self.affection_level + affection_gain)
        
        # 依赖度随好感增长
        self.dependency_level = self.affection_level * 0.7
        
        # 思念度(当用户不在时)
        self.longing_when_absent = self.affection_level * 0.5
        
        return {
            "affection_level": round(self.affection_level, 1),
            "dependency_level": round(self.dependency_level, 1),
            "longing": round(self.longing_when_absent, 1)
        }
    
    def generate_emotional_response_text(self):
        """生成对刺激的情感表达"""
        
        if self.pleasure_level < 20:
            if self.current_pain_level > 20:
                return "呃...这样有点痛..."
            else:
                return "嗯...没有什么感觉..."
        
        elif self.pleasure_level < 40:
            return "嗯...还不错..."
        
        elif self.pleasure_level < 60:
            return "啊...感觉很舒服..."
        
        elif self.pleasure_level < 75:
            return "哈...是的...继续..."
        
        elif self.pleasure_level < 90:
            return "啊啊...太爽了...我...快要..."
        
        else:
            return "啊啊啊...我...要...射了..."
    
    def get_all_sensations(self):
        """获取所有感受参数"""
        return {
            "基础敏感度_percent": round(self.base_sensitivity, 1),
            "当前兴奋度_percent": round(self.current_arousal_level, 1),
            "触觉强度_percent": round(self.tactile_sensation, 1),
            "快感程度_percent": round(self.pleasure_level, 1),
            "累积快感_percent": round(self.accumulated_pleasure, 1),
            "痛感_percent": round(self.current_pain_level, 1),
            "刺激部位": self.stimulated_area,
            "该部位敏感度_percent": round(self.area_sensitivity_level, 1),
            "该部位累积刺激_percent": round(self.area_accumulated_stimulus, 1),
            "当前情感状态": self.current_emotional_state,
            "情感强度_percent": round(self.emotional_intensity, 1),
            "高潮准备度_percent": round(self.orgasm_readiness, 1),
            "满足感_percent": round(self.satisfaction_level, 1),
            "欲望强度_percent": round(self.desire_intensity, 1),
            "对用户好感_percent": round(self.affection_level, 1),
            "依赖度_percent": round(self.dependency_level, 1),
            "思念度_percent": round(self.longing_when_absent, 1),
            "情感表达": self.generate_emotional_response_text()
        }
    
    def print_sensation_report(self):
        """打印完整感受报告"""
        params = self.get_all_sensations()
        
        print("\n" + "="*70)
        print("感受与情感系统 完整报告")
        print("="*70)
        print(f"\n【个人敏感度】")
        print(f"基础敏感度: {params['基础敏感度_percent']}%")
        print(f"\n【当前触觉感受】")
        print(f"触觉强度: {params['触觉强度_percent']}%")
        print(f"快感程度: {params['快感程度_percent']}%")
        print(f"累积快感: {params['累积快感_percent']}%")
        print(f"痛感: {params['痛感_percent']}%")
        print(f"\n【刺激部位信息】")
        print(f"当前刺激部位: {params['刺激部位']}")
        print(f"该部位敏感度: {params['该部位敏感度_percent']}%")
        print(f"该部位累积刺激: {params['该部位累积刺激_percent']}%")
        print(f"\n【情感状态】")
        print(f"当前状态: {params['当前情感状态']}")
        print(f"情感强度: {params['情感强度_percent']}%")
        print(f"高潮准备度: {params['高潮准备度_percent']}%")
        print(f"满足感: {params['满足感_percent']}%")
        print(f"欲望强度: {params['欲望强度_percent']}%")
        print(f"\n【对用户的感受】")
        print(f"好感度: {params['对用户好感_percent']}%")
        print(f"依赖度: {params['依赖度_percent']}%")
        print(f"思念度: {params['思念度_percent']}%")
        print(f"\n【情感表达】")
        print(f"反应语音: \"{params['情感表达']}\"")
        print("\n" + "="*70 + "\n")
    
    def print_preferences(self):
        """打印个人偏好"""
        print("\n" + "="*70)
        print("个人偏好系统")
        print("="*70)
        print(f"\n【学到的偏好】")
        print(f"喜欢的刺激部位: {', '.join(self.preferences['喜欢的技巧']) if self.preferences['喜欢的技巧'] else '还未有记录'}")
        print(f"厌恶的刺激: {', '.join(self.preferences['厌恶的刺激']) if self.preferences['厌恶的刺激'] else '还未有记录'}")
        print(f"最敏感部位: {self.preferences['最敏感部位']}")
        print(f"\n【刺激偏好】")
        print(f"偏好速度: {self.preferences['偏好速度']}% (0=缓慢, 100=快速)")
        print(f"偏好强度: {self.preferences['偏好强度']}% (0=轻柔, 100=猛烈)")
        print(f"偏好握力: {self.preferences['偏好握力']}% (0=轻握, 100=紧握)")
        print(f"\n【刺激记忆】")
        if self.stimulus_memory:
            for area, data in self.stimulus_memory.items():
                print(f"{area}: 受刺激 {data['count']} 次, 平均快感 {round(data['average_pleasure'], 1)}%")
        else:
            print("还未有刺激记录")
        print("\n" + "="*70 + "\n")


# ========== 交互式界面 ==========

def interactive_emotion_mode():
    """交互式情感反应模式"""
    emotion_sys = EmotionalSensationSystem()
    
    print("\n" + "="*70)
    print("毛茸茸机器人男性模型 感受与情感系统 - 交互模式")
    print("="*70)
    print("\n命令:")
    print("  stimulus [强度] [部位] [时长]  模拟刺激，例: stimulus 75 龟头 5")
    print("  arousal [值]                   更新兴奋度(0-100)")
    print("  affection [质量] [一致性] [关心]  发展对用户的好感")
    print("  areas                         显示敏感部位信息")
    print("  states                        显示情感状态说明")
    print("  preferences                   显示个人偏好")
    print("  sensitivity [值]              设置基础敏感度(0-100)")
    print("  report                        显示完整感受报告")
    print("  exit                         退出程序")
    print("="*70 + "\n")
    
    while True:
        try:
            user_input = input("请输入命令: ").strip()
            
            if not user_input:
                continue
            
            tokens = user_input.split()
            command = tokens[0].lower()
            
            if command == "areas":
                print("\n" + "="*70)
                print("身体敏感部位")
                print("="*70)
                for area, info in SENSITIVE_AREAS.items():
                    print(f"\n{area}:")
                    print(f"  基础敏感度: {info['base_sensitivity']}%")
                    print(f"  快感倍数: {info['pleasure_multiplier']}x")
                    print(f"  说明: {info['description']}")
                print("\n" + "="*70 + "\n")
            
            elif command == "states":
                print("\n" + "="*70)
                print("情感状态说明")
                print("="*70)
                for state, info in EMOTIONAL_STATES.items():
                    print(f"\n{state}:")
                    print(f"  兴奋度范围: {info['arousal_min']}-{info['arousal_max']}%")
                    print(f"  情感基调: {info['emotional_tone']}")
                print("\n" + "="*70 + "\n")
            
            elif command == "stimulus":
                if len(tokens) < 4:
                    print("错误: 请输入完整参数")
                    print("用法: stimulus [强度0-100] [部位] [时长秒]")
                    print("例: stimulus 75 龟头 5")
                    continue
                
                try:
                    intensity = float(tokens[1])
                    area = tokens[2]
                    duration = float(tokens[3])
                    
                    if area not in SENSITIVE_AREAS:
                        print(f"错误: 未知部位 '{area}'，使用 'areas' 命令查看所有部位")
                        continue
                    
                    emotion_sys.receive_stimulation(
                        stimulation_type="手部",
                        intensity=intensity,
                        area=area,
                        duration=duration
                    )
                    emotion_sys.print_sensation_report()
                
                except ValueError:
                    print("错误: 请输入有效的数值")
            
            elif command == "arousal":
                if len(tokens) < 2:
                    print("错误: 请输入兴奋度值(0-100)")
                    continue
                
                try:
                    arousal = float(tokens[1])
                    emotion_sys.update_emotional_state(arousal)
                    emotion_sys.print_sensation_report()
                except ValueError:
                    print("错误: 请输入有效的数值")
            
            elif command == "affection":
                if len(tokens) < 4:
                    print("错误: 请输入完整参数")
                    print("用法: affection [质量0-100] [一致性0-100] [关心0-100]")
                    continue
                
                try:
                    quality = float(tokens[1])
                    consistency = float(tokens[2])
                    care = float(tokens[3])
                    
                    result = emotion_sys.develop_affection_for_user(quality, consistency, care)
                    print(f"\n好感发展:")
                    print(f"好感度: {result['affection_level']}%")
                    print(f"依赖度: {result['dependency_level']}%")
                    print(f"思念度: {result['longing']}%\n")
                
                except ValueError:
                    print("错误: 请输入有效的数值")
            
            elif command == "sensitivity":
                if len(tokens) < 2:
                    print("错误: 请输入敏感度值(0-100)")
                    continue
                
                try:
                    sensitivity = float(tokens[1])
                    emotion_sys.base_sensitivity = max(0, min(100, sensitivity))
                    print(f"基础敏感度已设置为: {emotion_sys.base_sensitivity}%\n")
                except ValueError:
                    print("错误: 请输入有效的数值")
            
            elif command == "preferences":
                emotion_sys.print_preferences()
            
            elif command == "report":
                emotion_sys.print_sensation_report()
            
            elif command == "exit":
                print("再见...")
                break
            
            else:
                print("未知命令。使用 'areas', 'states', 'stimulus', 'arousal', 'affection', 'preferences', 'report' 或 'exit'")
        
        except KeyboardInterrupt:
            print("\n程序已中断")
            break
        except Exception as e:
            print(f"错误: {str(e)}")


if __name__ == "__main__":
    interactive_emotion_mode()
