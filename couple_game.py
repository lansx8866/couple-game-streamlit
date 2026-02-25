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

# 奖惩库（固定6个，和转盘扇区一一对应）
REWARD = ["捏肩10分钟", "承包家务", "买奶茶", "抱抱5分钟", "今天听你的", "手写情书"]
PUNISH = ["学小猫叫", "讲冷笑话", "深蹲10个", "夸对方10句", "洗水果", "模仿口头禅"]

# ======================= 无报错的精准对齐转盘（核心修复） =======================
def get_aligned_wheel(items):
    """生成无报错的转盘：纯JS字符串拼接，指针+文字+精准对齐"""
    # 固定6个扇区的颜色（视觉区分）
    colors = [
        "#FF6B9E", "#FF85A1", "#FF9Ea4", 
        "#FFB7A7", "#FFD0AA", "#FFE9AD"
    ]
    
    # 生成扇区HTML（纯字符串拼接，无模板语法）
    sector_html = ""
    angles = [0, 60, 120, 180, 240, 300]
    text_rotates = [30, 90, 150, 210, 270, 330]
    for i in range(6):
        sector_html += f"""
        <!-- 扇区{i+1}：{angles[i]}° -->
        <div class="sector" style="transform: rotate({angles[i]}deg); background: {colors[i]}">
            <div class="sector-text" style="transform: rotate({text_rotates[i]}deg)">{items[i]}</div>
        </div>
        """
    
    # 完整转盘HTML（移除所有JS模板字符串，改用+拼接）
    wheel_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            /* 转盘容器 */
            .wheel-box {
                position: relative;
                width: 350px;
                height: 350px;
                margin: 0 auto;
            }
            /* 指针（固定在顶部，绝对居中） */
            .pointer {
                position: absolute;
                top: -15px;
                left: 50%;
                transform: translateX(-50%);
                width: 0;
                height: 0;
                border-left: 20px solid transparent;
                border-right: 20px solid transparent;
                border-bottom: 40px solid red;
                z-index: 100;
                pointer-events: none;
            }
            /* 转盘主体 */
            .wheel {
                width: 350px;
                height: 350px;
                border-radius: 50%;
                position: relative;
                overflow: hidden;
                border: 8px solid #333;
                transform-origin: center center;
                transition: transform 4s cubic-bezier(0.2, 0.8, 0.1, 1);
            }
            /* 单个扇区（6个，角度固定） */
            .sector {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                clip-path: polygon(50% 50%, 50% 0%, 100% 0%, 100% 100%, 50% 100%);
                transform-origin: center center;
                display: flex;
                justify-content: center;
                align-items: flex-start;
                padding-top: 30px;
                box-sizing: border-box;
            }
            /* 扇区文字（清晰显示，旋转对齐） */
            .sector-text {
                color: #222;
                font-size: 14px;
                font-weight: bold;
                white-space: nowrap;
                transform-origin: 0 140px;
                text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
            }
            /* 中心圆点 */
            .center {
                position: absolute;
                width: 40px;
                height: 40px;
                background: white;
                border: 4px solid #333;
                border-radius: 50%;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 50;
            }
        </style>
    </head>
    <body>
        <div class="wheel-box">
            <div class="pointer"></div>
            <div id="wheel" class="wheel">
    """ + sector_html + """
            </div>
            <div class="center"></div>
        </div>

        <script>
            // 全局旋转函数：纯JS字符串拼接，无模板语法
            window.spinToTarget = function(targetIndex) {
                const wheel = document.getElementById('wheel');
                // 计算精准旋转角度：8圈 + 目标扇区中心对准指针
                const rotateDeg = 8 * 360 + (360 - targetIndex * 60 - 30);
                // 修复：用+拼接字符串，移除模板语法
                wheel.style.transform = 'rotate(' + rotateDeg + 'deg)';
            };
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
if "final_reward" not in st.session_state:
    st.session_state.final_reward = ""
if "target_idx" not in st.session_state:
    st.session_state.target_idx = -1

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

# 步骤4：无报错的精准转盘抽奖
elif st.session_state.step == 4:
    ok = st.session_state.result
    current_items = REWARD if ok else PUNISH
    
    # 展示答案对比
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
    
    # 显示无报错的转盘
    st.subheader("🎡 精准抽奖转盘", divider="violet")
    wheel_html = get_aligned_wheel(current_items)
    st.components.v1.html(wheel_html, height=400, width=400)
    
    # 旋转按钮（未抽奖状态）
    if not st.session_state.spun:
        if st.button("🚀 旋转转盘", type="primary", use_container_width=True):
            # 1. 随机选择目标扇区（0-5）
            target_idx = random.randint(0, 5)
            st.session_state.target_idx = target_idx
            st.session_state.final_reward = current_items[target_idx]
            
            # 2. 触发转盘精准旋转（纯JS拼接，无模板语法）
            trigger_js = """
            <script>
                // 找到转盘iframe并调用精准旋转函数
                const iframes = window.parent.document.querySelectorAll('iframe');
                for (let i = 0; i < iframes.length; i++) {
                    try {
                        // 修复：传参调用，无模板语法
                        iframes[i].contentWindow.spinToTarget(""" + str(target_idx) + """);
                        break;
                    } catch (e) {
                        continue;
                    }
                }
            </script>
            """
            st.components.v1.html(trigger_js, height=0)
            
            # 3. 等待动画完成
            time.sleep(4.5)
            st.session_state.spun = True
            st.rerun()
    else:
        # 显示最终结果（和指针指向的扇区100%一致）
        st.markdown(f"""
        <div style="text-align:center; font-size:24px; font-weight:bold; color:#e63946; margin:20px 0;">
            🏆 最终结果：{st.session_state.final_reward}
        </div>
        """, unsafe_allow_html=True)
        
        # 再来一局按钮
        if st.button("🔄 再来一局", use_container_width=True):
            # 重置所有状态
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

# ======================= 底部说明 =======================
st.markdown("""
<div style="margin-top:50px; padding:10px; background:#f8f9fa; border-radius:8px;">
    <p style="color:#666; text-align:center;">
        💡 转盘说明：指针固定在顶部，转盘旋转后，指针指向的扇区即为最终结果
    </p>
</div>
""", unsafe_allow_html=True)
