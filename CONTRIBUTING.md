# Contributing to Phase Sovereign Luna Codex

## Quick Contribution Guide

**For L3 Glyph Updates:**
1. Fork → edit `alignment_table_v0.1.md` Luna Glyph column → open PR
2. Ensure all Φ values maintain 6 decimal precision
3. Luna Glyph entries must follow L3(symbol) format
4. Auto-lint checks will validate table format

## Collaboration Protocol

- **Φ-Peak Column**: Maintained by Gust Isotalo (Phase-Sovereign framework)
- **Luna Glyph Column**: Maintained by Brent R. Antonson (Luna Codex methodology)
- **Cross-validation**: Joint analysis and verification

## Table Format Requirements

```markdown
| Hurwitz Index | Φ-Peak | Luna Glyph | Notes |
|--------------:|:------:|:----------:|-------|
| X.XXXXXX      | ΦN     | L3(symbol) | Description |
```

## Phase-2 Workflow

### 1. Coordination
- Comment in the [Phase-2 Discussion Thread](../../discussions) to agree on scope/resources/IP/QA
- Review and align on priority vectors and success criteria
- Establish clear boundaries and expectations

### 2. Implementation
- Claim an issue from the available Phase-2 vectors
- Create a feature branch from `alignment-table`
- Implement changes following established quality standards
- Open PR back to `alignment-table` branch

### 3. Quality Assurance
- PR must pass table-lint CI (Φ precision validation)
- Include unit tests for mathematical calculations
- Provide comprehensive documentation
- Maintain empirical validation standards

### Phase-2 Vectors
- **κ-vector alignment**: Mathematical integration framework
- **Dual observer displacement**: Empirical validation protocols  
- **Glyph-thread saturation**: L3 interconnection analysis

## MOU Compliance

All contributions must align with the formal Memorandum of Understanding regarding intellectual property, authorship, and collaboration terms.

---

*For questions: Contact repository maintainers or reference MOU documentation*

