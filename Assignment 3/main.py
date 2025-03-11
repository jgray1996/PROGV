from src.file_reader import GenbankReader
from src.genbank_parser import GenbankParser
from src.database_handler import DatabaseHandler
from src.config_handler import ConfigHandler
from src.init_db import DBCreater

CONFIG_PATH = "config.yaml"

if __name__ == "__main__":
    config_h = ConfigHandler()
    config = config_h.read_config(CONFIG_PATH)
    db_handler = DatabaseHandler()

    if config.get("init"):
        db_creater = DBCreater(config.get("db_name"),
                               config.get("sql_script"))
        db_creater.execute()

    reader = GenbankReader(config_object=config)
    parser = GenbankParser()
    db_handler.connect(config.get("db_name"))

    print("Parsing genbank records")
    for record in reader.read_files():
        r = parser.parse_record(record)
        db_handler.insert_ncbi_data(r)