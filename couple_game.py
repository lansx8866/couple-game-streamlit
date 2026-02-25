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

# ======================= 高级物理动画转盘（核心修复+升级） =======================
def get_advanced_wheel(items, is_reward):
    """高级物理动画转盘：带惯性、摩擦、精准停位"""
    # 颜色渐变配置（更高级的配色）
    reward_colors = [
        "#FF6B9E", "#FF85A1", "#FF9Ea4", "#FFB7A7", "#FFD0AA", "#FFE9AD"
    ]
    punish_colors = [
        "#FF9500", "#FFA726", "#FFB74D", "#FFC107", "#FFCA28", "#FFD54F"
    ]
    colors = reward_colors if is_reward else punish_colors
    
    # 生成6个扇区的HTML（固定角度）
    sectors = []
    angles = [0, 60, 120, 180, 240, 300]
    for i, (angle, text) in enumerate(zip(angles, items)):
        rotate_text = angle + 30  # 文字旋转角度
        sectors.append(f"""
            <div class="sector" style="
                transform: rotate({angle}deg);
                background: {colors[i]};
            ">
                <div class="sector-text" style="transform: rotate({rotate_text}deg)">
                    {text}
                </div>
            </div>
        """)
    
    # 高级动画转盘完整代码（修复语法错误+物理动画）
    wheel_html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            .wheel-container {{
                position: relative;
                width: 350px;
                height: 350px;
                margin: 0 auto;
            }}
            /* 转盘主体（高级样式） */
            .wheel {{
                width: 100%;
                height: 100%;
                border-radius: 50%;
                position: relative;
                overflow: hidden;
                border: 8px solid #212121;
                box-shadow: 
                    0 0 0 4px #f5f5f5,
                    0 0 20px rgba(0,0,0,0.3),
                    inset 0 0 10px rgba(0,0,0,0.2);
                transform-origin: center;
                transition: none; /* 关闭默认过渡，用JS控制物理动画 */
            }}
            /* 扇区样式 */
            .sector {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                clip-path: polygon(50% 50%, 50% 0%, 100% 0%, 100% 100%, 50% 100%);
                transform-origin: center;
                display: flex;
                align-items: flex-start;
                justify-content: center;
                padding-top: 25px;
                border: 1px solid rgba(255,255,255,0.3);
            }}
            /* 扇区文字（高级排版） */
            .sector-text {{
                color: #212121;
                font-weight: 600;
                font-size: 13px;
                white-space: nowrap;
                transform-origin: 0 140px;
                text-shadow: 0 1px 2px rgba(255,255,255,0.8);
            }}
            /* 高级指针（带阴影+高光） */
            .pointer {{
                position: absolute;
                top: -20px;
                left: 50%;
                transform: translateX(-50%);
                width: 0;
                height: 0;
                border-left: 20px solid transparent;
                border-right: 20px solid transparent;
                border-bottom: 40px solid #F44336;
                z-index: 10;
                filter: drop-shadow(0 3px 3px rgba(0,0,0,0.4));
                clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
            }}
            .pointer::after {{
                content: '';
                position: absolute;
                top: 5px;
                left: -15px;
                width: 0;
                height: 0;
                border-left: 15px solid transparent;
                border-right: 15px solid transparent;
                border-bottom: 30px solid #FFCDD2;
            }}
            /* 中心按钮（可点击） */
            .center-btn {{
                position: absolute;
                width: 40px;
                height: 40px;
                background: linear-gradient(#fff, #e0e0e0);
                border: 4px solid #212121;
                border-radius: 50%;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 5;
                cursor: pointer;
                box-shadow: 
                    0 2px 5px rgba(0,0,0,0.3),
                    inset 0 -2px 5px rgba(0,0,0,0.1),
                    inset 0 2px 5px rgba(255,255,255,0.8);
            }}
            .center-btn:active {{
                box-shadow: 
                    0 1px 2px rgba(0,0,0,0.3),
                    inset 0 -1px 2px rgba(0,0,0,0.1),
                    inset 0 1px 2px rgba(255,255,255,0.8);
                transform: translate(-50%, -50%) scale(0.95);
            }}
        </style>
    </head>
    <body>
        <div class="wheel-container">
            <div class="pointer"></div>
            <div id="wheel" class="wheel">
                {''.join(sectors)}
            </div>
            <div class="center-btn"></div>
        </div>

        <script>
            // 高级物理动画参数
            const wheel = document.getElementById('wheel');
            let isSpinning = false;
            let currentAngle = 0;
            let targetAngle = 0;
            let velocity = 0;
            const friction = 0.98; // 摩擦系数
            const acceleration = 5; // 加速度
            
            // 物理动画核心函数
            function animateWheel() {{
                if (isSpinning) {{
                    // 加速阶段
                    if (velocity < 30) {{
                        velocity += acceleration;
                    }}
                    // 减速阶段（接近目标角度）
                    const angleDiff = Math.abs(targetAngle - currentAngle) % 360;
                    if (angleDiff < 360 && velocity > 0.5) {{
                        velocity *= friction;
                    }} else if (velocity <= 0.5) {{
                        velocity = 0;
                        currentAngle = targetAngle;
                        isSpinning = false;
                    }}
                    
                    currentAngle += velocity;
                    wheel.style.transform = 'rotate(' + currentAngle + 'deg)';
                    requestAnimationFrame(animateWheel);
                }}
            }}
            
            // 外部调用的旋转函数（修复语法错误：用+拼接字符串）
            window.startAdvancedSpin = function(targetIndex) {{
                if (isSpinning) return;
                
                const sectorAngle = 60; // 每个扇区60度
                // 目标角度：8圈 + 精准停在扇区中心
                targetAngle = currentAngle + 8 * 360 + (360 - (targetIndex * sectorAngle + sectorAngle/2));
                isSpinning = true;
                velocity = 0;
                
                // 启动物理动画
                animateWheel();
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

# 步骤4：高级动画转盘（核心修复）
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
    
    # 显示高级动画转盘
    st.subheader("🎡 高级物理动画转盘", divider="violet")
    wheel_html = get_advanced_wheel(items, ok)
    st.components.v1.html(wheel_html, height=400, width=400)
    
    # 旋转按钮
    if not st.session_state.spun:
        if st.button("🚀 启动高级转盘", type="primary", use_container_width=True):
            # 随机选择目标扇区
            target_idx = random.randint(0, 5)
            st.session_state.final = items[target_idx]
            
            # 触发高级物理动画（修复JS调用方式）
            trigger_js = f"""
            <script>
                // 找到转盘的iframe并调用旋转函数
                const iframes = window.parent.document.querySelectorAll('iframe');
                for (let i = 0; i < iframes.length; i++) {{
                    try {{
                        iframes[i].contentWindow.startAdvancedSpin({target_idx});
                        break;
                    }} catch (e) {{
                        continue;
                    }}
                }}
            </script>
            """
            st.components.v1.html(trigger_js, height=0)
            
            # 等待动画完成
            time.sleep(8)  # 高级动画持续时间更长
            st.session_state.spun = True
            st.rerun()
    else:
        # 显示结果
        st.markdown(f"### 🏆 最终结果：{st.session_state.final}")
        if st.button("🔄 再来一局", use_container_width=True):
            # 重置所有状态
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
