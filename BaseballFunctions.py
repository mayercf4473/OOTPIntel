__author__ = 'cmayer'


def rawWOBA(ab, walks, singles, doubles, triples, homeRuns):
    #assumes above calculations are for 1000 at bats
    if (ab + walks) <= 0:
        wOBA = 0
    else:
        wOBA = (walks * .72 + singles * .9 + doubles * 1.24 + triples * 1.56 + homeRuns * 1.95) / (ab + walks)
    return wOBA

def rawWRAA(ab, woba, walks):
    #=(1000+AF2)*(AP2-320)/1200
    return (ab+walks) * (woba - .320) / 1.2

def rawFIP(ip, strikeOuts, homeRuns, walks):
    if ip <= 0:
        return 99
    return (13*homeRuns + 3*walks - 2*strikeOuts)/ip + 3.2

#very rough wSB
def rawWSB(sb, cs):
    return sb * .2 + cs * .32

def rawPWAR(innings, fip):
    if innings <= 0:
        return -20
    lgFIP = 4.28
    return (lgFIP - fip) / 9 * innings / 10
