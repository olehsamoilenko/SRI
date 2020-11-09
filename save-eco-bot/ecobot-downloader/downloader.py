#!/usr/bin/python3

import os
from datetime import datetime
import requests
import http
import time

def log(text: str):
    lf = open('log.txt', mode='a+')
    lf.write("{} | {}\n".format(datetime.now(), text))
    lf.close()

def load_page(id: int, path: str):
    try:
        resp = requests.get("https://www.saveecobot.com/en/station/{}".format(id))
    except requests.ConnectionError:
        log("Connection error, id: {} :(".format(id))
        time.sleep(10)
    except http.client.RemoteDisconnected:
        log("RemoteDisconnected, id: {} :(".format(id))
        time.sleep(10)
    if resp.status_code == 200:
        f = open('{}/{}.html'.format(path, id), 'w')
        f.write(resp.text)
        f.close()
    else:
        log("{}: code {}".format(id, resp.status_code))

def load_kyiv_pages():
    kyiv_ids = [28, 30, 43, 47, 108, 109, 902, 914, 915, 968, 1004, 1041, 1061, 1062, 1063, 1064, 
    1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1083, 1098, 1105, 1107, 1115, 1126, 1127, 1128, 
    1152, 1160, 1161, 1193, 1208, 1274, 1278, 1290, 1294, 1306, 1330, 1331, 1353, 1372, 1373, 1376, 1387, 
    1394, 1415, 1424, 1425, 1437, 1516, 1540, 1544, 1549, 1553, 1556, 1651, 2741, 2762, 2781, 2792, 
    2806, 2809, 2827, 2867, 2878, 2903, 2924, 2925, 2947, 2973, 3016, 3018, 3070, 3084, 3111, 3112, 
    3231, 3239, 3306, 3396, 3398, 3401, 3422, 3432, 3483, 3492, 3497, 3498, 3504, 3514, 3535, 3541, 
    3547, 3572, 3573, 3583, 3600, 3601, 3603, 3619, 3620, 3621, 3622, 3641, 3652, 3653, 3658, 3665, 
    3669, 3678, 3682, 3684, 3685, 3686, 3687, 3688, 3689, 3690, 3692, 3693, 3694, 3702, 3709, 4042, 
    4053, 4063, 4068, 4139, 4169, 4191, 4193, 4201, 4211, 4219, 4230, 4232, 4252, 11785, 12829, 12905, 
    12907, 12909, 12910, 12911, 12912, 12914, 12917, 12918, 12920, 12921, 12923, 12924, 12925, 12926, 
    12927, 12928, 12929, 12930, 12931, 12932, 12933, 12934, 12935, 12936, 12937, 12938, 12939, 12940, 
    12941, 12944, 12945, 12946, 12947, 12948, 12951, 12952, 12954, 12957, 12958, 12978, 12982, 12989, 
    12991, 12992, 13020, 13026, 13028, 13055, 13141, 13207, 13208, 13268, 13368, 13388, 13407, 13413, 
    13422, 13441, 13455, 13673, 13703, 13759, 13789, 13802, 13803, 13811, 13820, 13853]

    log("Woke up")
    path = "./{}".format(datetime.now().strftime('%Y-%m-%dT%H-%M'))
    os.mkdir(path)
    for id in kyiv_ids:
        load_page(id, path)
    log("Done.")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    load_kyiv_pages()
