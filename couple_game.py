# ======================= 顶部全局导入+依赖检查 =======================
import streamlit as st
import random
import time
import numpy as np

# 强制安装/导入matplotlib（解决Streamlit Cloud安装失败）
try:
    import matplotlib.pyplot as plt
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib>=3.7.0"])
    import matplotlib.pyplot as plt

# 解决matplotlib中文显示（兼容所有环境）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.switch_backend('Agg')  # 非交互式后端，避免渲染错误

# ======================= 【后端固定配置】 =======================
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
    "对方最吸引你的细节": ["笑起来", "认真做事", "摸我头", "照顾我", "吃醋的样子"],
    "希望对方多为你做的事": ["说晚安", "牵手", "分享日常", "夸我", "主动抱抱"],
    "你们最舒服的状态": ["安静陪伴", "互相打闹", "一起努力", "各自忙碌", "无话不谈"],
    "最想对对方说的话": ["谢谢你", "我很在乎你", "有你真好", "一起走下去", "你是我的偏爱"]
}

REWARD_LIST = ["捏肩10分钟", "承包当天家务", "买喜欢的奶茶", "专属抱抱5分钟", "今天听你的", "手写情书一封"]
PUNISH_LIST = ["学小猫叫5声", "讲3个冷笑话", "做10个深蹲", "夸对方10句不重样", "洗一次水果", "模仿口头禅10遍"]

# ======================= 转盘绘制核心函数 =======================
def draw_wheel(items, selected_idx=None):
    """绘制可视化转盘"""
    n = len(items)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]  # 闭合
    
    # 颜色配置
    if "捏肩" in items[0]:
        colors = ['#FFB6C1', '#FFC0CB', '#FFD1DC', '#FFE4E1', '#FFF0F5', '#F0E68C']
    else:
        colors = ['#FFA07A', '#FF7F50', '#FF6347', '#FF4500', '#F08080', '#CD5C5C']
    
    # 创建画布
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    
    # 绘制扇区
    for i, (angle, color) in enumerate(zip(angles[:-1], colors)):
        ax.fill_between([angle, angles[i+1]], 0, 1, color=color, alpha=0.7)
    
    # 添加文字标签（用英文/拼音兜底，避免中文报错）
    for i, (angle, item) in enumerate(zip(angles[:-1], items)):
        mid_angle = (angle + angles[i+1]) / 2
        ax.text(mid_angle, 0.5, item, ha='center', va='center', fontsize=11, fontweight='bold')
    
    # 绘制指针
    if selected_idx is not None:
        selected_angle = (angles[selected_idx] + angles[selected_idx+1]) / 2
        ax.plot([0, selected_angle], [0, 1.1], color='red', linewidth=3, marker='o', markersize=8)
    
    # 隐藏刻度
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['polar'].set_visible(False)
    
    plt.tight_layout()
    return fig

# ======================= 初始化会话状态 =======================
st.set_page_config(page_title="情侣默契大考验", page_icon="💘", layout="wide")

def init_session():
    default_state = {
        "step": 1, "question": "", "p1_answers": [], "p2_answers": [],
        "match_result": False, "same_count": 0, "wheel_items": [],
        "selected_reward_punish": "", "wheel_spun": False
    }
    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

# ======================= 游戏主流程 =======================
st.title("💖 情侣默契大考验 · 转盘版")
st.markdown("### ✨ 优点/缺点选3个，≥2个相同即成功～")

# 步骤1：选择问题
if st.session_state.step == 1:
    st.subheader("📝 第一步：选择考验题目", divider="violet")
    selected_question = st.selectbox("请选择题目", list(QUESTION_BANK.keys()))
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
        selected = st.multiselect("请选择3个答案", opts, max_selections=3, key="p1")
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
        selected = st.multiselect("请选择3个答案", opts, max_selections=3, key="p2")
        if len(selected) == 3:
            st.session_state.p2_answers = selected
            if st.button("🎯 查看默契结果", type="primary"):
                p1_set = set(st.session_state.p1_answers)
                p2_set = set(st.session_state.p2_answers)
                st.session_state.same_count = len(p1_set & p2_set)
                st.session_state.match_result = st.session_state.same_count >= 2
                st.session_state.wheel_items = REWARD_LIST if st.session_state.match_result else PUNISH_LIST
                st.session_state.step = 4
                st.rerun()
        else:
            st.info(f"当前已选{len(selected)}个，需选满3个！")
    else:
        selected = st.radio("请选择1个答案", opts, key="p2")
        st.session_state.p2_answers = [selected]
        if st.button("🎯 查看默契结果", type="primary"):
            p1_set = set(st.session_state.p1_answers)
            p2_set = set(st.session_state.p2_answers)
            st.session_state.same_count = len(p1_set & p2_set)
            st.session_state.match_result = st.session_state.same_count >= 1
            st.session_state.wheel_items = REWARD_LIST if st.session_state.match_result else PUNISH_LIST
            st.session_state.step = 4
            st.rerun()

# 步骤4：展示结果+转盘抽奖
elif st.session_state.step == 4:
    q = st.session_state.question
    p1 = st.session_state.p1_answers
    p2 = st.session_state.p2_answers
    same_count = st.session_state.same_count
    
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
    
    # 转盘抽奖
    st.subheader("🎡 转盘抽奖", divider="violet")
    wheel_items = st.session_state.wheel_items
    if not st.session_state.wheel_spun:
        try:
            st.pyplot(draw_wheel(wheel_items))
        except Exception as e:
            st.warning(f"转盘加载中...（{e}）")
            st.write("🎡 转盘选项：" + ", ".join(wheel_items))
        if st.button("🚀 开始转盘抽奖", type="primary", use_container_width=True):
            with st.spinner("转盘旋转中..."):
                time.sleep(2)
                selected_idx = random.randint(0, len(wheel_items)-1)
                st.session_state.selected_reward_punish = wheel_items[selected_idx]
                st.session_state.wheel_spun = True
            st.rerun()
    else:
        try:
            selected_idx = wheel_items.index(st.session_state.selected_reward_punish)
            st.pyplot(draw_wheel(wheel_items, selected_idx))
        except:
            st.write("🎡 转盘结果：" + st.session_state.selected_reward_punish)
        if st.session_state.match_result:
            st.markdown(f"### 🎁 恭喜抽到奖励：\n## {st.session_state.selected_reward_punish}")
        else:
            st.markdown(f"### ⚠️ 抽到惩罚：\n## {st.session_state.selected_reward_punish}")
    
    # 重新开始
    if st.button("🔄 再来一局", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_session()
        st.rerun()

# ======================= 侧边栏 =======================
with st.sidebar:
    st.header("📜 游戏规则")
    st.write("1. 优点/缺点选3个，≥2个相同=成功")
    st.write("2. 其他题目选1个，相同=成功")
    st.write("3. 成功→奖励转盘，失败→惩罚转盘")
