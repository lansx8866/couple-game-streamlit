import streamlit as st
import random
import time

# ======================= 基础配置 =======================
st.set_page_config(page_title="情侣默契转盘", layout="wide")

# 题目库
QUESTION_BANK = {
    "对方的三个优点": ["温柔体贴", "有责任心", "幽默有趣", "上进努力", "细心周到", "情绪稳定"],
    "我的三个优点": ["乐观开朗", "包容心强", "动手能力强", "善于倾听", "真诚坦率", "有耐心"],
    "对方的三个缺点": ["有点拖延", "偶尔脾气急", "不爱收拾", "太宅", "话少", "容易焦虑"],
    "我的三个缺点": ["有点敏感", "缺乏耐心", "熬夜", "挑食", "容易胡思乱想", "不爱主动"],
    "最想和对方一起做的事": ["看海边日出", "做烛光晚餐", "短途旅行", "拍情侣写真", "宅家追剧"],
}

# 奖惩库
REWARD = ["捏肩10分钟", "承包家务", "买奶茶", "抱抱5分钟", "今天听你的", "手写情书"]
PUNISH = ["学小猫叫", "讲冷笑话", "深蹲10个", "夸对方10句", "洗水果", "模仿口头禅"]

# ======================= 核心：100%能转的转盘代码 =======================
def get_working_wheel(items, is_reward):
    # 颜色配置
    color = "pink" if is_reward else "orange"
    
    # 直接写死6个扇区的转盘（最稳定）
    wheel_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            /* 转盘容器 */
            .wheel {{
                width: 300px;
                height: 300px;
                border-radius: 50%;
                position: relative;
                margin: 0 auto;
                overflow: hidden;
                border: 5px solid #333;
                transition: transform 3s ease-out; /* 核心：3秒旋转动画 */
                transform-origin: center;
            }}
            /* 扇区样式 */
            .slice {{
                position: absolute;
                width: 100%;
                height: 100%;
                clip-path: polygon(50% 50%, 50% 0%, 100% 0%);
                transform-origin: center;
                display: flex;
                align-items: flex-start;
                justify-content: center;
                padding-top: 20px;
                box-sizing: border-box;
            }}
            /* 扇区文字 */
            .slice span {{
                color: white;
                font-weight: bold;
                font-size: 12px;
                transform: rotate(var(--rotate));
                white-space: nowrap;
            }}
            /* 指针 */
            .pointer {{
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
            }}
            /* 中心圆点 */
            .center {{
                position: absolute;
                width: 25px;
                height: 25px;
                background: white;
                border: 3px solid #333;
                border-radius: 50%;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 5;
            }}
        </style>
    </head>
    <body>
        <div style="position: relative; width: 300px; margin: 0 auto;">
            <div class="pointer"></div>
            <div id="wheel" class="wheel">
                <!-- 6个扇区（固定角度） -->
                <div class="slice" style="transform: rotate(0deg); background: {color}; --rotate: 30deg;">
                    <span>{items[0]}</span>
                </div>
                <div class="slice" style="transform: rotate(60deg); background: {color}88; --rotate: 90deg;">
                    <span>{items[1]}</span>
                </div>
                <div class="slice" style="transform: rotate(120deg); background: {color}; --rotate: 150deg;">
                    <span>{items[2]}</span>
                </div>
                <div class="slice" style="transform: rotate(180deg); background: {color}88; --rotate: 210deg;">
                    <span>{items[3]}</span>
                </div>
                <div class="slice" style="transform: rotate(240deg); background: {color}; --rotate: 270deg;">
                    <span>{items[4]}</span>
                </div>
                <div class="slice" style="transform: rotate(300deg); background: {color}88; --rotate: 330deg;">
                    <span>{items[5]}</span>
                </div>
            </div>
            <div class="center"></div>
        </div>

        <script>
            // 全局旋转函数（外部可调用）
            window.startSpin = function(degrees) {{
                const wheel = document.getElementById('wheel');
                wheel.style.transform = `rotate(${degrees}deg)`;
            }};
        </script>
    </body>
    </html>
    """
    return wheel_html

# ======================= 会话状态初始化 =======================
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

# ======================= 游戏流程 =======================
# 步骤1：选择题目
if st.session_state.step == 1:
    st.subheader("📝 选择考验题目", divider="violet")
    q = st.selectbox("请选择题目", list(QUESTION_BANK.keys()))
    st.session_state.question = q
    if st.button("✅ 确定开始", type="primary"):
        st.session_state.step = 2
        st.rerun()

# 步骤2：玩家1答题
elif st.session_state.step == 2:
    q = st.session_state.question
    opts = QUESTION_BANK[q]
    st.subheader(f"👩 玩家1答题：{q}", divider="violet")
    
    if "优点" in q or "缺点" in q:
        selected = st.multiselect("选3个答案（最多3个）", opts, max_selections=3)
        if len(selected) == 3:
            st.session_state.p1 = selected
            if st.button("✅ 轮到玩家2", type="primary"):
                st.session_state.step = 3
                st.rerun()
        else:
            st.info(f"已选{len(selected)}/3个，需选满！")
    else:
        selected = st.radio("选1个答案", opts)
        st.session_state.p1 = [selected]
        if st.button("✅ 轮到玩家2", type="primary"):
            st.session_state.step = 3
            st.rerun()

# 步骤3：玩家2答题
elif st.session_state.step == 3:
    q = st.session_state.question
    opts = QUESTION_BANK[q]
    st.subheader(f"👨 玩家2答题：{q}", divider="violet")
    
    if "优点" in q or "缺点" in q:
        selected = st.multiselect("选3个答案（最多3个）", opts, max_selections=3)
        if len(selected) == 3:
            st.session_state.p2 = selected
            same = len(set(st.session_state.p1) & set(selected))
            st.session_state.result = same >= 2
            if st.button("🎯 查看结果", type="primary"):
                st.session_state.step = 4
                st.rerun()
        else:
            st.info(f"已选{len(selected)}/3个，需选满！")
    else:
        selected = st.radio("选1个答案", opts)
        st.session_state.p2 = [selected]
        same = len(set(st.session_state.p1) & set([selected]))
        st.session_state.result = same >= 1
        if st.button("🎯 查看结果", type="primary"):
            st.session_state.step = 4
            st.rerun()

# 步骤4：抽奖转盘（核心：100%能转）
elif st.session_state.step == 4:
    ok = st.session_state.result
    items = REWARD if ok else PUNISH
    
    # 展示结果
    st.subheader("🧩 默契结果", divider="violet")
    st.write(f"玩家1答案：{', '.join(st.session_state.p1)}")
    st.write(f"玩家2答案：{', '.join(st.session_state.p2)}")
    if ok:
        st.success("🎉 默契成功！抽奖励")
    else:
        st.warning("😜 默契不足！抽惩罚")
    
    # 显示转盘（核心）
    st.subheader("🎡 抽奖转盘", divider="violet")
    wheel_html = get_working_wheel(items, ok)
    st.components.v1.html(wheel_html, height=350, width=350)
    
    # 旋转按钮
    if not st.session_state.spun:
        if st.button("🚀 旋转转盘", type="primary", use_container_width=True):
            # 随机生成旋转角度（5圈+随机停止）
            random_deg = random.randint(1800, 3600)  # 5-10圈
            target_idx = random.randint(0, 5)
            st.session_state.final = items[target_idx]
            
            # 触发转盘旋转（核心：调用前端JS函数）
            st.components.v1.html(f"""
                <script>
                    window.parent.document.querySelector('iframe').contentWindow.startSpin({random_deg});
                </script>
            """, height=0)
            
            # 等待旋转完成
            time.sleep(3.5)
            st.session_state.spun = True
            st.rerun()
    else:
        # 显示结果
        st.markdown(f"### 🏆 抽到：{st.session_state.final}")
        if st.button("🔄 再来一局", use_container_width=True):
            # 重置状态
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
