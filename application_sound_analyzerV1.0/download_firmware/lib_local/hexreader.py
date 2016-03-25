def process_hex_line(line):
    addr = (int(line[3:7],base = 16))
    rawdata = line[9:len(line)-3]
    data = [] 
    for index in range(len(rawdata)/2):
        data.append((int(rawdata[index*2:index*2+2],base = 16)))
    return addr,data,len(data)

def process_iic_line(line):
    addr = (int(line[3:7],base = 16))
    rawdata = line[9:len(line)-3]
    data = [] 
    for index in range(len(rawdata)/2):
        data.append((int(rawdata[index*2:index*2+2],base = 16)))
    return addr,data,len(data)

