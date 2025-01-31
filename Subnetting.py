def ip_to_binary(ip):
    return ''.join(f'{int(x):08b}' for x in ip.split('.'))

def binary_to_ip(binary):
    return '.'.join(str(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

def calculate_network_and_broadcast(ip, mask):
    ip_bin = ip_to_binary(ip)
    mask_bin = ip_to_binary(mask)

    # Network address: Perform bitwise AND between IP and Mask
    network_bin = ''.join('1' if ip_bin[i] == '1' and mask_bin[i] == '1' else '0' for i in range(32))
    network_ip = binary_to_ip(network_bin)

    # Broadcast address: Invert the subnet mask and perform OR with network address
    inverted_mask_bin = ''.join('1' if bit == '0' else '0' for bit in mask_bin)
    broadcast_bin = ''.join('1' if network_bin[i] == '1' or inverted_mask_bin[i] == '1' else '0' for i in range(32))
    broadcast_ip = binary_to_ip(broadcast_bin)

    return network_ip, broadcast_ip

def get_usable_ips(network_ip, broadcast_ip):
    # Convert network and broadcast IP to binary
    network_bin = ip_to_binary(network_ip)
    broadcast_bin = ip_to_binary(broadcast_ip)

    # Find the first usable IP: Increment the host portion by 1
    first_usable_bin = network_bin[:-1] + '1'
    first_usable_ip = binary_to_ip(first_usable_bin)

    # Find the last usable IP: Decrement the broadcast portion by 1
    last_usable_bin = broadcast_bin[:-1] + '0'
    last_usable_ip = binary_to_ip(last_usable_bin)

    return first_usable_ip, last_usable_ip

def calculate_subnet(ip, mask):
    network_ip, broadcast_ip = calculate_network_and_broadcast(ip, mask)
    first_usable_ip, last_usable_ip = get_usable_ips(network_ip, broadcast_ip)

    print(f"IP Address: {ip}")
    print(f"Subnet Mask: {mask}")
    print(f"Network Address: {network_ip}")
    print(f"Broadcast Address: {broadcast_ip}")
    print(f"Usable IP Range: {first_usable_ip} - {last_usable_ip}")

def cidr_to_subnet(cidr):
    # Convert CIDR to subnet mask (e.g., /24 => 255.255.255.0)
    mask = ['1' * cidr + '0' * (32 - cidr)]
    mask = [mask[0][i:i+8] for i in range(0, 32, 8)]
    return '.'.join(str(int(octet, 2)) for octet in mask)

# Main function to run the tool
def main():
    while True:
        print("\nIP Addressing and Subnetting Tool")
        ip = input("Enter IP address (e.g., 192.168.1.1): ")
        mask = input("Enter Subnet Mask (e.g., 255.255.255.0) or CIDR (e.g., /24): ")

        if mask.startswith('/'):
            cidr = int(mask[1:])
            mask = cidr_to_subnet(cidr)

        if ip and mask:
            calculate_subnet(ip, mask)

        again = input("Do you want to calculate again? (y/n): ")
        if again.lower() != 'y' and again.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
