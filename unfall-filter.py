import argparse
import csv

parser = argparse.ArgumentParser(
                    prog='filter',
                    description='Filter Gemeinde',
                    epilog='License MIT, Copyright Hans Busch')
parser.add_argument('input')           # positional argument
parser.add_argument('output')           # positional argument
parser.add_argument('-k', '--key')      # option that takes a value
args = parser.parse_args()
keys = args.key.split(' ')
if len(keys) < 3:
    print("Provide blank separated <land> <kreis> <gemeinde>")
    exit()

print("keys %s %s %s", keys[0], keys[1], keys[2])

with open(args.input, 'r') as file:
    reader = csv.DictReader(file, delimiter=';')
    header = next(reader)  # Skip header row
    data = [row for row in reader if int(row['ULAND']) == int(keys[0]) and int(row['UREGBEZ']) == int(keys[1]) and int(row['UKREIS']) == int(keys[2])]  

# with open(args.output, 'w', newline='') as file:
#     writer = csv.writer(file, delimiter=';')
#     writer.writerow(header)
#     writer.writerows(data)

# print("Filtered Data:")
# for row in filtered_data:
#     print(row)

# Date;Time;Millis;Latitude;Longitude;Altitude; \
#   Course;Speed;HDOP;Satellites;BatteryLevel;Left;Right;Confirmed;Marked;Invalid; \
#   insidePrivacyArea;Factor;Measurements;Tms1;Lus1;Rus1;Tms2;Lus2;Rus2; \
#   Tms3;Lus3;Rus3;...;Tms60;Lus60;Rus60
otop = ['OBSDataFormat=2', 'OBSFirmwareVersion=v0.18-dev', 'DeviceId=e82a', 'DataPerMeasurement=3','MaximumMeasurementsPerLine=30',
        'OffsetLeft=30','OffsetRight=30','NumberOfDefinedPrivacyAreas=0','TrackId=5c0b301b-0f56-e74c-7c93-637282ab1831','PrivacyLevelApplied=AbsolutePrivacy',
        'MaximumValidFlightTimeMicroseconds=18560','BluetoothEnabled=1','PresetId=default','TimeZone=GPS','DistanceSensorsUsed=HC-SR04/JSN-SR04T']
oheader = ['Date','Time','Millis','Comment','Latitude','Longitude','Altitude', \
   'Course','Speed','HDOP','Satellites','BatteryLevel','Left','Right','Confirmed','Marked','Invalid', \
   'InsidePrivacyArea','Factor','Measurements','Tms1','Lus1','Rus1','Tms2','Lus2','Rus2', \
   'Tms3','Lus3','Rus3']
obs = []
obs.append(otop)
obs.append(oheader)
for x in range(0, len(data)):
    d = data[x]
    date = '01.'+ d['UMONAT'] + '.' + d['UJAHR']
    time = d['USTUNDE'] + ':00:00'
    ist = ''
    if d['IstRad'] == '1':
        ist += 'R'
    if d['IstPKW'] == '1': 
        ist += 'P'
    if d['IstFuss'] == '1':
        ist += 'F'
    if d['IstKrad'] == '1':
        ist += 'K'
    if 'IstGkfz' in d.keys() and d['IstGkfz'] == '1':
        ist += 'L'
    if 'IstSonstige' in d.keys() and d['IstSonstige'] == '1':
        ist += 'S'
    lat = d['YGCSWGS84'].replace(',', '.')
    lon = d['XGCSWGS84'].replace(',', '.')
    obs.append([date, time, '0', 'KAT:'+d['UKATEGORIE']+' ART:'+d['UART']+' TYP:'+d['UTYP1']+' IST:'+ist, lat, lon, 300, 240, 11, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0])

with open(args.output, 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(obs)
