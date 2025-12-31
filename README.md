# ☯ Pure Python Multi-Agent System

**2,943 lines | ZERO external dependencies | Standard library only**

A complete forensic & synthesis toolkit for iOS/Swift development, built entirely with Python's standard library.

## The Architecture

| Tool | Lines | Role | Function |
|------|-------|------|----------|
| `mas.py` | 1,011 | Core | Blackboard Multi-Agent System |
| `xcode_forensic.py` | 950 | **YIN** | Failure Detection & Risk Analysis |
| `yang_synthesizer.py` | 982 | **YANG** | Code Synthesis & Best Practices |

## ☯ Yin vs Yang

| | YIN | YANG |
|---|-----|------|
| **Purpose** | Find what's wrong | Create what's right |
| **Philosophy** | Destruction (analysis) | Construction (synthesis) |
| **Agents** | AxiomInverter, PatternRecognizer, PRA | CodeGenerator, PatternTransformer, AxiomEnforcer |
| **Output** | Risk scores, violations | Generated code, compliance scores |

## Quick Start

```bash
# Clone
git clone https://github.com/lordwilsonDev/pure-python-mas.git
cd pure-python-mas

# Run demos
python3 mas.py                    # Multi-Agent System demo
python3 xcode_forensic.py         # YIN - Failure detection demo
python3 yang_synthesizer.py       # YANG - Code synthesis demo
```

## YIN: Failure Detection

Detects iOS/Swift failure patterns:
- ✅ Init Side-Effect Leaks (memory explosion under hot reload)
- ✅ Symbol Mangling Errors (dlsym crashes)
- ✅ Cross-Domain Hallucinations (.NET/Go code in Swift)
- ✅ Missing -interposable Flags (silent hot-reload failure)
- ✅ Strong Self Closures (retain cycles)
- ✅ TCA Giant Test Antipattern

```bash
# Analyze a Swift file
python3 xcode_forensic.py MyView.swift

# Run demo with sample artifacts
python3 xcode_forensic.py
```

### Sample Output
```
>>> ANALYZING: CB_001 - SwiftUI Init Leak
[16:33:09] AxiomInverter      | VIOLATIONS      | Found 1 logical flaws
[16:33:09] PatternRecognizer  | MATCH_FOUND     | INIT_LEAK (1x)
[16:33:09] PRA_Agent          | VERDICT         | P(Failure) = 0.56 [MODERATE]

  Risk: [████████████████░░░░░░░░░░░░░░] 56%
```

## YANG: Code Synthesis

Generates correct Swift/SwiftUI code following architectural axioms:

```bash
# Generate a SwiftUI view
python3 yang_synthesizer.py view HomeView

# Generate a service with DI protocol
python3 yang_synthesizer.py service DataService

# Heal faulty code
python3 yang_synthesizer.py heal BrokenCode.swift

# Generate a complete project structure
python3 yang_synthesizer.py project MyApp
```

### Sample Output
```
☯ SYNTHESIZING VIEW: HomeView
[17:08:13] CodeGenerator  | SYNTHESIZED | Complete view: HomeView
[17:08:13] AxiomEnforcer  | ENFORCING   | Checking axiom compliance...

📝 Generated View (Compliance: 100%)
```

## Architectural Axioms

The system enforces these axioms:

| Axiom | Rule |
|-------|------|
| **INIT_PURITY** | Initialization must be side-effect free and O(1) |
| **WEAK_CAPTURE** | Closures must capture self weakly |
| **OBSERVABLE_STATE** | State changes must trigger observation notifications |
| **MAIN_ACTOR** | UI updates must occur on MainActor |
| **STRUCTURED_CONCURRENCY** | Async work must use structured concurrency |
| **DEPENDENCY_INJECTION** | Dependencies must be injected, not instantiated |
| **ERROR_HANDLING** | Errors must be handled explicitly |
| **INTERPOSABLE_CONFIG** | Debug builds must include -interposable flag |

## Why Zero Dependencies?

```python
# That's it. No pip install. Runs anywhere.
import sqlite3   # In-memory blackboard
import threading # Agent concurrency  
import re        # Pattern matching
import math      # Bayesian inference
import json      # Data serialization
```

Every feature is built using Python's standard library. No external packages. No `pip install`. Just Python.

## License

MIT

---

*Gemini researched. Claude implemented. Zero dependencies. The balance is complete.* ☯
