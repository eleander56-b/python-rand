# Math Experiments

Mathematical experiments in Python: Collatz conjecture explorer and large number demonstrations.

## Installation

```bash
pip install -e .
```

## Scripts

### Collatz Conjecture Explorer

Generates random starting numbers and runs them through the Collatz sequence (3x+1 problem), counting how many steps each takes to reach 1.

```bash
collatz --help
collatz --max-trials 1000 --no-email
collatz --upper-bound 1000000 --threshold 500
```

**Email alerts:** When a number exceeds the step threshold (default: 5000), an email alert is sent. Configure via environment variables (see `.env.example`):

```bash
cp .env.example .env
# Edit .env with your SMTP credentials
```

**Temperature monitoring (Linux only):** Requires `lm-sensors` (`sudo apt install lm-sensors`). Pauses execution if CPU temperature exceeds 70°C.

### Googolplex

Demonstrates the scale of large powers of 10, from feasible computations to the theoretical googolplex.

```bash
googolplex --help
googolplex --exponent 10000
```

## Development

```bash
pip install -e .
pip install ruff mypy pytest

# Run tests
pytest -v

# Lint
ruff check src/ tests/

# Type check
mypy src/
```
