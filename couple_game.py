import streamlit as st
import random

# ======================= 【后端固定题库：你在这里改】 =======================
QUESTION_BANK = {
    # ==================== 优点类（选3个）
    "对方的三个优点": ["温柔体贴", "有责任心", "幽默有趣", "上进努力", "细心周到", "情绪稳定"],
    "我的三个优点": ["乐观开朗", "包容心强", "动手能力强", "善于倾听", "真诚坦率", "有耐心"],

    # ==================== 缺点类（选3个）
    "对方的三个缺点": ["有点拖延", "偶尔脾气急", "不爱收拾", "太宅", "话少", "容易焦虑"],
    "我的三个缺点": ["有点敏感", "缺乏耐心", "熬夜", "挑食", "容易胡思乱想", "不爱主动"],

    # ==================== 其他类（选1个）
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

# 奖励 & 惩罚
REWARD = [
    "奖励：对方给你捏肩10分钟",
    "奖励：对方承包今天家务",
    "奖励：对方给你买奶茶",
    "奖励：专属抱抱5分钟",
    "奖励：今天你说了算，听你的"
]

PUNISH = [
    "惩罚：学小猫叫5声",
    "惩罚：讲3个冷笑话",
    "惩罚：做10个深蹲",
    "惩罚：夸对方10句不重样",
    "惩罚：给对方洗一次水果"
]

# ======================= 初始化状态 =======================
st.set_page_config(page_title="情侣默契大考验", page_icon="💘", layout="wide")

if "step" not in st.session_state:
    st.session_state.step = 1
if "question" not in st.session_state:
    st.session_state.question = ""
if "p1" not in st.session_state:
    st.session_state.p1 = []
if "p2" not in st.session_state:
    st.session_state.p2 = []
if "result" not in st.session_state:
    st.session_state.result = ""

# ======================= 页面 =======================
st.title("💖 情侣默契大考验 · 升级版")
st.markdown("### 优点/缺点选 **3个**，≥2个相同即成功～")

# --------------------- 步骤1：选问题 ---------------------
if st.session_state.step == 1:
    st.subheader("📝 第一步：选择题目")
    q = st.selectbox("选择要考验的问题", list(QUESTION_BANK.keys()))
    st.session_state.question = q

    if st.button("✅ 确定，开始答题", type="primary"):
        st.session_state.step = 2
        st.rerun()

# --------------------- 步骤2：玩家1答题 ---------------------
elif st.session_state.step == 2:
    q = st.session_state.question
    opts = QUESTION_BANK[q]

    st.subheader(f"👩 玩家1 答题：{q}")

    if "优点" in q or "缺点" in q:
        selected = st.multiselect("请选 **3个**", opts, max_selections=3, key="p1s")
        if len(selected) == 3:
            st.session_state.p1 = selected
            if st.button("✅ 答完，轮到玩家2", type="primary"):
                st.session_state.step = 3
                st.rerun()
        else:
            st.info("请选满 3 个")
    else:
        selected = st.radio("请选 **1个**", opts, key="p1s")
        st.session_state.p1 = [selected]
        if st.button("✅ 答完，轮到玩家2", type="primary"):
            st.session_state.step = 3
            st.rerun()

# --------------------- 步骤3：玩家2答题 ---------------------
elif st.session_state.step == 3:
    q = st.session_state.question
    opts = QUESTION_BANK[q]

    st.subheader(f"👨 玩家2 答题：{q}")

    if "优点" in q or "缺点" in q:
        selected = st.multiselect("请选 **3个**", opts, max_selections=3, key="p2s")
        if len(selected) == 3:
            st.session_state.p2 = selected
            if st.button("🎯 查看结果", type="primary"):
                st.session_state.step = 4
                st.rerun()
        else:
            st.info("请选满 3 个")
    else:
        selected = st.radio("请选 **1个**", opts, key="p2s")
        st.session_state.p2 = [selected]
        if st.button("🎯 查看结果", type="primary"):
            st.session_state.step = 4
            st.rerun()

# --------------------- 步骤4：判分 ---------------------
elif st.session_state.step == 4:
    q = st.session_state.question
    p1 = set(st.session_state.p1)
    p2 = set(st.session_state.p2)
    same = len(p1 & p2)

    st.subheader("🧩 答案对比")
    st.write(f"玩家1：{', '.join(p1)}")
    st.write(f"玩家2：{', '.join(p2)}")
    st.markdown(f"### 相同数量：**{same}**")

    # 判题规则
    success = False
    if "优点" in q or "缺点" in q:
        if same >= 2:
            success = True
    else:
        if same >= 1:
            success = True

    if success:
        st.success("🎉 默契成功！获得奖励")
        res = random.choice(REWARD)
    else:
        st.error("😈 默契不足！接受惩罚")
        res = random.choice(PUNISH)

    st.session_state.result = res
    st.markdown(f"# 🏆 {res}")

    if st.button("🔄 再来一局"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

with st.sidebar:
    st.markdown("## 📜 规则")
    st.write("• 优点/缺点：选3个，≥2个相同=成功")
    st.write("• 其他题目：选1个，相同=成功")
    st.write("• 所有内容在后端修改，前端只选不改")

