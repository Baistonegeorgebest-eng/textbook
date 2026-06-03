# Novel Skills v1.18.2 评估报告

> 评估时间：2026-05-07
> 基线版本：v1.18.1（71个skill，3.1MB）
> 当前版本：v1.18.2（71个skill，human-flavor已重构+3个新references）
> 参考源：人味注入协议 v4.4/v4.5（362本小说，11.6亿字）+ Claude Code 源码研究

---

## 一、v1.18.2 变更清单

### 1.1 核心变更：expert-human-flavor 重构

| 维度 | v1.18.1 | v1.18.2 |
|------|---------|---------|
| SKILL.md 行数 | 499行（含大量详细内容） | 410行（核心硬约束+摘要） |
| 严肃度标尺 | ❌ 无 | ✅ 摘要版（表格化）+ 完整版在references/ |
| AI鉴别指南 | ❌ 无 | ✅ 7个量化指纹+快速检测流程 |
| 退化预警 | ❌ 无 | ✅ 三种来源+核心阈值表+检测流程摘要 |
| 质量分级 | 简略 | ✅ T1/T2/T3摘要+完整prompt在references/ |
| 分层加载 | ❌ 全量加载 | ✅ 核心每次加载，references按需读取 |

### 1.2 新增 references 文件

| 文件 | 行数 | 内容 | 来源 |
|------|------|------|------|
| `references/tier-prompts.md` | 160行 | T1/T2/T3完整prompt模板+质检指标 | v4.4 §四 |
| `references/quality-degradation.md` | 170行 | 人味指数13项+退化检测流程+严肃度-标点锚定表 | v4.4 §十 |
| `references/style-reference.md` | 389行 | 33本参考小说风格DNA+标点指纹+叙事方法论 | v4.4 §十二 |

### 1.3 保留的已有 references

| 文件 | 说明 | 状态 |
|------|------|------|
| `references/diagnostics.md` | 169章全本诊断数据 | 保留不动 |
| `references/fingerprint-table.md` | 304本标点指纹全量数据 | 保留不动 |
| `references/quality-checks.md` | 人味指数7项+防退化 | 保留（与新quality-degradation.md互补） |
| `references/reader-dna.md` | 读者偏好逆炼DNA | 保留不动 |

---

## 二、v1.18.1 → v1.18.2 解决的问题

### 2.1 已解决 ✅

| 问题 | 严重度 | 解决方案 |
|------|--------|---------|
| human-flavor缺少严肃度标尺 | 🔴 | 核心文件摘要版+references完整版 |
| human-flavor缺少AI鉴别指南 | 🔴 | 7个量化指纹+快速检测流程 |
| human-flavor缺少退化预警 | 🔴 | 三种来源+量化阈值+检测流程 |
| human-flavor缺少风格参照库 | 🟡 | references/style-reference.md（33本真实数据） |
| human-flavor缺少T1/T2/T3完整prompt | 🟡 | references/tier-prompts.md |
| 核心文件太重（499行全量加载） | 🟡 | 重构为410行核心+按需references |
| 硬约束不能独立注入prompt | 🔴 | 核心文件的硬约束部分完全自包含 |

### 2.2 未解决（需要后续版本）

| 问题 | 严重度 | 建议方案 | 预计工作量 |
|------|--------|---------|-----------|
| **人味相关skill重叠** | 🔴 | 合并human-flavor-tiers+anti-ai-taste→废弃 | 0.5天 |
| **自动质检脚本缺失** | 🔴 | 基于public-transfer分析工具改造 | 1-2天 |
| **expert-hook示例过时** | 🟡 | 注入v4.4 §十二开局模式+文抄公公式 | 0.5天 |
| **expert-dialogue分类粗糙** | 🟡 | 替换为v4.4四种博弈类型 | 0.5天 |
| **expert-emotion模板化** | 🟡 | 注入江南式悲凉叙事+感官记忆锚点 | 0.5天 |
| **expert-character标签化** | 🟡 | 注入角色DNA卡模板+语言指纹 | 0.5天 |
| **expert-combat缺数据验证** | 🟡 | 注入严肃度-标点锚定 | 0.5天 |
| **expert-pacing缺弹性模板** | 🟡 | 注入升级循环四层结构 | 0.5天 |
| **skill总数过多（71个）** | 🟡 | 合并到40-45个 | 1-2天 |
| **平台数据需联网验证** | 🟢 | 番茄/起点算法半年一变 | 持续 |

---

## 三、全体系评估（71个skill扫描）

### 3.1 内容老化度评估

对71个skill进行抽样检查，评估示例/锚定作品的时效性：

| 老化等级 | skill数量 | 代表 | 特征 |
|---------|----------|------|------|
| 🟢 内容新鲜 | ~15个 | expert-human-flavor(v1.18.2), expert-fanqie-novel, expert-xuanhuan | 有2025-2026数据/趋势 |
| 🟡 部分过时 | ~35个 | expert-character, expert-emotion, expert-dialogue, expert-combat, expert-pacing | 框架可用但示例老套 |
| 🔴 严重过时 | ~10个 | expert-hook(示例全是2021模板), expert-plot-shuangdian, expert-title-outro | 示例是审核雷区 |
| ⚪ 无需更新 | ~11个 | novel-expert-system, expert-writing-safety, expert-logic, expert-memory | 调度/安全/逻辑类不依赖时效 |

### 3.2 各skill详细评估

#### 🔴 严重过时（需要重写示例）

**expert-hook（397行）**
- 问题：第一句写法全是2021番茄模板——"签字吧""你这个废物""她笑了笑"
- 问题：300字出冲突法则缺少2026年番茄审核标准的验证
- 问题：缺少v4.4的文抄公开局公式（Ch1意外→Ch2金手指→Ch3方向）
- 建议：注入v4.4 §十二12.8.1开局模式+12.8.2钩子设计

**expert-plot-shuangdian（412行）**
- 问题：爽点设计缺少弹性叙事模板（升级循环四层结构）
- 问题：缺少v4.4的"每次获益必须附带新压力"原则
- 建议：注入v4.4 §十二12.8.3弹性叙事模板

**expert-title-outro（394行）**
- 问题：标题/结尾设计缺少文抄公的"标题即钩子"手法
- 建议：注入v4.4 §十二12.8.2的章节末钩子类型表

#### 🟡 部分过时（需要更新示例+补充数据）

**expert-character（469行）**
- 问题：角色类型用"废物流/高冷学霸/嘴毒暖男"标签化分类
- 问题：缺少v4.4的角色语言DNA卡模板（说话节奏/高频词/禁区词/口癖/情感出口/感官偏好/语言缺陷/职业渗透）
- 问题：缺少角色声音区分的实测数据
- 建议：注入v4.4 §五角色语言DNA+§十二的对话类型分析

**expert-dialogue（400行）**
- 问题：对话分类用"用词风格/说话节奏/口头禅"三要素，太粗糙
- 问题：缺少v4.4的四种博弈类型（信息不对称/权力试探/荒诞缓冲/日常社交）
- 问题：缺少不同严肃度下的对话比例参考值
- 建议：替换为v4.4 §十二12.4对话类型+§十二12.5标点指纹

**expert-emotion（未统计行数）**
- 问题："甜宠五感写作法""她是我的人，谁敢动她？"——2020年霸总模板
- 问题：缺少v4.4江南式悲凉叙事五来源（宿命感/无常/沉默牺牲/温柔残忍/回不去）
- 问题：缺少感官记忆锚点技法
- 建议：注入v4.4 §十二江南分析+悲凉叙事五来源

**expert-combat（未统计行数）**
- 问题：战斗节奏公式（10%/30%/20%/20%/20%）没有数据验证
- 问题：缺少严肃度与战斗描写风格的对应关系
- 建议：注入v4.4 §十严肃度-标点锚定表

**expert-pacing（406行）**
- 问题：节奏控制缺少弹性叙事模板
- 问题：缺少v4.4的四层结构（微观1-3章/中观3-10章/宏观30-50章/卷级100-200章）
- 建议：注入v4.4 §十二12.8.3弹性叙事模板+12.8.5节奏控制

**expert-suspense（499行）**
- 问题：悬念设计缺少罗琳式信息经济+误导向手法
- 问题：缺少"假反派"设计和"可信的人做不可信的事"技法
- 建议：注入v4.4 §十二12.8.9罗琳叙事DNA

**expert-sensory-prose（未统计行数）**
- 问题：感官描写缺少v4.4的感官优先级表（按题材选2-3种重点写）
- 问题：缺少感官混搭技法（用味觉词修饰听觉等）
- 建议：注入v4.4 §九感官优先级+§十二12.3感官选择

**expert-literary-prose（未统计行数）**
- 问题：文学性描写缺少西方参照（托尔金/洛夫克拉夫特/阿西莫夫的量化指纹）
- 建议：注入v4.4 §十二12.8.9西方叙事参照

**expert-writing-style（未统计行数）**
- 问题：与expert-style-learner重叠
- 问题：风格参考缺少v4.4的33本全量标点指纹数据
- 建议：合并为expert-style-reference，注入v4.4 §十二完整参照库

**expert-xuanhuan（232行+references）**
- 问题：赛道分类还行，但缺少文抄公系统设计模式（面板型/吸收型/穿梭型/转生型）
- 问题：修炼体系设计缺少"系统必须有局限性"原则
- 建议：注入v4.4 §十二12.8.4升级系统设计

**expert-fanqie-novel（352行+references）**
- 问题：标注"2026校正版"但数据来源不明确
- 问题：平台算法标准链接可能失效
- 建议：联网验证2026最新算法+审核标准

**expert-guoxue（488行）**
- 问题：国学题材缺少历史文的标点参照（绍宋省略号9.41/千字+对话57.1%）
- 建议：注入v4.4 §十二榴弹怕水分析

**expert-rebirth（426行）**
- 问题：重生题材缺少文抄公的"退婚+自嘲"套路升级手法
- 建议：注入v4.4 §十二12.8.7退婚/打脸模板

#### 🟢 内容新鲜（无需大改）

- expert-human-flavor（v1.18.2重构版）
- expert-fanqie-novel（有references支撑）
- expert-xuanhuan（有references支撑）
- expert-worldbuilding（框架稳定）
- expert-quality-gate（门禁逻辑稳定）
- expert-writing-safety（合规红线稳定）
- novel-expert-system（调度逻辑稳定）
- novel-volume-workflow（工作流稳定）

#### ⚪ 无需时效性更新

- expert-logic（逻辑自洽，不依赖时效）
- expert-memory / novel-memory-3layer（记忆管理）
- expert-bookstatus（项目状态追踪）
- expert-footprint（重复检测）
- expert-dependency-map（依赖关系）
- expert-collaboration-protocol（多skill协同）
- skill-safety-protocol（安全协议）
- skill-deployment-protocol（部署协议）

---

## 四、架构评估

### 4.1 分层加载现状

| 层级 | 当前状态 | 期望状态 |
|------|---------|---------|
| 核心层（每次加载） | ❌ 无分层，71个全量 | 5-8个skill，≤3000 token |
| 按需层（创作阶段） | ❌ 无分层 | 15-20个skill |
| 参考层（质检/诊断） | ❌ 无分层 | 其余skill |

### 4.2 重叠skill清单

| 合并组 | 涉及skill | 建议 |
|--------|----------|------|
| 人味组 | human-flavor + human-flavor-tiers + anti-ai-taste | tiers和anti-ai-taste已并入human-flavor v1.18.2，可废弃 |
| 风格组 | writing-style + style-learner | 合并为style-reference |
| 情感组 | emotion + emotion-death | 合并为emotion |
| 修改组 | revise-loop + revision | 合并为revision |
| 记忆组 | memory + novel-memory-3layer | 合并为memory |
| 番茄组 | fanqie-short + fanqie-novel + fanqie-female | 按篇幅分references，合并为fanqie |

### 4.3 自动质检现状

| 维度 | 规则覆盖 | 自动检测 | 状态 |
|------|---------|---------|------|
| 标点指纹 | ✅ | ❌ | 需要脚本 |
| 句式多样性 | ✅ | ❌ | 需要脚本 |
| 感官密度 | ✅ | ❌ | 需要脚本 |
| 对话比例 | ✅ | ❌ | 需要脚本 |
| AI模板 | ✅ | ❌ | 需要脚本 |
| 禁用词冷却 | ✅ | ❌ | 需要脚本 |
| 退化检测 | ✅(v1.18.2新增) | ❌ | 需要脚本 |

**可复用的已有工具（public-transfer仓库）：**
- `scripts/extract-corpus-stats-v2.py` → 标点统计
- `batch-fingerprint.py` → 风格指纹
- `extract-sensory.py` → 感官密度
- `extract-tjss-deep.py` → 深度分析

---

## 五、与番茄审核被拒的关联

### 5.1 番茄AI检测机制（2025-2026）

| 检测维度 | 番茄关注点 | v1.18.2覆盖 |
|---------|-----------|------------|
| 标点指纹异常 | 句号碎片率高、省略号缺失、感叹号偏高 | ✅ AI鉴别7指纹 |
| 句式单一 | 连续相同句式结构 | ⚠️ 有规则无自动检测 |
| 情感表达模式化 | 直述情感过多 | ⚠️ 有规则无自动检测 |
| 感官偏科 | 只有视觉，缺嗅觉/触觉 | ⚠️ 有规则无自动检测 |
| 对话比例异常 | 过低或过高 | ⚠️ 有规则无自动检测 |
| 模糊表达泛滥 | "什么东西/某种/似乎"过多 | ✅ 硬约束+AI鉴别 |

### 5.2 关键发现

阅文副总编辑胡说（2025）：
> "DeepSeek的风格挺明显，有强烈的赛博科幻和视觉化、克系写作风格，很难校正。如果没有相应剧情支撑，看起来就言之无物，会让小说更空洞、更水。"

**v1.18.2的应对：** AI鉴别7指纹中#7（模糊表达泛滥）直接针对"言之无物"问题。但自动化检测仍是短板。

---

## 六、下一步路线图

### v1.18.3（建议1周内）

| 任务 | 优先级 | 工作量 |
|------|--------|--------|
| 废弃human-flavor-tiers+anti-ai-taste | 🔴 | 0.5天 |
| 更新expert-hook示例（注入v4.4开局模式） | 🔴 | 0.5天 |
| 更新expert-dialogue（注入四种博弈类型） | 🟡 | 0.5天 |
| 更新expert-emotion（注入江南式悲凉叙事） | 🟡 | 0.5天 |
| 合并writing-style+style-learner | 🟡 | 0.5天 |

### v1.19.0（建议2周内）

| 任务 | 优先级 | 工作量 |
|------|--------|--------|
| 搭建自动质检脚本 | 🔴 | 1-2天 |
| 更新expert-character（注入角色DNA卡） | 🟡 | 0.5天 |
| 更新expert-combat（注入严肃度锚定） | 🟡 | 0.5天 |
| 更新expert-pacing（注入弹性叙事模板） | 🟡 | 0.5天 |
| skill精简合并（71→40-45个） | 🟡 | 1-2天 |

### v1.20.0（建议1月内）

| 任务 | 优先级 | 工作量 |
|------|--------|--------|
| 联网验证番茄/起点最新算法 | 🟢 | 持续 |
| 建立反馈闭环（审核结果→质检标准） | 🟢 | 持续 |
| 更新剩余过时skill示例 | 🟢 | 持续 |

---

## 七、v1.18.2 文件清单

```
novel-skills-v1.18.2/
├── CHANGELOG.md                          # 变更日志
├── expert-human-flavor/
│   ├── SKILL.md                          # 核心文件（410行）
│   └── references/
│       ├── tier-prompts.md               # T1/T2/T3 prompt模板（160行）
│       ├── quality-degradation.md        # 质检/退化（170行）
│       ├── style-reference.md            # 风格参照库（389行）
│       ├── diagnostics.md                # 诊断数据（已有）
│       ├── fingerprint-table.md          # 标点指纹（已有）
│       ├── quality-checks.md             # 人味指数（已有）
│       └── reader-dna.md                 # 读者DNA（已有）
├── expert-acg-fanfic/                    # （不变）
├── expert-acg-short/                     # （不变）
├── expert-anti-ai-taste/                 # （不变，待v1.18.3废弃）
├── ...（其余68个skill不变）
```
