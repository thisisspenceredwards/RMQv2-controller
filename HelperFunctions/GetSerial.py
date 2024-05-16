def get_serial():
    cpu_serial = "ERROR000000000"

    try:
        f= open("/proc/cpuinfo", "r")
        for line in f:
            if line[0:6] == "Serial":
                cpu_serial = line[10:26]
                f.close()
                break
    except Exception as e:
        print(e)

    return cpu_serial
