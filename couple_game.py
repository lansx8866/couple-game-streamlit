import streamlit as st
import random
import time

# ---------------------- 后端固定配置（核心：题库+奖惩库） ----------------------
# 21个情侣互动问题库（覆盖你的7类场景，可直接修改）
QUESTION_BANK = {
    # 1. 优点类
    "对方的三个优点（选1个）": ["温柔体贴", "有责任心", "幽默有趣", "上进努力", "细心周到"],
    "自己的三个优点（选1个）": ["乐观开朗", "包容心强", "动手能力强", "情绪稳定", "善于倾听"],
    # 2. 缺点类
    "对方的三个缺点（选1个）": ["有点拖延", "偶尔脾气急", "不爱收拾", "话少", "太宅"],
    "自己的三个缺点（选1个）": ["有点敏感", "缺乏耐心", "花钱大手大脚", "熬夜", "挑食"],
    # 3. 想一起做的事
    "最想和对方一起做的事（选1个）": ["看海边日出", "做烛光晚餐", "短途旅行", "拍情侣写真", "学做甜品"],
    "今年最想和对方完成的小事（选1个）": ["一起健身", "打卡10家餐厅", "看一场演唱会", "养一盆绿植", "一起拼乐高"],
    "下辈子想和对方一起做的事（选1个）": ["做同桌", "做邻居", "一起环游世界", "开小店", "当青梅竹马"],
    # 4. 感动瞬间
    "对方做哪些事会让你感动（选1个）": ["记住我的小习惯", "难过时陪着我", "主动分担家务", "给我准备小惊喜", "为我让步"],
    "最让你感动的一次对方的行为（选1个）": ["生病时照顾我", "跨城来看我", "记住我说过的话", "帮我解决困难", "公开维护我"],
    "希望对方多做的暖心小事（选1个）": ["睡前说晚安", "出门牵我的手", "分享日常", "夸夸我", "帮我吹头发"],
    # 5. 生气瞬间
    "对方做哪些事会让你生气（选1个）": ["不回消息", "答应的事没做到", "忽略我的感受", "和异性边界不清", "翻旧账"],
    "最让你生气的一次对方的行为（选1个）": ["吵架时冷暴力", "忘记重要日子", "说话不算数", "不理解我", "敷衍我的分享"],
    "希望对方改掉的惹人生气的行为（选1个）": ["熬夜打游戏", "吃饭吧唧嘴", "乱丢东西", "爱抬杠", "遇事不沟通"],
    # 6. 无法忍受的行为
    "最忍受不了对方的哪些行为（选1个）": ["撒谎", "不尊重我的家人", "沉迷手机", "不讲卫生", "抱怨负能量"],
    "无法忍受对方的朋友的哪些行为（选1个）": ["劝酒", "说我坏话", "带坏对方", "借钱不还", "八卦我们的事"],
    "恋爱中最无法忍受的相处模式（选1个）": ["冷暴力", "翻旧账", "AA太计较", "不分享情绪", "控制欲强"],
    # 7. 形容对方
    "形容自己的男朋友/女朋友（选1个）": ["可爱", "帅气/漂亮", "靠谱", "粘人", "独立"],
    "用一个词形容和对方的关系（选1个）": ["舒服", "甜蜜", "安稳", "有趣", "互补"],
    "对方在你心中像什么（选1个）": ["小太阳", "小棉袄", "充电宝", "开心果", "避风港"],
    # 补充类
    "最想和对方说的一句心里话（选1个）": ["谢谢你陪着我", "我很在乎你", "对不起让你委屈了", "想和你一直走下去", "你是我的偏爱"],
    "对方的哪个小细节最吸引你（选1个）": ["笑起来的样子", "认真做事的样子", "摸我头的样子", "吃醋的样子", "照顾我的样子"],
    "如果可以送对方一件礼物（选1个）": ["手表", "口红", "球鞋", "项链", "手写情书"]
}

# 奖惩库（后端固定，可修改）
REWARD_LIST = [
    "奖励：对方给你捏肩10分钟",
    "奖励：对方承包今天的家务",
    "奖励：对方给你买一杯喜欢的奶茶",
    "奖励：收到对方的专属拥抱",
    "奖励：对方给你写一封手写情书",
    "奖励：周末由你决定去哪里玩",
    "奖励：对方帮你吹头发",
    "奖励：对方陪你看喜欢的电影"
]

PUNISH_LIST = [
    "惩罚：给对方讲3个冷笑话",
    "惩罚：学小猫叫5声",
    "惩罚：做10个深蹲",
    "惩罚：帮对方洗一次袜子",
    "惩罚：夸对方10分钟不重样",
    "惩罚：模仿对方的口头禅说10遍",
    "惩罚：给对方跳一支搞怪舞蹈",
    "惩罚：背对方走50米"
]

# ---------------------- 初始化会话状态 ----------------------
st.set_page_config(
    page_title="情侣互动小游戏 💖",
    page_icon="💞",
    layout="wide"
)

def init_session():
    default_state = {
        "selected_question": "",  # 选中的问题
        "p1_answer": "",          # 出题方答案
        "p2_answer": "",          # 答题方答案
        "is_matched": None,       # 是否匹配（True/False/None）
        "reward_punish": "",      # 奖惩结果
        "step": 1                 # 游戏步骤：1-选问题 2-出题方答 3-答题方答 4-看结果
    }
    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

# ---------------------- 游戏流程 ----------------------
st.title("💖 情侣默契大考验 💖")

# 步骤1：选择问题
if st.session_state.step == 1:
    st.subheader("🎯 第一步：选择要考验的问题", divider="violet")
    # 展示后端题库的所有问题，供选择
    question = st.selectbox(
        "请选择一个问题（所有问题已固定，无需输入）",
        options=list(QUESTION_BANK.keys()),
        key="question_select"
    )
    st.session_state.selected_question = question
    
    if st.button("确定问题，进入下一步 🚀", type="primary"):
        if question:
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("请先选择一个问题！")

# 步骤2：出题方（宝贝1号）填写答案
elif st.session_state.step == 2:
    st.subheader(f"✍️ 第二步：宝贝1号回答（问题：{st.session_state.selected_question}）", divider="violet")
    question = st.session_state.selected_question
    options = QUESTION_BANK[question]
    
    st.write("请从以下选项中选择你的答案：")
    p1_ans = st.radio(
        "你的答案",
        options=options,
        key="p1_ans"
    )
    st.session_state.p1_answer = p1_ans
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("返回上一步 ←"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("确认答案，轮到宝贝2号 🎤", type="primary"):
            if p1_ans:
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("请先选择你的答案！")

# 步骤3：答题方（宝贝2号）回答
elif st.session_state.step == 3:
    st.subheader(f"🤔 第三步：宝贝2号答题（问题：{st.session_state.selected_question}）", divider="violet")
    question = st.session_state.selected_question
    options = QUESTION_BANK[question]
    
    st.write("请从以下选项中选择你的答案（不要偷看宝贝1号的答案哦～）：")
    p2_ans = st.radio(
        "你的答案",
        options=options,
        key="p2_ans"
    )
    st.session_state.p2_answer = p2_ans
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("返回上一步 ←"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("确认答案，查看默契结果 🎉", type="primary"):
            if p2_ans:
                # 匹配逻辑：答案一致则成功
                st.session_state.is_matched = (st.session_state.p1_answer == st.session_state.p2_answer)
                # 随机生成奖惩
                if st.session_state.is_matched:
                    st.session_state.reward_punish = random.choice(REWARD_LIST)
                else:
                    st.session_state.reward_punish = random.choice(PUNISH_LIST)
                st.session_state.step = 4
                st.rerun()
            else:
                st.error("请先选择你的答案！")

# 步骤4：展示结果
elif st.session_state.step == 4:
    st.subheader("🏆 第四步：默契结果揭晓", divider="violet")
    
    # 展示双方答案
    st.write(f"📝 考验问题：{st.session_state.selected_question}")
    st.write(f"👩 宝贝1号的答案：{st.session_state.p1_answer}")
    st.write(f"👨 宝贝2号的答案：{st.session_state.p2_answer}")
    
    # 展示匹配结果
    if st.session_state.is_matched:
        st.success("💞 恭喜！答案一致，你们超有默契～")
    else:
        st.warning("😜 有点小遗憾！答案不一致，继续加油～")
    
    # 展示奖惩（模拟转盘效果）
    st.subheader("🎡 奖惩结果", divider="violet")
    with st.spinner("转盘旋转中..."):
        time.sleep(2)
    st.markdown(f"### {st.session_state.reward_punish}")
    
    # 重新开始按钮
    if st.button("🔄 再来一局", type="primary"):
        # 重置所有状态
        for key in st.session_state.keys():
            del st.session_state[key]
        init_session()
        st.rerun()

# ---------------------- 侧边栏说明 ----------------------
with st.sidebar:
    st.header("📖 游戏规则")
    st.write("1. 所有问题和选项均已固定，无需手动输入；")
    st.write("2. 宝贝1号选问题+答答案（出题方）；")
    st.write("3. 宝贝2号答同一问题的答案（答题方）；")
    st.write("4. 答案一致→随机奖励，不一致→随机惩罚；")
    st.write("5. 所有配置可在后端代码中修改。")
    
    st.divider()
    st.write("💌 如需修改问题/选项/奖惩，直接修改后端代码即可～")
