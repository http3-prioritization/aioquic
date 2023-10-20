# inspired by https://github.com/rmarx/aioquic/tree/master/scripts

import subprocess

# need to run setup.py first to make sure all our changes are compiled before running
# if you didn't make changes to aioquic, you can comment this step out
# need to run this from inside the root dir
# so in /srv/aioquic, do python3 scripts/run_tests.py

print("Compiling...")
process = subprocess.run("{}".format("python3 /srv/aioquic/setup.py install"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

if process.returncode != 0:
    print ("ERROR in compilation: ", process.returncode, " != 0?")
    print ( process.stderr )

print("Compilation done!")

basecommand = "python3 /srv/aioquic/examples/http3_client.py --insecure -v"

# class Endpoint:
#     def __init__(self, url, name):
#         self.url = url
#         self.name = name

# runname = ""

# proper_endpoints = [
#     # Endpoint("https://neqo:4123/{}", "neqo"),
#     Endpoint("https://h3.stammw.eu:4433/{}", "quinn"),
#     Endpoint("https://test.privateoctopus.com:4433/{}", "picoquicFIFO"), 
#     Endpoint("https://quic.aiortc.org/{}", "aioquic"),
#     Endpoint("https://http3-test.litespeedtech.com:4433/{}", "lsquic"),
#     Endpoint("https://fb.mvfst.net:443/{}", "mvfst"),
#     Endpoint("https://nghttp2.org:4433/{}", "ngtcp2"),
#     Endpoint("https://quic.examp1e.net/{}", "quicly"),
#     Endpoint("https://quic.rocks:4433/{}", "google"),
# ]

# f5          = "https://f5quic.com:4433"                 # only has 50000, 5000000, 10000000 (50KB, 5MB , 10MB)
# msquic      = "https://quic.westus.cloudapp.azure.com"  # only has 5000000.txt, 10000000.txt, 1MBfile.txt (1MB, 5MB, 10MB)
# quiche      = "https://quic.tech:8443"                  # only has 1MB.png, 5MB.png
# quiche_nginx = "https://cloudflare-quic.com"            # only has 1MB.png, 5MB.png
# facebook    = "https://www.facebook.com"                # "rsrc.php/v3iXG34/y_/l/en_GB/ppT9gy-P_lf.js?_nc_x=Ij3Wp8lg5Kz"
# fbcdn       = "https://scontent.xx.fbcdn.net"           # only has /speedtest-1MB, /speedtest-5MB, /speedtest-10MB
# fbcdn_india = "https://xx-fbcdn-shv-01-bom1.fbcdn.net"  # only has /speedtest-1MB, /speedtest-5MB, /speedtest-10MB
# ats         = "https://quic.ogre.com:4433"              # en/latest/admin-guide/files/records.config.en.html
# akamai      = "https://ietf.akaquic.com"                # /10k, /100k, /1M

# def run_single(size, testname):

#     for endpoint in proper_endpoints:
#         url = endpoint.url.format(str(size))
#         cmd = basecommand + " " + "--quic-log /srv/aioquic/qlog/run"+ runname +"_single_" + testname + "_" + endpoint.name + ".qlog " + url
#         print ("Executing ", cmd)
#         run_command ( cmd )

# def run_single_endpoint(url, testname, endpointName):

#     cmd = basecommand + " " + "--quic-log /srv/aioquic/qlog/run"+ runname +"_single_" + testname + "_" + endpointName + ".qlog \"" + url + "\""
#     print ("Executing ", cmd)
#     run_command ( cmd )

# def run_parallel(size, amount, delay, testname):
#     for endpoint in proper_endpoints:
#         url = endpoint.url.format(str(size))
#         delaystr = ""
#         if delay > 0:
#             delaystr = " --delay-parallel " + str(delay) + " " # delay is in SECONDS

#         cmd = basecommand + " " + "--parallel " + str(amount) + delaystr + " --quic-log /srv/aioquic/qlog/run"+ runname +"_parallel_" + testname + "_" + endpoint.name + ".qlog " + url
#         print ("Executing ", cmd)
#         run_command ( cmd )

# def run_parallel_endpoint(url, amount, delay, testname, endpointName):
#     delaystr = ""
#     if delay > 0:
#         delaystr = " --delay-parallel " + str(delay) + " " # delay is in SECONDS

#     cmd = basecommand + " " + "--parallel " + str(amount) + delaystr + " --quic-log /srv/aioquic/qlog/run"+ runname +"_parallel_" + testname + "_" + endpointName + ".qlog \"" + url + "\""
#     print ("Executing ", cmd)
#     run_command ( cmd )


def run_command(cmd):
    process = subprocess.run("{}".format(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    if ( len(process.stdout) > 0 ):
        print ( process.stdout )

    if len(process.stderr) != 0 or process.returncode != 0:
        # print ("Potential ERROR in process: ", process.returncode, " != 0?")
        print ( process.stderr )

# run_command( basecommand + " --quic-log /srv/aioquic/qlog/test_qlog_output2_fastly.qlog " + "https://www.fastly.com" )
#run_command( basecommand + " --quic-log /srv/aioquic/qlog/test_qlog_output2_bing.qlog " + "https://www.bing.com" )
# run_command( basecommand + " --quic-log /srv/aioquic/qlog/test_qlog_output2_eurodrive.qlog " + "https://www.sew-eurodrive.de/home.html" )
# run_command( basecommand + " --quic-log /srv/aioquic/qlog/test_qlog_output2_internetonmars.qlog " + "https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png" )

# run_command( basecommand + " --quic-log /srv/aioquic/qlog/test_qlog_output2_internetonmars_multi2.qlog " + "https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png" )

# run_command( basecommand + " --quic-log /srv/aioquic/qlog/test_qlog_output2_quiccloud_test4.qlog " + "https://www.quic.cloud/wp-content/uploads/2021/12/world-map.png https://www.quic.cloud/wp-content/uploads/2021/12/world-map.png https://www.quic.cloud/wp-content/uploads/2021/12/world-map.png https://www.quic.cloud/wp-content/uploads/2021/12/world-map.png" )

# larger than image because we don't support gzip :) 
# run_command( basecommand + " --quic-log /srv/aioquic/qlog/test_qlog_output2_quiccloud_test2JS.qlog " + "https://www.quic.cloud/wp-content/litespeed/js/4719a4072c1a2469d85886b6a8e768ad.js?ver=b9fc0 https://www.quic.cloud/wp-content/litespeed/js/4719a4072c1a2469d85886b6a8e768ad.js?ver=b9fc0")


# 1.3MB JS without gzip

# run_command( basecommand +  " --experiment no-headers-instant " + " --quic-log /srv/aioquic/qlog/Cloudflare " + "https://www.cloudflare.com/app-fb825b9f46d28bd11d98.js")
# run_command( basecommand +  " --experiment no-headers-instant " + " --quic-log /srv/aioquic/qlog/Akamai " + "https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png")
# run_command( basecommand +  " --experiment no-headers-instant " + " --quic-log /srv/aioquic/qlog/QUICCloud " + "https://www.quic.cloud/wp-content/litespeed/js/4719a4072c1a2469d85886b6a8e768ad.js?ver=b9fc0")

# run_command( basecommand +  " --experiment u3-incremental-instant " + " --quic-log /srv/aioquic/qlog/Cloudflare " + "https://www.cloudflare.com/app-fb825b9f46d28bd11d98.js")
# run_command( basecommand +  " --experiment u3-incremental-instant " + " --quic-log /srv/aioquic/qlog/Akamai " + "https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png")

# run_command( basecommand +  " --experiment u3-incremental-instant " + " --quic-log /srv/aioquic/qlog/QUICCloud " + "https://www.quic.cloud/wp-content/litespeed/js/4719a4072c1a2469d85886b6a8e768ad.js?ver=b9fc0")

# run_command( basecommand +  " --experiment late-highprio-delayed " + " --quic-log /srv/aioquic/qlog/Cloudflare " + "https://www.cloudflare.com/app-fb825b9f46d28bd11d98.js") 
# run_command( basecommand +  " --experiment late-highprio-delayed " + " --quic-log /srv/aioquic/qlog/Akamai " + "https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png")
# run_command( basecommand +  " --experiment late-highprio-delayed " + " --quic-log /srv/aioquic/qlog/QUICCloud " + "https://www.quic.cloud/wp-content/litespeed/js/4719a4072c1a2469d85886b6a8e768ad.js?ver=b9fc0")

run_command( basecommand +  " --experiment late-highprio-instant " + " --quic-log /srv/aioquic/qlog/Cloudflare " + "https://www.cloudflare.com/app-fb825b9f46d28bd11d98.js") 
run_command( basecommand +  " --experiment late-highprio-instant " + " --quic-log /srv/aioquic/qlog/Akamai " + "https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png")
run_command( basecommand +  " --experiment late-highprio-instant " + " --quic-log /srv/aioquic/qlog/QUICCloud " + "https://www.quic.cloud/wp-content/litespeed/js/4719a4072c1a2469d85886b6a8e768ad.js?ver=b9fc0")


# run_command( basecommand + " --quic-log /srv/aioquic/qlog/test_qlog_output2_akam_test4img.qlog " + "https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png")



# run_command( basecommand + " --quic-log /srv/aioquic/qlog " + "https://www.fastly.com" )