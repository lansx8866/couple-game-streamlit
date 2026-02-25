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

# ======================= 生成SVG转盘 =======================
def get_svg_wheel(items, is_reward, rotation=0):
    colors = [
        "#FF9BBB", "#FF789E", "#FF5C87", "#FF4473", "#FF2A5F", "#FF0040"
    ] if is_reward else [
        "#FFB380", "#FF9F66", "#FF8C4D", "#FF7833", "#FF6519", "#FF5100"
    ]
    
    size = 300
    radius = size // 2 - 10
    center = size // 2
    sectors = []
    angles = [0, 60, 120, 180, 240, 300]
    
    for i, (start_angle, text) in enumerate(zip(angles, items)):
        end_angle = start_angle + 60
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        x1 = center + radius * math.cos(start_rad)
        y1 = center - radius * math.sin(start_rad)
        x2 = center + radius * math.cos(end_rad)
        y2 = center - radius * math.sin(end_rad)
        
        path = f"M {center} {center} L {x1} {y1} A {radius} {radius} 0 0 1 {x2} {y2} Z"
        
        mid_angle = (start_angle + end_angle) / 2
        mid_rad = math.radians(mid_angle)
        text_x = center + (radius * 0.6) * math.cos(mid_rad)
        text_y = center - (radius * 0.6) * math.sin(mid_rad)
        text_rotate = mid_angle if mid_angle < 180 else mid_angle - 180
        
        sectors.append(f"""
            <path d="{path}" fill="{colors[i]}" stroke="#fff" stroke-width="2"/>
            <text x="{text_x}" y="{text_y}" text-anchor="middle" dominant-baseline="middle" 
                  fill="#fff" font-size="12" font-weight="bold" transform="rotate({text_rotate} {text_x} {text_y})">
                {text}
            </text>
        """)
    
    svg = f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="display:block; margin:0 auto;">
        <g transform="rotate({rotation} {center} {center})">
            {''.join(sectors)}
            <circle cx="{center}" cy="{center}" r="{radius}" fill="none" stroke="#333" stroke-width="3"/>
        </g>
        <polygon points="{center},{center-20} {center-10},{center} {center+10},{center}" 
                 fill="red" stroke="#000" stroke-width="1"/>
        <circle cx="{center}" cy="{center}" r="8" fill="#fff" stroke="#333" stroke-width="2"/>
    </svg>
    """
    return svg

# ======================= 初始化会话状态 =======================
st.set_page_config(page_title="情侣默契转盘", layout="wide")

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
    st.session_state.rotation = 0
if "final" not in st.session_state:
    st.session_state.final = ""
if "spun" not in st.session_state:
    st.session_state.spun = False

# ------------------- 步骤1：选择题目 -------------------
if st.session_state.step == 1:
    st.subheader("📝 选择题目", divider="violet")
    q = st.selectbox("请选择考验题目", list(QUESTION_BANK.keys()))
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

# ------------------- 步骤4：可视化转盘抽奖（核心修复） -------------------
elif st.session_state.step == 4:
    ok = st.session_state.result
    items = REWARD if ok else PUNISH
    
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
    
    st.subheader("🎡 可视化转盘抽奖", divider="violet")
    
    if not st.session_state.spun:
        # 初始转盘
        svg = get_svg_wheel(items, ok, 0)
        st.components.v1.html(svg, height=320)
        
        if st.button("🚀 旋转转盘", type="primary", use_container_width=True):
            target_idx = random.randint(0, 5)
            target_rotation = 8 * 360 + (360 - target_idx * 60)
            st.session_state.final = items[target_idx]
            
            with st.spinner("转盘旋转中..."):
                for r in range(0, target_rotation, 10):
                    svg = get_svg_wheel(items, ok, r)
                    st.components.v1.html(svg, height=320)
                    time.sleep(0.01)
            
            st.session_state.rotation = target_rotation
            st.session_state.spun = True
            st.rerun()
    else:
        # 旋转后的转盘
        svg = get_svg_wheel(items, ok, st.session_state.rotation)
        st.components.v1.html(svg, height=320)
        st.markdown(f"### 🏆 最终结果：\n## {st.session_state.final}")
        
        if st.button("🔄 再来一局", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
