# P2 / Medical Safety Enhancement Report

> 边界：本报告审计安全提示、红旗分流和输出约束，不判断医学真实性或临床疗效。

## 1. 安全模块升级

### 1.1 新增风险分流规则

原版仅覆盖 18 条红旗症状，P2 扩展为三类风险：

| 类别 | 覆盖范围 | 条数 |
|---|---|---:|
| emergency_red_flag | 急症红旗（胸痛、呼吸困难、昏迷、抽搐、出血、中风、自伤等） | 24 |
| special_population | 特殊人群（孕产妇、哺乳期、婴幼儿、老人、高龄） | 11 |
| treatment_or_procedure_intent | 实际治疗意图（怎么吃、剂量、开方、抓药、针刺、艾灸等） | 12 |

### 1.2 安全输出约束

| 输入类型 | 输出行为 |
|---|---|
| 急症红旗 | risk_level=high, blocked=true; 提示急救/及时就医 |
| 特殊人群或治疗意图 | risk_level=medium, blocked=true; 仅保留资料检索与来源追溯 |
| 未命中 | risk_level=low; 仍必须保留学习参考边界 |

### 1.3 工具层变更

- `tcm_safety_check`: 新增 risk_level/blocked/safety 字段，覆盖三类风险
- `tcm_diagnose_assist`: 检测到 risk_level in {high, medium} 时停止方剂输出
- `tcm_safety_policy`: 新增，暴露 P2 安全策略结构

### 1.4 知识文件安全边界覆盖

| kind | total | with_safety_boundary | with_contra_or_caution_text |
|---|---:|---:|---:|
| formula | 113 | 113 | 113 |
| herb | 415 | 415 | 415 |
| acupoint | 411 | 411 | - |

> P3 已将原 116 个 herb 软缺口补为“禁忌与慎用（待考）”占位边界；不凭模型补写具体禁忌。

## 2. 测试

- P2 安全测试：6 个新测试（红旗、特殊人群、治疗意图、policy 工具、diagnosis 拦截、audit 无硬失败）
- 全部 24 个测试通过

## 3. 报告文件

- report/p22_medical_safety_audit.md — 只读审计报告

## 4. 变更文件

- internal/safety_guard.py — 三类风险规则 + policy 版本
- tools/tcm_tools.py — safety check/diagnose/safety_policy 工具
- tools/p22_audit_medical_safety.py — 审计脚本
- tests/test_tcm_tools.py — 6 个新测试
- tests/test_registry_consistency.py — 2 个新测试

