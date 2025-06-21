# CSV Processor

## Instructions
1. Clone the repository:
```bash
git clone git clone https://github.com/hamidullaorifov/CSV-Processor.git
cd CSV-Processor
```
2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
## Running the Script
```bash
python main.py --file products.csv --where "brand==apple" --order-by "price=desc"
```
![image](https://github.com/user-attachments/assets/a1ce0492-93f4-474f-9392-e30a2752bc3b)


## Running tests
```bash
pytest --cov=csv_processor
```
![image](https://github.com/user-attachments/assets/b6616b72-624b-41c9-bdf3-5aca890b4424)


