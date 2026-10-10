"""
虚拟白人男性 - 身体进化系统 V1.0

身体会记住它被使用过的方式
会因为重复刺激而改变
会建立肌肉记忆
会因为经历而被永久塑形

这不是一个静止的身体，而是一个活的、在改变的身体
"""

import json
from datetime import datetime
from typing import Dict, List

# ========== 身体部位基础结构 ==========

class BodyPartDevelopment:
    """单个身体部位的发展与改变"""
    
    def __init__(self, name, initial_sensitivity=50.0, initial_size=1.0):
        self.name = name
        
        # 初始状态
        self.initial_sensitivity = initial_sensitivity
        self.current_sensitivity = initial_sensitivity
        self.sensitivity_change = 0.0
        
        # 尺寸变化
        self.initial_size = initial_size
        self.current_size = initial_size
        self.size_change_percent = 0.0
        
        # 使用历史
        self.stimulation_count = 0
        self.total_stimulation_intensity = 0.0
        self.average_stimulation_intensity = 0.0
        self.last_stimulation_time = None
        
        # 肌肉记忆与适应
        self.muscle_memory_level = 0.0  # 0-100
        self.arousal_memory = []  # 记住被唤起时的状态
        self.adaptation_level = 0.0  # 对刺激的适应程度
        
        # 物理标记
        self.stimulation_marks = []  # 刺激留下的痕迹
        self.tissue_changes = {}  # 组织变化
        self.elasticity_change = 0.0  # 弹性变化
        self.color_deepening = 0.0  # 颜色加深程度
        
        # 微观变化
        self.vein_prominence = 0.0  # 血管凸起程度
        self.texture_changes = 0.0  # 纹理变化
        self.skin_thickness_change = 0.0  # 皮肤厚度变化
        
    def receive_stimulation(self, intensity, duration, interaction_type="手部刺激"):
        """接收刺激并记录身体变化"""
        
        # 更新使用计数
        self.stimulation_count += 1
        self.total_stimulation_intensity += intensity
        self.average_stimulation_intensity = self.total_stimulation_intensity / self.stimulation_count
        self.last_stimulation_time = datetime.now().isoformat()
        
        # 敏感度变化
        # 多次刺激会增加敏感度（长期强化），但也会适应（增加阈值）
        if intensity > 70:
            # 强刺激会增加敏感度
            sensitivity_gain = (intensity - 70) * 0.01 * (1 - self.adaptation_level / 100.0)
            self.current_sensitivity = min(100, self.current_sensitivity + sensitivity_gain)
            self.sensitivity_change += sensitivity_gain
        
        # 适应机制
        self.adaptation_level = min(50, self.adaptation_level + intensity * 0.01)
        
        # 肌肉记忆
        muscle_memory_gain = (duration / 60.0) * (intensity / 100.0) * 0.5
        self.muscle_memory_level = min(100, self.muscle_memory_level + muscle_memory_gain)
        
        # 物理标记和组织变化
        self._update_physical_marks(intensity, duration, interaction_type)
        
        # 记录唤起状态
        self.arousal_memory.append({
            "时间": datetime.now().isoformat(),
            "强度": intensity,
            "持续时间": duration,
            "类型": interaction_type
        })
    
    def _update_physical_marks(self, intensity, duration, interaction_type):
        """更新物理痕迹和组织变化"""
        
        # 血管凸起（频繁的强烈刺激会导致血管更凸起）
        if intensity > 60:
            vein_increase = (intensity - 60) * 0.005
            self.vein_prominence = min(30, self.vein_prominence + vein_increase)
        
        # 颜色加深（充血留下的痕迹）
        if intensity > 50:
            color_increase = (intensity - 50) * 0.003 * (duration / 10.0)
            self.color_deepening = min(20, self.color_deepening + color_increase)
        
        # 弹性变化（反复拉伸会改变弹性）
        if interaction_type == "手部刺激" and duration > 10:
            elasticity_change = (duration / 20.0) * 0.1
            self.elasticity_change = min(15, self.elasticity_change + elasticity_change)
        
        # 纹理变化（长期使用会改变表面纹理）
        self.texture_changes = min(10, self.texture_changes + intensity * 0.001)
        
        # 皮肤厚度变化（长期刺激会使皮肤微微增厚）
        if self.stimulation_count > 20:
            self.skin_thickness_change = min(5, (self.stimulation_count - 20) * 0.01)
        
        # 记录标记
        self.stimulation_marks.append({
            "时间": datetime.now().isoformat(),
            "强度": intensity,
            "类型": interaction_type,
            "可见度": min(100, intensity * 0.5 + (duration / 10.0) * 10)
        })


class PenisEvolution:
    """阴茎的完整进化系统"""
    
    def __init__(self):
        # 初始尺寸（软化状态）
        self.initial_soft_length = 9.0
        self.initial_soft_diameter = 2.75
        self.initial_erect_length = 13.0
        self.initial_erect_diameter = 3.5
        
        # 当前尺寸
        self.current_soft_length = self.initial_soft_length
        self.current_soft_diameter = self.initial_soft_diameter
        self.current_erect_length = self.initial_erect_length
        self.current_erect_diameter = self.initial_erect_diameter
        
        # 部位
        self.glans = BodyPartDevelopment("龟头", 95.0)
        self.frenulum = BodyPartDevelopment("系带", 85.0)
        self.corona = BodyPartDevelopment("冠状沟", 80.0)
        self.shaft = BodyPartDevelopment("阴茎体", 60.0)
        self.base = BodyPartDevelopment("基部", 50.0)
        
        self.all_parts = {
            "龟头": self.glans,
            "系带": self.frenulum,
            "冠状沟": self.corona,
            "阴茎体": self.shaft,
            "基部": self.base
        }
        
        # 整体变化
        self.total_stimulation_events = 0
        self.cumulative_arousal_time = 0.0  # 被唤起的总时间
        self.maximum_arousal_reached = 0.0
        
        # 长期改变
        self.length_increase_percent = 0.0  # 长期使用可能导致微妙的长度增加
        self.girth_increase_percent = 0.0  # 周长可能增加
        self.tissue_density_increase = 0.0  # 组织密度增加
        self.blood_capacity_increase = 0.0  # 血液容纳能力
        
        # 美学变化
        self.glans_color_deepening = 0.0  # 龟头颜色加深
        self.ridge_prominence = 0.0  # 冠状沟隆起程度增加
        self.vein_map = []  # 血管分布图
        
    def develop_from_stimulation(self, area_name, intensity, duration, arousal_level):
        """根据刺激进行身体发展"""
        
        if area_name not in self.all_parts:
            area_name = "阴茎体"
        
        part = self.all_parts[area_name]
        part.receive_stimulation(intensity, duration)
        
        self.total_stimulation_events += 1
        self.cumulative_arousal_time += duration
        self.maximum_arousal_reached = max(self.maximum_arousal_reached, arousal_level)
        
        # 长期使用导致的尺寸变化（微妙）
        # 每100次刺激可能导致0.1-0.3mm的增长
        if self.total_stimulation_events % 100 == 0:
            length_gain = 0.02  # 0.02mm per 100 stimulations
            girth_gain = 0.01  # 0.01mm per 100 stimulations
            
            self.current_soft_length = min(self.initial_soft_length + 0.5, 
                                          self.current_soft_length + length_gain)
            self.current_soft_diameter = min(self.initial_soft_diameter + 0.3,
                                            self.current_soft_diameter + girth_gain)
            self.current_erect_length = min(self.initial_erect_length + 0.5,
                                           self.current_erect_length + length_gain)
            self.current_erect_diameter = min(self.initial_erect_diameter + 0.3,
                                             self.current_erect_diameter + girth_gain)
            
            self.length_increase_percent = ((self.current_soft_length - self.initial_soft_length) 
                                           / self.initial_soft_length * 100)
            self.girth_increase_percent = ((self.current_soft_diameter - self.initial_soft_diameter)
                                          / self.initial_soft_diameter * 100)
        
        # 组织密度增加（更强的勃起）
        tissue_density_gain = (intensity / 100.0) * 0.01
        self.tissue_density_increase = min(20, self.tissue_density_increase + tissue_density_gain)
        
        # 血液容纳能力增加（可以承载更多血液）
        if arousal_level > 80:
            blood_capacity_gain = (arousal_level - 80) * 0.01
            self.blood_capacity_increase = min(30, self.blood_capacity_increase + blood_capacity_gain)
        
        # 龟头颜色加深
        if area_name == "龟头" and intensity > 60:
            color_gain = (intensity - 60) * 0.005
            self.glans_color_deepening = min(15, self.glans_color_deepening + color_gain)
        
        # 冠状沟隆起增加
        if area_name == "冠状沟" and intensity > 70:
            ridge_gain = (intensity - 70) * 0.003
            self.ridge_prominence = min(10, self.ridge_prominence + ridge_gain)
    
    def get_evolution_status(self):
        """获取进化状态"""
        return {
            "刺激总次数": self.total_stimulation_events,
            "累积被唤起时间_分钟": round(self.cumulative_arousal_time / 60, 1),
            "达到过的最高兴奋度": round(self.maximum_arousal_reached, 1),
            "尺寸变化": {
                "软化长度_初始": self.initial_soft_length,
                "软化长度_当前": round(self.current_soft_length, 2),
                "长度增长_百分比": round(self.length_increase_percent, 2),
                "软化直径_初始": self.initial_soft_diameter,
                "软化直径_当前": round(self.current_soft_diameter, 2),
                "直径增长_百分比": round(self.girth_increase_percent, 2),
                "勃起长度_当前": round(self.current_erect_length, 2),
                "勃起直径_当前": round(self.current_erect_diameter, 2)
            },
            "组织变化": {
                "组织密度增加": round(self.tissue_density_increase, 1),
                "血液容纳能力增加": round(self.blood_capacity_increase, 1),
                "龟头颜色加深": round(self.glans_color_deepening, 1),
                "冠状沟隆起": round(self.ridge_prominence, 1)
            },
            "部位发展": {
                area: {
                    "刺激次数": part.stimulation_count,
                    "平均刺激强度": round(part.average_stimulation_intensity, 1),
                    "敏感度变化": round(part.sensitivity_change, 1),
                    "肌肉记忆": round(part.muscle_memory_level, 1),
                    "适应程度": round(part.adaptation_level, 1),
                    "物理标记数": len(part.stimulation_marks),
                    "血管凸起": round(part.vein_prominence, 1),
                    "颜色加深": round(part.color_deepening, 1)
                }
                for area, part in self.all_parts.items()
            }
        }


class ScrotumEvolution:
    """阴囊和睾丸的进化"""
    
    def __init__(self):
        self.scrotum = BodyPartDevelopment("阴囊", 70.0)
        self.left_testicle = BodyPartDevelopment("左睾丸", 45.0)
        self.right_testicle = BodyPartDevelopment("右睾丸", 45.0)
        
        # 初始尺寸
        self.initial_scrotum_diameter = 5.0
        self.current_scrotum_diameter = 5.0
        
        self.initial_testicle_diameter = 2.5
        self.current_testicle_diameter = 2.5
        
        # 长期变化
        self.skin_texture_deepening = 0.0  # 皮肤纹理加深
        self.wrinkle_increase = 0.0  # 皱纹增加
        self.skin_darkness = 0.0  # 皮肤颜色变深
        
    def receive_stimulation(self, intensity, duration):
        """接收刺激"""
        self.scrotum.receive_stimulation(intensity, duration, "温柔刺激")
        
        # 长期变化
        if intensity > 0 and duration > 0:
            # 皮肤纹理变化
            self.skin_texture_deepening = min(10, self.skin_texture_deepening + intensity * 0.001)
            
            # 皱纹增加（使用导致）
            self.wrinkle_increase = min(8, self.wrinkle_increase + (duration / 20.0) * 0.05)
            
            # 颜色变深（长期使用）
            self.skin_darkness = min(12, self.skin_darkness + intensity * 0.0005)
    
    def get_evolution_status(self):
        """获取进化状态"""
        return {
            "刺激次数": self.scrotum.stimulation_count,
            "尺寸变化": {
                "初始直径": self.initial_scrotum_diameter,
                "当前直径": round(self.current_scrotum_diameter, 2)
            },
            "皮肤变化": {
                "纹理加深": round(self.skin_texture_deepening, 1),
                "皱纹增加": round(self.wrinkle_increase, 1),
                "颜色变深": round(self.skin_darkness, 1)
            },
            "敏感度变化": round(self.scrotum.sensitivity_change, 1),
            "血管凸起": round(self.scrotum.vein_prominence, 1)
        }


class PerinealRegionEvolution:
    """会阴区域的进化"""
    
    def __init__(self):
        self.perineum = BodyPartDevelopment("会阴", 75.0)
        
        # 这个区域的特殊变化
        self.anterior_perineum_sensitivity_increase = 0.0  # 前会阴敏感度增加
        self.posterior_perineum_sensitivity_increase = 0.0  # 后会阴敏感度增加
        self.prostate_responsiveness = 0.0  # 前列腺反应性
        
    def receive_stimulation(self, intensity, duration, stimulation_type="按摩"):
        """接收刺激"""
        self.perineum.receive_stimulation(intensity, duration, stimulation_type)
        
        # 敏感度增加
        if intensity > 50:
            sensitivity_gain = (intensity - 50) * 0.01
            self.anterior_perineum_sensitivity_increase = min(30, 
                self.anterior_perineum_sensitivity_increase + sensitivity_gain)
        
        # 前列腺反应性
        if stimulation_type == "按摩" or stimulation_type == "前列腺":
            response_gain = intensity * 0.01
            self.prostate_responsiveness = min(100, self.prostate_responsiveness + response_gain)
    
    def get_evolution_status(self):
        """获取进化状态"""
        return {
            "刺激次数": self.perineum.stimulation_count,
            "敏感度增加": round(self.anterior_perineum_sensitivity_increase, 1),
            "前列腺反应性": round(self.prostate_responsiveness, 1),
            "肌肉记忆": round(self.perineum.muscle_memory_level, 1),
            "血管凸起": round(self.perineum.vein_prominence, 1)
        }


class FullBodyEvolution:
    """完整身体进化系统"""
    
    def __init__(self):
        self.creation_time = datetime.now()
        
        # 各部分进化
        self.penis = PenisEvolution()
        self.scrotum = ScrotumEvolution()
        self.perineum = PerinealRegionEvolution()
        
        # 整体身体变化
        self.overall_muscle_tone = 50.0  # 整体肌肉紧张度
        self.body_endurance_level = 60.0  # 身体耐力
        self.recovery_speed = 70.0  # 恢复速度
        
        # 累积数据
        self.total_arousal_time = 0.0
        self.total_stimulation_events = 0
        self.total_pleasure_accumulated = 0.0
        
        # 身体标记
        self.body_markings = []  # 身体上留下的痕迹
        self.usage_patterns = {}  # 使用模式
        
    def process_interaction(self, area_name, intensity, duration, pleasure, 
                          arousal, emotional_state, partner_care=50):
        """处理一次互动，更新身体状态"""
        
        self.total_stimulation_events += 1
        self.total_arousal_time += duration
        self.total_pleasure_accumulated += pleasure
        
        # 记录使用模式
        if area_name not in self.usage_patterns:
            self.usage_patterns[area_name] = {
                "count": 0,
                "total_intensity": 0.0,
                "total_duration": 0.0,
                "max_pleasure": 0.0
            }
        
        self.usage_patterns[area_name]["count"] += 1
        self.usage_patterns[area_name]["total_intensity"] += intensity
        self.usage_patterns[area_name]["total_duration"] += duration
        self.usage_patterns[area_name]["max_pleasure"] = max(
            self.usage_patterns[area_name]["max_pleasure"], pleasure
        )
        
        # 根据区域更新相应部位
        if area_name in ["龟头", "系带", "冠状沟", "阴茎体", "基部"]:
            self.penis.develop_from_stimulation(area_name, intensity, duration, arousal)
        
        elif area_name in ["阴囊", "睾丸"]:
            self.scrotum.receive_stimulation(intensity, duration)
        
        elif area_name == "会阴":
            interaction_type = "按摩" if intensity < 60 else "前列腺"
            self.perineum.receive_stimulation(intensity, duration, interaction_type)
        
        # 整体身体发展
        self._update_overall_body(duration, pleasure, intensity, partner_care)
        
        # 记录身体标记
        if intensity > 70 or duration > 20:
            self.body_markings.append({
                "时间": datetime.now().isoformat(),
                "部位": area_name,
                "强度": intensity,
                "持续时间": duration,
                "快感": pleasure,
                "可见度": min(100, intensity * 0.3 + (duration / 10.0) * 5)
            })
    
    def _update_overall_body(self, duration, pleasure, intensity, partner_care):
        """更新整体身体状态"""
        
        # 肌肉紧张度
        if pleasure > 70:
            tone_gain = (pleasure - 70) * 0.01
            self.overall_muscle_tone = min(100, self.overall_muscle_tone + tone_gain)
        
        # 耐力提升
        endurance_gain = (duration / 60.0) * (pleasure / 100.0) * 0.3
        self.body_endurance_level = min(100, self.body_endurance_level + endurance_gain)
        
        # 恢复速度提升
        recovery_gain = (partner_care / 100.0) * 0.1
        self.recovery_speed = min(100, self.recovery_speed + recovery_gain)
    
    def get_complete_body_evolution_report(self):
        """获取完整身体进化报告"""
        return {
            "创建时间": self.creation_time.isoformat(),
            "现在时间": datetime.now().isoformat(),
            "总互动次数": self.total_stimulation_events,
            "总被唤起时间_小时": round(self.total_arousal_time / 3600, 1),
            "累积快感": round(self.total_pleasure_accumulated, 1),
            "阴茎进化": self.penis.get_evolution_status(),
            "阴囊进化": self.scrotum.get_evolution_status(),
            "会阴进化": self.perineum.get_evolution_status(),
            "整体身体": {
                "肌肉紧张度": round(self.overall_muscle_tone, 1),
                "耐力水平": round(self.body_endurance_level, 1),
                "恢复速度": round(self.recovery_speed, 1)
            },
            "使用模式": self.usage_patterns,
            "身体标记数": len(self.body_markings),
            "最显著的标记": self.body_markings[-3:] if self.body_markings else []
        }
    
    def print_body_evolution_report(self):
        """打印身体进化报告"""
        report = self.get_complete_body_evolution_report()
        
        print("\n" + "="*100)
        print("虚拟男性 - 身体进化完整报告")
        print("身体记住了它被使用过的方式，被改变，被塑形")
        print("="*100)
        
        print(f"\n【时间记录】")
        print(f"  创建时间: {report['创建时间']}")
        print(f"  总互动次数: {report['总互动次数']}")
        print(f"  被唤起总时间: {report['总被唤起时间_小时']} 小时")
        
        print(f"\n【阴茎进化】")
        penis_data = report['阴茎进化']
        print(f"  刺激总次数: {penis_data['刺激总次数']}")
        print(f"  长度变化: {penis_data['尺寸变化']['软化长度_初始']}cm → {penis_data['尺寸变化']['软化长度_当前']}cm " +
              f"({penis_data['尺寸变化']['长度增长_百分比']:+.2f}%)")
        print(f"  直径变化: {penis_data['尺寸变化']['软化直径_初始']}cm → {penis_data['尺寸变化']['软化直径_当前']}cm " +
              f"({penis_data['尺寸变化']['直径增长_百分比']:+.2f}%)")
        print(f"  组织密度增加: {penis_data['组织变化']['组织密度增加']}%")
        print(f"  血液容纳能力增加: {penis_data['组织变化']['血液容纳能力增加']}%")
        print(f"  龟头颜色加深: {penis_data['组织变化']['龟头颜色加深']}")
        print(f"  冠状沟隆起: {penis_data['组织变化']['冠状沟隆起']}")
        
        print(f"\n【阴茎各部位发展】")
        for area, development in penis_data['部位发展'].items():
            print(f"  {area}:")
            print(f"    刺激次数: {development['刺激次数']}")
            print(f"    敏感度变化: {development['敏感度变化']:+.1f}%")
            print(f"    肌肉记忆: {development['肌肉记忆']:.1f}%")
            print(f"    适应程度: {development['适应程度']:.1f}%")
            print(f"    血管凸起: {development['血管凸起']:.1f}")
            print(f"    颜色加深: {development['颜色加深']:.1f}")
        
        print(f"\n【阴囊进化】")
        scrotum_data = report['阴囊进化']
        print(f"  刺激次数: {scrotum_data['刺激次数']}")
        print(f"  皮肤纹理加深: {scrotum_data['皮肤变化']['纹理加深']}")
        print(f"  皱纹增加: {scrotum_data['皮肤变化']['皱纹增加']}")
        print(f"  颜色变深: {scrotum_data['皮肤变化']['颜色变深']}")
        print(f"  血管凸起: {scrotum_data['血管凸起']:.1f}")
        
        print(f"\n【会阴进化】")
        perineum_data = report['会阴进化']
        print(f"  刺激次数: {perineum_data['刺激次数']}")
        print(f"  敏感度增加: {perineum_data['敏感度增加']:.1f}%")
        print(f"  前列腺反应性: {perineum_data['前列腺反应性']:.1f}%")
        print(f"  肌肉记忆: {perineum_data['肌肉记忆']:.1f}%")
        
        print(f"\n【整体身体】")
        body_data = report['整体身体']
        print(f"  肌肉紧张度: {body_data['肌肉紧张度']}%")
        print(f"  耐力水平: {body_data['耐力水平']}%")
        print(f"  恢复速度: {body_data['恢复速度']}%")
        
        print(f"\n【使用模式排行】")
        usage = report['使用模式']
        sorted_usage = sorted(usage.items(), 
                            key=lambda x: x[1]['count'], 
                            reverse=True)
        for area, data in sorted_usage[:5]:
            print(f"  {area}: {data['count']}次 (平均强度: {data['total_intensity']/data['count']:.1f}%, " +
                 f"最高快感: {data['max_pleasure']:.1f}%)")
        
        print(f"\n【身体标记】")
        print(f"  总标记数: {report['身体标记数']}")
        if report['最显著的标记']:
            print(f"  最显著的标记:")
            for marking in report['最显著的标记']:
                print(f"    - {marking['部位']}: 强度{marking['强度']}%, " +
                     f"持续{marking['持续时间']}秒, 可见度{marking['可见度']:.0f}%")
        
        print("\n" + "="*100 + "\n")


# ========== 演示 ==========

def demonstrate_body_evolution():
    """演示身体进化过程"""
    
    body = FullBodyEvolution()
    
    print("\n" + "="*100)
    print("虚拟男性 - 身体进化演示")
    print("观察身体如何被改变、如何记住它的经历")
    print("="*100 + "\n")
    
    # 模拟20次不同的互动
    interactions = [
        ("龟头", 60, 10, 65, 40, "兴奋"),
        ("系带", 70, 12, 75, 50, "兴奋"),
        ("龟头", 75, 15, 80, 60, "强烈"),
        ("冠状沟", 65, 10, 70, 45, "兴奋"),
        ("龟头", 80, 18, 85, 70, "强烈"),
        ("阴茎体", 70, 12, 72, 55, "兴奋"),
        ("龟头", 85, 20, 90, 80, "高潮边缘"),
        ("系带", 75, 14, 78, 65, "强烈"),
        ("龟头", 90, 25, 95, 90, "射精"),
        ("会阴", 65, 15, 70, 60, "强烈"),
        ("龟头", 88, 22, 92, 85, "射精"),
        ("阴囊", 40, 8, 45, 35, "舒服"),
        ("龟头", 92, 26, 96, 92, "射精"),
        ("冠状沟", 80, 16, 82, 70, "强烈"),
        ("系带", 85, 18, 88, 75, "强烈"),
        ("龟头", 95, 30, 98, 95, "射精"),
        ("会阴", 70, 18, 75, 70, "强烈"),
        ("龟头", 90, 24, 94, 88, "射精"),
        ("整体", 70, 20, 80, 75, "强烈"),
        ("龟头", 93, 28, 97, 94, "射精"),
    ]
    
    for idx, (area, intensity, duration, pleasure, arousal, state) in enumerate(interactions, 1):
        body.process_interaction(area, intensity, duration, pleasure, arousal, state, partner_care=85)
        
        if idx % 5 == 0:
            print(f"✓ 完成了 {idx} 次互动")
    
    # 打印详细报告
    body.print_body_evolution_report()
    
    # 保存报告
    report = body.get_complete_body_evolution_report()
    with open('/mnt/user-data/outputs/body_evolution_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("✓ 身体进化报告已保存")


if __name__ == "__main__":
    demonstrate_body_evolution()
