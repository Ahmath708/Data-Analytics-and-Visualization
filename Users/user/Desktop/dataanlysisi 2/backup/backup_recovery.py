import pandas as pd
import shutil
import os
from datetime import datetime
import hashlib
import json

DATA_PATH = 'C:/Users/user/Desktop/dataanlysisi 2/data/dataset.xlsx'
BACKUP_PATH = 'C:/Users/user/Desktop/dataanlysisi 2/backup/'
ARCHIVE_PATH = BACKUP_PATH + 'archives/'

def create_backup():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'{ARCHIVE_PATH}backup_{timestamp}.xlsx'
    
    if not os.path.exists(ARCHIVE_PATH):
        os.makedirs(ARCHIVE_PATH)
    
    shutil.copy2(DATA_PATH, backup_file)
    
    file_hash = calculate_hash(backup_file)
    
    metadata = {
        'backup_date': timestamp,
        'file': backup_file,
        'hash': file_hash,
        'size': os.path.getsize(backup_file)
    }
    
    with open(BACKUP_PATH + 'backup_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Backup created: {backup_file}")
    print(f"File hash: {file_hash}")
    return backup_file, metadata

def calculate_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def verify_backup(backup_file):
    if os.path.exists(backup_file):
        current_hash = calculate_hash(backup_file)
        print(f"Backup verified: {current_hash}")
        return True
    return False

def list_backups():
    if not os.path.exists(ARCHIVE_PATH):
        print("No backups found")
        return []
    
    backups = []
    for f in os.listdir(ARCHIVE_PATH):
        if f.endswith('.xlsx'):
            full_path = os.path.join(ARCHIVE_PATH, f)
            backups.append({
                'file': f,
                'date': datetime.fromtimestamp(os.path.getctime(full_path)),
                'size': os.path.getsize(full_path)
            })
    return sorted(backups, key=lambda x: x['date'], reverse=True)

def restore_backup(backup_file, restore_path=None):
    if restore_path is None:
        restore_path = DATA_PATH
    
    if os.path.exists(backup_file):
        shutil.copy2(backup_file, restore_path)
        print(f"Restored from: {backup_file}")
        return True
    return False

def export_to_csv():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    export_path = BACKUP_PATH + f'export_{timestamp}/'
    
    os.makedirs(export_path, exist_ok=True)
    
    excel = pd.ExcelFile(DATA_PATH)
    for sheet in excel.sheet_names:
        df = pd.read_excel(DATA_PATH, sheet_name=sheet)
        df.to_csv(f"{export_path}{sheet}.csv", index=False)
    
    print(f"Data exported to: {export_path}")
    return export_path

def get_data_summary():
    excel = pd.ExcelFile(DATA_PATH)
    summary = {}
    
    for sheet in excel.sheet_names:
        df = pd.read_excel(DATA_PATH, sheet_name=sheet)
        summary[sheet] = {
            'rows': len(df),
            'columns': len(df.columns),
            'columns_list': list(df.columns)
        }
    
    print("\nData Summary:")
    for sheet, info in summary.items():
        print(f"\n{sheet}: {info['rows']} rows, {info['columns']} columns")
    
    return summary

if __name__ == '__main__':
    print("=" * 50)
    print("DATA BACKUP AND RECOVERY TOOL")
    print("=" * 50)
    
    print("\n1. Create Backup")
    backup_file, metadata = create_backup()
    
    print("\n2. Verify Backup")
    verify_backup(backup_file)
    
    print("\n3. Export to CSV")
    export_path = export_to_csv()
    
    print("\n4. Data Summary")
    get_data_summary()
    
    print("\n" + "=" * 50)
    print("Backup operations completed!")
    print("=" * 50)