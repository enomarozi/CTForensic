from django.shortcuts import render
from django.http import JsonResponse
from .models import NetworkFile
from scapy.all import *
import base64

def analisaPCAP(request, id_):
	fileName = NetworkFile.objects.get(pk=id_)
	path_file = "uploads/"+fileName.name
	packets = rdpcap(path_file)
	summary_data = str(packets).split(' ')
	context = {
		'id_':id_,
		"title":"Analysis PCAP",
		'summary': summary_data[1]+" "+summary_data[2]+" "+summary_data[3]+" "+summary_data[4][:-1],
		'metadata':fileName,
		'ip': getIP(packets)
	}
	return render(request, 'networkforensics/analisa_pcap.html', context)

def getIP(packets):
	IPresultSRCtoDST = []
	for i in packets:
	    if IP in i:
	        iter_ = i[IP].src+"-"+i[IP].dst
	        IPresultSRCtoDST.append(iter_)
	    elif IPv6 in i:
	    	iter_ = i[IPv6].src+"-"+i[IPv6].dst
	    	IPresultSRCtoDST.append(iter_)
	result = {}
	for i in set(IPresultSRCtoDST):
	    result[i] = str(IPresultSRCtoDST.count(i))
	return result

def checkPacket(request):
	if request.method == 'GET':
		ip_address = request.GET.get('ip')
		id_ = request.GET.get('id')
		fileName = NetworkFile.objects.get(pk=id_)
		path_file = "uploads/"+fileName.name
		packets = rdpcap(path_file)
		response_data = {
			'type':bytesData(packets,ip_address)[3],
			'sport':bytesData(packets,ip_address)[0],
			'dport':bytesData(packets,ip_address)[1],
			'bytes_data_encode':str(bytesData(packets,ip_address)[2]),
		}
		return JsonResponse(response_data)

def bytesData(packets,ip_address):
	result = ""
	ip_src, ip_dst = ip_address.split("-")
	sport, dport, type_ = set(),set(),set()
	result_byte = b''
	for i in packets:
		try:
			if ":" in ip_src or ":" in ip_dst:
				if i[IPv6].src == ip_src and i[IPv6].dst == ip_dst:
					result_byte = i[Raw].load
					sport.add(i[IPv6].sport)
					dport.add(i[IPv6].dport)
					if "TCP" in i[IPv6]:
						type_.add("TCP")
					elif "UDP" in i[IPv6]:
						type_.add("UDP")
					result_byte += raw_data_base64
			elif "." in ip_src or "." in ip_dst:
				if i[IP].src == ip_src and i[IP].dst == ip_dst:
					result_byte = i[Raw].load
					sport.add(i[IP].sport)
					dport.add(i[IP].dport)
					if "TCP" in i[IP]:
						type_.add("TCP")
					elif "UDP" in i[IP]:
						type_.add("UDP")
					result_byte += i[Raw].load

		except Exception as e:
			pass
	if len(sport) == 0:
		sport.add("Tidak ada port")
	if len(dport) == 0:
		dport.add("Tidak ada port")
	if len(type_) == 0:
		type_.add("Others")
	return (list(sport)[0],list(dport)[0],result_byte,list(type_))