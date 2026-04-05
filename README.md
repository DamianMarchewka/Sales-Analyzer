# Sales Analizer

## Project Overview

This project is a high-performance **Sales Data Validation Tool** designed to ensure data integrity before downstream processing.

### Core Capabilities:
*   **Double Validation**: Checks both data schema (structure) and individual records (content).
*   **Quality Control**: Provides detailed error reporting and strict enforcement via error-rate thresholds.
*   **Clean Architecture**: Built with a clear separation between business logic and data handling, ensuring the codebase is modular, testable, and easy to maintain.


## Key Features

- **Structural Validation**: Ensures all required columns are present.
- **Record-Level Validation**: Validates types and constraints (dates, non-empty products, positive prices).
- **Quality Gates**: Configurable `strict_threshold` to abort processing if the error rate is too high.
- **Detailed Reporting**: Granular error messages per row for easy debugging.
- **Clean Separation**: Distinct handling of valid and invalid records.
- **Full Test Coverage**: Robust test suite using `pytest`.

## Tech Stack

- **Language:** Python 3.12
- **Data Handling:** [pandas](https://pydata.org)
- **Validation:** [Pydantic V2](https://pydantic.dev)
- **Testing:** [pytest](https://pytest.org)

## Quick Start

### Installation

1. **Clone the repository:**
```
```bash
git clone <https://github.com/DamianMarchewka/Sales-Analyzer>
cd sales-data-validation
```


Set up virtual environment:
```
bash
python -m venv venv
source venv/bin/activate #Linux/McOS
venv\Scripts\activate #Windows
```


Install dependencies:
```
bash
pip install -r requirements.txt
```


Usage Example
```
python
import pandas as pd
from src.validator import SalesValidator
```

# Sample data
```
df = pd.DataFrame([
    {"date": "2024-01-02", "product": "keyboard", "quantity": 1, "price": 10},
    {"date": "2024-01-02", "product": "", "quantity": 1, "price": -5} # Invalid
])
```

# Initialize validator with 10% error threshold
```
validator = SalesValidator(strict_threshold=0.1)
result = validator.validate(df)

if result.is_valid:
    print(f"Validated records: {len(result.valid_data)}")
else:
    print(f"Errors found: {result.errors}")
```

## Architecture
The project follows Clean Architecture layers to ensure low coupling:
- Domain (Validation): Pydantic models defining core business rules (e.g., price ≥ 0, non-future dates).
- Application (Use Case): Logic for iterating over data, calculating error rates, and enforcing thresholds.
- Infrastructure: Data loading and transformation (pandas).
- Interface (Future): API/CLI entry points.

## Error Handling

| Error Category | Logic | System Behavior |
| :--- | :--- | :--- |
| **Structure Error** | Missing or renamed columns | Raises `ValueError` immediately |
| **Record Error** | Validation failed (e.g., negative price) | Collected and returned in the report |
| **Threshold Exceeded** | Invalid records > `strict_threshold` | Aborts processing with `ValueError` |



## Testing
- The project uses pytest to ensure reliability. 
- Tests cover edge cases like empty strings, future dates, and threshold limits.
Run tests with verbosity:
```
bash
pytest -v
```

## Project Status

The project is currently in the **Active Development** phase. Core validation logic and unit testing are completed, with a focus now shifting towards integration and API exposure.

## Roadmap & Future Improvements

### Phase 1: Core (Completed)
- [x] Initial validation logic (structure + records)
- [x] Implementation of `strict_threshold` logic
- [x] Comprehensive unit test suite with `pytest`
- [x] Basic Clean Architecture layer separation

### Phase 2: Integration (In Progress)
- [ ] **REST API**: Implementation using **FastAPI**
- [ ] **DTO Design**: Refactoring input/output contracts for better type safety
- [ ] **Containerization**: Adding `Dockerfile` for easy deployment

### Phase 3: Advanced Features (Planned)
- [ ] **Sales Analytics**: Insights like best/worst performing products
- [ ] **Data Quality Dashboard**: Visual metrics for error rates
- [ ] **Async Support**: Processing large CSV files asynchronously
- [ ] **Export Options**: Support for PDF/JSON validation reports
