import streamlit as st
import random
import time
import math

# ======================= 题目库 =======================
QUESTION_BANK = {
    "对方的三个优点": ["温柔体贴", "有责任心", "幽默有趣", "上进努力", "细心周到", "情绪稳定"],
    "我的三个优点": ["乐观开朗", "包容心强", "动手能力强", "善于倾听", "真诚坦率", "有耐心"],
    "对方的三个缺点": ["有点拖延", "偶尔脾气急", "不爱收拾", "太宅", "话少", "容易焦虑"],
    "我的三个缺点": ["有点敏感", "缺乏耐心", "熬夜", "挑食", "容易胡思乱想", "不爱主动"],
    "最想和对方一起做的事": ["看海边日出", "做烛光晚餐", "短途旅行", "拍情侣写真", "宅家追剧"],
    "对方做什么最让你感动": ["记住小习惯", "难过时陪着", "主动分担家务", "准备小惊喜", "公开维护我"],
    "对方做什么会让你生气": ["不回消息", "冷暴力", "忘记重要日子", "敷衍", "边界不清"],
    "最忍受不了的行为": ["撒谎", "不尊重家人", "沉迷手机", "翻旧账", "负能量爆棚"],
    "形容你的另一半": ["可爱", "靠谱", "粘人", "温柔", "独立", "帅气/漂亮"],
    "对方最吸引你的细节": ["笑起来", "认真做事", "照顾我", "摸我头", "吃醋的样子"],
}

REWARD = ["捏肩10分钟", "承包家务", "买奶茶", "抱抱5分钟", "今天听你的", "手写情书"]
PUNISH = ["学小猫叫", "讲冷笑话", "深蹲10个", "夸对方10句", "洗水果", "模仿口头禅"]

# ======================= 生成SVG转盘（指针同步动） =======================
def get_svg_wheel(items, is_reward, rotation=0):
    """转盘旋转，指针反向旋转（视觉上指针动）"""
    # 颜色配置
    colors = [
        "#FF9BBB", "#FF789E", "#FF5C87", "#FF4473", "#FF2A5F", "#FF0040"
    ] if is_reward else [
        "#FFB380", "#FF9F66", "#FF8C4D", "#FF7833", "#FF6519", "#FF5100"
    ]
    
    # 转盘基础参数
    size = 350  # 放大转盘，更清晰
    radius = size // 2 - 15
    center = size // 2
    sectors = []
    angles = [0, 60, 120, 180, 240, 300]  # 6个扇区，每个60度
    
    # 生成扇区
    for i, (start_angle, text) in enumerate(zip(angles, items)):
        end_angle = start_angle + 60
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # 扇区路径坐标
        x1 = center + radius * math.cos(start_rad)
        y1 = center - radius * math.sin(start_rad)
        x2 = center + radius * math.cos(end_rad)
        y2 = center - radius * math.sin(end_rad)
        
        # 扇区路径
        path = f"M {center} {center} L {x1} {y1} A {radius} {radius} 0 0 1 {x2} {y2} Z"
        
        # 文字位置（扇区中间）
        mid_angle = (start_angle + end_angle) / 2
        mid_rad = math.radians(mid_angle)
        text_x = center + (radius * 0.6) * math.cos(mid_rad)
        text_y = center - (radius * 0.6) * math.sin(mid_rad)
        text_rotate = mid_angle if mid_angle < 180 else mid_angle - 180
        
        # 扇区+文字
        sectors.append(f"""
            <path d="{path}" fill="{colors[i]}" stroke="#fff" stroke-width="3"/>
            <text x="{text_x}" y="{text_y}" text-anchor="middle" dominant-baseline="middle" 
                  fill="#fff" font-size="14" font-weight="bold" transform="rotate({text_rotate} {text_x} {text_y})">
                {text}
            </text>
        """)
    
    # 完整SVG（转盘旋转+指针反向旋转，视觉上指针动）
    svg = f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="display:block; margin:0 auto;">
        <!-- 转盘背景 -->
        <circle cx="{center}" cy="{center}" r="{radius+5}" fill="#f5f5f5" stroke="#333" stroke-width="4"/>
        
        <!-- 转盘扇区（正向旋转） -->
        <g transform="rotate({rotation} {center} {center})">
            {''.join(sectors)}
            <circle cx="{center}" cy="{center}" r="{radius}" fill="none" stroke="#333" stroke-width="2"/>
        </g>
        
        <!-- 指针（反向旋转，视觉上指针动） -->
        <g transform="rotate({-rotation} {center} {center})">
            <!-- 指针主体（更醒目） -->
            <polygon points="{center},{center-30} {center-15},{center+10} {center+15},{center+10}" 
                     fill="red" stroke="#000" stroke-width="2"/>
            <!-- 指针尖端高亮 -->
            <circle cx="{center}" cy="{center-30}" r="5" fill="yellow" stroke="red" stroke-width="1"/>
        </g>
        
        <!-- 中心圆点（加大） -->
        <circle cx="{center}" cy="{center}" r="12" fill="#fff" stroke="#333" stroke-width="3"/>
        <circle cx="{center}" cy="{center}" r="8" fill="#333"/>
    </svg>
    """
    return svg

# ======================= 初始化会话状态 =======================
st.set_page_config(page_title="情侣默契转盘", layout="wide")

# 初始化所有状态
if "step" not in st.session_state:
    st.session_state.step = 1
if "question" not in st.session_state:
    st.session_state.question = ""
if "p1" not in st.session_state:
    st.session_state.p1 = []
if "p2" not in st.session_state:
    st.session_state.p2 = []
if "result" not in st.session_state:
    st.session_state.result = None
if "rotation" not in st.session_state:
    st.session_state.rotation = 0  # 旋转角度
if "final" not in st.session_state:
    st.session_state.final = ""
if "spun" not in st.session_state:
    st.session_state.spun = False
if "animating" not in st.session_state:
    st.session_state.animating = False

# ------------------- 步骤1：选择题目 -------------------
if st.session_state.step == 1:
    st.subheader("📝 选择题目", divider="violet")
    q = st.selectbox("请选择考验题目", list(QUESTION_BANK.keys()), key="q_select")
    st.session_state.question = q
    if st.button("✅ 确定开始", type="primary"):
        st.session_state.step = 2
        st.rerun()

# ------------------- 步骤2：玩家1答题 -------------------
elif st.session_state.step == 2:
    q = st.session_state.question
    opt = QUESTION_BANK[q]
    st.subheader(f"👩 玩家1答题：{q}", divider="violet")
    
    if "优点" in q or "缺点" in q:
        s = st.multiselect("请选择3个答案（最多3个）", opt, max_selections=3, key="p1s")
        if len(s) == 3:
            st.session_state.p1 = s
            if st.button("✅ 答完，轮到玩家2", type="primary"):
                st.session_state.step = 3
                st.rerun()
        else:
            st.info(f"已选 {len(s)}/3 个，需选满3个！")
    else:
        s = st.radio("请选择1个答案", opt, key="p1s")
        st.session_state.p1 = [s]
        if st.button("✅ 答完，轮到玩家2", type="primary"):
            st.session_state.step = 3
            st.rerun()

# ------------------- 步骤3：玩家2答题 -------------------
elif st.session_state.step == 3:
    q = st.session_state.question
    opt = QUESTION_BANK[q]
    st.subheader(f"👨 玩家2答题：{q}", divider="violet")
    
    if "优点" in q or "缺点" in q:
        s = st.multiselect("请选择3个答案（最多3个）", opt, max_selections=3, key="p2s")
        if len(s) == 3:
            st.session_state.p2 = s
            if st.button("🎯 查看默契结果", type="primary"):
                same = len(set(st.session_state.p1) & set(st.session_state.p2))
                st.session_state.result = same >= 2
                st.session_state.step = 4
                st.rerun()
        else:
            st.info(f"已选 {len(s)}/3 个，需选满3个！")
    else:
        s = st.radio("请选择1个答案", opt, key="p2s")
        st.session_state.p2 = [s]
        if st.button("🎯 查看默契结果", type="primary"):
            same = len(set(st.session_state.p1) & set(st.session_state.p2))
            st.session_state.result = same >= 1
            st.session_state.step = 4
            st.rerun()

# ------------------- 步骤4：可视化转盘抽奖（修复语法错误） -------------------
elif st.session_state.step == 4:
    ok = st.session_state.result
    items = REWARD if ok else PUNISH
    
    # 展示结果
    st.subheader("🧩 默契结果揭晓", divider="violet")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**玩家1答案**：{', '.join(st.session_state.p1)}")
        st.write(f"**玩家2答案**：{', '.join(st.session_state.p2)}")
    with col2:
        if ok:
            st.success("🎉 默契成功！解锁奖励转盘～")
        else:
            st.warning("😜 默契不足！开启惩罚转盘～")
    
    # 转盘区域（核心修复：不用placeholder链式调用）
    st.subheader("🎡 可视化转盘抽奖", divider="violet")
    
    # 未抽奖/动画中
    if not st.session_state.spun and not st.session_state.animating:
        # 初始转盘（指针在顶部）
        svg = get_svg_wheel(items, ok, st.session_state.rotation)
        st.components.v1.html(svg, height=380)
        
        if st.button("🚀 旋转转盘", type="primary", use_container_width=True):
            st.session_state.animating = True
            target_idx = random.randint(0, 5)
            # 旋转角度：10圈+随机停止位置（先快后慢）
            total_rotation = 10 * 360 + (360 - target_idx * 60)
            st.session_state.final = items[target_idx]
            
            # 清空当前转盘，准备动画
            st.empty()
            
            # 分阶段动画：先快后慢（更真实）
            with st.spinner("转盘旋转中..."):
                # 快速旋转阶段（前8圈）
                for r in range(0, 8*360, 20):
                    st.session_state.rotation = r
                    svg = get_svg_wheel(items, ok, r)
                    st.components.v1.html(svg, height=380)
                    time.sleep(0.005)
                    st.empty()  # 清空上一帧
                
                # 减速阶段（后2圈）
                for r in range(8*360, total_rotation, 5):
                    st.session_state.rotation = r
                    svg = get_svg_wheel(items, ok, r)
                    st.components.v1.html(svg, height=380)
                    time.sleep(0.02)
                    st.empty()  # 清空上一帧
            
            # 最终停止（显示最终转盘）
            st.session_state.rotation = total_rotation
            final_svg = get_svg_wheel(items, ok, total_rotation)
            st.components.v1.html(final_svg, height=380)
            
            st.session_state.spun = True
            st.session_state.animating = False
            st.rerun()
    
    # 抽奖完成显示结果
    elif st.session_state.spun:
        # 显示最终停止的转盘
        final_svg = get_svg_wheel(items, ok, st.session_state.rotation)
        st.components.v1.html(final_svg, height=380)
        
        st.markdown(f"### 🏆 最终结果：\n## {st.session_state.final}")
        
        if st.button("🔄 再来一局", use_container_width=True):
            # 重置所有状态
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
