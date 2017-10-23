import sys, socket, struct

def txt_to_hex(text):
    converted_text = []
    for i in list(text):
        converted_text.append((hex(ord(i))).replace("0x", "%"))
    converted_text = "".join(converted_text)
    return converted_text

def obscure_ip(ip, output_format):
    if output_format == "decimal":
        return struct.unpack("!L", socket.inet_aton(ip))[0]

    else:
        octets = ip.split(".")
        converted_ip = []

        if output_format == "octal":
            for i in octets:
                converted_ip.append(oct(int(i)))

        else:
            for i in octets:
                converted_ip.append(hex(int(i)))

        return ".".join(converted_ip)

def output_assembler(str_list):
    output = ""
    if str_list[0] in ["http:", "https:", "ftp:"]:
        output = output + str_list[0] + "//"

    output = output + str(str_list[1])

    if str_list[2] != "":
        for i in str_list[2]:
            output = output + "/" + i

    return output

def url_splitter(url):
    url = url.split("/")
    if url[0] in ["https:", "http:", "ftp:"]:
        protocol = url[0]
        domain = url[2]
        if len(url) > 3:
            directory = url[3:]
        else:
            directory = ""
    else:
        protocol = ""
        domain = url[0]
        if len(url) > 1:
            directory = url[1:]
        else:
            directory = ""
    return [protocol, domain, directory]

if __name__ == "__main__":
    help_message = """python [FLAGS] [URL/IP]
    Valid URL/IP:
    8ch.net
    8ch.net/tech
    https://www.8ch.net
    127.0.0.1

    Flags
    -h --- prints this message
    -t --- converts url text to hex
    -d --- converts the directory text to hex as well
    -u --- for URLs that are to be converted to IPs
    -i --- for IPs
    -b --- for converting IPs to decimal
    -o --- for converting IPs to octal
    -s --- for converting IPs to hex
    
    Examples:
    -td  --- converts both the domain and the directory to hex
    -uod --- finds the IP, converts it to octal and the directory to hex
    -is  --- converts given IP to hex, leaves directory alone

    Invalid flag combinations:
    -h with anything invalid 
    -t with anything but d is invalid
    -u and i together is invalid
    -b, o, s together in any combination is invalid
     
    """
    if len(sys.argv) > 2:
        flags = list(sys.argv[1])
        string = url_splitter(sys.argv[2])

        if "h" in flags:
            print(help_message)
    
        if "u" in flags:
            string[1] = socket.gethostbyname(string[1]) 

        if "t" in flags:
            string[1] = txt_to_hex(string[1]) 

        if "d" in flags:
            string[2] = [txt_to_hex(i) for i in string[2]]

        if "b" in flags:
            string[1] = obscure_ip(string[1], "decimal")

        elif "o" in flags:
            string[1] = obscure_ip(string[1], "octal")

        elif "s" in flags: 
            string[1] = obscure_ip(string[1], "hexadecimal")

        print(output_assembler(string))

    else:
        print(help_message)
