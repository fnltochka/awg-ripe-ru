import requests
import requests_cache
import json
import datetime
from concurrent.futures import ProcessPoolExecutor
from netaddr import IPRange, cidr_merge, IPNetwork
from rich.progress import track

URL = "https://stat.ripe.net/data/country-resource-list/data.json?resource=RU"
FILE_NAME = "build/runet.json"
FILE_NAME_REDUCED = "build/runet_reduced.json"
FILE_NAME_REDUCED_16 = "build/runet_reduced_16.json"
FILE_NAME_REDUCED_8 = "build/runet_reduced_8.json"

def get_ipv4_list():
    expire_after = datetime.timedelta(hours=1)
    requests_cache.install_cache('cache/ripe-ru', expire_after=expire_after)
    response = requests.get(URL)
    data = response.json()
    return data["data"]["resources"]["ipv4"]


def process_ip(ip):
    if "-" in ip:
        start_ip, end_ip = ip.split("-")
        ip_range = IPRange(start_ip, end_ip)
        return [str(cidr) for cidr in cidr_merge(list(ip_range))]
    else:
        return [ip]

def reduce_mask(ip_list):
    ip_networks = [IPNetwork(ip) for ip in ip_list]
    merged_networks = cidr_merge(ip_networks)
    reduced_list = [str(network) for network in merged_networks]
    return reduced_list

def reduce_mask_n(ip_list, n):
    reduced_list = []
    for ip in ip_list:
        ip_network = IPNetwork(ip)
        ip_network.prefixlen = n
        reduced_list.append(str(ip_network))
    reduced_list_n = reduce_mask(reduced_list)
    return reduced_list_n

def process_ips(ipv4_list):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_ip, ipv4_list))
        return [ip for result in results for ip in result]

def process_range(ip):
    return {"hostname": ip, "ip": ""}

def process_ranges(ip_list):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_range, ip_list))
        return results

def write_to_file(result, file_name):
    with open(file_name, "w") as f:
        json.dump(result, f)

def main():
    ipv4_list = get_ipv4_list()
    ip_list = process_ips(track(ipv4_list, description="Обработка ipv4_list"))
    write_to_file(process_ranges(ip_list), FILE_NAME)
    reduced_ip_list = reduce_mask(track(ip_list, description="Уменьшение маски"))
    write_to_file(process_ranges(reduced_ip_list), FILE_NAME_REDUCED)
    reduced_ip_list = reduce_mask_n(track(ip_list, description="Уменьшение маски до 16"), 16)
    write_to_file(process_ranges(reduced_ip_list), FILE_NAME_REDUCED_16)
    reduced_ip_list = reduce_mask_n(track(ip_list, description="Уменьшение маски до 8"), 8)
    write_to_file(process_ranges(reduced_ip_list), FILE_NAME_REDUCED_8)


if __name__ == "__main__":
    main()
