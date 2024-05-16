import socket
import psutil



#
# Original from https://github.com/giampaolo/psutil/blob/master/scripts/ifconfig.py
#

class ActiveNIF:    #Active Network Interfaces

    _af_map = {
        socket.AF_INET: 'IPv4',
        socket.AF_INET6: 'IPv6',
        psutil.AF_LINK: 'MAC',
    }

    @staticmethod
    def _initSnic():
        snic = {}
        snic['name'] = None

        desc = ActiveNIF._af_map[socket.AF_INET]
        snic[desc] = None

        desc = ActiveNIF._af_map[socket.AF_INET6]
        snic[desc] = None

        desc = ActiveNIF._af_map[psutil.AF_LINK]
        snic[desc] = None

        snic['broadcast'] = None
        snic['netmask'] = None
        snic['ptp'] = None

        return snic


    @staticmethod
    def _initSnic():
        snic = {}
        snic['name'] = None

        desc = ActiveNIF._af_map[socket.AF_INET]
        snic[desc] = None

        desc = ActiveNIF._af_map[socket.AF_INET6]
        snic[desc] = None

        desc = ActiveNIF._af_map[psutil.AF_LINK]
        snic[desc] = None

        snic['broadcast'] = None
        snic['netmask'] = None
        snic['ptp'] = None

        return snic


    def _findActiveNetIfaces(self):

            # Find all active Network Interfaces
            #
            # This excludes the Loopback interface 
            #
            # Originally, all interfaces are in the dictionary returned by net_if_addrs().
            # The dictionary contains a list of dictionary for each interface
            #
            # NIC = network interface card
            #
            # { NIC # 1 name,
            #     [
            #        {family, address, broadcast addr, netmask, peer2peer addr},
            #        {family, address, broadcast addr, netmask, peer2peer addr},
            #        ...
            #     ]
            # },
            # { NIC # 2 name,
            #     [
            #        {family, address, broadcast addr, netmask, peer2peer addr},
            #        {family, address, broadcast addr, netmask, peer2peer addr},
            #        ...
            #     ]
            # }
            # ....
            #  
            # addresses can be one of several address families: MAC, IPV4, IPV6
            #
            # The _activeNIF data created by this routine is a dictionary of dictionaries
            # The first key is the NIC Name.  Using it will return the dictionary
            # containing the specific values for that NIC interface.
            #

         # for each net IF examine its list of dictionaries to identify
            # the active NICs, and the addresses associated with each
            #
            # { NIC # 1 name,
            #    { family : address,  broadcast : addr, netmask : address, peer2peer : addr },
            # { NIC # 2 name,
            #    { family : address,  broadcast : addr, netmask : address, peer2peer : addr },
            # ...
            #
            # where family is one of the _af_map values above

        stats = psutil.net_if_stats()   #need this to identify active interface(s)
        io_counters = psutil.net_io_counters(pernic=True)

        skip = False

        for nic, addresses in psutil.net_if_addrs().items():
            if 'Loopback' in nic:           # skip the windows Loopback interface
                continue
            if 'lo' in nic:                 # skip the linux Loopback interface
                continue
            if not nic in stats:
                continue
            if not stats[nic].isup:         # is it active?
                continue
            skip = False
            if nic in io_counters:
                io = io_counters[nic]
                if (io.bytes_recv + io.bytes_sent) == 0:
                    skip = True
            if skip:
                continue
            snic = ActiveNIF._initSnic()
            snic['name'] = nic
            for addr in addresses:
                if addr.address == '127.0.0.1':
                    skip = True
                    break
                family = ActiveNIF._af_map.get(addr.family)
                snic[family] = addr.address
                if snic['broadcast'] is None:
                    snic['broadcast'] = addr.broadcast
                if snic['netmask'] is None:
                      snic['netmask'] = addr.netmask
                if snic['ptp'] is None:
                    snic['ptp'] = addr.ptp
            if not skip:
                self._activeNIF.append(snic)
        return



    def __init__(self):
        self._activeNIF = []
        self._findActiveNetIfaces()
        return


    def getIpAddr(self):
        return (self._activeNIF[0])['IPv4']


    def getMacAddrWithDashes(self):
        return (self._activeNIF[0])['MAC']


    def getMacAddrAsHexStr(self):
        dashes = (self._activeNIF[0])['MAC']
        newstr = dashes.translate({ord(c): None for c in '-:'})
        return newstr.lower()


    def printNetIfaces(self):
        for netIf in self._activeNIF:
            for k, v in netIf.items():
                print("\t{} : {}".format(k, v))
            print()

    @staticmethod
    def test():
        anif = ActiveNIF()
        anif.printNetIfaces()
        print("IP Addr :", anif.getIpAddr())
        print("MAC Addr '-' :", anif.getMacAddrWithDashes())
        print("MAC Addr  0x :", anif.getMacAddrAsHexStr())
        return


###################


if __name__ == '__main__':
    ActiveNIF.test()

