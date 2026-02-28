# Sub-Agent Task Template

## Before Starting (Must Do)

1. **Read existing code style**
   - Read target project's main.py or similar
   - Understand class structure and method patterns

2. **Get project context**
   - What is this project for?
   - What is the existing functionality?
   - What is the coding style?

## Task Distribution Template

```
## Project: [Project Name]
## Location: [Path]

### Code Style Found:
- Class naming: [e.g., Road3D, PhotoManager]
- Method style: [e.g., add_xxx(), get_xxx()]
- Data storage: [e.g., self.xxx = []]

### Your Task:
1. [Specific task 1]
2. [Specific task 2]
3. [Specific task 3]

### Requirements:
- Follow existing code style exactly
- Integrate with existing modules
- Test after completion
- Direct execution, no questions

### Verification:
Run: python [main file]
Expected: [what should work]
```

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Timeout | 60s too short | Use 120s |
| No context | Didn't read code | Read first |
| Asking too much | Not explicit enough | Give direct instructions |
| Files not created | Encoding issues | Use ASCII in code |
| Import errors | Module not found | Check PYTHONPATH |

## Workflow

1. **Analyze** → Read existing code
2. **Plan** → Understand what to do
3. **Execute** → Write code directly
4. **Verify** → Run and test
5. **Report** → Summarize what was done
