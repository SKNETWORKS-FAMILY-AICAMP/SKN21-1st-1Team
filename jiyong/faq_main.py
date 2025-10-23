from faq_csv_reader import read_faq_csv
from faq_db_writer import recreate_faq_table, save_faq_to_db

def main():
    recreate_faq_table()
    df = read_faq_csv()
    save_faq_to_db(df)

if __name__ == "__main__":
    main()
