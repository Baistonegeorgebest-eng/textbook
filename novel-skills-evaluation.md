# 小说 Skill 体系评估报告

> 评估时间：2026-05-07
> 评估版本：novel-skills-v1.18.1
> 评估对象：70 个 SKILL.md + references 体系（3.1MB）
> 关联仓库：public-transfer（人味协议 v4.5，362 本小说分析，11.6 亿字数据）

---

## 一、体系全貌

### 1.1 三层架构

```
第一层：调度中枢（3 个）
  novel-expert-system      → 全流程路由入口
  novel-volume-workflow    → 卷级自动编排（用户说"推进第二卷"即走完全链路）
  expert-collaboration-protocol → 多 expert 协同协议（67 个 skill 索引）

第二层：领域专家（60+ 个）
  平台类：fanqie-short / fanqie-novel / fanqie-female / qidian / qidian-long / jjwxc
  题材类：xuanhuan / xihuan / guoxue / acg / sci-fi / horror / suspense / urban / farming / rebirth
  技艺类：character / combat / dialogue / emotion / hook / pacing / plot-shuangdian
  系统类：skill-system / worldbuilding / weapons / cosmology-physics
  人味类：human-flavor / human-flavor-tiers / anti-ai-taste / character-dna / style-learner
  运营类：serialization-ops / platform-metrics / reader-tracker / bookstatus

第三层：质量保障（5+ 个）
  expert-quality-gate      → 门禁验证（Pre-Write / Post-Write / Full Audit）
  expert-writing-safety    → 安全合规
  expert-revise-loop       → 修正循环
  expert-logic             → 逻辑自洽
  expert-footprint         → 重复检测
```

### 1.2 规模数据

| 指标 | 数值 |
|------|------|
| SKILL.md 总数 | 70 个 |
| 总体积 | 3.1 MB |
| references 文件 | 含大量参考文档（题材分析、平台规则、技法库等） |
| 协议版本 | 人味注入协议 v4.5（基于 362 本小说 + 11.6 亿字 + 6 篇学术论文） |
| 分析报告 | 859 份（含 56 份深度对比/进化分析） |

---

## 二、优势评估（做得好的地方）

### 2.1 调度设计 ⭐⭐⭐⭐⭐

- `novel-volume-workflow` 实现了"一句话走完全链路"：用户说"推进第二卷"，自动执行 规划→预标注→逐章→质检→更新
- 不需要手动调用每个 skill，调度中枢自动编排
- 预标注机制（每章标记主调用 expert + 协同 expert）很聪明

### 2.2 人味体系 ⭐⭐⭐⭐⭐

**这是整个体系的核心竞争力。**

三层人味模型：
- 第一层：通用人味（犹豫/浪费/缺陷/个性/噪音）— 像某个人写的
- 第二层：平台人味（T1/T2/T3 质量分级）— 达到对应质量标准
- 第三层：作者人味（作者 DNA 注入）— 像你写的

关键洞察：
> "大部分'去AI味'教程只处理第一层。所以你用了 expert-anti-ai-taste 的 769 行规则，文字还是假——因为它只在处理表面症状，没有触及第二层和第三层。"

数据支撑：
- 卷一→卷三长句从 8.6% 降到 0.8%（AI 在"优化"过程中去掉了人类特征）
- 省略号从 1.6/章降到 0.2/章
- 嗅觉从 4% 降到 1%（美食题材核心感官消失）

滑动窗口机制：
- 不逐章强制，而是 5 章窗口达标
- 允许有些章节"干净"——干净本身就是人味
- 风格轮转：每章侧重不同的人味维度

### 2.3 质量门禁 ⭐⭐⭐⭐

- Pre-Write / Post-Write / Full Audit 三种模式
- BOOK-STATUS.md 状态追踪
- 独立验证（防自我确认偏差）
- "已修改 ≠ 已正确"原则

### 2.4 数据驱动 ⭐⭐⭐⭐⭐

- 不是拍脑袋写的规则，基于 362 本小说全本分析
- 185+ 位作者的风格 DNA 指纹
- 严肃度 1-10 全量标尺（有锚定作品和场景映射）
- 学术论文支撑（Nath et al. 2024 MPI、随机词汇注入实验等）

---

## 三、核心问题（需要解决的）

### 问题一：70 个 skill 太重，模型执行不到位 ⚠️ 最严重

**现状：**
- 70 个 SKILL.md，3.1MB 文本
- 人味协议 v4.4 有 2987 行
- 核心 skill 描述嵌在 system prompt 里，即使分层加载也很重

**影响：**
- MiMo V2 Pro 的 1M 上下文窗口理论上够，但长 prompt 的指令遵循率显著下降
- 模型会"选择性遗忘"后面的规则
- 规则越多，每条规则被执行到的概率越低

**建议：**
把 70 个 skill 按使用频率分三级：

| 级别 | skill | 加载时机 |
|------|-------|---------|
| **每次必加载**（5-8 个） | novel-expert-system、novel-volume-workflow、expert-human-flavor、expert-quality-gate、expert-writing-safety、expert-character-dna | system prompt |
| **按需加载**（15-20 个） | 题材专家（xuanhuan/xihuan/...）、平台专家（fanqie/qidian/...）、技艺专家（combat/dialogue/emotion/...） | 创作阶段动态注入 |
| **参考查阅**（其余） | expert-writing-style、expert-style-learner、expert-reader-tracker、运营类等 | 只在质检或诊断时读取 |

### 问题二：人味相关 skill 有大量重叠 ⚠️

以下 5 个 skill 之间内容重叠严重：

| Skill | 行数 | 核心内容 |
|-------|------|---------|
| expert-human-flavor | ~520 行 | 人味注入协议核心（三层模型/硬约束/缓冲句式） |
| expert-human-flavor-tiers | 未统计 | T1/T2/T3 质量分级 + 严肃度波动 |
| expert-anti-ai-taste | ~192 行 | 人味生成过程审计（五维度评估） |
| expert-writing-style | 未统计 | 大神风格参考 |
| expert-style-learner | 未统计 | 风格学习 |

**建议合并为 2 个：**
- **expert-human-flavor**（合并 human-flavor + anti-ai-taste + tiers）— 人味生成 + 审计
- **expert-style-reference**（合并 writing-style + style-learner）— 风格参考

### 问题三：最新协议没迭代进 skill ⚠️

`public-transfer` 仓库中的 `human-flavor-protocol-v4.4.md`（2987 行）比 skill 里的版本更完善：

| 特性 | skill 中的版本 | v4.4 协议 |
|------|--------------|----------|
| 严肃度 1-10 标尺 | ❌ 无 | ✅ 完整（含锚定作品和场景映射） |
| 滑动窗口详细说明 | 简略 | ✅ 详细（5 窗口 + 风格轮转 + 休眠章） |
| 退化预警量化 | ❌ 无 | ✅ 有（基于 169 章退化数据） |
| AI 鉴别指南 | ❌ 无 | ✅ 有（量化检测清单） |
| 过程模拟指令 | 简略 | ✅ 完整（"凌晨 3 点写小说"模拟） |
| 比喻替代规则 | ❌ 无 | ✅ 有（"像…的"结构限制 + 替代表） |

**建议：将 v4.4 的核心内容提炼后更新到 expert-human-flavor 的 SKILL.md 中。**

### 问题四：缺少自动化的量化质检 ⚠️ 关键短板

**当前状态：**
- `expert-quality-gate` 是基于规则的人工对照检查清单
- `public-transfer` 仓库有 `extract-sensory.py`、`batch-fingerprint.py` 等分析工具，但用于分析别人的小说

**缺失的环节：**
```
当前：写完 → 人工对照检查清单 → 修改（靠模型自觉，不可靠）
应该：写完 → 自动跑脚本检查 → 输出量化指标 → 不达标自动重写
```

**建议搭建自动质检 pipeline：**

```python
# 输入：AI 生成的章节 txt
# 输出：质检报告（哪些指标不达标）

def quality_check(chapter_text):
    results = {}
    results['long_sentence_ratio'] = check_long_sentences(chapter_text, threshold=0.03)
    results['dialogue_ratio'] = check_dialogue_ratio(chapter_text, min_ratio=0.20)
    results['prohibited_words'] = check_prohibited_words(chapter_text, cooldown=5)
    results['ellipsis_count'] = count_ellipsis(chapter_text, min_per_chapter=0.5)
    results['sensory_density'] = check_sensory_density(chapter_text, min_density=0.5)
    results['exclamation_ratio'] = check_exclamation_ratio(chapter_text, max_per_1000=5)
    results['repeated_patterns'] = check_repeated_patterns(chapter_text)
    results['ai_template_score'] = detect_ai_templates(chapter_text)
    
    return {
        'passed': all(v for v in results.values() if isinstance(v, bool)),
        'details': results,
        'failed_items': [k for k, v in results.items() if isinstance(v, bool) and not v]
    }
```

**已有可复用的工具（在 public-transfer 仓库中）：**
- `scripts/extract-corpus-stats-v2.py` — 标点统计提取
- `batch-fingerprint.py` — 风格指纹分析
- `extract-sensory.py` — 感官密度分析
- `extract-tjss-deep.py` — 深度分析

这些工具的分析逻辑可以改造成"写后质检"脚本。

---

## 四、与番茄审核被拒的关联分析

### 4.1 被拒的可能原因

番茄小说的 AI 检测机制主要看：
1. **标点指纹异常**：句号碎片率高、省略号缺失、感叹号偏高
2. **句式单一**：连续相同句式结构
3. **情感表达模式化**：直述情感（"他感到XX"）过多
4. **感官偏科**：只有视觉，缺少嗅觉/触觉/听觉
5. **对话比例异常**：过低或过高

### 4.2 当前 skill 体系的覆盖情况

| 检测维度 | skill 是否覆盖 | 是否有量化标准 | 是否有自动检测 |
|----------|--------------|--------------|--------------|
| 标点指纹 | ✅ expert-human-flavor | ✅ 有（滑动窗口） | ❌ 无自动脚本 |
| 句式多样性 | ✅ expert-writing-expert | ✅ 有（禁连续 3 句同句式） | ❌ 无自动脚本 |
| 情感表达 | ✅ expert-emotion | ✅ 有（禁直述情感） | ❌ 无自动脚本 |
| 感官密度 | ✅ expert-sensory-prose | ✅ 有（按题材标准） | ❌ 无自动脚本 |
| 对话比例 | ✅ expert-dialogue | ✅ 有（平台标准） | ❌ 无自动脚本 |
| AI 模板检测 | ✅ expert-anti-ai-taste | ✅ 有（十大特征） | ❌ 无自动脚本 |

**结论：规则都有，但全部靠模型自觉执行，没有自动化验证。这是被拒的根本原因。**

---

## 五、优先级排序的改进行动

### 🔴 P0：立刻做（解决审核被拒）

1. **搭建自动质检脚本**
   - 基于 public-transfer 的分析工具改造
   - 检测：标点指纹、句式多样性、感官密度、对话比例、AI 模板
   - 输出：通过/不通过 + 具体不达标项
   - 集成到 novel-volume-workflow 的 Post-Write 链路

2. **精简核心 skill 加载**
   - 每次必加载的 skill 压缩到 5-8 个
   - 总 prompt token 控制在 5000 以内
   - 其余 skill 改为按需读取

### 🟡 P1：一周内做（提升生成质量）

3. **更新人味协议**
   - 将 v4.4 的严肃度标尺、退化预警、AI 鉴别迭代进 expert-human-flavor
   - 合并 human-flavor + anti-ai-taste + tiers 为一个 skill

4. **实现种子写作法**
   - 用户手写每章前 500-1000 字（关键场景/对话/情绪转折）
   - AI 基于种子续写
   - 质检 agent 检查续写是否偏离种子风格

### 🟢 P2：持续优化

5. **skill 精简合并**
   - 将 70 个 skill 合并到 40-45 个
   - 消除重叠内容
   - 每个 skill 控制在 200 行以内

6. **建立反馈闭环**
   - 番茄审核结果 → 自动更新质检标准
   - 读者数据（完读率/追读率）→ 调整 skill 规则
   - 形成"发布→数据→优化→再发布"的循环

---

## 六、技术实现建议

### 6.1 自动质检脚本架构

```
novel-quality-checker/
├── checker.py              # 主入口
├── modules/
│   ├── punctuation.py      # 标点指纹检测
│   ├── sentence.py         # 句式多样性检测
│   ├── sensory.py          # 感官密度检测
│   ├── dialogue.py         # 对话比例检测
│   ├── ai_template.py      # AI 模板检测
│   ├── prohibited_words.py # 禁用词冷却检测
│   └── emotion.py          # 情感表达检测
├── config/
│   ├── thresholds.yaml     # 阈值配置（按平台/题材）
│   └── prohibited_words.yaml
└── reports/
    └── {chapter}_report.md # 质检报告
```

### 6.2 集成到工作流

```yaml
# novel-volume-workflow Phase 3 Post-Write 链路更新
Phase 3 Post-Write:
  1. expert-writing-safety    # 安全合规检查
  2. expert-anti-ai-taste     # 人味审计
  3. quality-checker --auto   # ← 新增：自动量化质检
     - 如果不通过 → 标记具体问题 → 自动重写对应段落
     - 如果通过 → 继续
  4. expert-quality-gate      # 门禁验证（最终确认）
  5. 更新 BOOK-STATUS.md
```

### 6.3 Skill 精简方案

```
保留（核心）：
  novel-expert-system           # 调度中枢
  novel-volume-workflow         # 卷级编排
  expert-human-flavor           # 人味注入（合并版）
  expert-quality-gate           # 质量门禁
  expert-writing-safety         # 安全合规
  expert-character-dna          # 角色 DNA
  expert-memory                 # 全局记忆
  expert-bookstatus             # 项目状态

按需加载（题材/平台）：
  expert-fanqie-novel           # 番茄长篇
  expert-fanqie-short           # 番茄短篇
  expert-qidian                 # 起点
  expert-xuanhuan               # 玄幻
  expert-xihuan                 # 西幻
  expert-horror                 # 恐怖
  expert-sci-fi                 # 科幻
  ...（按用户选择的题材加载）

合并/精简：
  expert-human-flavor + expert-human-flavor-tiers + expert-anti-ai-taste → expert-human-flavor
  expert-writing-style + expert-style-learner → expert-style-reference
  expert-emotion + expert-emotion-death → expert-emotion
  expert-revise-loop + expert-revision → expert-revision
```

---

## 七、总结

### 评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 理论深度 | ⭐⭐⭐⭐⭐ | 362 本数据分析、学术论文支撑、三层人味模型 |
| 架构设计 | ⭐⭐⭐⭐ | 分层清晰、调度合理、但 skill 太多 |
| 可执行性 | ⭐⭐⭐ | 规则太多模型执行不到位、缺少自动化质检 |
| 实际效果 | ⭐⭐ | 被番茄打回审核，说明还没跑通最后一公里 |

### 核心结论

**这套 skill 体系的"理论深度"是顶级的，但"工程落地"还有差距。**

理论层面：70 个 skill 覆盖了从构思到发布的全流程，人味注入协议基于 11.6 亿字数据分析，严肃度标尺有锚定作品映射——这些在行业里是领先的。

执行层面：规则太多导致模型执行不到位，缺少自动化质检导致问题无法被发现和修复。被番茄审核拒掉不是规则不够，是规则没有被严格执行。

**离"能发布"只差一步：把 2987 行的协议变成 50 行可执行的硬约束 + 一个自动质检脚本。不是规则越多越好，是关键规则被严格执行才好。**

---

_评估人：OpenClaw (MiMo V2 Pro)_
_评估日期：2026-05-07_
_数据来源：novel-skills-v1.18.1.tar.gz + public-transfer 仓库_
