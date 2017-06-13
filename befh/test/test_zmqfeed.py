import zmq
import itchat
import time

market_feed_name = "marketfeed"
context = zmq.Context()
sock = context.socket(zmq.SUB)
# sock.connect("ipc://%s" % market_feed_name)
sock.connect("tcp://127.0.0.1:6001")
sock.setsockopt_string(zmq.SUBSCRIBE, '')

# in-memory database
exchanges_snapshot = {}
itchatsendtime = {}

# itchat
itchat.auto_login(hotReload=True)
# itchat.send("test", toUserName="filehelper")

print("Started...")
while True:
    # ret = sock.recv_pyobj()
    # message = sock.recv()
    mjson = sock.recv_json()

    exchanges_snapshot[mjson["exchange"] + "_" + mjson["instmt"]] = mjson
    keys = exchanges_snapshot.keys()

    if "Bitfinex_SPOT_XRPBTC" in keys and \
                    "JUBI_Spot_SPOT_XRPCNY" in keys and \
                    "JUBI_Spot_SPOT_BTCCNY" in keys:
        ratio = 1 / exchanges_snapshot["Bitfinex_SPOT_XRPBTC"]["a1"] * exchanges_snapshot["JUBI_Spot_SPOT_XRPCNY"][
            "b1"] / exchanges_snapshot["JUBI_Spot_SPOT_BTCCNY"]["a1"] - 0.005 - 0.006 - 1
        timekey = "JUBI.CNY_BTC(buy)->Bitfinex.BTC_XRP(buy)->JUBI.XRP_CNY(sell)"
        if timekey not in itchatsendtime.keys():
            itchatsendtime[timekey] = 0
        if time.time() - itchatsendtime[timekey] > 60 and ratio > 0.01:
            itchat.send(
                "warning: " + "BTC:" + str(exchanges_snapshot["JUBI_Spot_SPOT_BTCCNY"]["a1"]) + " XRPBTC:" + str(
                    exchanges_snapshot["Bitfinex_SPOT_XRPBTC"]["a1"]) + " XRP:" + str(
                    exchanges_snapshot["JUBI_Spot_SPOT_XRPCNY"]["b1"]) + " " + timekey + ": " + "{:.2%}".format(ratio),
                toUserName="filehelper")
            itchatsendtime[timekey] = time.time()
        elif time.time() - itchatsendtime[timekey] > 600:
            itchat.send(timekey + ": " + "{:.2%}".format(ratio), toUserName="filehelper")
            itchatsendtime[timekey] = time.time()

        ratio = exchanges_snapshot["Bitfinex_SPOT_XRPBTC"]["b1"] * exchanges_snapshot["JUBI_Spot_SPOT_BTCCNY"]["b1"] / \
                exchanges_snapshot["JUBI_Spot_SPOT_XRPCNY"]["a1"] - 0.005 - 0.015 - 1
        timekey = "JUBI.CNY_XRP(buy)->Bitfinex.XRP_BTC(sell)->JUBI.BTC_CNY(sell)"
        if timekey not in itchatsendtime.keys():
            itchatsendtime[timekey] = 0
        if time.time() - itchatsendtime[timekey] > 60 and ratio > 0.01:
            itchat.send(
                "warning: " + "XRP:" + str(exchanges_snapshot["JUBI_Spot_SPOT_XRPCNY"]["a1"]) + " XRPBTC:" + str(
                    exchanges_snapshot["Bitfinex_SPOT_XRPBTC"]["b1"]) + " BTC:" + str(
                    exchanges_snapshot["JUBI_Spot_SPOT_BTCCNY"]["b1"]) + " " + timekey + ": " + "{:.2%}".format(ratio),
                toUserName="filehelper")
            itchatsendtime[timekey] = time.time()
        elif time.time() - itchatsendtime[timekey] > 600:
            itchat.send(timekey + ": " + "{:.2%}".format(ratio), toUserName="filehelper")
            itchatsendtime[timekey] = time.time()

    if "Bitfinex_SPOT_ETHBTC" in keys and \
                    "JUBI_Spot_SPOT_ETHCNY" in keys and \
                    "JUBI_Spot_SPOT_BTCCNY" in keys:
        ratio = 1 / exchanges_snapshot["Bitfinex_SPOT_ETHBTC"]["a1"] * exchanges_snapshot["JUBI_Spot_SPOT_ETHCNY"][
            "b1"] / exchanges_snapshot["JUBI_Spot_SPOT_BTCCNY"]["a1"] - 0.005 - 0.006 - 1
        timekey = "JUBI.CNY_BTC(buy)->Bitfinex.BTC_ETH(buy)->JUBI.ETH_CNY(sell)"
        if timekey not in itchatsendtime.keys():
            itchatsendtime[timekey] = 0
        if time.time() - itchatsendtime[timekey] > 60 and ratio > 0.01:
            itchat.send(
                "warning: " + "BTC:" + str(exchanges_snapshot["JUBI_Spot_SPOT_BTCCNY"]["a1"]) + " ETHBTC:" + str(
                    exchanges_snapshot["Bitfinex_SPOT_ETHBTC"]["a1"]) + " ETH:" + str(
                    exchanges_snapshot["JUBI_Spot_SPOT_ETHCNY"]["b1"]) + " " + timekey + ": " + "{:.2%}".format(ratio),
                toUserName="filehelper")
            itchatsendtime[timekey] = time.time()
        elif time.time() - itchatsendtime[timekey] > 600:
            itchat.send(timekey + ": " + "{:.2%}".format(ratio), toUserName="filehelper")
            itchatsendtime[timekey] = time.time()

        ratio = exchanges_snapshot["Bitfinex_SPOT_ETHBTC"]["b1"] * exchanges_snapshot["JUBI_Spot_SPOT_BTCCNY"]["b1"] / \
                exchanges_snapshot["JUBI_Spot_SPOT_ETHCNY"]["a1"] - 0.005 - 0.006 - 1
        timekey = "JUBI.CNY_ETH(buy)->Bitfinex.ETH_BTC(sell)->JUBI.BTC_CNY(sell)"
        if timekey not in itchatsendtime.keys():
            itchatsendtime[timekey] = 0
        if time.time() - itchatsendtime[timekey] > 60 and ratio > 0.01:
            itchat.send(
                "warning: " + "ETH:" + str(exchanges_snapshot["JUBI_Spot_SPOT_ETHCNY"]["a1"]) + " ETHBTC:" + str(
                    exchanges_snapshot["Bitfinex_SPOT_ETHBTC"]["b1"]) + " BTC:" + str(
                    exchanges_snapshot["JUBI_Spot_SPOT_BTCCNY"]["b1"]) + " " + timekey + ": " + "{:.2%}".format(ratio),
                toUserName="filehelper")
            itchatsendtime[timekey] = time.time()
        elif time.time() - itchatsendtime[timekey] > 600:
            itchat.send(timekey + ": " + "{:.2%}".format(ratio), toUserName="filehelper")
            itchatsendtime[timekey] = time.time()

    if "Bitfinex_SPOT_ETHBTC" in keys and \
                    "OkCoinCN_SPOT_ETHCNY" in keys and \
                    "OkCoinCN_SPOT_BTCCNY" in keys:
        ratio = 1 / exchanges_snapshot["Bitfinex_SPOT_ETHBTC"]["a1"] * exchanges_snapshot["OkCoinCN_SPOT_ETHCNY"][
            "b1"] / exchanges_snapshot["OkCoinCN_SPOT_BTCCNY"]["a1"] - 0.005 - 0.001 - 1
        timekey = "OkCoinCN.CNY_BTC(buy)->Bitfinex.BTC_ETH(buy)->OkCoinCN.ETH_CNY(sell)"
        if timekey not in itchatsendtime.keys():
            itchatsendtime[timekey] = 0
        if time.time() - itchatsendtime[timekey] > 60 and ratio > 0.01:
            itchat.send("warning: " + "BTC:" + str(exchanges_snapshot["OkCoinCN_SPOT_BTCCNY"]["a1"]) + " ETHBTC:" + str(
                exchanges_snapshot["Bitfinex_SPOT_ETHBTC"]["a1"]) + " ETH:" + str(
                exchanges_snapshot["OkCoinCN_SPOT_ETHCNY"]["b1"]) + " " + timekey + ": " + "{:.2%}".format(ratio),
                        toUserName="filehelper")
            itchatsendtime[timekey] = time.time()
        elif time.time() - itchatsendtime[timekey] > 600:
            itchat.send(timekey + ": " + "{:.2%}".format(ratio), toUserName="filehelper")
            itchatsendtime[timekey] = time.time()

        ratio = exchanges_snapshot["Bitfinex_SPOT_ETHBTC"]["b1"] * exchanges_snapshot["OkCoinCN_SPOT_BTCCNY"]["b1"] / \
                exchanges_snapshot["OkCoinCN_SPOT_ETHCNY"]["a1"] - 0.005 - 0.001 - 1
        timekey = "OkCoinCN.CNY_ETH(buy)->Bitfinex.ETH_BTC(sell)->OkCoinCN.BTC_CNY(sell)"
        if timekey not in itchatsendtime.keys():
            itchatsendtime[timekey] = 0
        if time.time() - itchatsendtime[timekey] > 60 and ratio > 0.01:
            itchat.send("warning: " + "ETH:" + str(exchanges_snapshot["OkCoinCN_SPOT_ETHCNY"]["a1"]) + " ETHBTC:" + str(
                exchanges_snapshot["Bitfinex_SPOT_ETHBTC"]["b1"]) + " BTC:" + str(
                exchanges_snapshot["OkCoinCN_SPOT_BTCCNY"]["b1"]) + " " + timekey + ": " + "{:.2%}".format(ratio),
                        toUserName="filehelper")
            itchatsendtime[timekey] = time.time()
        elif time.time() - itchatsendtime[timekey] > 600:
            itchat.send(timekey + ": " + "{:.2%}".format(ratio), toUserName="filehelper")
            itchatsendtime[timekey] = time.time()

    if "Bitfinex_SPOT_ETCBTC" in keys and \
                    "JUBI_Spot_SPOT_ETCCNY" in keys and \
                    "JUBI_Spot_SPOT_BTCCNY" in keys:
        ratio = 1 / exchanges_snapshot["Bitfinex_SPOT_ETCBTC"]["a1"] * \
                exchanges_snapshot["JUBI_Spot_SPOT_ETCCNY"][
                    "b1"] / exchanges_snapshot["JUBI_Spot_SPOT_BTCCNY"]["a1"] - 0.005 - 0.006 - 1
        timekey = "JUBI.CNY_BTC(buy)->Bitfinex.BTC_ETC(buy)->JUBI.ETC_CNY(sell)"
        if timekey not in itchatsendtime.keys():
            itchatsendtime[timekey] = 0
        if time.time() - itchatsendtime[timekey] > 60 and ratio > 0.01:
            itchat.send(
                "warning: " + "BTC:" + str(exchanges_snapshot["JUBI_Spot_SPOT_BTCCNY"]["a1"]) + " ETCBTC:" + str(
                    exchanges_snapshot["Bitfinex_SPOT_ETCBTC"]["a1"]) + " ETC:" + str(
                    exchanges_snapshot["JUBI_Spot_SPOT_ETCCNY"]["b1"]) + " " + timekey + ": " + "{:.2%}".format(
                    ratio),
                toUserName="filehelper")
            itchatsendtime[timekey] = time.time()
        elif time.time() - itchatsendtime[timekey] > 600:
            itchat.send(timekey + ": " + "{:.2%}".format(ratio), toUserName="filehelper")
            itchatsendtime[timekey] = time.time()

        ratio = exchanges_snapshot["Bitfinex_SPOT_ETCBTC"]["b1"] * exchanges_snapshot["JUBI_Spot_SPOT_BTCCNY"][
            "b1"] / \
                exchanges_snapshot["JUBI_Spot_SPOT_ETCCNY"]["a1"] - 0.005 - 0.006 - 1
        timekey = "JUBI.CNY_ETC(buy)->Bitfinex.ETC_BTC(sell)->JUBI.BTC_CNY(sell)"
        if timekey not in itchatsendtime.keys():
            itchatsendtime[timekey] = 0
        if time.time() - itchatsendtime[timekey] > 60 and ratio > 0.01:
            itchat.send(
                "warning: " + "ETC:" + str(exchanges_snapshot["JUBI_Spot_SPOT_ETCCNY"]["a1"]) + " ETCBTC:" + str(
                    exchanges_snapshot["Bitfinex_SPOT_ETCBTC"]["b1"]) + " BTC:" + str(
                    exchanges_snapshot["JUBI_Spot_SPOT_BTCCNY"]["b1"]) + " " + timekey + ": " + "{:.2%}".format(
                    ratio),
                toUserName="filehelper")
            itchatsendtime[timekey] = time.time()
        elif time.time() - itchatsendtime[timekey] > 600:
            itchat.send(timekey + ": " + "{:.2%}".format(ratio), toUserName="filehelper")
            itchatsendtime[timekey] = time.time()

    if "Poloniex_BTCBTS" in keys and \
                    "JUBI_Spot_SPOT_BTSCNY" in keys and \
                    "BTCC_Spot_SPOT_BTCCNY" in keys:
        ratio = 1 / exchanges_snapshot["Poloniex_BTCBTS"]["a1"] * \
                exchanges_snapshot["JUBI_Spot_SPOT_BTSCNY"][
                    "b1"] / exchanges_snapshot["BTCC_Spot_SPOT_BTCCNY"]["a1"] - 0.0055 - 0.006 - 1
        timekey = "BTCC.CNY_BTC(buy)->Poloniex.BTC_BTS(buy)->JUBI.BTS_CNY(sell)"
        if timekey not in itchatsendtime.keys():
            itchatsendtime[timekey] = 0
        if time.time() - itchatsendtime[timekey] > 60 and ratio > 0.01:
            itchat.send(
                "warning: " + "BTC:" + str(
                    exchanges_snapshot["BTCC_Spot_SPOT_BTCCNY"]["a1"]) + " BTSBTC:" + str(
                    exchanges_snapshot["Poloniex_BTCBTS"]["a1"]) + " BTS:" + str(
                    exchanges_snapshot["JUBI_Spot_SPOT_BTSCNY"]["b1"]) + " " + timekey + ": " + "{:.2%}".format(
                    ratio),
                toUserName="filehelper")
            itchatsendtime[timekey] = time.time()
        elif time.time() - itchatsendtime[timekey] > 600:
            itchat.send(timekey + ": " + "{:.2%}".format(ratio), toUserName="filehelper")
            itchatsendtime[timekey] = time.time()

        ratio = exchanges_snapshot["Poloniex_BTCBTS"]["b1"] * exchanges_snapshot["BTCC_Spot_SPOT_BTCCNY"][
            "b1"] / \
                exchanges_snapshot["JUBI_Spot_SPOT_BTSCNY"]["a1"] - 0.005 - 0.006 - 1
        timekey = "JUBI.CNY_BTS(buy)->Poloniex.BTS_BTC(sell)->BTCC.BTC_CNY(sell)"
        if timekey not in itchatsendtime.keys():
            itchatsendtime[timekey] = 0
        if time.time() - itchatsendtime[timekey] > 60 and ratio > 0.01:
            itchat.send(
                "warning: " + "BTS:" + str(
                    exchanges_snapshot["JUBI_Spot_SPOT_BTSCNY"]["a1"]) + " BTSBTC:" + str(
                    exchanges_snapshot["Poloniex_BTCBTS"]["b1"]) + " BTC:" + str(
                    exchanges_snapshot["BTCC_Spot_SPOT_BTCCNY"]["b1"]) + " " + timekey + ": " + "{:.2%}".format(
                    ratio),
                toUserName="filehelper")
            itchatsendtime[timekey] = time.time()
        elif time.time() - itchatsendtime[timekey] > 600:
            itchat.send(timekey + ": " + "{:.2%}".format(ratio), toUserName="filehelper")
            itchatsendtime[timekey] = time.time()

            # print(mjson)