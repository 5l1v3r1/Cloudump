#!/usr/bin/python
#
####################################################################################
#[S] SCRIP : Cloudump                                                              #
#[J]   JOB : identifying real IP of CloudFlare protected website.                  #
#[A]Codedby: Oseid Aldary                                                          #
####################################################################################
##
##Modlues
try:
        import mechanize,re,socket,urllib2,json,sys
        from os import system as sy
        from time import sleep
        sy("")
except ImportError, e:
        e = e[0][16:]
        if e =="json":
                e = "simplejson"
        print("\n[!] Error: Please Install [ "+e+" ] Library And Try Again !!!\n[*] Use This Command For Install It: pip install "+e)
	exit(1)

####=COLORS=########
wi = '\033[1;37m' ##>>White
rd = '\033[1;31m' ##>Red
gr = '\033[1;32m' ##>Green
yl = '\033[1;33m' ##>Yallow
bl = '\033[1;34m' ##>Blue
pu = '\033[1;35m' ##>Purple
cy = '\033[1;36m' ##>Cyan
####################
class DumpIP:
        def cnet(self):
                try:
                        ip = socket.gethostbyname("www.google.com")
			con = socket.create_connection((ip,80),2)
			return True
		except socket.error:
			pass
		return False
	def geoIPinfo(self, ip):
                try:
                        url = "http://ip-api.com/json/"
                        response = urllib2.urlopen(url + str(ip))
                        name = response.read()
                        labs = json.loads(name.decode("utf-8"))
                        region = labs['regionName'].encode('ascii','replace')
                        print(rd+"     GeoIP INFO"+gr+":["+wi+str(ip)+gr+"]===:")
                        sleep(0.10)
                        print(gr + "\t\t IP: " +wi+ labs['query'].encode('ascii','replace'))
                        sleep(0.10)
                        print(gr+ "\t\t Status: " +wi+ labs['status'].encode('ascii','replace'))
                        sleep(0.10)
                        print(gr+ "\t\t Region: "+wi+"{}".format(region))
                        sleep(0.10)
                        print(gr + "\t\t Country: " +wi+ labs['country'].encode('ascii','replace'))
                        sleep(0.10)
                        print(gr + "\t\t City: " +wi+ labs['city'].encode('ascii','replace'))
                        sleep(0.10)
                        print(gr + "\t\t ISP: "+wi + labs['isp'].encode('ascii','replace'))
                        sleep(0.10)
                        print(gr + "\t\t Lat,Lon: "+wi + str(labs['lat']).encode('ascii','replace') + "," + str(labs['lon']).encode('ascii','replace'))
                        sleep(0.10)
                        print(gr + "\t\t ZIPCODE: "+wi + labs['zip'].encode('ascii','replace'))
                        sleep(0.10)
                        print(gr + "\t\t TimeZone: " +wi+ labs['timezone'].encode('ascii','replace'))
                        sleep(0.10)
                        print(gr + "\t\t AS: " +wi+ labs['as'].encode('ascii','replace'))
                        sleep(0.10)
                        print(pu+"===============================\n"+wi)
                except Exception:
                        print(rd+"\n["+yl+"!"+rd+"]"+yl+" Something Went Wrong"+rd+" !!!"+wi)
                        print(wi+"\n["+yl+"!"+wi+"]"+yl+" You Can Show The GeoIP OF Target In [ "+wi+"https://whatismyipaddress.com/ip/"+str(ip)+yl+" ]")
                        exit(1)
	def dumpIP(self, url):
		if self.cnet() !=True:
                        print(rd+"\n["+yl+"!"+rd+"]"+yl+" Error: Please Check Your Internet Connection "+rd+"!!!")
                        exit(1)
                if url[:7] =="http://" or url[:8] =="https://":
                        curl = url[7:] if url[:7] =="http://" else url[8:]
                        curl = curl.lower()
                        curl = curl.strip("/")
                        try:
                                colIP = socket.gethostbyname(curl)
                        except socket.error:
                                print(rd+"["+yl+"!"+rd+"]"+yl+" ERRORCode["+rd+"404"+yl+"]: Server Not Found!")
                                print(rd+"["+yl+"!"+rd+"]"+wi+" Please Check Your URL !")
                                exit(1)
                                
                        url = url.strip("/")
                else:
                        try:
                                colIP = socket.gethostbyname(url)
                        except socket.error:
                                print(rd+"["+yl+"!"+rd+"]"+yl+" ERRORCode["+rd+"404"+yl+"]: Server Not Found!")
                                print(rd+"["+yl+"!"+rd+"]"+wi+" Please Check Your URL !")
                                exit(1)
                        except socket.gaierror:
                                print(rd+"["+yl+"!"+rd+"]"+yl+" Error: Please Check Your URL[ "+rd+url+yl+" ]"+rd+" !!!")
                                exit(1)
                        url = "http://"+url
                try:
                        print(yl+"\n["+wi+"~"+yl+"]"+gr+" Analysis "+yl+"Website[ "+wi+url+yl+" ]"+rd+"...")
                        br = mechanize.Browser()
                        br.set_handle_robots(False)
                        br.addheaders = [ ('user-agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36" ) ]
                        br.open("http://www.crimeflare.org:82/cfs.html")
                        br.select_form(nr=0)
                        br["cfS"]=url
                        res = br.submit()
                        data = res.get_data()
                        print(wi+"======================"+"="*len(url)+"=====")
                        if "No working nameservers are registered." in data:
                                print(rd+"  ["+yl+"!"+rd+"]"+yl+" ERRORCode["+rd+"404"+yl+"]: Server Not Found!")
                                print(rd+"  ["+yl+"!"+rd+"]"+wi+" Please Check Your URL !")
                        if "these are not CloudFlare-user nameservers" in data and "No working nameservers are registered." not in data:
                                print(rd+"  ["+yl+"!"+rd+"]"+yl+" CloudFlare "+wi+"STATUS: "+rd+" Disabled"+yl+"!")
                                print(rd+"  ["+yl+"!"+rd+"]"+yl+" This Website Not Using "+rd+"CloudFlare"+yl+" Security"+rd+" !!!"+wi)
                                print(wi+"==================================================")
                                print(gr+"["+wi+"+"+gr+"]"+wi+" IP: "+gr+colIP)
                                self.geoIPinfo(colIP)
                        if "Sorry, but the domain name must contain one or two dots." in data:
                                print(rd+"  ["+yl+"!"+rd+"] "+yl+"Sorry,"+wi+" but the domain name must contain one or two dots."+rd+" !!!"+wi)
                        if "A direct-connect IP address was found:" in data:
                                ips =  re.findall( r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",data)
                                print(wi+"  ["+gr+">"+wi+"]"+yl+" CloudFlare "+wi+" STATUS:"+gr+" Enabled")
                                print(wi+"  ["+gr+">"+wi+"]"+gr+" CloudFlare IP Is: "+wi+colIP)
                                print(yl+"  ======================"+"="*len(colIP))
                                print(gr+"  ["+wi+"+"+gr+"]"+wi+" Real IP Is: "+gr+ips[0])
                                print(yl+"  ================"+"="*len(ips[0]))
                                self.geoIPinfo(ips[0])
                        if "No direct-connect IP address was found for this domain." in data:
                                print(rd+"  ["+yl+"!"+rd+"] "+yl+"Sorry,"+wi+" I Can't Find The Real IP Address Of This Website"+yl+"!"+rd+" :("+wi)            
                except KeyboardInterrupt:
                        print(" ")
                        exit(1)
dumpIP = DumpIP()
if len(sys.argv) !=2:
        print("""

###########################################################################\ 
###  [S] SCRIP : Cloudump                                                   \ 
###  [J]   JOB : Identifying Real IP Of CloudFlare Protected Website.       #> 
###  [A] AUTHOR: Oseid Aldary                                               /     
###########################################################################/ 
""")
        print("[*]====> Let's Bypass CloudFlare <====[*]")
        try:
                url = raw_input("\n[?] Site URL: ")
                while url=="" or url is None:
                        url = raw_input("  [!] Site URL?: ")
                dumpIP.dumpIP(url)
        except KeyboardInterrupt:
                print(cy+"\n~"+gr+"GoodBye"+yl+" :)")
                exit(1)
else:
   url = sys.argv[1]
   if url in ["-h","--help","-hh","?","/?","help","HELP","-H","--HELP","-HH"]:
           print("Usage: python cloudump.py <Website URL>\nEx: python cloudump.py http://www.example.com")
           exit(1)
   else:
            dumpIP.dumpIP(url)

##############################################################
##################### 		     #########################
#####################   END OF TOOL  #########################
#####################                #########################
##############################################################
#This Tool by Oseid Aldary
#Have a nice day :)
#GoodBye
