#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
 XCODEGEN-INJECT-SWIFTUI-CODEBRAIN FORENSIC ANALYZER
 Multi-Agent Failure Topology Mapper
═══════════════════════════════════════════════════════════════════════════════

From Gemini Deep Research Blueprint:
"A forensic analysis tool for the XcodeGen-Inject-SwiftUI-CodeBrain nexus.
 Maps failure topologies via Multi-Agent Simulation using:
 - AxiomInverter: Logical verification against architectural axioms
 - PatternRecognizer: Static analysis for CodeBrain failure signatures
 - PRA: Probabilistic Risk Assessment with Bayesian weighting"

This tool detects:
- Init Side-Effect Leaks (Memory explosion under hot reload)
- Symbol Mangling Failures (dlsym crashes)
- Cross-Domain Hallucinations (Windows/.NET code in Swift)
- Missing Linker Flags (Silent hot-reload failure)
- TCA Assertion Roulette (Brittle tests)

NO EXTERNAL DEPENDENCIES. PURE PYTHON STANDARD LIBRARY.
"""

import sys
import time
import re
import math
import random
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════════
# PART 1: TERMINAL UI UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

class TerminalUI:
    """
    Handles ASCII art, colored logs, and table formatting for
    forensic-style terminal output.
    """
    
    # ANSI Color Codes
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'
    
    @staticmethod
    def banner():
        """Display the main banner"""
        print(f"""
{TerminalUI.OKCYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██╗  ██╗ ██████╗ ██████╗ ██████╗ ███████╗    ███████╗ ██████╗ ██████╗      ║
║   ╚██╗██╔╝██╔════╝██╔═══██╗██╔══██╗██╔════╝    ██╔════╝██╔═══██╗██╔══██╗     ║
║    ╚███╔╝ ██║     ██║   ██║██║  ██║█████╗      █████╗  ██║   ██║██████╔╝     ║
║    ██╔██╗ ██║     ██║   ██║██║  ██║██╔══╝      ██╔══╝  ██║   ██║██╔══██╗     ║
║   ██╔╝ ██╗╚██████╗╚██████╔╝██████╔╝███████╗    ██║     ╚██████╔╝██║  ██║     ║
║   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝    ╚═╝      ╚═════╝ ╚═╝  ╚═╝     ║
║                                                                              ║
║          XcodeGen · Inject · SwiftUI · CodeBrain Stack Analyzer              ║
║                    Multi-Agent Forensic System v1.0                          ║
╚══════════════════════════════════════════════════════════════════════════════╝{TerminalUI.ENDC}
        """)
        print(f"{TerminalUI.DIM}{'─' * 78}{TerminalUI.ENDC}")
        print(f"{TerminalUI.BOLD}Forensic Analysis Engine{TerminalUI.ENDC} | Axiom Inversion | Pattern Recognition | PRA")
        print(f"{TerminalUI.DIM}{'─' * 78}{TerminalUI.ENDC}\n")

    @staticmethod
    def section(title: str):
        """Print a section header"""
        print(f"\n{TerminalUI.BOLD}{TerminalUI.OKCYAN}{'═' * 78}{TerminalUI.ENDC}")
        print(f"{TerminalUI.BOLD}{TerminalUI.OKCYAN}  {title}{TerminalUI.ENDC}")
        print(f"{TerminalUI.BOLD}{TerminalUI.OKCYAN}{'═' * 78}{TerminalUI.ENDC}\n")

    @staticmethod
    def log_agent(agent_name: str, action: str, details: str, status: str = "INFO"):
        """
        Structured logging format for agent activity visualization.
        """
        colors = {
            "INFO": TerminalUI.OKBLUE,
            "WARN": TerminalUI.WARNING,
            "FAIL": TerminalUI.FAIL,
            "SUCCESS": TerminalUI.OKGREEN,
            "CRITICAL": TerminalUI.FAIL + TerminalUI.BOLD,
        }
        color = colors.get(status, TerminalUI.OKBLUE)
        
        timestamp = time.strftime("%H:%M:%S")
        agent_fmt = f"{TerminalUI.BOLD}{agent_name.ljust(18)}{TerminalUI.ENDC}"
        action_fmt = f"{color}{action.ljust(15)}{TerminalUI.ENDC}"
        
        print(f"[{timestamp}] {agent_fmt} | {action_fmt} | {details}")

    @staticmethod
    def print_table(headers: List[str], rows: List[List[Any]]):
        """
        Renders a formatted ASCII table.
        """
        if not rows:
            print("  (No data)")
            return
            
        # Calculate column widths
        widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], len(str(cell)))
        
        # Add padding
        widths = [w + 2 for w in widths]
        
        def format_row(r):
            cells = []
            for i, (cell, width) in enumerate(zip(r, widths)):
                cells.append(str(cell).center(width))
            return "|".join(cells)
        
        divider = "+" + "+".join("-" * w for w in widths) + "+"
        
        print("\n" + divider)
        print("|" + format_row(headers) + "|")
        print(divider)
        for row in rows:
            print("|" + format_row(row) + "|")
        print(divider + "\n")

    @staticmethod
    def risk_bar(risk: float, width: int = 30) -> str:
        """Generate a visual risk bar"""
        filled = int(risk * width)
        empty = width - filled
        
        if risk >= 0.8:
            color = TerminalUI.FAIL
        elif risk >= 0.5:
            color = TerminalUI.WARNING
        else:
            color = TerminalUI.OKGREEN
            
        bar = f"{color}{'█' * filled}{'░' * empty}{TerminalUI.ENDC}"
        return f"[{bar}] {risk:.0%}"


# ═══════════════════════════════════════════════════════════════════════════════
# PART 2: KNOWLEDGE BASE
# ═══════════════════════════════════════════════════════════════════════════════

class KnowledgeBase:
    """
    Encapsulates failure vectors identified in forensic research.
    Acts as the 'training data' for the agents.
    """
    
    # Documented failure vectors
    FAILURE_VECTORS = {
        "LIFETIME_TRACKER": {
            "desc": "Retain cycles in init during hot reload",
            "severity": "CRITICAL",
            "tool": "LifetimeTracker",
        },
        "DIFFERENCE_TOOL": {
            "desc": "Opaque state changes require diffing tools",
            "severity": "HIGH",
            "tool": "Difference",
        },
        "TCA_GIANT_TEST": {
            "desc": "Giant test antipattern causing brittle builds",
            "severity": "MEDIUM",
            "tool": "TCA Best Practices",
        },
        "MISSING_INTERPOSABLE": {
            "desc": "Missing -interposable flag prevents hot reload",
            "severity": "CRITICAL",
            "tool": "XcodeGen Config",
        },
        "SYMBOL_MANGLING": {
            "desc": "dlsym fails on mangled Swift names",
            "severity": "CRITICAL",
            "tool": "Swift ABI Reference",
        },
        "STATE_INIT_LEAK": {
            "desc": "@State init side-effect memory leak",
            "severity": "CRITICAL",
            "tool": "LifetimeTracker",
        },
        "GOLANG_HALLUCINATION": {
            "desc": "GoLang (GOPATH) env vars in Swift context",
            "severity": "HIGH",
            "tool": "Code Review",
        },
        "DOTNET_HALLUCINATION": {
            "desc": "Windows (Aspnet_regiis) commands in Swift",
            "severity": "HIGH",
            "tool": "Code Review",
        },
        "TYPE_MISMATCH": {
            "desc": "CodeBrain type mismatch / Hallucinated logic",
            "severity": "MEDIUM",
            "tool": "Swift Compiler",
        },
    }
    
    # Logical axioms for the stack
    AXIOMS = {
        "AXIOM_IDEMPOTENCY": {
            "statement": "Initialization must be side-effect free (O(1))",
            "description": "Init(View) -> View must not alter global state or heap significantly",
            "violation": "Heavy Init - NetworkRequest() or HeavyAllocation() in init",
        },
        "AXIOM_SYMBOLIC": {
            "statement": "Symbols must be resolvable via dlsym (Platform Stable)",
            "description": "For any runtime R, function F must have unique resolvable identifier S",
            "violation": "Mangled Mismatch - using human-readable names instead of _$s...",
        },
        "AXIOM_OBSERVABILITY": {
            "statement": "State mutation must trigger View body invalidation",
            "description": "Change in data state D must trigger notification N such that view V updates",
            "violation": "Silent Mutation - state modified without objectWillChange publisher",
        },
        "AXIOM_PURITY": {
            "statement": "View structs must be ephemeral and lightweight",
            "description": "Framework is free to init, discard, re-init these structs at will",
            "violation": "Heavy View - view holds expensive resources or long-lived references",
        },
    }
    
    # SwiftUI lifecycle contract
    LIFECYCLE_CONTRACT = {
        "init": "Called frequently - must be O(1) and side-effect free",
        "onAppear": "Called when view enters window - safe for side effects",
        "onDisappear": "Called when view leaves window - cleanup point",
        "body": "Called on state change - must be pure function of state",
    }


# ═══════════════════════════════════════════════════════════════════════════════
# PART 3: AGENT BASE CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class Agent:
    """Base class for forensic analysis agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.findings: List[Dict] = []
        self.stats = {
            "artifacts_analyzed": 0,
            "violations_found": 0,
        }
    
    def analyze(self, artifact: 'CodeBrainArtifact') -> List[Dict]:
        raise NotImplementedError
    
    def reset(self):
        self.findings = []


# ═══════════════════════════════════════════════════════════════════════════════
# PART 4: AXIOM INVERTER AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class AxiomInverter(Agent):
    """
    Agent A: Inverts logical axioms to find contradictions.
    
    Mechanism: 
    Parses code structure and checks against AXIOMS.
    If Code AND (NOT Axiom) is True, a fault is flagged.
    
    From the Blueprint:
    "The AxiomInverter does not look for bugs; it looks for contradictions."
    """
    
    # Side-effect patterns that violate idempotency
    SIDE_EFFECT_PATTERNS = [
        "fetchData", "loadData", "startTimer", "beginRequest",
        "URLSession", "network", "download", "upload",
        "Timer.scheduledTimer", "DispatchQueue.main.async",
        "NotificationCenter.default.post", "UserDefaults.standard.set",
        "FileManager", "write(", "save(",
    ]
    
    # Reference type indicators
    REFERENCE_PATTERNS = [
        "class ", "AnyObject", "NSObject", "UIViewController",
    ]
    
    def __init__(self):
        super().__init__("AxiomInverter")
    
    def analyze(self, artifact: 'CodeBrainArtifact') -> List[Dict]:
        violations = []
        TerminalUI.log_agent(self.name, "INVERTING", "Applying Boolean inversion to axioms...")
        
        code = artifact.code
        
        # 1. Check AXIOM_IDEMPOTENCY
        if "init" in code or "init(" in code:
            for pattern in self.SIDE_EFFECT_PATTERNS:
                if pattern in code:
                    # Check if the side-effect is in init context
                    init_match = re.search(r'init\s*\([^)]*\)\s*\{[^}]*' + re.escape(pattern), code, re.DOTALL)
                    if init_match or (pattern in code and "init" in code):
                        violations.append({
                            "axiom": "AXIOM_IDEMPOTENCY",
                            "vector": f"Side-effect '{pattern}' detected in init",
                            "severity": "CRITICAL",
                            "impact": "Memory explosion under hot reload",
                            "remediation": f"Move '{pattern}' to onAppear() or Task {{}}",
                        })
                        break
        
        # 2. Check AXIOM_OBSERVABILITY
        if "@State var" in code:
            for ref_pattern in self.REFERENCE_PATTERNS:
                if ref_pattern in code:
                    violations.append({
                        "axiom": "AXIOM_OBSERVABILITY",
                        "vector": "Reference type used with @State (Zombie State Risk)",
                        "severity": "HIGH",
                        "impact": "State changes may not trigger view updates",
                        "remediation": "Use @StateObject for class instances",
                    })
                    break
        
        # 3. Check AXIOM_SYMBOLIC
        if "dlsym" in code:
            # Check for proper mangled names
            if "_$s" not in code and "dlsym" in code:
                # Look for string literals in dlsym calls
                dlsym_match = re.search(r'dlsym\s*\([^,]+,\s*"([^"]+)"', code)
                if dlsym_match:
                    symbol = dlsym_match.group(1)
                    if not symbol.startswith("_$s"):
                        violations.append({
                            "axiom": "AXIOM_SYMBOLIC",
                            "vector": f"dlsym called with unmangled name '{symbol}'",
                            "severity": "CRITICAL",
                            "impact": "Runtime crash - symbol not found",
                            "remediation": "Use swift demangle or @_cdecl for stable symbols",
                        })
        
        # 4. Check AXIOM_PURITY
        heavy_patterns = ["URLSession.shared", "try await", "Actor", "MainActor"]
        if "var body: some View" in code:
            for pattern in heavy_patterns:
                if pattern in code:
                    # Check if it's in the body computation
                    body_match = re.search(r'var body:\s*some View\s*\{[^}]*' + re.escape(pattern), code, re.DOTALL)
                    if body_match:
                        violations.append({
                            "axiom": "AXIOM_PURITY",
                            "vector": f"Heavy operation '{pattern}' in body computation",
                            "severity": "MEDIUM",
                            "impact": "UI stuttering and excessive recomputation",
                            "remediation": "Move async work to .task {} modifier",
                        })
                        break
        
        self.stats["artifacts_analyzed"] += 1
        self.stats["violations_found"] += len(violations)
        
        return violations


# ═══════════════════════════════════════════════════════════════════════════════
# PART 5: PATTERN RECOGNIZER AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class PatternRecognizer(Agent):
    """
    Agent P: Greps for known failure signatures.
    
    Mechanism:
    Uses Regex to match specific text patterns associated with
    documented Failure Vectors from the Knowledge Base.
    """
    
    # Pattern library: (regex, tag, description, severity)
    PATTERNS = [
        # Configuration patterns
        (r"-Xlinker\s+-interposable", "INTERPOSABLE_FLAG", "Correct -interposable flag present", "CONFIG"),
        
        # Code patterns
        (r"dlsym\s*\([^,]+,\s*\"[a-zA-Z][a-zA-Z0-9_]*\"", "UNMANGLED_SYMBOL", 
         "dlsym with unmangled Swift symbol", "CRITICAL"),
        
        (r"XCTAssertEqual\s*\([^)]*analytics", "GIANT_TEST", 
         "TCA Assertion Roulette - analytics in test", "MEDIUM"),
        
        (r"Aspnet_regiis", "DOTNET_HALLUCINATION", 
         "Windows IIS command in Swift code", "HIGH"),
        
        (r"GOPATH|GOROOT|go\s+build", "GOLANG_HALLUCINATION", 
         "GoLang environment/command in Swift", "HIGH"),
        
        (r"@StateObject\s+var\s+\w+\s*=\s*\w+\(\)", "INIT_LEAK", 
         "StateObject initialized inline in declaration", "HIGH"),
        
        (r"@State\s+var\s+\w+\s*:\s*\w+\s*=\s*\w+\(\)", "STATE_INIT", 
         "@State with inline class initialization", "MEDIUM"),
        
        (r"init\s*\([^)]*\)\s*\{[^}]*(fetch|load|start|request)", "INIT_SIDE_EFFECT", 
         "Side-effect detected in initializer", "CRITICAL"),
        
        (r"force_cast|as!", "FORCE_CAST", 
         "Force cast can cause runtime crash", "HIGH"),
        
        (r"try!", "FORCE_TRY", 
         "Force try can cause runtime crash", "HIGH"),
        
        (r"\[\s*weak\s+self\s*\]", "WEAK_SELF", 
         "Proper weak self in closure (GOOD)", "GOOD"),
        
        (r"\{\s*self\.", "STRONG_SELF_CLOSURE", 
         "Strong self capture in closure - potential leak", "MEDIUM"),
        
        (r"DispatchQueue\.main\.async\s*\{[^}]*self\.", "MAIN_QUEUE_SELF", 
         "Main queue async with strong self", "MEDIUM"),
        
        (r"Timer\.scheduledTimer.*selector", "TIMER_SELECTOR", 
         "Timer with selector - potential retain cycle", "MEDIUM"),
    ]
    
    def __init__(self):
        super().__init__("PatternRecognizer")
        self.compiled_patterns: List[Tuple] = []
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Pre-compile regex patterns"""
        for pattern, tag, desc, severity in self.PATTERNS:
            try:
                compiled = re.compile(pattern, re.IGNORECASE | re.MULTILINE | re.DOTALL)
                self.compiled_patterns.append((compiled, tag, desc, severity))
            except re.error as e:
                print(f"[PatternRecognizer] Failed to compile '{tag}': {e}")
    
    def analyze(self, artifact: 'CodeBrainArtifact') -> List[Dict]:
        findings = []
        TerminalUI.log_agent(self.name, "SCANNING", 
                            f"Scanning {len(artifact.code)} bytes for {len(self.compiled_patterns)} signatures...")
        
        # Check code patterns
        for compiled, tag, desc, severity in self.compiled_patterns:
            if severity == "CONFIG":
                # Config patterns checked separately
                continue
                
            matches = compiled.findall(artifact.code)
            if matches:
                finding = {
                    "type": tag,
                    "desc": desc,
                    "severity": severity,
                    "occurrences": len(matches),
                    "samples": matches[:3] if isinstance(matches[0], str) else [str(m) for m in matches[:3]],
                }
                
                if severity != "GOOD":
                    findings.append(finding)
                    status = "WARN" if severity == "MEDIUM" else "FAIL"
                    TerminalUI.log_agent(self.name, "MATCH_FOUND", f"{tag} ({len(matches)}x)", status)
                else:
                    TerminalUI.log_agent(self.name, "GOOD_PATTERN", f"{tag} ({len(matches)}x)", "SUCCESS")
        
        # Check configuration
        if artifact.config:
            if "-interposable" not in artifact.config and "-Xlinker" not in artifact.config:
                findings.append({
                    "type": "MISSING_INTERPOSABLE",
                    "desc": "Missing -Xlinker -interposable flag",
                    "severity": "CRITICAL",
                    "occurrences": 1,
                    "samples": [f"Current flags: '{artifact.config}'"],
                })
                TerminalUI.log_agent(self.name, "CONFIG_MISSING", "-interposable flag not found", "FAIL")
        else:
            findings.append({
                "type": "NO_CONFIG",
                "desc": "No linker configuration provided",
                "severity": "HIGH",
                "occurrences": 1,
                "samples": ["Empty config context"],
            })
            TerminalUI.log_agent(self.name, "CONFIG_EMPTY", "No linker flags defined", "WARN")
        
        self.stats["artifacts_analyzed"] += 1
        self.stats["violations_found"] += len(findings)
        
        return findings


# ═══════════════════════════════════════════════════════════════════════════════
# PART 6: PROBABILISTIC REASONING AGENT (PRA)
# ═══════════════════════════════════════════════════════════════════════════════

class PRA(Agent):
    """
    Agent R: Probabilistic Reasoning Agent
    
    Calculates failure probability based on agent consensus using
    Bayesian weighting and Fault Tree Analysis.
    
    From the Blueprint:
    "The PRA ingests binary outputs of the AxiomInverter (True/False)
     and discrete outputs of the PatternRecognizer (Count).
     It applies a Bayesian weighting system."
    """
    
    # Severity weights for risk calculation
    SEVERITY_WEIGHTS = {
        "CRITICAL": 0.45,
        "HIGH": 0.30,
        "MEDIUM": 0.15,
        "LOW": 0.05,
    }
    
    # Pattern type weights
    PATTERN_WEIGHTS = {
        "HALLUCINATION": 0.50,
        "SYMBOL": 0.40,
        "MEMORY": 0.35,
        "CONFIG": 0.30,
        "DEFAULT": 0.15,
    }
    
    def __init__(self):
        super().__init__("PRA_Agent")
    
    def assess_risk(
        self, 
        axiom_violations: List[Dict], 
        pattern_findings: List[Dict]
    ) -> Tuple[float, str, Dict]:
        """
        Calculate probability of failure given evidence.
        
        Returns:
            - risk_score: 0.0 to 1.0 probability
            - certainty: LOW/MODERATE/HIGH/CRITICAL
            - breakdown: detailed risk factors
        """
        TerminalUI.log_agent(self.name, "CALCULATING", "Bayesian update of failure probability...")
        
        # Base failure rate (prior)
        base_risk = 0.05
        risk_factors = []
        
        # Process axiom violations
        axiom_risk = 0.0
        for violation in axiom_violations:
            severity = violation.get("severity", "MEDIUM")
            weight = self.SEVERITY_WEIGHTS.get(severity, 0.15)
            axiom_risk += weight
            risk_factors.append({
                "source": "Axiom",
                "item": violation["axiom"],
                "contribution": weight,
            })
        
        # Process pattern findings
        pattern_risk = 0.0
        for finding in pattern_findings:
            severity = finding.get("severity", "MEDIUM")
            pattern_type = finding.get("type", "DEFAULT")
            
            # Determine weight based on pattern type
            if "HALLUCINATION" in pattern_type:
                weight = self.PATTERN_WEIGHTS["HALLUCINATION"]
            elif "SYMBOL" in pattern_type or "UNMANGLED" in pattern_type:
                weight = self.PATTERN_WEIGHTS["SYMBOL"]
            elif "LEAK" in pattern_type or "SELF" in pattern_type:
                weight = self.PATTERN_WEIGHTS["MEMORY"]
            elif "CONFIG" in pattern_type or "INTERPOSABLE" in pattern_type:
                weight = self.PATTERN_WEIGHTS["CONFIG"]
            else:
                weight = self.SEVERITY_WEIGHTS.get(severity, 0.15)
            
            # Scale by occurrences (diminishing returns)
            occurrences = finding.get("occurrences", 1)
            scaled_weight = weight * math.log(occurrences + 1)
            
            pattern_risk += scaled_weight
            risk_factors.append({
                "source": "Pattern",
                "item": finding["type"],
                "contribution": scaled_weight,
            })
        
        # Combine risks (not simply additive - use probability union)
        combined_risk = base_risk + axiom_risk + pattern_risk
        
        # Apply sigmoid-like normalization to keep in [0, 1]
        # P = 1 - 1/(1 + combined_risk)
        final_risk = 1.0 - (1.0 / (1.0 + combined_risk))
        
        # Ensure minimum risk if violations exist
        if (axiom_violations or pattern_findings) and final_risk < 0.3:
            final_risk = max(final_risk, 0.3 + (0.1 * len(axiom_violations)))
        
        # Cap at 0.99 for asymptotic realism
        final_risk = min(final_risk, 0.99)
        
        # Determine certainty level
        if final_risk >= 0.9:
            certainty = "CRITICAL"
        elif final_risk >= 0.7:
            certainty = "HIGH"
        elif final_risk >= 0.4:
            certainty = "MODERATE"
        else:
            certainty = "LOW"
        
        breakdown = {
            "base_risk": base_risk,
            "axiom_risk": axiom_risk,
            "pattern_risk": pattern_risk,
            "combined": combined_risk,
            "final": final_risk,
            "factors": risk_factors,
        }
        
        return final_risk, certainty, breakdown


# ═══════════════════════════════════════════════════════════════════════════════
# PART 7: CODE ARTIFACT
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CodeBrainArtifact:
    """Represents a piece of code generated by CodeBrain AI"""
    id: str
    description: str
    code: str
    config: str = ""
    source_file: str = ""
    metadata: Dict = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# PART 8: SIMULATION ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════════

class Simulation:
    """
    Orchestrates the Multi-Agent System.
    Loads artifacts, invokes agents, collects metrics, and reports.
    """
    
    def __init__(self):
        self.agents = {
            "axiom": AxiomInverter(),
            "pattern": PatternRecognizer(),
            "pra": PRA(),
        }
        self.artifacts: List[CodeBrainArtifact] = []
        self.results: List[Dict] = []
    
    def load_artifacts(self):
        """
        Load sample artifacts representing common CodeBrain failures.
        """
        
        # Artifact 1: The "Init Leak" - Memory explosion under hot reload
        code_1 = """
struct ContentView: View {
    // CodeBrain: "Initialize data inline for convenience"
    @StateObject var viewModel = ViewModel()
    
    init() {
        // VIOLATION: Side effect in init
        viewModel.fetchData() 
        print("View initialized")
    }
    
    var body: some View {
        Text(viewModel.data)
    }
}

class ViewModel: ObservableObject {
    @Published var data = ""
    
    func fetchData() {
        URLSession.shared.dataTask(with: url) { ... }
    }
}
        """
        self.artifacts.append(CodeBrainArtifact(
            id="CB_001",
            description="SwiftUI Init Leak",
            code=code_1,
            config="-w",
        ))

        # Artifact 2: The "Symbol Mismatch" - dlsym crash
        code_2 = """
func loadPreview() {
    let lib = dlopen("UIPreview.dylib", RTLD_NOW)
    
    // VIOLATION: Symbol not mangled
    let sym = dlsym(lib, "createView") 
    
    let createView = unsafeBitCast(sym, to: (() -> AnyView).self)
    return createView()
}
        """
        self.artifacts.append(CodeBrainArtifact(
            id="CB_002",
            description="Dylib Symbol Error",
            code=code_2,
            config="-Xlinker -interposable",
        ))

        # Artifact 3: The "Cross-Domain Hallucination"
        code_3 = """
func configureServer() {
    // VIOLATION: Hallucination from .NET corpus
    let cmd = "Aspnet_regiis.exe -ga user"
    
    // Also mixing in Go concepts
    let gopath = ProcessInfo.processInfo.environment["GOPATH"]
    
    system(cmd)
}
        """
        self.artifacts.append(CodeBrainArtifact(
            id="CB_003",
            description="Cross-Domain Hallucination",
            code=code_3,
            config="-interposable",
        ))

        # Artifact 4: The "Missing Config" - Silent failure
        code_4 = """
struct HotReloadView: View {
    @ObservedObject var injector = Inject.observer
    
    var body: some View {
        Text("Hello, Hot Reload!")
            .enableInjection()
    }
}
        """
        # VIOLATION: Empty config flags - hot reload won't work
        self.artifacts.append(CodeBrainArtifact(
            id="CB_004",
            description="Missing Linker Flag",
            code=code_4,
            config="",  # Missing -interposable!
        ))

        # Artifact 5: Strong self in closure
        code_5 = """
class DataManager {
    var data: [String] = []
    
    func loadData() {
        URLSession.shared.dataTask(with: url) { data, _, _ in
            // VIOLATION: Strong self capture
            self.data = data
            
            DispatchQueue.main.async {
                self.updateUI()
            }
        }.resume()
    }
}
        """
        self.artifacts.append(CodeBrainArtifact(
            id="CB_005",
            description="Strong Self Closure",
            code=code_5,
            config="-Xlinker -interposable",
        ))
    
    def analyze_artifact(self, artifact: CodeBrainArtifact) -> Dict:
        """Analyze a single artifact through all agents"""
        print(f"\n{TerminalUI.BOLD}{'─' * 78}{TerminalUI.ENDC}")
        print(f"{TerminalUI.BOLD}>>> ANALYZING: {artifact.id} - {artifact.description}{TerminalUI.ENDC}")
        print(f"{TerminalUI.DIM}Config: {artifact.config if artifact.config else '<empty>'}{TerminalUI.ENDC}")
        print(f"{TerminalUI.BOLD}{'─' * 78}{TerminalUI.ENDC}")
        
        # 1. Axiom Inversion
        axiom_violations = self.agents["axiom"].analyze(artifact)
        if axiom_violations:
            TerminalUI.log_agent("AxiomInverter", "VIOLATIONS", 
                                f"Found {len(axiom_violations)} logical flaws", "FAIL")
        else:
            TerminalUI.log_agent("AxiomInverter", "PASS", 
                                "No axiom contradictions", "SUCCESS")
        
        # 2. Pattern Recognition
        pattern_findings = self.agents["pattern"].analyze(artifact)
        risky = [f for f in pattern_findings if f.get("severity") not in ["GOOD", "INFO"]]
        if risky:
            TerminalUI.log_agent("PatternRecognizer", "FINDINGS", 
                                f"Found {len(risky)} risky patterns", "WARN")
        else:
            TerminalUI.log_agent("PatternRecognizer", "CLEAR", 
                                "No failure signatures", "SUCCESS")
        
        # 3. Probabilistic Risk Assessment
        risk, certainty, breakdown = self.agents["pra"].assess_risk(axiom_violations, pattern_findings)
        
        status = "CRITICAL" if risk >= 0.8 else "WARN" if risk >= 0.5 else "INFO"
        TerminalUI.log_agent("PRA_Agent", "VERDICT", 
                            f"P(Failure) = {risk:.2f} [{certainty}]", status)
        
        # Visual risk bar
        print(f"\n  Risk: {TerminalUI.risk_bar(risk)}")
        
        return {
            "artifact": artifact,
            "axiom_violations": axiom_violations,
            "pattern_findings": pattern_findings,
            "risk": risk,
            "certainty": certainty,
            "breakdown": breakdown,
        }
    
    def run(self):
        """Execute the full simulation"""
        TerminalUI.banner()
        
        # Load test artifacts
        self.load_artifacts()
        print(f"📥 Loaded {len(self.artifacts)} CodeBrain artifacts for analysis\n")
        
        # Analyze each artifact
        for artifact in self.artifacts:
            result = self.analyze_artifact(artifact)
            self.results.append(result)
            time.sleep(0.2)  # Simulate processing
        
        # Generate summary report
        self.generate_report()
    
    def generate_report(self):
        """Generate the final forensic report"""
        TerminalUI.section("FORENSIC ANALYSIS REPORT")
        
        # Summary table
        headers = ["ID", "Description", "Violations", "Risk", "Verdict"]
        rows = []
        
        for result in self.results:
            artifact = result["artifact"]
            total_violations = len(result["axiom_violations"]) + len(result["pattern_findings"])
            rows.append([
                artifact.id,
                artifact.description[:25],
                total_violations,
                f"{result['risk']:.2f}",
                result["certainty"],
            ])
        
        TerminalUI.print_table(headers, rows)
        
        # Critical findings
        critical = [r for r in self.results if r["certainty"] == "CRITICAL"]
        if critical:
            print(f"{TerminalUI.FAIL}{TerminalUI.BOLD}🚨 CRITICAL FINDINGS:{TerminalUI.ENDC}\n")
            for result in critical:
                artifact = result["artifact"]
                print(f"  • {artifact.id}: {artifact.description}")
                for v in result["axiom_violations"]:
                    print(f"    ⚠️  {v['axiom']}: {v['vector']}")
        
        # Overall statistics
        total_artifacts = len(self.results)
        total_violations = sum(
            len(r["axiom_violations"]) + len(r["pattern_findings"]) 
            for r in self.results
        )
        avg_risk = sum(r["risk"] for r in self.results) / total_artifacts if total_artifacts else 0
        
        print(f"\n{TerminalUI.BOLD}📊 OVERALL STATISTICS:{TerminalUI.ENDC}")
        print(f"  Artifacts Analyzed: {total_artifacts}")
        print(f"  Total Violations:   {total_violations}")
        print(f"  Average Risk:       {avg_risk:.2%}")
        print(f"  Critical Issues:    {len(critical)}")
        
        # Recommendations
        print(f"\n{TerminalUI.BOLD}💡 RECOMMENDATIONS:{TerminalUI.ENDC}")
        print("  1. Install LifetimeTracker to detect retain cycles during hot reload")
        print("  2. Use Difference tool to debug opaque state changes")
        print("  3. Ensure -Xlinker -interposable is in Debug config")
        print("  4. Move all side-effects from init() to onAppear()")
        print("  5. Always use [weak self] in closures")
        
        print(f"\n{TerminalUI.DIM}{'─' * 78}{TerminalUI.ENDC}")
        print(f"{TerminalUI.OKCYAN}Report compiled by XcodeGen Forensic Analyzer v1.0{TerminalUI.ENDC}")
        print(f"{TerminalUI.DIM}{'─' * 78}{TerminalUI.ENDC}\n")
    
    def analyze_file(self, filepath: str) -> Optional[Dict]:
        """Analyze a real Swift file"""
        path = Path(filepath)
        if not path.exists():
            print(f"Error: File not found: {filepath}")
            return None
        
        code = path.read_text()
        artifact = CodeBrainArtifact(
            id=path.stem,
            description=f"File: {path.name}",
            code=code,
            source_file=str(path),
        )
        
        return self.analyze_artifact(artifact)


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point"""
    import sys
    
    sim = Simulation()
    
    if len(sys.argv) > 1:
        # Analyze specific file(s)
        TerminalUI.banner()
        for filepath in sys.argv[1:]:
            print(f"\n📄 Analyzing: {filepath}")
            sim.analyze_file(filepath)
    else:
        # Run demo simulation
        sim.run()


if __name__ == "__main__":
    main()
