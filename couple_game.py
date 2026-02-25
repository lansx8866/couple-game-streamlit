import streamlit as st
import random
import time

# ======================= 【后端固定配置】 =======================
QUESTION_BANK = {
    # 优点类（选3个）
    "对方的三个优点": ["温柔体贴", "有责任心", "幽默有趣", "上进努力", "细心周到", "情绪稳定"],
    "我的三个优点": ["乐观开朗", "包容心强", "动手能力强", "善于倾听", "真诚坦率", "有耐心"],
    # 缺点类（选3个）
    "对方的三个缺点": ["有点拖延", "偶尔脾气急", "不爱收拾", "太宅", "话少", "容易焦虑"],
    "我的三个缺点": ["有点敏感", "缺乏耐心", "熬夜", "挑食", "容易胡思乱想", "不爱主动"],
    # 其他类（选1个）
    "最想和对方一起做的事": ["看海边日出", "做烛光晚餐", "短途旅行", "拍情侣写真", "宅家追剧"],
    "对方做什么最让你感动": ["记住小习惯", "难过时陪着", "主动分担家务", "准备小惊喜", "公开维护我"],
    "对方做什么会让你生气": ["不回消息", "冷暴力", "忘记重要日子", "敷衍", "边界不清"],
    "最忍受不了的行为": ["撒谎", "不尊重家人", "沉迷手机", "翻旧账", "负能量爆棚"],
    "形容你的另一半": ["可爱", "靠谱", "粘人", "温柔", "独立", "帅气/漂亮"],
    "对方最吸引你的细节": ["笑起来", "认真做事", "摸我头", "照顾我", "吃醋的样子"],
    "希望对方多为你做的事": ["说晚安", "牵手", "分享日常", "夸我", "主动抱抱"],
    "你们最舒服的状态": ["安静陪伴", "互相打闹", "一起努力", "各自忙碌", "无话不谈"],
    "最想对对方说的话": ["谢谢你", "我很在乎你", "有你真好", "一起走下去", "你是我的偏爱"]
}

# 奖励/惩罚库
REWARD_LIST = [
    "捏肩10分钟", "承包当天家务", "买喜欢的奶茶", 
    "专属抱抱5分钟", "今天听你的", "手写情书一封"
]

PUNISH_LIST = [
    "学小猫叫5声", "讲3个冷笑话", "做10个深蹲", 
    "夸对方10句不重样", "洗一次水果", "模仿口头禅10遍"
]

# ======================= CSS动画转盘核心代码 =======================
def get_wheel_html(items, is_reward=True, rotation_deg=0):
    """生成纯CSS动画转盘的HTML代码"""
    # 颜色配置
    colors = [
        "#FFB6C1", "#FFC0CB", "#FFD1DC", "#FFE4E1", "#FFF0F5", "#F0E68C"
    ] if is_reward else [
        "#FFA07A", "#FF7F50", "#FF6347", "#FF4500", "#F08080", "#CD5C5C"
    ]
    
    # 生成转盘扇区HTML
    sectors_html = ""
    n = len(items)
    angle_per_sector = 360 / n
    
    for i in range(n):
        start_angle = i * angle_per_sector
        end_angle = (i + 1) * angle_per_sector
        color = colors[i % len(colors)]
        
        # 扇区样式
        sector_style = f"""
            position: absolute;
            width: 200px;
            height: 200px;
            clip-path: polygon(50% 50%, 50% 0%, {100 - (start_angle/360)*100}% {100 - (end_angle/360)*100}%);
            background: {color};
            transform-origin: center;
            transform: rotate({start_angle}deg);
        """
        
        # 文字样式（旋转对齐扇区）
        text_style = f"""
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%) rotate({(start_angle + end_angle)/2}deg);
            transform-origin: 50% 80px;
            font-size: 12px;
            font-weight: bold;
            white-space: nowrap;
        """
        
        sectors_html += f"""
            <div style="{sector_style}">
                <div style="{text_style}">{items[i]}</div>
            </div>
        """
    
    # 完整转盘HTML（含旋转动画）
    wheel_html = f"""
    <div style="position: relative; width: 220px; height: 220px; margin: 0 auto;">
        <!-- 转盘容器（带旋转动画） -->
        <div style="
            position: relative;
            width: 200px;
            height: 200px;
            border-radius: 50%;
            overflow: hidden;
            border: 3px solid #333;
            transform: rotate({rotation_deg}deg);
            transition: transform 3s cubic-bezier(0.2, 0.8, 0.2, 1);
        ">
            {sectors_html}
        </div>
        <!-- 指针 -->
        <div style="
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-bottom: 30px solid red;
            z-index: 10;
        "></div>
    </div>
    """
    return wheel_html

# ======================= 初始化会话状态 =======================
st.set_page_config(page_title="情侣默契大考验", page_icon="💘", layout="wide")

def init_session():
    default_state = {
        "step": 1,
        "question": "",
        "p1_answers": [],
        "p2_answers": [],
        "match_result": False,
        "same_count": 0,
        "wheel_items": [],
        "selected_reward_punish": "",
        "wheel_rotated": False,
        "rotation_deg": 0
    }
    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

# ======================= 游戏主流程 =======================
st.title("💖 情侣默契大考验 · 动画转盘版")
st.markdown("### ✨ 优点/缺点选3个，≥2个相同即成功～")

# 步骤1：选择问题
if st.session_state.step == 1:
    st.subheader("📝 第一步：选择考验题目", divider="violet")
    selected_question = st.selectbox("请选择题目（所有内容已固定）", list(QUESTION_BANK.keys()))
    st.session_state.question = selected_question
    
    if st.button("✅ 确定题目", type="primary"):
        st.session_state.step = 2
        st.rerun()

# 步骤2：玩家1答题
elif st.session_state.step == 2:
    q = st.session_state.question
    opts = QUESTION_BANK[q]
    
    st.subheader(f"👩 第二步：玩家1答题 - {q}", divider="violet")
    if "优点" in q or "缺点" in q:
        selected = st.multiselect("请选择3个答案（最多3个）", opts, max_selections=3, key="p1")
        if len(selected) == 3:
            st.session_state.p1_answers = selected
            if st.button("✅ 答完，轮到玩家2", type="primary"):
                st.session_state.step = 3
                st.rerun()
        else:
            st.info(f"当前已选{len(selected)}个，需选满3个！")
    else:
        selected = st.radio("请选择1个答案", opts, key="p1")
        st.session_state.p1_answers = [selected]
        if st.button("✅ 答完，轮到玩家2", type="primary"):
            st.session_state.step = 3
            st.rerun()

# 步骤3：玩家2答题
elif st.session_state.step == 3:
    q = st.session_state.question
    opts = QUESTION_BANK[q]
    
    st.subheader(f"👨 第三步：玩家2答题 - {q}", divider="violet")
    if "优点" in q or "缺点" in q:
        selected = st.multiselect("请选择3个答案（最多3个）", opts, max_selections=3, key="p2")
        if len(selected) == 3:
            st.session_state.p2_answers = selected
            if st.button("🎯 查看默契结果", type="primary"):
                # 计算相同答案数量
                p1_set = set(st.session_state.p1_answers)
                p2_set = set(st.session_state.p2_answers)
                same_count = len(p1_set & p2_set)
                st.session_state.same_count = same_count
                
                # 判断是否成功
                st.session_state.match_result = same_count >= 2
                st.session_state.wheel_items = REWARD_LIST if st.session_state.match_result else PUNISH_LIST
                
                st.session_state.step = 4
                st.rerun()
        else:
            st.info(f"当前已选{len(selected)}个，需选满3个！")
    else:
        selected = st.radio("请选择1个答案", opts, key="p2")
        st.session_state.p2_answers = [selected]
        if st.button("🎯 查看默契结果", type="primary"):
            # 计算相同答案数量
            p1_set = set(st.session_state.p1_answers)
            p2_set = set(st.session_state.p2_answers)
            same_count = len(p1_set & p2_set)
            st.session_state.same_count = same_count
            
            # 判断是否成功
            st.session_state.match_result = same_count >= 1
            st.session_state.wheel_items = REWARD_LIST if st.session_state.match_result else PUNISH_LIST
            
            st.session_state.step = 4
            st.rerun()

# 步骤4：展示匹配结果 + CSS动画转盘抽奖
elif st.session_state.step == 4:
    q = st.session_state.question
    p1 = st.session_state.p1_answers
    p2 = st.session_state.p2_answers
    same_count = st.session_state.same_count
    
    # 展示答案对比
    st.subheader("🧩 第四步：默契结果揭晓", divider="violet")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**考验题目**：{q}")
        st.write(f"**玩家1答案**：{', '.join(p1)}")
        st.write(f"**玩家2答案**：{', '.join(p2)}")
        st.markdown(f"### 相同答案数量：**{same_count}**")
    
    with col2:
        if st.session_state.match_result:
            st.success("🎉 默契成功！解锁奖励转盘～")
        else:
            st.warning("😜 默契不足！开启惩罚转盘～")
    
    # CSS动画转盘抽奖区域
    st.subheader("🎡 动画转盘抽奖", divider="violet")
    wheel_items = st.session_state.wheel_items
    is_reward = st.session_state.match_result
    
    # 未抽奖时显示初始转盘
    if not st.session_state.wheel_rotated:
        # 生成初始转盘HTML
        wheel_html = get_wheel_html(wheel_items, is_reward, rotation_deg=0)
        st.components.v1.html(wheel_html, height=250)
        
        if st.button("🚀 开始转盘抽奖", type="primary", use_container_width=True):
            # 随机选择目标奖项
            target_idx = random.randint(0, len(wheel_items)-1)
            # 计算旋转角度（转5圈+目标角度）
            angle_per_sector = 360 / len(wheel_items)
            target_rotation = 1800 + (360 - (target_idx * angle_per_sector + angle_per_sector/2))
            st.session_state.rotation_deg = target_rotation
            st.session_state.selected_reward_punish = wheel_items[target_idx]
            st.session_state.wheel_rotated = True
            st.rerun()
    # 抽奖完成显示旋转后的转盘
    else:
        # 生成旋转后的转盘HTML
        wheel_html = get_wheel_html(wheel_items, is_reward, rotation_deg=st.session_state.rotation_deg)
        st.components.v1.html(wheel_html, height=250)
        
        # 展示最终结果
        if is_reward:
            st.markdown(f"### 🎁 恭喜抽到奖励：\n## {st.session_state.selected_reward_punish}")
        else:
            st.markdown(f"### ⚠️ 抽到惩罚：\n## {st.session_state.selected_reward_punish}")
    
    # 重新开始按钮
    if st.button("🔄 再来一局", use_container_width=True):
        # 重置所有状态
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_session()
        st.rerun()

# ======================= 侧边栏说明 =======================
with st.sidebar:
    st.header("📜 游戏规则")
    st.write("1. 优点/缺点类题目：选3个，≥2个相同=成功")
    st.write("2. 其他题目：选1个，相同=成功")
    st.write("3. 成功→奖励转盘，失败→惩罚转盘")
    st.write("4. 纯CSS动画转盘，零外部库依赖")
    
    st.divider()
    st.markdown("💌 题库/转盘样式可在代码中自定义调整～")
