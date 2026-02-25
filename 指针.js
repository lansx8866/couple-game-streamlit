// 核心对齐逻辑：旋转角度=8圈 + (360 - 目标扇区角度 - 30°)
const rotateDeg = 8 * 360 + (360 - targetIndex * 60 - 30);