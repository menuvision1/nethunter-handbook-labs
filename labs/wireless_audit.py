"""Offline synthetic configuration exercise. No radio or network access."""
import csv
import sys

def audit(path):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        required = {'bssid','ssid','role','approved','security','pmf','wps'}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError('Missing required CSV columns')
        rows = list(reader)
    if not rows:
        raise ValueError('Empty evidence is not a successful assessment')
    deviations = unknown = 0
    seen = set()
    for row in rows:
        if any(not row.get(k) for k in required):
            raise ValueError('Incomplete evidence row')
        if row['bssid'] in seen:
            raise ValueError('Duplicate BSSID requires investigation')
        seen.add(row['bssid'])
        if row['approved'] not in {'yes','no'}:
            raise ValueError('approved must be yes or no')
        if row['approved'] == 'no':
            unknown += 1
        elif row['role'] == 'staff':
            deviations += sum(row[k] != v for k,v in
                              [('security','WPA3-Personal'),('pmf','required'),('wps','disabled')])
    return deviations, unknown

if __name__ == '__main__':
    d,u = audit(sys.argv[1])
    print(f'approved_staff_deviations={d}')
    print(f'unrecognized_bssids={u}')
    print('segmentation=not_tested')
