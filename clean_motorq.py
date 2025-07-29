import pandas as pd
import json
from tqdm import tqdm

CSV_PATH = "Test_Case_dataCleaning/Test_Case_dataCleaning.csv"
CHUNK_SIZE = 5000
OUTPUT_ROWS = 1000

all_rows = []
unique_attrs = set()

reader = pd.read_csv(CSV_PATH, chunksize=CHUNK_SIZE)

for chunk in reader:
    for idx, row in tqdm(chunk.iterrows(), total=len(chunk), desc="Parsing JSON rows"):
        raw_json = row.get("BODY_CLEANED")
        try:
            full_record = json.loads(raw_json)

            meta = full_record.get("meta", {})
            poller_fetch_time = meta.get("pollerFetchTime")

            timestamp = full_record.get("timestamp")  
            vin_list = full_record.get("vinList", [])

            if not vin_list:
                continue 

            vin_entry = vin_list[0]
            vin = vin_entry.get("vin")
            status_timestamp_obj = vin_entry.get("statusTimestamp", {})
            status_timestamp = status_timestamp_obj.get("time", timestamp)

            status_data = vin_entry.get("statusData", [])

            record = {
                "VIN": vin,
                "statusTimestamp": status_timestamp,
                "pollerFetchTime": poller_fetch_time
            }

            for item in status_data:
                attr = item.get("attribute")
                val = item.get("value")
                if attr is not None:
                    record[attr] = val
                    unique_attrs.add(attr)

            all_rows.append(record)

        except Exception as e:
            print(f"Error parsing row {idx}: {e}")
            continue

        if len(all_rows) >= OUTPUT_ROWS:
            break

    if len(all_rows) >= OUTPUT_ROWS:
        break

df = pd.DataFrame(all_rows)
print(df.columns)
df2=df[['VIN','statusTimestamp','pollerFetchTime','odometer','gasLevel','ignStatus','speed']]
df2.to_csv("FinalTable.csv",index=False)