# Log: [UC/Task Name]

**Date:** YYYY-MM-DD  
**Owner:** [Name]  
**UC:** [e.g. UC5 - Search]  
**Techniques:** [e.g. Structured + Few-shot]

## Version 1: Baseline

**Prompt:** [paste]  
**Result:** [summary]  
**Tests:** ✓/✗ (which passed/failed)  
**Bandit:** ✓/✗  
**Pylint:** X.X/10  
**Bugs:** [list]

## Version 2: Refined

**Changes:** [list]  
**Result:** [better?]  
**Tests:** ✓/✗  
**Bugs:** [list]

## Comparison

| Metric  | v1  | v2  | Improvement |
|---------|-----|-----|-------------|
| Tests   | 4/7 | 7/7 | ✓           |
| Bandit  | 3   | 0   | ✓           |
| Pylint  | 7.2 | 9.1 | ✓           |

## Decision
✓ ACCEPT v2 → Integrate  
Commit: `feat(uc): implement X with LLM v2`
