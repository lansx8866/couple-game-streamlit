import streamlit as st
import random
import time

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

REWARD = [
    "捏肩10分钟", "承包家务", "买奶茶", "抱抱5分钟", "今天听你的", "手写情书"
]

PUNISH = [
    "学小猫叫", "讲冷笑话", "深蹲10个", "夸对方10句", "洗水果", "模仿口头禅"
]

# ======================= 漂亮前端转盘（真正可视化） =======================
def wheel_html(items, is_reward):
    colors = ["#ff9bbb","#ff789e","#ff5c87","#ff4473","#ff2a5f","#ff0040"] if is_reward else \
             ["#ffb380","#ff9f66","#ff8c4d","#ff7833","#ff6519","#ff5100"]

    options = []
    for i, text in enumerate(items):
        options.append(f'''{{"text":"{text}","fillColor":"{colors[i]}"}}''')

    options_str = ",".join(options)

    return f'''
    <div id="wheel-container" style="width:320px; height:320px; margin:20px auto;"></div>
    <script src="https://cdn.jsdelivr.net/npm/wheel-color@1.0.0/dist/wheel-color.min.js"></script>
    <script>
    const wheel = new WheelColor({{
        container: document.getElementById("wheel-container"),
        items: [{options_str}],
        lineWidth: 3,
        textColor: "#fff",
        textSize: 14,
        pointerColor: "red",
        radius: 140
    }});
    wheel.draw();
    window.startSpin = function(target) {{
        wheel.spin({{
            duration: 4000,
            rotations: 8,
            targetIndex: target,
            easing: "easeOutCubic"
        }});
    }};
    </script>
    '''

# ======================= 流程 =======================
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
if "spun" not in st.session_state:
    st.session_state.spun = False
if "final" not in st.session_state:
    st.session_state.final = ""

# ------------------- 步骤1 -------------------
if st.session_state.step == 1:
    st.subheader("📝 选择题目")
    q = st.selectbox("题目", list(QUESTION_BANK.keys()))
    st.session_state.question = q
    if st.button("✅ 开始", type="primary"):
        st.session_state.step = 2
        st.rerun()

# ------------------- 步骤2 -------------------
elif st.session_state.step == 2:
    q = st.session_state.question
    opt = QUESTION_BANK[q]
    st.subheader(f"👩 玩家1：{q}")
    if "优点" in q or "缺点" in q:
        s = st.multiselect("选3个", opt, max_selections=3, key="p1s")
        if len(s) == 3:
            st.session_state.p1 = s
            if st.button("✅ 玩家2答题", type="primary"):
                st.session_state.step = 3
                st.rerun()
    else:
        s = st.radio("选1个", opt, key="p1s")
        st.session_state.p1 = [s]
        if st.button("✅ 玩家2答题", type="primary"):
            st.session_state.step = 3
            st.rerun()

# ------------------- 步骤3 -------------------
elif st.session_state.step == 3:
    q = st.session_state.question
    opt = QUESTION_BANK[q]
    st.subheader(f"👨 玩家2：{q}")
    if "优点" in q or "缺点" in q:
        s = st.multiselect("选3个", opt, max_selections=3, key="p2s")
        if len(s) == 3:
            st.session_state.p2 = s
            if st.button("🎯 看结果", type="primary"):
                same = len(set(st.session_state.p1) & set(st.session_state.p2))
                ok = False
                if "优点" in q or "缺点" in q:
                    ok = same >=2
                else:
                    ok = same >=1
                st.session_state.result = ok
                st.session_state.step = 4
                st.rerun()
    else:
        s = st.radio("选1个", opt, key="p2s")
        st.session_state.p2 = [s]
        if st.button("🎯 看结果", type="primary"):
            same = len(set(st.session_state.p1) & set(st.session_state.p2))
            st.session_state.result = (same >=1)
            st.session_state.step = 4
            st.rerun()

# ------------------- 步骤4 —— 真正可视化转盘 -------------------
elif st.session_state.step == 4:
    ok = st.session_state.result
    items = REWARD if ok else PUNISH

    st.subheader("🧩 答案对比")
    st.write(f"玩家1：{', '.join(st.session_state.p1)}")
    st.write(f"玩家2：{', '.join(st.session_state.p2)}")

    if ok:
        st.success("🎉 默契成功！抽奖励")
    else:
        st.error("⚠️ 默契不足！抽惩罚")

    st.subheader("🎡 可视化转盘")

    # 渲染真正的圆形转盘
    st.components.v1.html(wheel_html(items, ok), height=360)

    if not st.session_state.spun:
        if st.button("🚀 旋转转盘", type="primary", use_container_width=True):
            idx = random.randint(0,5)
            st.session_state.final = items[idx]
            st.session_state.spun = True

            js = f"""
            <script>
            setTimeout(() => window.startSpin({idx}), 300);
            </script>
            """
            st.components.v1.html(js, height=0)

            time.sleep(4.5)
            st.rerun()
    else:
        st.markdown(f"# 🏆 {st.session_state.final}")
        if st.button("🔄 再来一局"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
