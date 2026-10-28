from src.extract_load import main as extract_load
from src.clean_data import main as clean_data

if __name__ == "__main__":
    extract_load()
    clean_data()
    print("Pipeline completed successfully.")
