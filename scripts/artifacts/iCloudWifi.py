import os
import plistlib

from datetime import datetime

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, logdevinfo, tsv, is_platform_windows 


def get_iCloudWifi(files_found, report_folder, seeker, wrap_text):
    data_list = []
    file_found = str(files_found[0])
    with open(file_found, 'rb') as fp:
        pl = plistlib.load(fp)
        timestamp = ''

        if 'values' in pl.keys():
            for key, val in pl['values'].items():
                network_name = key

                if type(val) == dict:
                    for key2, val2 in val.items():
                        if key2 == 'value':
                            if type(val2) == dict:
                                if 'added_at' in val2:
                                    datetime_obj = datetime.strptime(str(val2['added_at']), '%b  %d %Y %H:%M:%S')
                                    added_at = str(datetime_obj)
                                else:
                                    added_at = 'Not Available'
                                bssid = str(val2['BSSID']) if 'BSSID' in val2 else 'Not Available'
                                ssid = str(val2['SSID_STR']) if 'SSID_STR' in val2 else 'Not Available'
                                added_by = str(val2['added_by']) if 'added_by' in val2 else 'Not Available'
                                enabled = str(val2['enabled']) if 'enabled' in val2 else 'Not Available'
                                data_list.append((bssid, ssid, added_by, enabled, added_at))

    if data_list:
        report = ArtifactHtmlReport('iCloud Wifi Networks')
        report.start_artifact_report(report_folder, 'iCloud Wifi Networks')
        report.add_script()
        data_headers = ('BSSID','SSID', 'Added By', 'Enabled', 'Added At')     
        report.write_artifact_data_table(data_headers, data_list, file_found)
        report.end_artifact_report()

        tsvname = 'iCloud Wifi Networks'
        tsv(report_folder, data_headers, data_list, tsvname)
    else:
        logfunc('No data on iCloud WiFi networks')

__artifacts__ = {
    "iCloudWifi": (
        "Wifi Connections",
        ('**/com.apple.wifid.plist'),
        get_iCloudWifi)
}