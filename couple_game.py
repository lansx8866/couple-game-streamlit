import streamlit as st
import random
import time

# 设置页面配置（标题、图标）
st.set_page_config(
    page_title="情侣互动小游戏 💖",
    page_icon="💞",
    layout="wide"
)

# 初始化会话状态（保存用户选择/自定义内容，刷新不丢失）
if "events" not in st.session_state:
    st.session_state.events = [
        "一起看海边日出", "一起做烛光晚餐", "一起去游乐园",
        "一起打卡网红餐厅", "一起窝沙发看电影", "一起短途旅行"
    ]
if "rewards" not in st.session_state:
    st.session_state.rewards = [
        "捏肩10分钟", "承包当天家务", "买喜欢的奶茶",
        "专属拥抱", "手写情书", "陪做想做的事"
    ]
if "punishments" not in st.session_state:
    st.session_state.punishments = [
        "讲3个冷笑话", "学小猫叫5声", "做10个深蹲",
        "洗一次袜子", "夸10分钟不重样", "模仿口头禅10遍"
    ]
if "p1_choices" not in st.session_state:
    st.session_state.p1_choices = []
if "p2_choices" not in st.session_state:
    st.session_state.p2_choices = []
if "has_match" not in st.session_state:
    st.session_state.has_match = False
if "same_events" not in st.session_state:
    st.session_state.same_events = []
if "spin_result" not in st.session_state:
    st.session_state.spin_result = ""

# ---------------------- 自定义内容模块 ----------------------
st.title("💖 情侣互动小游戏 💖")
st.subheader("✨ 自定义事件/奖惩", divider="pink")

# 自定义事件
col1, col2, col3 = st.columns(3)
with col1:
    new_event = st.text_input("添加想要一起做的事", placeholder="比如：一起养小宠物")
    if st.button("添加事件", key="add_event"):
        if new_event and new_event not in st.session_state.events:
            st.session_state.events.append(new_event)
            st.success(f"✅ 添加事件：{new_event}")
        elif new_event in st.session_state.events:
            st.warning("❌ 该事件已存在！")
        else:
            st.error("❌ 事件不能为空！")

# 自定义奖励
with col2:
    new_reward = st.text_input("添加奖励", placeholder="比如：买一支口红")
    if st.button("添加奖励", key="add_reward"):
        if new_reward and new_reward not in st.session_state.rewards:
            st.session_state.rewards.append(new_reward)
            st.success(f"✅ 添加奖励：{new_reward}")
        elif new_reward in st.session_state.rewards:
            st.warning("❌ 该奖励已存在！")
        else:
            st.error("❌ 奖励不能为空！")

# 自定义惩罚
with col3:
    new_punish = st.text_input("添加惩罚", placeholder="比如：背对方走50米")
    if st.button("添加惩罚", key="add_punish"):
        if new_punish and new_punish not in st.session_state.punishments:
            st.session_state.punishments.append(new_punish)
            st.success(f"✅ 添加惩罚：{new_punish}")
        elif new_punish in st.session_state.punishments:
            st.warning("❌ 该惩罚已存在！")
        else:
            st.error("❌ 惩罚不能为空！")

# ---------------------- 双人选择模块 ----------------------
st.subheader("💘 选择想要一起做的事（1-3件）", divider="pink")
col_p1, col_p2 = st.columns(2)

# 第一个人选择
with col_p1:
    st.markdown("### 👩 宝贝1号")
    p1_selected = st.multiselect(
        "请选择（最多3件）",
        options=st.session_state.events,
        max_selections=3,
        key="p1_select"
    )
    st.session_state.p1_choices = p1_selected
    st.info(f"已选：{len(p1_selected)} 件")

# 第二个人选择
with col_p2:
    st.markdown("### 👨 宝贝2号")
    p2_selected = st.multiselect(
        "请选择（最多3件）",
        options=st.session_state.events,
        max_selections=3,
        key="p2_select"
    )
    st.session_state.p2_choices = p2_selected
    st.info(f"已选：{len(p2_selected)} 件")

# 提交选择，匹配结果
if st.button("🎯 提交选择，查看匹配结果", type="primary"):
    if len(st.session_state.p1_choices) == 0 or len(st.session_state.p2_choices) == 0:
        st.error("❌ 两人都需要至少选择1件事哦！")
    else:
        # 匹配相同事件
        same_events = list(set(st.session_state.p1_choices) & set(st.session_state.p2_choices))
        st.session_state.same_events = same_events
        st.session_state.has_match = len(same_events) > 0

        # 展示结果
        st.subheader("🎊 匹配结果", divider="pink")
        if same_events:
            st.success(f"💞 你们选到了相同的事：{', '.join(same_events)}")
        else:
            st.warning(f"😯 你们没有选到相同的事哦～")

        # 展示各自独选的
        p1_only = list(set(st.session_state.p1_choices) - set(same_events))
        p2_only = list(set(st.session_state.p2_choices) - set(same_events))
        if p1_only:
            st.write(f"👩 宝贝1号独选：{', '.join(p1_only)}")
        if p2_only:
            st.write(f"👨 宝贝2号独选：{', '.join(p2_only)}")

# ---------------------- 转盘抽奖模块 ----------------------
if st.session_state.has_match or (len(st.session_state.p1_choices) > 0 and len(st.session_state.p2_choices) > 0):
    st.subheader("🎡 转盘抽奖", divider="pink")
    wheel_type = "奖励" if st.session_state.has_match else "惩罚"
    wheel_items = st.session_state.rewards if st.session_state.has_match else st.session_state.punishments

    # 转盘抽奖逻辑
    if st.button(f"开始{wheel_type}抽奖 🎲"):
        with st.spinner("转盘旋转中..."):
            time.sleep(2)  # 模拟旋转动画
            st.session_state.spin_result = random.choice(wheel_items)

    # 展示抽奖结果
    if st.session_state.spin_result:
        if st.session_state.has_match:
            st.markdown(f"### 🎉 恭喜抽到奖励：\n## {st.session_state.spin_result}")
        else:
            st.markdown(f"### 😜 接受惩罚：\n## {st.session_state.spin_result}")

# 重置游戏按钮
if st.button("🔄 重新开始游戏"):
    # 清空所有会话状态
    st.session_state.clear()
    st.rerun()  # 刷新页面