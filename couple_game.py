import streamlit as st
import random
import time

# ---------- 题库配置（可后端编辑） ----------
questions_db = [
    # 优点 (multi)
    {
        "id": 1,
        "category": "优点",
        "question": "选择对方的三个优点",
        "options": ["善良", "聪明", "幽默", "体贴", "大方", "有耐心", "有责任心", "上进", "真诚", "浪漫"],
        "type": "multi"
    },
    {
        "id": 2,
        "category": "优点",
        "question": "对方最让你欣赏的三个品质是？",
        "options": ["乐观", "幽默", "体贴", "细心", "浪漫", "真诚", "温柔", "大方", "聪明", "独立"],
        "type": "multi"
    },
    {
        "id": 3,
        "category": "优点",
        "question": "你认为对方最有魅力的三个优点是？",
        "options": ["自信", "有主见", "善解人意", "有才华", "勤奋", "开朗", "稳重", "风趣", "慷慨", "包容"],
        "type": "multi"
    },
    # 缺点 (multi)
    {
        "id": 4,
        "category": "缺点",
        "question": "选择对方的三个缺点",
        "options": ["拖延", "粗心", "脾气急", "固执", "唠叨", "花钱大手大脚", "不爱运动", "熬夜", "不爱整理", "挑食"],
        "type": "multi"
    },
    {
        "id": 5,
        "category": "缺点",
        "question": "对方最让你头疼的三个缺点是？",
        "options": ["太宅", "不主动沟通", "爱玩手机", "情绪化", "记仇", "多疑", "自私", "小气", "不浪漫", "邋遢"],
        "type": "multi"
    },
    {
        "id": 6,
        "category": "缺点",
        "question": "你认为对方最需要改进的三个缺点是？",
        "options": ["懒散", "急躁", "健忘", "优柔寡断", "敏感", "爱抱怨", "冲动", "嘴硬", "玻璃心", "拖延"],
        "type": "multi"
    },
    # 一起做的事 (single)
    {
        "id": 7,
        "category": "一起做的事",
        "question": "最想和对方一起做的事是什么？",
        "options": ["旅行", "看电影", "做饭", "健身", "读书", "打游戏", "逛街", "露营", "看日出", "养宠物"],
        "type": "single"
    },
    {
        "id": 8,
        "category": "一起做的事",
        "question": "你心中最浪漫的和对方一起做的事？",
        "options": ["看海", "山顶看日出", "烛光晚餐", "散步", "听音乐会", "去游乐园", "滑雪", "泡温泉", "自驾游", "野餐"],
        "type": "single"
    },
    {
        "id": 9,
        "category": "一起做的事",
        "question": "你最期待和对方一起体验的活动？",
        "options": ["学习新技能", "参加派对", "做手工", "逛博物馆", "看演唱会", "运动", "冥想", "摄影", "钓鱼", "种花"],
        "type": "single"
    },
    # 感动的事 (single)
    {
        "id": 10,
        "category": "感动的事",
        "question": "对方做哪些事会让你感动？",
        "options": ["记得你的生日", "生病时照顾你", "给你惊喜", "为你做饭", "支持你的梦想", "陪伴你", "送你礼物", "写情书", "拥抱你", "说情话"],
        "type": "single"
    },
    {
        "id": 11,
        "category": "感动的事",
        "question": "什么情况下你会觉得对方特别暖心？",
        "options": ["你累了给你按摩", "为你准备早餐", "帮你解决问题", "给你鼓励", "记得你随口说的话", "替你分担家务", "给你小惊喜", "照顾你的情绪", "为你着想", "包容你"],
        "type": "single"
    },
    {
        "id": 12,
        "category": "感动的事",
        "question": "对方做什么会让你觉得被深爱着？",
        "options": ["公开表白", "为你改变", "为你付出时间", "关注你的细节", "为你挺身而出", "为你流泪", "为你努力", "为你妥协", "把你放在第一位", "给你安全感"],
        "type": "single"
    },
    # 生气的事 (single)
    {
        "id": 13,
        "category": "生气的事",
        "question": "对方做哪些事会让你生气？",
        "options": ["不回消息", "忘记约定", "和异性暧昧", "对你发脾气", "撒谎", "不尊重你", "忽略你", "挑剔你", "指责你", "冷战"],
        "type": "single"
    },
    {
        "id": 14,
        "category": "生气的事",
        "question": "什么行为会让你瞬间对对方发火？",
        "options": ["说话不算数", "敷衍你", "当众让你难堪", "翻旧账", "不信任你", "打游戏不理你", "跟别人过于亲密", "不听你解释", "贬低你", "忽视你的感受"],
        "type": "single"
    },
    {
        "id": 15,
        "category": "生气的事",
        "question": "你最讨厌对方什么行为？",
        "options": ["抽烟喝酒", "乱扔东西", "拖延", "迟到", "跟你顶嘴", "小气", "八卦", "炫耀", "爱抱怨", "负能量"],
        "type": "single"
    },
    # 忍受不了的行为 (single)
    {
        "id": 16,
        "category": "忍受不了",
        "question": "最忍受不了女朋友/男朋友的哪些行为？",
        "options": ["当众让你难堪", "翻看手机", "控制欲强", "不信任你", "过度依赖", "不修边幅", "沉迷游戏", "不爱干净", "说话刻薄", "没有主见"],
        "type": "single"
    },
    {
        "id": 17,
        "category": "忍受不了",
        "question": "对方的什么行为会让你想分手？",
        "options": ["家暴", "出轨", "欺骗", "不尊重你父母", "不上进", "啃老", "赌博", "酗酒", "自私自利", "冷暴力"],
        "type": "single"
    },
    {
        "id": 18,
        "category": "忍受不了",
        "question": "你绝对无法容忍对方的哪种习惯？",
        "options": ["撒谎成性", "邋遢", "斤斤计较", "大男子/女子主义", "妈宝", "暴力倾向", "情绪不稳定", "极端", "不负责任", "不忠诚"],
        "type": "single"
    },
    # 形容对方 (single)
    {
        "id": 19,
        "category": "形容对方",
        "question": "用一个词形容你的男朋友/女朋友？",
        "options": ["可爱的", "温柔的", "帅气的", "聪明的", "幽默的", "靠谱的", "呆萌的", "高冷的", "霸道的", "暖心的"],
        "type": "single"
    },
    {
        "id": 20,
        "category": "形容对方",
        "question": "你觉得对方最贴切的形容词是？",
        "options": ["阳光的", "稳重的", "有趣的", "善良的", "真诚的", "大方的", "细心的", "浪漫的", "独立的", "坚强的"],
        "type": "single"
    },
    {
        "id": 21,
        "category": "形容对方",
        "question": "如果让你用一个词描述对方给你的感觉？",
        "options": ["安心的", "快乐的", "幸福的", "温暖的", "甜蜜的", "踏实的", "心动的", "舒服的", "骄傲的", "依赖的"],
        "type": "single"
    }
]

# 奖励和惩罚池（可后端编辑）
rewards = [
    "深情拥抱10秒", "亲吻一下", "说一句情话", "为对方按摩5分钟",
    "陪对方做一件想做的事", "送一个小礼物", "写一封情书", "为对方唱一首歌"
]
punishments = [
    "做10个俯卧撑", "学狗叫三声", "发朋友圈表白", "打扫卫生一天",
    "请对方喝奶茶", "背对方走10步", "讲一个笑话", "接受对方挠痒痒惩罚"
]

# ---------- 初始化 session state ----------
if "stage" not in st.session_state:
    st.session_state.stage = "player1"          # 游戏阶段：player1, player2, spin, result
    st.session_state.selected_category = None
    st.session_state.selected_question = None
    st.session_state.correct_answers = None     # 玩家1设定的正确答案
    st.session_state.player2_answers = None      # 玩家2提交的答案
    st.session_state.is_correct = None           # 玩家2是否答对
    st.session_state.spin_result = None          # 转盘结果
    st.session_state.spin_pool = None             # 当前转盘池（奖励或惩罚列表）

# ---------- 辅助函数 ----------
def get_question_by_id(qid):
    for q in questions_db:
        if q["id"] == qid:
            return q
    return None

def check_answer(question, correct, player2):
    """判断玩家2是否正确"""
    if question["type"] == "multi":
        # 要求双方都选三个，交集≥2即正确
        if len(correct) != 3 or len(player2) != 3:
            return False
        common = set(correct) & set(player2)
        return len(common) >= 2
    else:
        # 单选直接比较
        return correct == player2

# ---------- 页面布局 ----------
st.set_page_config(page_title="默契考验小游戏", page_icon="🎮")
st.title("🎮 默契大考验")
st.markdown("---")

# 显示当前阶段
if st.session_state.stage == "player1":
    st.header("👨 玩家1：出题阶段")
elif st.session_state.stage == "player2":
    st.header("👩 玩家2：答题阶段")
elif st.session_state.stage == "spin":
    st.header("🎲 转盘抽奖")
else:
    st.header("🏆 游戏结束")

st.markdown("---")

# ---------- 玩家1：选择问题并设定正确答案 ----------
if st.session_state.stage == "player1":
    # 选择类别
    categories = sorted(list(set(q["category"] for q in questions_db)))
    selected_cat = st.selectbox("选择问题类别", categories, key="cat_select")
    st.session_state.selected_category = selected_cat

    # 根据类别筛选问题
    cat_questions = [q for q in questions_db if q["category"] == selected_cat]
    question_titles = {f"{q['id']}: {q['question']}": q["id"] for q in cat_questions}
    selected_title = st.selectbox("选择具体问题", list(question_titles.keys()), key="q_select")
    qid = question_titles[selected_title]
    question = get_question_by_id(qid)
    st.session_state.selected_question = question

    st.markdown("---")
    st.subheader("设定正确答案（只有你知道）")

    if question["type"] == "multi":
        st.write("请选择 **三个** 优点/缺点（作为正确答案）：")
        correct = st.multiselect(
            "选择三个选项",
            question["options"],
            max_selections=3,
            key="correct_multi"
        )
        if len(correct) != 3:
            st.warning("请恰好选择三个选项")
        else:
            if st.button("✅ 确认出题", type="primary"):
                st.session_state.correct_answers = correct
                st.session_state.stage = "player2"
                st.rerun()
    else:
        st.write("请选择一个正确答案：")
        correct = st.radio(
            "选择一个选项",
            question["options"],
            key="correct_single",
            index=None
        )
        if correct is None:
            st.warning("请选择一个选项")
        else:
            if st.button("✅ 确认出题", type="primary"):
                st.session_state.correct_answers = correct
                st.session_state.stage = "player2"
                st.rerun()

# ---------- 玩家2：回答问题 ----------
elif st.session_state.stage == "player2":
    question = st.session_state.selected_question
    st.subheader(f"问题：{question['question']}")

    if question["type"] == "multi":
        st.write("请选择 **三个** 选项（你的答案）：")
        player2 = st.multiselect(
            "你的选择",
            question["options"],
            max_selections=3,
            key="player2_multi"
        )
        if len(player2) != 3:
            st.warning("请恰好选择三个选项")
        else:
            if st.button("📤 提交答案", type="primary"):
                st.session_state.player2_answers = player2
                # 判断对错
                correct = st.session_state.correct_answers
                is_correct = check_answer(question, correct, player2)
                st.session_state.is_correct = is_correct
                # 根据对错设置转盘池
                if is_correct:
                    st.session_state.spin_pool = rewards
                else:
                    st.session_state.spin_pool = punishments
                st.session_state.spin_result = None  # 清空之前结果
                st.session_state.stage = "spin"
                st.rerun()
    else:
        st.write("请选择一个选项：")
        player2 = st.radio(
            "你的答案",
            question["options"],
            key="player2_single",
            index=None
        )
        if player2 is None:
            st.warning("请选择一个选项")
        else:
            if st.button("📤 提交答案", type="primary"):
                st.session_state.player2_answers = player2
                correct = st.session_state.correct_answers
                is_correct = check_answer(question, correct, player2)
                st.session_state.is_correct = is_correct
                if is_correct:
                    st.session_state.spin_pool = rewards
                else:
                    st.session_state.spin_pool = punishments
                st.session_state.spin_result = None
                st.session_state.stage = "spin"
                st.rerun()

# ---------- 转盘阶段 ----------
elif st.session_state.stage == "spin":
    st.subheader("🎁 转动转盘，看看你的运气！")
    pool = st.session_state.spin_pool
    is_correct = st.session_state.is_correct

    if is_correct:
        st.success("✅ 恭喜你答对了！现在转动奖励转盘～")
    else:
        st.error("❌ 很遗憾答错了，转动惩罚转盘吧～")

    # 显示所有选项（模拟转盘上的格子）
    st.markdown("**转盘上的选项：**")
    cols = st.columns(4)
    for i, item in enumerate(pool):
        with cols[i % 4]:
            st.markdown(f"- {item}")

    # 如果还没有旋转结果，显示旋转按钮
    if st.session_state.spin_result is None:
        if st.button("🎲 旋转转盘", type="primary"):
            # 模拟转盘旋转过程（简单动画效果）
            with st.spinner("转盘转起来啦......"):
                time.sleep(1)  # 假装旋转
            # 随机选择一个结果
            result = random.choice(pool)
            st.session_state.spin_result = result
            # 添加一些庆祝效果
            if is_correct:
                st.balloons()
            else:
                st.snow()
            st.rerun()
    else:
        # 显示旋转结果
        st.markdown("---")
        st.subheader(f"✨ 转盘停在了：**{st.session_state.spin_result}**")
        st.markdown("---")

        # 显示双方答案对比（可选）
        question = st.session_state.selected_question
        with st.expander("查看答案详情"):
            st.write(f"**问题**：{question['question']}")
            st.write(f"**玩家1的正确答案**：{st.session_state.correct_answers}")
            st.write(f"**玩家2的答案**：{st.session_state.player2_answers}")

        if st.button("🔄 再来一局", type="primary"):
            # 重置状态，保留题库
            st.session_state.stage = "player1"
            st.session_state.selected_category = None
            st.session_state.selected_question = None
            st.session_state.correct_answers = None
            st.session_state.player2_answers = None
            st.session_state.is_correct = None
            st.session_state.spin_result = None
            st.session_state.spin_pool = None
            st.rerun()

# 底部说明
st.markdown("---")
st.caption("规则：玩家1选择问题并设定正确答案（优点/缺点需选三个，其他单选）。玩家2作答，优点/缺点类需至少猜对两个即算正确，其他需完全一致。正确/错误后通过转盘随机抽取奖励/惩罚。")
