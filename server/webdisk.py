# df api. returns a json blob with storage device information from hosts.

from fabric import Connection
import math

hostlist = ('192.168.1.10', '192.168.1.11')
SSH_USER = 'username'
SSH_KEY_DIR = 'ssh/id_rsa'

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def disk_stats(host):
    df_command = "df -k --total | awk '{print $1,$2,$3,$5,$6}' | grep -e '^/dev/*' -e 'total'"
    return host.run(df_command, hide=True).stdout.strip()

def get_disk_info():
    storage_total_capacity = 0
    storage_total_used = 0

    disk_info = []

    for host in hostlist:
        # SSH key auth must be configured on remote hosts
        conn = Connection(host, SSH_USER, connect_kwargs={'key_filename':[SSH_KEY_DIR]})
        disks = disk_stats(conn)
        devices = disks.splitlines()

        print(f"[ DISK INFO: {host} ]")

        storage_local_capacity = 0
        storage_local_used = 0
        storage_device_info = []

        for storage_device in devices:
            device_info = storage_device.split()
            filesystem = device_info[0]
            size = int(int(device_info[1])/1024)
            used = int(int(device_info[2])/1024)
            used_perc = device_info[3]
            mount_point = device_info[4]

            total_devices = len(devices)-1
            size_in_bytes = size * (1024**2)
            used_in_bytes = used * (1024**2)
            available_in_bytes = size_in_bytes - used_in_bytes
            size_conv = convert_size(size_in_bytes)
            used_conv = convert_size(used_in_bytes)
            available_conv = convert_size(available_in_bytes)

            storage_device = {
                'filesystem': filesystem,
                'mount_location': mount_point,
                'space_available': available_conv,
                'space_used': used_conv,
                'space_size': size_conv,
                'space_percentage': used_perc,
                'root': 'false'
            }
            storage_device_info.append(storage_device)

            if mount_point == '/':
                storage_device['root'] = 'true'
                print(f"ROOT DISK: {filesystem} @ {mount_point}\n\t{used_conv} used of {size_conv} ({used_perc})\n\t{available_conv} free")
            else:
                if filesystem != 'total':
                    print(f"DISK: {filesystem} @ {mount_point}\n\t{used_conv} used of {size_conv} ({used_perc})\n\t{available_conv} free")

        if filesystem == 'total':
            print(f"SUMMARY: \nFound {total_devices} mount points\n{used_conv} used of {size_conv} ({used_perc})\nAVAILABLE: {available_conv}\n")
            host_info = {
                        'host': host,
                        'storage_devices': storage_device_info,
                        'device_count': total_devices
            }
            disk_info.append(host_info)

            storage_total_capacity += size
            storage_total_used += used

    storage_total_capacity_in_bytes = storage_total_capacity * (1024**2)
    storage_total_used_in_bytes = storage_total_used * (1024**2)
    storage_total_avail_in_bytes = storage_total_capacity_in_bytes - storage_total_used_in_bytes

    total_capacity_conv = convert_size(storage_total_capacity_in_bytes)
    total_used_conv = convert_size(storage_total_used_in_bytes)
    total_avail_conv = convert_size(storage_total_avail_in_bytes)
    total_used_perc = (storage_total_used_in_bytes / storage_total_capacity_in_bytes) * 100

    print("[ TOTAL ]")
    print(f"{total_used_conv} used of {total_capacity_conv} ({total_used_perc:.0f})%\nAVAILABLE: {total_avail_conv}")

    return disk_info 

               