#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
 PURE PYTHON MULTI-AGENT SYSTEM (MAS)
 Zero Dependencies - Standard Library Only
═══════════════════════════════════════════════════════════════════════════════

From Gemini Deep Research Blueprint:
"A Blackboard-based Multi-Agent System using Python's standard library.
 This system mimics the cognitive processes of a security researcher and
 a reliability engineer, distributed across specialized autonomous agents."

Components:
- Blackboard: Thread-safe SQLite knowledge repository
- Axiom Inverter Agent: Negates assumptions to find failure modes
- Pattern Recognizer Agent: Static analysis for risk patterns
- PRA Agent: Probabilistic Risk Assessment with Bayesian inference

NO EXTERNAL DEPENDENCIES. RUNS ON ANY PYTHON 3.8+
"""

import sqlite3
import threading
import queue
import time
import re
import math
import json
import hashlib
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════════
# BLACKBOARD: The Central Knowledge Repository
# ═══════════════════════════════════════════════════════════════════════════════

class Blackboard:
    """
    The central knowledge repository for the Multi-Agent System.
    Uses an in-memory SQLite database to store axioms, hypotheses, and risk scores.
    Thread-safe via explicit locking.
    """
    
    def __init__(self, db_path: str = ":memory:"):
        self.lock = threading.RLock()
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self._setup_schema()
        self.subscribers: List[queue.Queue] = []
        
    def _setup_schema(self):
        """Initialize the database schema"""
        with self.lock:
            # Axioms: Core assumptions of the system
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS axioms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    component TEXT NOT NULL,
                    domain TEXT,
                    statement TEXT NOT NULL,
                    inverted_statement TEXT,
                    status TEXT DEFAULT 'PENDING',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP
                )
            ''')
            
            # Failure Vectors: Identified risks
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS failure_vectors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    axiom_id INTEGER,
                    description TEXT NOT NULL,
                    mechanism TEXT,
                    probability REAL DEFAULT 0.0,
                    severity REAL DEFAULT 0.0,
                    risk_score REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'IDENTIFIED',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(axiom_id) REFERENCES axioms(id)
                )
            ''')
            
            # Patterns: Recognized code/architecture patterns
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    pattern_type TEXT,
                    regex TEXT,
                    risk_level TEXT,
                    description TEXT,
                    occurrences INTEGER DEFAULT 0
                )
            ''')
            
            # Events: System event log
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    payload TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.connection.commit()
    
    def subscribe(self) -> queue.Queue:
        """Subscribe to blackboard events"""
        q = queue.Queue()
        self.subscribers.append(q)
        return q
    
    def _notify(self, event: Dict[str, Any]):
        """Notify all subscribers of an event"""
        for q in self.subscribers:
            try:
                q.put_nowait(event)
            except queue.Full:
                pass
    
    def add_axiom(self, component: str, statement: str, domain: str = None) -> int:
        """Registers a fundamental truth assumed by the architecture."""
        with self.lock:
            self.cursor.execute(
                "INSERT INTO axioms (component, domain, statement, status) VALUES (?, ?, ?, 'PENDING')",
                (component, domain, statement)
            )
            self.connection.commit()
            axiom_id = self.cursor.lastrowid
            
            self._log_event("Blackboard", "AXIOM_ADDED", {
                "axiom_id": axiom_id,
                "component": component,
                "statement": statement
            })
            self._notify({"type": "AXIOM_ADDED", "axiom_id": axiom_id})
            
            return axiom_id
    
    def update_axiom_inversion(self, axiom_id: int, inverted_statement: str):
        """The Axiom Inverter Agent updates the blackboard with the logical inverse."""
        with self.lock:
            self.cursor.execute(
                "UPDATE axioms SET inverted_statement = ?, status = 'INVERTED', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (inverted_statement, axiom_id)
            )
            self.connection.commit()
            
            self._log_event("AxiomInverter", "AXIOM_INVERTED", {
                "axiom_id": axiom_id,
                "inverted": inverted_statement
            })
            self._notify({"type": "AXIOM_INVERTED", "axiom_id": axiom_id})
    
    def record_failure_vector(
        self,
        axiom_id: int,
        description: str,
        probability: float,
        severity: float,
        mechanism: str = None
    ) -> int:
        """The PRA Agent records a quantified risk."""
        risk_score = probability * severity
        
        with self.lock:
            self.cursor.execute(
                """INSERT INTO failure_vectors 
                   (axiom_id, description, mechanism, probability, severity, risk_score) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (axiom_id, description, mechanism, probability, severity, risk_score)
            )
            self.connection.commit()
            vector_id = self.cursor.lastrowid
            
            self._log_event("PRA", "VECTOR_RECORDED", {
                "vector_id": vector_id,
                "risk_score": risk_score
            })
            self._notify({"type": "VECTOR_RECORDED", "vector_id": vector_id})
            
            return vector_id
    
    def add_pattern(
        self,
        name: str,
        pattern_type: str,
        regex: str,
        risk_level: str,
        description: str = None
    ) -> int:
        """Register a pattern for the Pattern Recognizer"""
        with self.lock:
            self.cursor.execute(
                """INSERT INTO patterns (name, pattern_type, regex, risk_level, description)
                   VALUES (?, ?, ?, ?, ?)""",
                (name, pattern_type, regex, risk_level, description)
            )
            self.connection.commit()
            return self.cursor.lastrowid
    
    def increment_pattern_occurrence(self, pattern_id: int):
        """Track pattern occurrences"""
        with self.lock:
            self.cursor.execute(
                "UPDATE patterns SET occurrences = occurrences + 1 WHERE id = ?",
                (pattern_id,)
            )
            self.connection.commit()
    
    def get_pending_axioms(self) -> List[Dict]:
        """Get axioms awaiting inversion"""
        with self.lock:
            self.cursor.execute(
                "SELECT id, component, domain, statement FROM axioms WHERE status = 'PENDING'"
            )
            return [dict(row) for row in self.cursor.fetchall()]
    
    def get_inverted_axioms(self) -> List[Dict]:
        """Get axioms that have been inverted"""
        with self.lock:
            self.cursor.execute(
                """SELECT id, component, domain, statement, inverted_statement 
                   FROM axioms WHERE status = 'INVERTED'"""
            )
            return [dict(row) for row in self.cursor.fetchall()]
    
    def get_all_failure_vectors(self) -> List[Dict]:
        """Get all recorded failure vectors"""
        with self.lock:
            self.cursor.execute(
                """SELECT fv.*, a.component, a.statement, a.inverted_statement
                   FROM failure_vectors fv
                   LEFT JOIN axioms a ON fv.axiom_id = a.id
                   ORDER BY fv.risk_score DESC"""
            )
            return [dict(row) for row in self.cursor.fetchall()]
    
    def get_patterns(self) -> List[Dict]:
        """Get all registered patterns"""
        with self.lock:
            self.cursor.execute("SELECT * FROM patterns")
            return [dict(row) for row in self.cursor.fetchall()]
    
    def _log_event(self, agent: str, event_type: str, payload: Dict):
        """Log an event to the blackboard"""
        with self.lock:
            self.cursor.execute(
                "INSERT INTO events (agent, event_type, payload) VALUES (?, ?, ?)",
                (agent, event_type, json.dumps(payload))
            )
            self.connection.commit()
    
    def get_statistics(self) -> Dict:
        """Get system statistics"""
        with self.lock:
            stats = {}
            
            self.cursor.execute("SELECT COUNT(*) FROM axioms")
            stats["total_axioms"] = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM axioms WHERE status = 'INVERTED'")
            stats["inverted_axioms"] = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM failure_vectors")
            stats["failure_vectors"] = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT AVG(risk_score) FROM failure_vectors")
            avg = self.cursor.fetchone()[0]
            stats["avg_risk_score"] = round(avg, 3) if avg else 0
            
            self.cursor.execute("SELECT MAX(risk_score) FROM failure_vectors")
            max_risk = self.cursor.fetchone()[0]
            stats["max_risk_score"] = round(max_risk, 3) if max_risk else 0
            
            return stats
    
    def export_report(self) -> Dict:
        """Export full analysis report"""
        return {
            "statistics": self.get_statistics(),
            "axioms": self.get_inverted_axioms(),
            "failure_vectors": self.get_all_failure_vectors(),
            "patterns": self.get_patterns(),
            "generated_at": datetime.now().isoformat()
        }


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT BASE CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class Agent(threading.Thread):
    """Base class for all agents"""
    
    def __init__(self, name: str, blackboard: Blackboard):
        super().__init__(name=name)
        self.blackboard = blackboard
        self.daemon = True
        self.running = True
        self.event_queue = blackboard.subscribe()
        self.stats = {
            "tasks_processed": 0,
            "errors": 0,
            "start_time": None,
        }
    
    def run(self):
        self.stats["start_time"] = time.time()
        self.on_start()
        
        while self.running:
            try:
                self.process()
                time.sleep(self.get_poll_interval())
            except Exception as e:
                self.stats["errors"] += 1
                self.on_error(e)
    
    def stop(self):
        self.running = False
    
    def get_poll_interval(self) -> float:
        return 0.5
    
    def on_start(self):
        """Called when agent starts"""
        pass
    
    def on_error(self, error: Exception):
        """Called on error"""
        print(f"[{self.name}] Error: {error}")
    
    def process(self):
        """Main processing loop - override in subclass"""
        raise NotImplementedError


# ═══════════════════════════════════════════════════════════════════════════════
# AXIOM INVERTER AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class AxiomInverterAgent(Agent):
    """
    The Axiom Inverter Agent is the engine of critical thinking.
    It systematically negates system axioms to reveal failure modes.
    
    From the Blueprint:
    "In software engineering, developers rely on implicit axioms. 
     The Axiom Inverter systematically negates these. If the architecture
     is robust, the negation should be impossible or handled gracefully.
     If fragile, the negation reveals a catastrophic failure vector."
    """
    
    # Semantic inversion rules
    INVERSIONS = {
        "deterministic": "non-deterministic and entropy-dependent",
        "consistent": "eventually consistent or divergent",
        "immutable": "mutated by external side-effects",
        "available": "unavailable or rate-limited",
        "atomic": "interleaved and race-prone",
        "static": "dynamically interposed",
        "synchronous": "asynchronous and uncoordinated",
        "reliable": "unreliable and failure-prone",
        "secure": "vulnerable and exposed",
        "fast": "slow and latency-bound",
        "safe": "unsafe and hazardous",
        "stable": "unstable and volatile",
        "isolated": "shared and contended",
        "unique": "duplicated or colliding",
        "valid": "invalid or malformed",
        "complete": "partial or truncated",
        "ordered": "unordered or shuffled",
        "cached": "uncached and cold",
        "persistent": "ephemeral and transient",
        "idempotent": "non-idempotent with side-effects",
        "stateless": "stateful and context-dependent",
        "guaranteed": "best-effort and lossy",
        "sequential": "concurrent and racy",
        "blocking": "non-blocking but incomplete",
        "trusted": "untrusted and adversarial",
    }
    
    # Negation prefixes
    NEGATIONS = {
        "always": "sometimes fails to",
        "never": "occasionally does",
        "will": "may not",
        "must": "might not",
        "should": "could fail to",
        "can": "cannot reliably",
        "is": "is not necessarily",
        "are": "are not guaranteed to be",
        "has": "may lack",
        "does": "may fail to",
    }
    
    def __init__(self, blackboard: Blackboard):
        super().__init__("AxiomInverter", blackboard)
    
    def on_start(self):
        print(f"[{self.name}] 🔄 Axiom Inverter Agent started")
    
    def process(self):
        pending = self.blackboard.get_pending_axioms()
        
        for axiom in pending:
            inverted = self.invert_logic(axiom["statement"])
            self.blackboard.update_axiom_inversion(axiom["id"], inverted)
            self.stats["tasks_processed"] += 1
            
            print(f"[{self.name}] ⚡ Inverted: '{axiom['statement'][:40]}...' → '{inverted[:40]}...'")
    
    def invert_logic(self, statement: str) -> str:
        """
        Applies heuristic rules to semantically invert technical axioms.
        Uses rule-based templates derived from distributed systems failure modes.
        """
        words = statement.split()
        new_words = []
        
        for i, word in enumerate(words):
            lower_word = word.lower().strip(".,;:!?")
            
            # Check for negation patterns
            if lower_word in self.NEGATIONS:
                new_words.append(self.NEGATIONS[lower_word])
                continue
            
            # Check for inversion patterns
            if lower_word in self.INVERSIONS:
                new_words.append(self.INVERSIONS[lower_word])
                continue
            
            new_words.append(word)
        
        result = " ".join(new_words)
        
        # If no changes made, apply general negation
        if result == statement:
            result = f"It is NOT guaranteed that: {statement}"
        
        return result


# ═══════════════════════════════════════════════════════════════════════════════
# PATTERN RECOGNIZER AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class PatternRecognizerAgent(Agent):
    """
    The Pattern Recognizer Agent serves as the "eyes" of the system.
    It uses Static Analysis techniques to scan for high-risk code constructs.
    
    From the Blueprint:
    "Given the constraints (no pip install), this agent utilizes Python's
     re module to identify high-risk code constructs such as singletons,
     global state, or dyld interposing flags."
    """
    
    # Built-in risky patterns
    DEFAULT_PATTERNS = [
        {
            "name": "Singleton Pattern",
            "type": "architecture",
            "regex": r"shared\s*=\s*\w+\(\)|\.shared\b|static\s+let\s+instance",
            "risk_level": "MEDIUM",
            "description": "Singleton introduces global state and testing difficulties"
        },
        {
            "name": "Force Unwrap",
            "type": "safety",
            "regex": r"!\s*$|!\.",
            "risk_level": "HIGH",
            "description": "Force unwrapping can cause runtime crashes"
        },
        {
            "name": "Missing Weak Self",
            "type": "memory",
            "regex": r"\{\s*\[?\s*self\b(?!\s*\])",
            "risk_level": "HIGH",
            "description": "Closure may retain self strongly, causing memory leak"
        },
        {
            "name": "Side Effect in Init",
            "type": "lifecycle",
            "regex": r"init\s*\([^)]*\)\s*\{[^}]*(?:start|fetch|load|request)",
            "risk_level": "MEDIUM",
            "description": "Side effects in init can cause duplicate execution"
        },
        {
            "name": "Interposable Flag",
            "type": "linker",
            "regex": r"-interposable|-Xlinker\s+-interposable",
            "risk_level": "CRITICAL",
            "description": "Linker flag can leak to release builds"
        },
        {
            "name": "Global Mutable State",
            "type": "concurrency",
            "regex": r"var\s+\w+\s*:\s*\[[^\]]+\]\s*=\s*\[\]",
            "risk_level": "HIGH",
            "description": "Global mutable collection is race-prone"
        },
        {
            "name": "Hardcoded Credentials",
            "type": "security",
            "regex": r"(?:password|secret|api_key|token)\s*=\s*['\"][^'\"]+['\"]",
            "risk_level": "CRITICAL",
            "description": "Hardcoded credentials are security vulnerabilities"
        },
        {
            "name": "Race Condition Pattern",
            "type": "concurrency",
            "regex": r"DispatchQueue\.global\(\)\.async\s*\{[^}]*self\.",
            "risk_level": "HIGH",
            "description": "Async access to self without synchronization"
        },
    ]
    
    def __init__(self, blackboard: Blackboard):
        super().__init__("PatternRecognizer", blackboard)
        self.compiled_patterns: List[Tuple[Dict, re.Pattern]] = []
        self._initialize_patterns()
    
    def _initialize_patterns(self):
        """Register and compile default patterns"""
        for pattern in self.DEFAULT_PATTERNS:
            pattern_id = self.blackboard.add_pattern(
                name=pattern["name"],
                pattern_type=pattern["type"],
                regex=pattern["regex"],
                risk_level=pattern["risk_level"],
                description=pattern["description"]
            )
            pattern["id"] = pattern_id
            
            try:
                compiled = re.compile(pattern["regex"], re.IGNORECASE | re.MULTILINE)
                self.compiled_patterns.append((pattern, compiled))
            except re.error as e:
                print(f"[{self.name}] Failed to compile pattern: {e}")
    
    def on_start(self):
        print(f"[{self.name}] 👁️ Pattern Recognizer Agent started ({len(self.compiled_patterns)} patterns)")
    
    def process(self):
        # Check inverted axioms for pattern matches
        inverted = self.blackboard.get_inverted_axioms()
        
        for axiom in inverted:
            if not axiom.get("inverted_statement"):
                continue
            
            # Analyze the inversion for risk indicators
            for pattern, compiled in self.compiled_patterns:
                # Check if the inverted statement suggests this pattern is relevant
                if self._is_pattern_relevant(axiom, pattern):
                    self.blackboard.increment_pattern_occurrence(pattern["id"])
                    self.stats["tasks_processed"] += 1
    
    def _is_pattern_relevant(self, axiom: Dict, pattern: Dict) -> bool:
        """Check if a pattern is relevant to an axiom"""
        inv = axiom.get("inverted_statement", "").lower()
        
        relevance_map = {
            "memory": ["leak", "retain", "weak", "strong"],
            "concurrency": ["race", "async", "thread", "concurrent"],
            "security": ["vulnerable", "exposed", "untrusted"],
            "safety": ["crash", "fail", "unsafe"],
        }
        
        pattern_type = pattern.get("type", "")
        keywords = relevance_map.get(pattern_type, [])
        
        return any(kw in inv for kw in keywords)
    
    def scan_text(self, text: str) -> List[Dict]:
        """Scan text for pattern matches"""
        matches = []
        
        for pattern, compiled in self.compiled_patterns:
            found = compiled.findall(text)
            if found:
                matches.append({
                    "pattern": pattern["name"],
                    "risk_level": pattern["risk_level"],
                    "occurrences": len(found),
                    "samples": found[:3],  # First 3 matches
                })
                self.blackboard.increment_pattern_occurrence(pattern["id"])
        
        return matches
    
    def scan_file(self, filepath: Path) -> List[Dict]:
        """Scan a file for pattern matches"""
        try:
            with open(filepath) as f:
                content = f.read()
            return self.scan_text(content)
        except Exception as e:
            return [{"error": str(e)}]


# ═══════════════════════════════════════════════════════════════════════════════
# PROBABILISTIC RISK ASSESSOR (PRA) AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class PRAAgent(Agent):
    """
    The PRA Agent applies Bayesian Network logic to quantify risk.
    It models failure as a probability distribution.
    
    From the Blueprint:
    "Using Fault Tree Analysis (FTA), this agent calculates the probability
     of the 'Top Event' (e.g., Build Pipeline Failure). It models the system
     using logic gates (AND/OR) implemented in Python."
    """
    
    # Risk categorization thresholds
    RISK_THRESHOLDS = {
        "CRITICAL": 0.8,
        "HIGH": 0.6,
        "MEDIUM": 0.4,
        "LOW": 0.2,
    }
    
    # Domain-specific base failure rates
    BASE_RATES = {
        "memory": 0.15,
        "concurrency": 0.20,
        "security": 0.10,
        "build": 0.05,
        "runtime": 0.12,
        "network": 0.08,
        "storage": 0.05,
        "default": 0.10,
    }
    
    def __init__(self, blackboard: Blackboard):
        super().__init__("PRA", blackboard)
    
    def on_start(self):
        print(f"[{self.name}] 📊 Probabilistic Risk Assessor started")
    
    def process(self):
        # Analyze inverted axioms and create failure vectors
        inverted = self.blackboard.get_inverted_axioms()
        
        for axiom in inverted:
            # Calculate risk based on the inversion
            probability, severity = self.assess_risk(axiom)
            
            if probability > 0.1:  # Only record significant risks
                description = self.generate_failure_description(axiom)
                mechanism = self.identify_mechanism(axiom)
                
                self.blackboard.record_failure_vector(
                    axiom_id=axiom["id"],
                    description=description,
                    probability=probability,
                    severity=severity,
                    mechanism=mechanism
                )
                
                self.stats["tasks_processed"] += 1
                
                risk_level = self.categorize_risk(probability * severity)
                print(f"[{self.name}] ⚠️ {risk_level}: {description[:50]}... (P={probability:.2f}, S={severity:.2f})")
    
    def assess_risk(self, axiom: Dict) -> Tuple[float, float]:
        """
        Calculate probability and severity using Bayesian inference.
        
        P(Failure|Evidence) = (P(Evidence|Failure) * P(Failure)) / P(Evidence)
        """
        domain = axiom.get("domain", "default")
        inverted = axiom.get("inverted_statement", "").lower()
        
        # Base probability from domain
        prior = self.BASE_RATES.get(domain, self.BASE_RATES["default"])
        
        # Adjust based on keywords in inverted statement
        risk_keywords = {
            "crash": 0.3,
            "fail": 0.2,
            "corrupt": 0.25,
            "leak": 0.2,
            "race": 0.25,
            "vulnerable": 0.3,
            "deadlock": 0.35,
            "overflow": 0.3,
            "undefined": 0.2,
        }
        
        likelihood_boost = sum(
            boost for kw, boost in risk_keywords.items() if kw in inverted
        )
        
        probability = min(0.95, prior + likelihood_boost)
        
        # Calculate severity based on impact keywords
        severity_keywords = {
            "data loss": 1.0,
            "crash": 0.9,
            "security": 0.95,
            "corrupt": 0.85,
            "deadlock": 0.8,
            "memory": 0.7,
            "performance": 0.5,
        }
        
        severity = 0.5  # Base severity
        for kw, sev in severity_keywords.items():
            if kw in inverted:
                severity = max(severity, sev)
        
        return probability, severity
    
    def calculate_bayesian_probability(
        self,
        prior: float,
        likelihood: float,
        marginal: float
    ) -> float:
        """
        P(Failure|Evidence) = (P(Evidence|Failure) * P(Failure)) / P(Evidence)
        """
        if marginal == 0:
            return prior
        return (likelihood * prior) / marginal
    
    def categorize_risk(self, risk_score: float) -> str:
        """Categorize risk level"""
        for level, threshold in self.RISK_THRESHOLDS.items():
            if risk_score >= threshold:
                return level
        return "LOW"
    
    def generate_failure_description(self, axiom: Dict) -> str:
        """Generate a human-readable failure description"""
        component = axiom.get("component", "System")
        statement = axiom.get("statement", "")
        inverted = axiom.get("inverted_statement", "")
        
        return f"{component} failure when: {inverted}"
    
    def identify_mechanism(self, axiom: Dict) -> str:
        """Identify the failure mechanism"""
        inverted = axiom.get("inverted_statement", "").lower()
        
        mechanisms = {
            "race": "Race Condition",
            "leak": "Resource Leak",
            "crash": "Runtime Exception",
            "corrupt": "Data Corruption",
            "deadlock": "Deadlock",
            "overflow": "Buffer Overflow",
            "timeout": "Timeout",
            "inconsistent": "State Inconsistency",
        }
        
        for keyword, mechanism in mechanisms.items():
            if keyword in inverted:
                return mechanism
        
        return "Unknown Mechanism"
    
    def fault_tree_analysis(self, vectors: List[Dict]) -> Dict:
        """
        Perform Fault Tree Analysis on failure vectors.
        Calculate probability of top-level events using OR/AND gates.
        """
        if not vectors:
            return {"top_event_probability": 0, "critical_paths": []}
        
        # OR gate: P(A OR B) = P(A) + P(B) - P(A)P(B)
        def or_gate(probabilities: List[float]) -> float:
            result = 0
            for p in probabilities:
                result = result + p - (result * p)
            return result
        
        # AND gate: P(A AND B) = P(A) * P(B)
        def and_gate(probabilities: List[float]) -> float:
            result = 1
            for p in probabilities:
                result *= p
            return result
        
        # Group by component
        by_component = {}
        for v in vectors:
            comp = v.get("component", "Unknown")
            if comp not in by_component:
                by_component[comp] = []
            by_component[comp].append(v["probability"])
        
        # Calculate per-component failure probability (OR gate)
        component_probs = {
            comp: or_gate(probs) for comp, probs in by_component.items()
        }
        
        # Top event: any component fails (OR gate)
        top_event = or_gate(list(component_probs.values()))
        
        # Identify critical paths (highest risk)
        critical = sorted(vectors, key=lambda x: x.get("risk_score", 0), reverse=True)[:5]
        
        return {
            "top_event_probability": round(top_event, 4),
            "component_probabilities": {k: round(v, 4) for k, v in component_probs.items()},
            "critical_paths": [
                {"description": v["description"], "risk_score": v["risk_score"]}
                for v in critical
            ]
        }


# ═══════════════════════════════════════════════════════════════════════════════
# MULTI-AGENT SYSTEM ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════════

class MultiAgentSystem:
    """
    The orchestrator that coordinates all agents.
    
    From the Blueprint:
    "This decoupling allows the Axiom Inverter to propose a logical fallacy,
     which the Pattern Recognizer then validates against the codebase,
     and the PRA Agent finally quantifies."
    """
    
    def __init__(self, db_path: str = ":memory:"):
        self.blackboard = Blackboard(db_path)
        self.agents: List[Agent] = []
        self.running = False
    
    def add_agent(self, agent_class: type) -> Agent:
        """Add an agent to the system"""
        agent = agent_class(self.blackboard)
        self.agents.append(agent)
        return agent
    
    def start(self):
        """Start all agents"""
        print("═" * 60)
        print("  🧠 MULTI-AGENT SYSTEM - Starting")
        print("═" * 60)
        
        self.running = True
        for agent in self.agents:
            agent.start()
        
        print(f"  ✅ {len(self.agents)} agents started")
        print("═" * 60)
    
    def stop(self):
        """Stop all agents"""
        self.running = False
        for agent in self.agents:
            agent.stop()
        
        for agent in self.agents:
            agent.join(timeout=2.0)
        
        print("\n✅ All agents stopped")
    
    def add_axiom(self, component: str, statement: str, domain: str = None) -> int:
        """Add an axiom to be analyzed"""
        return self.blackboard.add_axiom(component, statement, domain)
    
    def add_axioms_bulk(self, axioms: List[Dict]):
        """Add multiple axioms"""
        for axiom in axioms:
            self.add_axiom(
                component=axiom.get("component", "Unknown"),
                statement=axiom["statement"],
                domain=axiom.get("domain")
            )
    
    def wait_for_analysis(self, timeout: float = 10.0):
        """Wait for agents to complete analysis"""
        start = time.time()
        last_count = 0
        stable_for = 0
        
        while time.time() - start < timeout:
            stats = self.blackboard.get_statistics()
            current = stats["failure_vectors"]
            
            if current == last_count:
                stable_for += 0.5
                if stable_for >= 2.0:  # Stable for 2 seconds
                    break
            else:
                stable_for = 0
                last_count = current
            
            time.sleep(0.5)
    
    def get_report(self) -> Dict:
        """Get the full analysis report"""
        return self.blackboard.export_report()
    
    def print_summary(self):
        """Print analysis summary"""
        stats = self.blackboard.get_statistics()
        vectors = self.blackboard.get_all_failure_vectors()
        
        print("\n" + "═" * 60)
        print("  📊 ANALYSIS SUMMARY")
        print("═" * 60)
        print(f"  Axioms Analyzed:  {stats['total_axioms']}")
        print(f"  Axioms Inverted:  {stats['inverted_axioms']}")
        print(f"  Failure Vectors:  {stats['failure_vectors']}")
        print(f"  Average Risk:     {stats['avg_risk_score']:.3f}")
        print(f"  Maximum Risk:     {stats['max_risk_score']:.3f}")
        print("═" * 60)
        
        if vectors:
            print("\n  🚨 TOP FAILURE VECTORS:")
            for i, v in enumerate(vectors[:5], 1):
                risk = v["risk_score"]
                level = "🔴" if risk > 0.6 else "🟡" if risk > 0.3 else "🟢"
                print(f"  {i}. {level} [{risk:.2f}] {v['description'][:50]}...")
        
        print("═" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point"""
    import sys
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗ ██╗   ██╗██████╗ ███████╗    ██████╗ ██╗   ██╗████████╗██╗  ██╗   ║
║   ██╔══██╗██║   ██║██╔══██╗██╔════╝    ██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║   ║
║   ██████╔╝██║   ██║██████╔╝█████╗      ██████╔╝ ╚████╔╝    ██║   ███████║   ║
║   ██╔═══╝ ██║   ██║██╔══██╗██╔══╝      ██╔═══╝   ╚██╔╝     ██║   ██╔══██║   ║
║   ██║     ╚██████╔╝██║  ██║███████╗    ██║        ██║      ██║   ██║  ██║   ║
║   ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝   ║
║                                                                              ║
║               MULTI-AGENT SYSTEM - ZERO DEPENDENCIES                        ║
║                      Standard Library Only                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Create system
    mas = MultiAgentSystem()
    
    # Add agents
    mas.add_agent(AxiomInverterAgent)
    mas.add_agent(PatternRecognizerAgent)
    mas.add_agent(PRAAgent)
    
    # Start agents
    mas.start()
    
    # Demo: Add some axioms to analyze
    demo_axioms = [
        {"component": "FileSystem", "statement": "File writes are atomic and consistent", "domain": "storage"},
        {"component": "Memory", "statement": "Objects are deallocated when no longer referenced", "domain": "memory"},
        {"component": "Network", "statement": "API calls will always receive a response", "domain": "network"},
        {"component": "Cache", "statement": "Cached data is always fresh and valid", "domain": "storage"},
        {"component": "Auth", "statement": "Tokens are secure and cannot be forged", "domain": "security"},
        {"component": "Database", "statement": "Transactions are isolated and serializable", "domain": "storage"},
        {"component": "Scheduler", "statement": "Tasks execute in the order they are submitted", "domain": "concurrency"},
        {"component": "UI", "statement": "State updates are synchronous and immediate", "domain": "runtime"},
    ]
    
    print("\n📥 Loading axioms for analysis...")
    mas.add_axioms_bulk(demo_axioms)
    
    # Wait for analysis
    print("⏳ Analyzing...")
    mas.wait_for_analysis(timeout=10.0)
    
    # Print summary
    mas.print_summary()
    
    # Export report
    report = mas.get_report()
    report_path = Path.home() / ".trinity" / "mas_report.json"
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📄 Full report saved to: {report_path}")
    
    # Stop agents
    mas.stop()


if __name__ == "__main__":
    main()
