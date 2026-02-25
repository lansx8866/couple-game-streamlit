import streamlit as st
import random

# ======================= 题目库 =======================
QUESTION_BANK = {
    "对方的三个优点": ["温柔体贴", "有责任心", "幽默有趣", "上进努力", "细心周到", "情绪稳定"],
    "我的三个优点": ["乐观开朗", "包容心强", "动手能力强", "善于倾听", "真诚坦率", "有耐心"],
    "对方的三个缺点": ["有点拖延", "偶尔脾气急", "不爱收拾", "太宅", "话少", "容易焦虑"],
    "我的三个缺点": ["有点敏感", "缺乏耐心", "熬夜", "挑食", "容易胡思乱想", "不爱主动"],
    "最想和对方一起做的事": ["看海边日出", "做烛光晚餐", "短途旅行", "拍情侣写真", "宅家追剧"],
}

REWARD = ["捏肩10分钟", "承包家务", "买奶茶", "抱抱5分钟", "今天听你的", "手写情书"]
PUNISH = ["学小猫叫", "讲冷笑话", "深蹲10个", "夸对方10句", "洗水果", "模仿口头禅"]

# ======================= 真正会转的转盘（纯前端） =======================
def spinning_wheel(items, is_reward):
    colors = [
        "#FF9BBB", "#FF789E", "#FF5C87", "#FF4473", "#FF2A5F", "#FF0040"
    ] if is_reward else [
        "#FFB380", "#FF9F66", "#FF8C4D", "#FF7833", "#FF6519", "#FF5100"
    ]

    sectors = []
    n = len(items)
    angle = 360 / n

    for i, text in enumerate(items):
        start = i * angle
        end = (i + 1) * angle
        sectors.append(f"""
            <div class="sector" style="
                --start: {start}deg;
                --end: {end}deg;
                background: {colors[i]};
            ">
                <span class="sector-text">{text}</span>
            </div>
        """)

    sectors_html = "\n".join(sectors)

    return f"""
    <style>
        .wheel-container {{
            position: relative;
            width: 320px;
            height: 320px;
            margin: 20px auto;
        }}
        .wheel {{
            width: 100%;
            height: 100%;
            border-radius: 50%;
            position: relative;
            overflow: hidden;
            border: 6px solid #333;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
            transition: transform 4s cubic-bezier(0.2, 0.8, 0.2, 1);
        }}
        .sector {{
            position: absolute;
            width: 100%;
            height: 100%;
            clip-path: polygon(50% 50%, 50% 0%, 100% 0%);
            transform-origin: center;
            transform: rotate(var(--start));
        }}
        .sector-text {{
            position: absolute;
            top: 20%;
            left: 50%;
            transform: translate(-50%, 0) rotate(calc((var(--start) + var(--end)) / 2 - 90deg));
            transform-origin: 50% 160px;
            color: white;
            font-weight: bold;
            font-size: 12px;
            white-space: nowrap;
        }}
        .pointer {{
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 18px solid transparent;
            border-right: 18px solid transparent;
            border-top: 35px solid red;
            filter: drop-shadow(0 2px 2px rgba(0,0,0,0.4));
            z-index: 10;
        }}
        .center {{
            position: absolute;
            width: 30px;
            height: 30px;
            background: white;
            border: 4px solid #333;
            border-radius: 50%;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 5;
        }}
    </style>

    <div class="wheel-container">
        <div class="pointer"></div>
        <div id="wheel" class="wheel">
            {sectors_html}
        </div>
        <div class="center"></div>
    </div>

    <script>
        let spinning = false;
        window.spinWheel = function(targetIndex) {{
            if (spinning) return;
            spinning = true;

            const wheel = document.getElementById('wheel');
            const n = {n};
            const anglePer = 360 / n;
            const targetAngle = 1800 + (360 - (targetIndex * anglePer + anglePer / 2)); // 5圈 + 目标位置

            wheel.style.transform = `rotate(${{targetAngle}}deg)`;

            setTimeout(() => {{
                spinning = false;
                // 通知Streamlit结果
                window.parent.postMessage({{
                    type: "WHEEL_RESULT",
                    result: "{items[0]}".replace(/"/g, '&quot;') // 占位，实际由Python控制
                }}, "*");
            }}, 4000);
        }};
    </script>
    """

# ======================= 游戏流程 =======================
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
if "final" not in st.session_state:
    st.session_state.final = ""
if "spun" not in st.session_state:
    st.session_state.spun = False

# ------------------- 步骤1：选题目 -------------------
if st.session_state.step == 1:
    st.subheader("📝 选择题目")
    q = st.selectbox("题目", list(QUESTION_BANK.keys()))
    st.session_state.question = q
    if st.button("✅ 开始", type="primary"):
        st.session_state.step = 2
        st.rerun()

# ------------------- 步骤2：玩家1答题 -------------------
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

# ------------------- 步骤3：玩家2答题 -------------------
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
                    ok = same >= 2
                else:
                    ok = same >= 1
                st.session_state.result = ok
                st.session_state.step = 4
                st.rerun()
    else:
        s = st.radio("选1个", opt, key="p2s")
        st.session_state.p2 = [s]
        if st.button("🎯 看结果", type="primary"):
            same = len(set(st.session_state.p1) & set(st.session_state.p2))
            st.session_state.result = (same >= 1)
            st.session_state.step = 4
            st.rerun()

# ------------------- 步骤4：真正会转的转盘 -------------------
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

    st.subheader("🎡 真正会转的转盘")

    # 渲染转盘
    wheel_html = spinning_wheel(items, ok)
    st.components.v1.html(wheel_html, height=400)

    if not st.session_state.spun:
        if st.button("🚀 旋转转盘", type="primary", use_container_width=True):
            idx = random.randint(0, 5)
            st.session_state.final = items[idx]

            # 触发前端旋转
            js = f"""
            <script>
                setTimeout(() => window.spinWheel({idx}), 300);
            </script>
            """
            st.components.v1.html(js, height=0)

            # 等待动画结束，再显示结果
            import time
            time.sleep(4.5)
            st.session_state.spun = True
            st.rerun()
    else:
        st.markdown(f"# 🏆 {st.session_state.final}")
        if st.button("🔄 再来一局"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
