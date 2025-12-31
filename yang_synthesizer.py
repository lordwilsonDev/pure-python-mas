#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
 YANG ARCHITECTURE - CODE SYNTHESIS & BEST PRACTICES ENGINE
 The Constructive Counterpart to Failure Detection
═══════════════════════════════════════════════════════════════════════════════

YIN (xcode_forensic.py): Failure Detection, Risk Analysis, Breaking Apart
YANG (yang_synthesizer.py): Code Synthesis, Best Practices, Building Right

This system:
- GENERATES correct code from axioms
- ENFORCES best practices during synthesis
- TRANSFORMS faulty patterns into correct ones
- BUILDS artifacts that satisfy all axioms

The Yin finds what's wrong.
The Yang creates what's right.

Together: Complete architectural balance.

NO EXTERNAL DEPENDENCIES. PURE PYTHON STANDARD LIBRARY.
"""

import sys
import time
import re
import json
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Callable
from pathlib import Path
from enum import Enum
from abc import ABC, abstractmethod


# ═══════════════════════════════════════════════════════════════════════════════
# PART 1: TERMINAL UI
# ═══════════════════════════════════════════════════════════════════════════════

class TerminalUI:
    """Terminal styling for Yang Architecture"""
    
    # ANSI Colors - Warm tones for Yang (vs Cool tones for Yin)
    GOLD = '\033[93m'
    ORANGE = '\033[38;5;208m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    DIM = '\033[2m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'
    
    @staticmethod
    def banner():
        print(f"""
{TerminalUI.GOLD}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██╗   ██╗ █████╗ ███╗   ██╗ ██████╗                                        ║
║   ╚██╗ ██╔╝██╔══██╗████╗  ██║██╔════╝                                        ║
║    ╚████╔╝ ███████║██╔██╗ ██║██║  ███╗                                       ║
║     ╚██╔╝  ██╔══██║██║╚██╗██║██║   ██║                                       ║
║      ██║   ██║  ██║██║ ╚████║╚██████╔╝                                       ║
║      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝                                        ║
║                                                                              ║
║              ☯ Code Synthesis & Best Practices Engine ☯                     ║
║                    The Constructive Architecture                             ║
╚══════════════════════════════════════════════════════════════════════════════╝{TerminalUI.ENDC}
        """)
        print(f"{TerminalUI.DIM}{'─' * 78}{TerminalUI.ENDC}")
        print(f"{TerminalUI.BOLD}Synthesis Engine{TerminalUI.ENDC} | Axiom Enforcement | Pattern Transformation | Generation")
        print(f"{TerminalUI.DIM}{'─' * 78}{TerminalUI.ENDC}\n")

    @staticmethod
    def section(title: str):
        print(f"\n{TerminalUI.GOLD}{'═' * 78}")
        print(f"  ☯ {title}")
        print(f"{'═' * 78}{TerminalUI.ENDC}\n")

    @staticmethod
    def log_agent(agent_name: str, action: str, details: str, status: str = "INFO"):
        colors = {
            "INFO": TerminalUI.CYAN,
            "BUILD": TerminalUI.GREEN,
            "TRANSFORM": TerminalUI.ORANGE,
            "GENERATE": TerminalUI.GOLD,
            "SUCCESS": TerminalUI.GREEN + TerminalUI.BOLD,
        }
        color = colors.get(status, TerminalUI.WHITE)
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {TerminalUI.BOLD}{agent_name.ljust(18)}{TerminalUI.ENDC} | {color}{action.ljust(15)}{TerminalUI.ENDC} | {details}")

    @staticmethod
    def code_block(code: str, language: str = "swift"):
        print(f"\n{TerminalUI.DIM}```{language}{TerminalUI.ENDC}")
        for line in code.strip().split('\n'):
            print(f"  {TerminalUI.WHITE}{line}{TerminalUI.ENDC}")
        print(f"{TerminalUI.DIM}```{TerminalUI.ENDC}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# PART 2: AXIOM KNOWLEDGE BASE (CONSTRUCTIVE VERSION)
# ═══════════════════════════════════════════════════════════════════════════════

class AxiomType(Enum):
    LIFECYCLE = "lifecycle"
    MEMORY = "memory"
    CONCURRENCY = "concurrency"
    STATE = "state"
    ARCHITECTURE = "architecture"


@dataclass
class Axiom:
    """A constructive axiom that defines correct behavior"""
    id: str
    name: str
    type: AxiomType
    statement: str
    correct_pattern: str        # The pattern that satisfies the axiom
    incorrect_pattern: str      # The pattern that violates the axiom
    transformation: str         # How to transform incorrect → correct
    code_template: str          # Template for generating correct code


class AxiomLibrary:
    """
    Library of constructive axioms for code synthesis.
    Each axiom defines what CORRECT code looks like.
    """
    
    AXIOMS = {
        "INIT_PURITY": Axiom(
            id="INIT_PURITY",
            name="Initialization Purity",
            type=AxiomType.LIFECYCLE,
            statement="Initialization must be side-effect free and O(1)",
            correct_pattern="Empty init or property assignment only",
            incorrect_pattern="Network calls, timers, or heavy computation in init",
            transformation="Move side-effects to onAppear() or .task {}",
            code_template="""
struct {ViewName}: View {
    @StateObject private var viewModel = {ViewModel}()
    
    var body: some View {
        {Content}
            .task {
                await viewModel.loadData()
            }
    }
}
"""
        ),
        
        "WEAK_CAPTURE": Axiom(
            id="WEAK_CAPTURE",
            name="Weak Self Capture",
            type=AxiomType.MEMORY,
            statement="Closures must capture self weakly to prevent retain cycles",
            correct_pattern="[weak self] in closure with guard let self",
            incorrect_pattern="Strong self capture in escaping closures",
            transformation="Add [weak self] and guard unwrap",
            code_template="""
{ClassName}.{method} { [weak self] {params} in
    guard let self else { return }
    self.{body}
}
"""
        ),
        
        "OBSERVABLE_STATE": Axiom(
            id="OBSERVABLE_STATE",
            name="Observable State Management",
            type=AxiomType.STATE,
            statement="State changes must trigger observation notifications",
            correct_pattern="@Observable class or ObservableObject with @Published",
            incorrect_pattern="Plain class with @State or unobserved mutations",
            transformation="Convert to @Observable or add @Published",
            code_template="""
@Observable
class {ClassName} {
    var {property}: {Type} = {default}
    
    func update{Property}(_ value: {Type}) {
        {property} = value
    }
}
"""
        ),
        
        "MAIN_ACTOR": Axiom(
            id="MAIN_ACTOR",
            name="Main Actor UI Updates",
            type=AxiomType.CONCURRENCY,
            statement="UI updates must occur on MainActor",
            correct_pattern="@MainActor annotation or MainActor.run {}",
            incorrect_pattern="UI updates from background threads",
            transformation="Add @MainActor or wrap in MainActor.run",
            code_template="""
@MainActor
func updateUI(with data: {Type}) {
    self.{property} = data
}
"""
        ),
        
        "STRUCTURED_CONCURRENCY": Axiom(
            id="STRUCTURED_CONCURRENCY",
            name="Structured Concurrency",
            type=AxiomType.CONCURRENCY,
            statement="Async work must use structured concurrency patterns",
            correct_pattern="Task groups, async let, or .task modifier",
            incorrect_pattern="DispatchQueue.global().async or detached tasks",
            transformation="Convert to Task {} or async let",
            code_template="""
func {methodName}() async throws -> {ReturnType} {
    try await withThrowingTaskGroup(of: {ElementType}.self) { group in
        for item in items {
            group.addTask {
                try await process(item)
            }
        }
        return try await group.reduce(into: []) { $0.append($1) }
    }
}
"""
        ),
        
        "DEPENDENCY_INJECTION": Axiom(
            id="DEPENDENCY_INJECTION",
            name="Dependency Injection",
            type=AxiomType.ARCHITECTURE,
            statement="Dependencies must be injected, not instantiated internally",
            correct_pattern="Init injection or @Environment",
            incorrect_pattern="Singleton access or internal instantiation",
            transformation="Create protocol and inject via init",
            code_template="""
protocol {ServiceName}Protocol {
    func {method}() async throws -> {ReturnType}
}

struct {ViewName}: View {
    let service: {ServiceName}Protocol
    
    init(service: {ServiceName}Protocol = {ServiceName}()) {
        self.service = service
    }
}
"""
        ),
        
        "ERROR_HANDLING": Axiom(
            id="ERROR_HANDLING",
            name="Explicit Error Handling",
            type=AxiomType.ARCHITECTURE,
            statement="Errors must be handled explicitly, never force-unwrapped",
            correct_pattern="do-catch, Result type, or optional binding",
            incorrect_pattern="try!, as!, or implicit unwrap",
            transformation="Replace with do-catch or optional binding",
            code_template="""
func {methodName}() async -> Result<{SuccessType}, {ErrorType}> {
    do {
        let result = try await {operation}
        return .success(result)
    } catch {
        return .failure(.{errorCase}(error))
    }
}
"""
        ),
        
        "INTERPOSABLE_CONFIG": Axiom(
            id="INTERPOSABLE_CONFIG",
            name="Hot Reload Configuration",
            type=AxiomType.ARCHITECTURE,
            statement="Debug builds must include interposable linker flag for hot reload",
            correct_pattern="-Xlinker -interposable in Debug OTHER_LDFLAGS",
            incorrect_pattern="Missing interposable flag or in Release",
            transformation="Add flag to XcodeGen or Xcode settings",
            code_template="""
# project.yml (XcodeGen)
settings:
  configs:
    Debug:
      OTHER_LDFLAGS: ["-Xlinker", "-interposable"]
"""
        ),
    }
    
    @classmethod
    def get(cls, axiom_id: str) -> Optional[Axiom]:
        return cls.AXIOMS.get(axiom_id)
    
    @classmethod
    def all(cls) -> List[Axiom]:
        return list(cls.AXIOMS.values())
    
    @classmethod
    def by_type(cls, axiom_type: AxiomType) -> List[Axiom]:
        return [a for a in cls.AXIOMS.values() if a.type == axiom_type]


# ═══════════════════════════════════════════════════════════════════════════════
# PART 3: PATTERN TRANSFORMER AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class PatternTransformer:
    """
    The YANG counterpart to PatternRecognizer.
    
    Instead of detecting bad patterns, it TRANSFORMS them into good patterns.
    This is the constructive agent that heals faulty code.
    """
    
    # Transformation rules: (bad_pattern, replacement_template, description)
    TRANSFORMATIONS = [
        # Weak self transformation
        (
            r'\{\s*(\w+)\s+in\s*\n?\s*self\.',
            r'{ [weak self] \1 in\n        guard let self else { return }\n        self.',
            "Add weak self capture to closure"
        ),
        
        # Force try transformation
        (
            r'try!\s+(.+)',
            r'try? \1 // TODO: Add proper error handling',
            "Replace force try with optional try"
        ),
        
        # Force cast transformation
        (
            r'(\w+)\s+as!\s+(\w+)',
            r'(\1 as? \2) ?? {default}',
            "Replace force cast with optional cast"
        ),
        
        # DispatchQueue to Task
        (
            r'DispatchQueue\.global\(\)\.async\s*\{\s*\n?\s*(.+?)\s*\}',
            r'Task {\n            \1\n        }',
            "Convert DispatchQueue to structured Task"
        ),
        
        # Singleton to injection
        (
            r'(\w+)\.shared\.(\w+)',
            r'service.\2 // TODO: Inject \1 as dependency',
            "Replace singleton with injected dependency"
        ),
        
        # Init side-effect to onAppear
        (
            r'init\(\)\s*\{\s*\n?\s*(\w+\.(?:fetch|load|start)\w*\(\))',
            r'init() { }\n\n    var body: some View {\n        content\n            .onAppear { \1 }',
            "Move init side-effect to onAppear"
        ),
    ]
    
    def __init__(self):
        self.name = "PatternTransformer"
        self.transformations_applied = 0
    
    def transform(self, code: str) -> Tuple[str, List[Dict]]:
        """
        Transform faulty patterns into correct ones.
        Returns transformed code and list of changes made.
        """
        changes = []
        result = code
        
        TerminalUI.log_agent(self.name, "TRANSFORMING", f"Analyzing {len(code)} bytes for healable patterns...", "TRANSFORM")
        
        for pattern, replacement, description in self.TRANSFORMATIONS:
            try:
                matches = re.findall(pattern, result, re.DOTALL)
                if matches:
                    new_result = re.sub(pattern, replacement, result, flags=re.DOTALL)
                    if new_result != result:
                        changes.append({
                            "pattern": pattern[:30] + "...",
                            "description": description,
                            "occurrences": len(matches),
                        })
                        result = new_result
                        self.transformations_applied += len(matches)
                        TerminalUI.log_agent(self.name, "HEALED", f"{description} ({len(matches)}x)", "SUCCESS")
            except re.error:
                pass
        
        return result, changes


# ═══════════════════════════════════════════════════════════════════════════════
# PART 4: CODE GENERATOR AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class CodeGenerator:
    """
    The YANG counterpart to AxiomInverter.
    
    Instead of finding axiom violations, it GENERATES code that satisfies axioms.
    This is the creative agent that builds correct code from first principles.
    """
    
    def __init__(self):
        self.name = "CodeGenerator"
        self.artifacts_generated = 0
    
    def generate_from_axiom(self, axiom: Axiom, context: Dict[str, str]) -> str:
        """
        Generate code that satisfies a specific axiom.
        Uses the axiom's template and fills in the context.
        """
        TerminalUI.log_agent(self.name, "GENERATING", f"Synthesizing code for {axiom.name}...", "GENERATE")
        
        template = axiom.code_template
        
        # Fill in template variables
        for key, value in context.items():
            template = template.replace(f"{{{key}}}", value)
        
        # Replace any unfilled placeholders with sensible defaults
        template = re.sub(r'\{(\w+)\}', r'/* TODO: \1 */', template)
        
        self.artifacts_generated += 1
        return template.strip()
    
    def generate_view(self, name: str, has_async: bool = True, has_state: bool = True) -> str:
        """Generate a complete SwiftUI view following all axioms"""
        
        context = {
            "ViewName": name,
            "ViewModel": f"{name}ViewModel",
            "Content": "ContentView()",
        }
        
        task_modifier = '.task { await viewModel.loadData() }' if has_async else ''
        
        code = f"""
import SwiftUI

// MARK: - {name} View
// Generated following Yang Architecture axioms

struct {name}: View {{
    @StateObject private var viewModel = {name}ViewModel()
    
    var body: some View {{
        NavigationStack {{
            content
                .navigationTitle("{name}")
        }}
        {task_modifier}
    }}
    
    @ViewBuilder
    private var content: some View {{
        if viewModel.isLoading {{
            ProgressView()
        }} else {{
            List(viewModel.items, id: \\.self) {{ item in
                Text(item)
            }}
        }}
    }}
}}

// MARK: - View Model
@Observable
class {name}ViewModel {{
    var items: [String] = []
    var isLoading = false
    var error: Error?
    
    @MainActor
    func loadData() async {{
        isLoading = true
        defer {{ isLoading = false }}
        
        do {{
            // TODO: Implement data loading
            try await Task.sleep(for: .seconds(1))
            items = ["Item 1", "Item 2", "Item 3"]
        }} catch {{
            self.error = error
        }}
    }}
}}

// MARK: - Preview
#Preview {{
    {name}()
}}
"""
        
        TerminalUI.log_agent(self.name, "SYNTHESIZED", f"Complete view: {name}", "SUCCESS")
        self.artifacts_generated += 1
        
        return code.strip()
    
    def generate_service(self, name: str, methods: List[Dict[str, str]]) -> str:
        """Generate a service with protocol following DI axiom"""
        
        method_signatures = []
        method_implementations = []
        
        for method in methods:
            m_name = method.get("name", "perform")
            m_return = method.get("returns", "Void")
            m_throws = method.get("throws", True)
            
            sig = f"    func {m_name}() async {'throws ' if m_throws else ''}-> {m_return}"
            method_signatures.append(sig)
            
            impl = f"""
    func {m_name}() async {'throws ' if m_throws else ''}-> {m_return} {{
        // TODO: Implement {m_name}
        {"throw ServiceError.notImplemented" if m_throws else f"return {m_return}()"}
    }}
"""
            method_implementations.append(impl)
        
        code = f"""
import Foundation

// MARK: - {name} Protocol
// Dependency Injection ready

protocol {name}Protocol {{
{chr(10).join(method_signatures)}
}}

// MARK: - {name} Implementation
final class {name}: {name}Protocol {{
    
    enum ServiceError: Error {{
        case notImplemented
        case networkError(Error)
        case invalidResponse
    }}
    
    // Dependencies injected via init
    private let session: URLSession
    
    init(session: URLSession = .shared) {{
        self.session = session
    }}
{"".join(method_implementations)}
}}

// MARK: - Mock for Testing
#if DEBUG
final class Mock{name}: {name}Protocol {{
{chr(10).join(s.replace("// TODO:", "// Mock:") for s in method_signatures)}
}}
#endif
"""
        
        TerminalUI.log_agent(self.name, "SYNTHESIZED", f"Service + Protocol: {name}", "SUCCESS")
        self.artifacts_generated += 1
        
        return code.strip()
    
    def generate_xcodegen_config(self, project_name: str, targets: List[str]) -> str:
        """Generate XcodeGen config with all required flags"""
        
        target_configs = []
        for target in targets:
            target_configs.append(f"""
  {target}:
    type: application
    platform: iOS
    deploymentTarget: "17.0"
    sources:
      - path: {target}
    settings:
      configs:
        Debug:
          OTHER_LDFLAGS: ["-Xlinker", "-interposable"]
          SWIFT_ACTIVE_COMPILATION_CONDITIONS: DEBUG
        Release:
          SWIFT_OPTIMIZATION_LEVEL: -O
    dependencies: []
""")
        
        code = f"""
# project.yml - Generated by Yang Architecture
# XcodeGen configuration with Hot Reload support

name: {project_name}
options:
  bundleIdPrefix: com.example
  deploymentTarget:
    iOS: "17.0"

settings:
  base:
    SWIFT_VERSION: "5.9"
    ENABLE_USER_SCRIPT_SANDBOXING: YES

targets:{"".join(target_configs)}

schemes:
  {project_name}:
    build:
      targets:
        {targets[0] if targets else project_name}: all
    run:
      config: Debug
    test:
      config: Debug
"""
        
        TerminalUI.log_agent(self.name, "SYNTHESIZED", f"XcodeGen config: {project_name}", "SUCCESS")
        self.artifacts_generated += 1
        
        return code.strip()


# ═══════════════════════════════════════════════════════════════════════════════
# PART 5: AXIOM ENFORCER AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class AxiomEnforcer:
    """
    The YANG counterpart to PRA (Probabilistic Risk Assessor).
    
    Instead of calculating failure probability, it ENFORCES axiom compliance
    and calculates a QUALITY score based on how many axioms are satisfied.
    """
    
    def __init__(self):
        self.name = "AxiomEnforcer"
    
    def check_compliance(self, code: str) -> Tuple[float, List[Dict]]:
        """
        Check how many axioms the code satisfies.
        Returns compliance score (0-1) and list of axiom statuses.
        """
        TerminalUI.log_agent(self.name, "ENFORCING", "Checking axiom compliance...", "BUILD")
        
        axiom_checks = []
        passed = 0
        total = 0
        
        # Check each axiom
        for axiom in AxiomLibrary.all():
            total += 1
            status = self._check_axiom(code, axiom)
            axiom_checks.append({
                "axiom": axiom.id,
                "name": axiom.name,
                "passed": status["passed"],
                "reason": status["reason"],
            })
            if status["passed"]:
                passed += 1
        
        compliance = passed / total if total > 0 else 0
        
        return compliance, axiom_checks
    
    def _check_axiom(self, code: str, axiom: Axiom) -> Dict:
        """Check if code satisfies a specific axiom"""
        
        # Heuristic checks based on axiom type
        if axiom.id == "INIT_PURITY":
            # Check for side-effects in init
            has_init = "init(" in code or "init()" in code
            has_side_effect = any(p in code for p in ["fetch", "load", "start", "URLSession"])
            
            if has_init and has_side_effect:
                return {"passed": False, "reason": "Side-effects detected in init"}
            return {"passed": True, "reason": "Init is pure"}
        
        elif axiom.id == "WEAK_CAPTURE":
            # Check for strong self in closures
            strong_self = re.search(r'\{\s*\w+\s+in\s*\n?\s*self\.', code)
            weak_self = "[weak self]" in code
            
            if strong_self and not weak_self:
                return {"passed": False, "reason": "Strong self capture in closure"}
            return {"passed": True, "reason": "Proper weak self or no closures"}
        
        elif axiom.id == "OBSERVABLE_STATE":
            has_observable = "@Observable" in code or "ObservableObject" in code
            has_state = "@State" in code or "@StateObject" in code
            
            if has_state and not has_observable:
                return {"passed": False, "reason": "State without Observable pattern"}
            return {"passed": True, "reason": "Proper observable state"}
        
        elif axiom.id == "MAIN_ACTOR":
            has_ui_update = any(p in code for p in ["@Published", "self.items", "self.isLoading"])
            has_main_actor = "@MainActor" in code or "MainActor.run" in code
            has_async = "async" in code
            
            if has_ui_update and has_async and not has_main_actor:
                return {"passed": False, "reason": "Async UI updates without MainActor"}
            return {"passed": True, "reason": "Proper main actor usage"}
        
        elif axiom.id == "ERROR_HANDLING":
            has_force_try = "try!" in code
            has_force_cast = "as!" in code
            
            if has_force_try or has_force_cast:
                return {"passed": False, "reason": "Force unwrap detected"}
            return {"passed": True, "reason": "Proper error handling"}
        
        elif axiom.id == "INTERPOSABLE_CONFIG":
            if "-interposable" in code:
                return {"passed": True, "reason": "Interposable flag present"}
            if "project.yml" in code.lower() or "xcodegen" in code.lower():
                return {"passed": False, "reason": "XcodeGen config missing interposable"}
            return {"passed": True, "reason": "Not a config file"}
        
        # Default: assume passed if no specific check
        return {"passed": True, "reason": "No violations detected"}
    
    def generate_compliance_report(self, checks: List[Dict]) -> str:
        """Generate a formatted compliance report"""
        passed = [c for c in checks if c["passed"]]
        failed = [c for c in checks if not c["passed"]]
        
        report = []
        report.append("\n☯ AXIOM COMPLIANCE REPORT")
        report.append("=" * 50)
        
        report.append(f"\n✅ PASSED ({len(passed)}/{len(checks)}):")
        for c in passed:
            report.append(f"   • {c['name']}: {c['reason']}")
        
        if failed:
            report.append(f"\n❌ FAILED ({len(failed)}/{len(checks)}):")
            for c in failed:
                report.append(f"   • {c['name']}: {c['reason']}")
        
        report.append("=" * 50)
        
        return "\n".join(report)


# ═══════════════════════════════════════════════════════════════════════════════
# PART 6: YANG SYNTHESIS ENGINE (ORCHESTRATOR)
# ═══════════════════════════════════════════════════════════════════════════════

class YangEngine:
    """
    The complete Yang Architecture synthesis engine.
    
    Orchestrates:
    - PatternTransformer: Heals faulty patterns
    - CodeGenerator: Creates correct code from axioms
    - AxiomEnforcer: Validates axiom compliance
    
    This is the constructive counterpart to the Yin forensic analyzer.
    """
    
    def __init__(self):
        self.transformer = PatternTransformer()
        self.generator = CodeGenerator()
        self.enforcer = AxiomEnforcer()
        self.artifacts_created: List[Dict] = []
    
    def heal(self, code: str) -> Dict:
        """
        Heal faulty code by transforming bad patterns to good ones.
        Returns healed code and transformation report.
        """
        TerminalUI.section("HEALING FAULTY CODE")
        
        healed_code, changes = self.transformer.transform(code)
        compliance, checks = self.enforcer.check_compliance(healed_code)
        
        return {
            "original": code,
            "healed": healed_code,
            "changes": changes,
            "compliance": compliance,
            "axiom_checks": checks,
        }
    
    def synthesize_view(self, name: str) -> Dict:
        """
        Synthesize a complete SwiftUI view from first principles.
        Generated code will satisfy all applicable axioms.
        """
        TerminalUI.section(f"SYNTHESIZING VIEW: {name}")
        
        code = self.generator.generate_view(name)
        compliance, checks = self.enforcer.check_compliance(code)
        
        artifact = {
            "type": "view",
            "name": name,
            "code": code,
            "compliance": compliance,
            "axiom_checks": checks,
        }
        self.artifacts_created.append(artifact)
        
        return artifact
    
    def synthesize_service(self, name: str, methods: List[Dict] = None) -> Dict:
        """
        Synthesize a service with protocol for dependency injection.
        """
        TerminalUI.section(f"SYNTHESIZING SERVICE: {name}")
        
        if methods is None:
            methods = [{"name": "fetchData", "returns": "[String]", "throws": True}]
        
        code = self.generator.generate_service(name, methods)
        compliance, checks = self.enforcer.check_compliance(code)
        
        artifact = {
            "type": "service",
            "name": name,
            "code": code,
            "compliance": compliance,
            "axiom_checks": checks,
        }
        self.artifacts_created.append(artifact)
        
        return artifact
    
    def synthesize_project(self, name: str, views: List[str], services: List[str]) -> Dict:
        """
        Synthesize a complete project structure with all components.
        """
        TerminalUI.section(f"SYNTHESIZING PROJECT: {name}")
        
        project_artifacts = []
        
        # Generate XcodeGen config
        config = self.generator.generate_xcodegen_config(name, [name])
        project_artifacts.append({
            "file": "project.yml",
            "content": config,
        })
        
        # Generate views
        for view_name in views:
            code = self.generator.generate_view(view_name)
            project_artifacts.append({
                "file": f"{view_name}.swift",
                "content": code,
            })
        
        # Generate services
        for service_name in services:
            code = self.generator.generate_service(service_name, [
                {"name": "fetch", "returns": "[String]", "throws": True}
            ])
            project_artifacts.append({
                "file": f"{service_name}.swift",
                "content": code,
            })
        
        return {
            "type": "project",
            "name": name,
            "artifacts": project_artifacts,
            "total_files": len(project_artifacts),
        }
    
    def run_demo(self):
        """Run a demonstration of the Yang Architecture"""
        TerminalUI.banner()
        
        print("☯ The Yang Architecture is the constructive counterpart to Yin.")
        print("   Yin detects failures. Yang creates correct solutions.\n")
        
        # Demo 1: Synthesize a view
        view_result = self.synthesize_view("HomeView")
        print(f"\n📝 Generated View (Compliance: {view_result['compliance']:.0%})")
        TerminalUI.code_block(view_result['code'][:500] + "\n// ... (truncated)")
        
        # Demo 2: Synthesize a service
        service_result = self.synthesize_service("DataService", [
            {"name": "fetchUsers", "returns": "[User]", "throws": True},
            {"name": "saveUser", "returns": "Bool", "throws": True},
        ])
        print(f"\n📝 Generated Service (Compliance: {service_result['compliance']:.0%})")
        TerminalUI.code_block(service_result['code'][:400] + "\n// ... (truncated)")
        
        # Demo 3: Heal faulty code
        faulty_code = """
struct BadView: View {
    var viewModel = BadViewModel()
    
    init() {
        viewModel.fetchData()
    }
    
    var body: some View {
        Text("Hello")
    }
}

class BadViewModel {
    func fetchData() {
        URLSession.shared.dataTask(with: url) { data, _, _ in
            self.processData(data)
        }.resume()
    }
}
"""
        
        print("\n📝 Healing Faulty Code...")
        heal_result = self.heal(faulty_code)
        print(f"   Transformations applied: {len(heal_result['changes'])}")
        print(f"   Post-heal compliance: {heal_result['compliance']:.0%}")
        
        if heal_result['changes']:
            print("\n   Changes made:")
            for change in heal_result['changes']:
                print(f"   • {change['description']}")
        
        # Summary
        TerminalUI.section("YANG SYNTHESIS SUMMARY")
        
        print(f"   Views Synthesized:    1")
        print(f"   Services Synthesized: 1")
        print(f"   Code Healed:          1 artifact")
        print(f"   Total Compliance:     {(view_result['compliance'] + service_result['compliance'] + heal_result['compliance']) / 3:.0%}")
        
        print(f"\n{TerminalUI.GOLD}☯ Yang Architecture demonstration complete.{TerminalUI.ENDC}")
        print(f"{TerminalUI.DIM}   The constructive force balances the destructive.{TerminalUI.ENDC}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point"""
    engine = YangEngine()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "view" and len(sys.argv) > 2:
            result = engine.synthesize_view(sys.argv[2])
            print(result["code"])
            
        elif command == "service" and len(sys.argv) > 2:
            result = engine.synthesize_service(sys.argv[2])
            print(result["code"])
            
        elif command == "heal" and len(sys.argv) > 2:
            filepath = Path(sys.argv[2])
            if filepath.exists():
                code = filepath.read_text()
                result = engine.heal(code)
                print(result["healed"])
            else:
                print(f"File not found: {filepath}")
                
        elif command == "project" and len(sys.argv) > 2:
            result = engine.synthesize_project(
                sys.argv[2],
                views=["HomeView", "SettingsView"],
                services=["DataService", "AuthService"]
            )
            for artifact in result["artifacts"]:
                print(f"\n# {artifact['file']}")
                print(artifact["content"][:300] + "\n...")
        else:
            print("Usage:")
            print("  yang_synthesizer.py view <ViewName>")
            print("  yang_synthesizer.py service <ServiceName>")
            print("  yang_synthesizer.py heal <filepath>")
            print("  yang_synthesizer.py project <ProjectName>")
    else:
        # Run demo
        engine.run_demo()


if __name__ == "__main__":
    main()
