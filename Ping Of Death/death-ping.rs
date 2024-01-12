use pnet::packet::icmp::{IcmpPacket, echo_request};
use pnet::packet::ip::IpNextHeaderProtocols;
use pnet::packet::ipv4::{Ipv4Packet, MutableIpv4Packet};
use pnet::transport::{icmp_packet_iter, transport_channel, TransportChannelType::Layer3};
use std::net::IpAddr;
use std::time::Duration;

const SOURCE_IP: &str = "10.0.1.1";
const TARGET_IP: &str = "10.0.1.5";
const MESSAGE: &[u8] = b"T";
const NUMBER_PACKETS: usize = 5;

fn main() {

    let protocol = Layer3(IpNextHeaderProtocols::Icmp);
    let (mut tx, _) = transport_channel(4096, protocol).expect("Failed to create transport channel");


    let source_ip: IpAddr = SOURCE_IP.parse().expect("Invalid source IP address");
    let target_ip: IpAddr = TARGET_IP.parse().expect("Invalid target IP address");

    for _ in 0..NUMBER_PACKETS {
        
        let mut ipv4_packet = MutableIpv4Packet::owned(vec![0u8; 20 + MESSAGE.len()]).unwrap();
        ipv4_packet.set_version(4);
        ipv4_packet.set_header_length(5);
        ipv4_packet.set_total_length(ipv4_packet.packet().len() as u16);
        ipv4_packet.set_ttl(64);
        ipv4_packet.set_source(source_ip);
        ipv4_packet.set_destination(target_ip);
        ipv4_packet.set_next_level_protocol(IpNextHeaderProtocols::Icmp);

        
        let mut icmp_packet = echo_request::MutableEchoRequestPacket::new(&mut ipv4_packet).unwrap();
        icmp_packet.set_sequence_number(1);
        icmp_packet.set_identifier(1);
        icmp_packet.set_payload(MESSAGE);

        tx.send_to(ipv4_packet.to_immutable(), target_ip).expect("Failed to send packet");

 
        std::thread::sleep(Duration::from_millis(100));
    }
}

