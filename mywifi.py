import utime as time
import network


def init(config):
    # Configure WIFI
    network.WLAN(network.AP_IF).active(False)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    # Find usable WAP from list in wifi.json
    connect(config)

    print(("WLAN Connected: %s" % sta_if.ifconfig()[0]))


def connect(config):

    sta_if = network.WLAN(network.STA_IF)
    sta_if.config(dhcp_hostname=config['hostname'])

    ssid = None

    while not sta_if.isconnected():

        print("Scanning for Access Points")
        ap_list = sta_if.scan()

        for found_ap in ap_list:
            ssid = str(found_ap[0], 'utf-8')
            if ssid in config["networks"]:
                break
        else:
            ssid = None
            print("No configured WAPs found")
            time.sleep(10)

        if ssid:
            count = 0
            print(("Trying to connect to: %s" % ssid))
            sta_if.connect(ssid, config['networks'][ssid])

            ## Stall for connection/DHCP
            while not sta_if.isconnected():
                print("Waiting for WLAN")
                count += 1
                if count > 10:
                    print(("Timeout on WAP: %s" % ssid))
                    sta_if.disconnect()
                    break
                time.sleep(1)

    else:
        if ssid:
            print(("Connected to WAP: %s" % ssid))
        else:
            print(("Connected to last used WAP"))


def disconnect():
    network.WLAN(network.STA_IF).disconnect()
