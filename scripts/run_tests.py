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

class Endpoint:
    def __init__(self, name, urls):
        self.urls = urls
        self.name = name

# runname = ""

endpoints = [
    Endpoint("Cloudflare", ["https://www.cloudflare.com/app-fb825b9f46d28bd11d98.js"]), # 1.3MB JS
    Endpoint("Akamai", ["https://www.internetonmars.org/h3prios/server-tests/test.js"]), # same 1.3MB JS as Cloudflare, to keep results as consistent as possible (I have direct control over this Akamai deployment)
    Endpoint("QUICCloud", ["https://www.quic.cloud/wp-content/litespeed/js/4719a4072c1a2469d85886b6a8e768ad.js?ver=b9fc0"]), # 366 KB, largest I could find
    Endpoint("Fastly", ["https://www.fastly.com/app-d3379d2cd2b112b78397.js"]), # 526 KB

    Endpoint("AmazonCloudfront", ["https://a.b.cdn.console.awsstatic.com/a/v1/C2LGMTKF7HUIMXMWTJOQPYZ4QQM6U7NBNAZLZEQRWULUVZAZFLVQ/module.js"]), # 1.1 MB
    Endpoint("GoogleCloudCDN", ["https://cdn.hackersandslackers.com/2017/11/_retina/pandasmerge@2x.jpg"]), # 544 KB
    
    Endpoint("Caddy", ["https://nodefalcon.com/img/art-collection-management.jpg", "https://moebuta.org/posts/using-templates-with-caddy-and-hugo/go_integration_with_go_templates.animated_hu0048abfae485ab9ce34f494d8251d3d0_401071_720x0_resize_box_1.gif"]), # 2.1MB gif

    Endpoint("jsdelivr", ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.css"]),
    Endpoint("gstatic", ["https://www.gstatic.com/devrel-devsite/prod/v89c3b644dadab0c1b29fcdfaa83db3f3db74c1887a83ba5a78318ee59aec3871/cloud/js/devsite_app_custom_elements_module.js"]), # 1.1 MB JS 

    Endpoint("Shopify", ["https://cdn.shopify.com/shopifycloud/brochure-iii/production/_assets/brochureV2-DT5SJUFK.css", "https://cdn.shopify.com/b/shopify-brochure2-assets/288aa2d76b4e7aaff082af1eb4279091.avif"])
]

experiments = [
    # "no-headers-instant",
    # "no-headers-delayed",
    # "u3-incremental-instant",
    # "u3-incremental-delayed",

    # "late-highprio-instant",
    # "late-highprio-delayed",
    "late-highprio-incremental-instant",
    # "late-highprio-incremental-delayed",

    "mixed-bucket-instant",
    # "mixed-bucket-delayed"
]

# handshake failure for some reason... seems to work with chrome though
# Endpoint("nginx", ["https://welcome.huddersfield.click/wp-content/themes/twentytwenty/assets/fonts/inter/Inter-upright-var.woff2"]),

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

def run_experiments():
    # want to build a string as such: 
    # basecommand +  " --experiment no-headers-instant " + " --quic-log /srv/aioquic/qlog/CF4 " + "https://www.cloudflare.com/app-fb825b9f46d28bd11d98.js"
    for experiment in experiments:
        for endpoint in endpoints:
            cmd = basecommand + " --experiment " + experiment + " --quic-log /srv/aioquic/qlog/" + endpoint.name + " " + endpoint.urls[0]
            print( "Running ", cmd )
            run_command( cmd )

run_experiments()

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

# run_command( basecommand +  " --experiment no-headers-instant " + " --quic-log /srv/aioquic/qlog/Caddy " + "https://nodefalcon.com/img/art-collection-management.jpg")


# run_command( basecommand +  " --experiment u3-incremental-instant " + " --quic-log /srv/aioquic/qlog/Cloudflare " + "https://www.cloudflare.com/app-fb825b9f46d28bd11d98.js")
# run_command( basecommand +  " --experiment u3-incremental-instant " + " --quic-log /srv/aioquic/qlog/Akamai " + "https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png")

# run_command( basecommand +  " --experiment u3-incremental-instant " + " --quic-log /srv/aioquic/qlog/QUICCloud " + "https://www.quic.cloud/wp-content/litespeed/js/4719a4072c1a2469d85886b6a8e768ad.js?ver=b9fc0")

# run_command( basecommand +  " --experiment late-highprio-delayed " + " --quic-log /srv/aioquic/qlog/Cloudflare " + "https://www.cloudflare.com/app-fb825b9f46d28bd11d98.js") 
# run_command( basecommand +  " --experiment late-highprio-delayed " + " --quic-log /srv/aioquic/qlog/Akamai " + "https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png")
# run_command( basecommand +  " --experiment late-highprio-delayed " + " --quic-log /srv/aioquic/qlog/QUICCloud " + "https://www.quic.cloud/wp-content/litespeed/js/4719a4072c1a2469d85886b6a8e768ad.js?ver=b9fc0")

# run_command( basecommand +  " --experiment late-highprio-instant " + " --quic-log /srv/aioquic/qlog/Cloudflare " + "https://www.cloudflare.com/app-fb825b9f46d28bd11d98.js") 
# run_command( basecommand +  " --experiment late-highprio-instant " + " --quic-log /srv/aioquic/qlog/Akamai " + "https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png")
# run_command( basecommand +  " --experiment late-highprio-instant " + " --quic-log /srv/aioquic/qlog/QUICCloud " + "https://www.quic.cloud/wp-content/litespeed/js/4719a4072c1a2469d85886b6a8e768ad.js?ver=b9fc0")

# run_command( basecommand +  " --experiment late-highprio-delayed " + " --quic-log /srv/aioquic/qlog/Caddy " + "https://moebuta.org/posts/using-templates-with-caddy-and-hugo/go_integration_with_go_templates.animated_hu0048abfae485ab9ce34f494d8251d3d0_401071_720x0_resize_box_1.gif")

# run_command( basecommand + " --quic-log /srv/aioquic/qlog/test_qlog_output2_akam_test4img.qlog " + "https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png https://www.internetonmars.org/posts/h2-server-push/images/7_bandwidthopportunities.png")


# run_command( basecommand +  " --experiment no-headers-instant " + " --quic-log /srv/aioquic/qlog/fastly " + "https://www.fastly.com/app-d3379d2cd2b112b78397.js")
# run_command( basecommand +  " --experiment late-highprio-delayed " + " --quic-log /srv/aioquic/qlog/fastly " + "https://www.fastly.com/app-d3379d2cd2b112b78397.js")


# run_command( basecommand +  " --experiment no-headers-instant " + " --quic-log /srv/aioquic/qlog/Shopify2 " + "https://cdn.shopify.com/shopifycloud/brochure-iii/production/_assets/brochureV2-DT5SJUFK.css")
# run_command( basecommand +  " --experiment late-highprio-delayed " + " --quic-log /srv/aioquic/qlog/Shopify2 " + "https://cdn.shopify.com/shopifycloud/brochure-iii/production/_assets/brochureV2-DT5SJUFK.css")


# run_command( basecommand +  " --experiment no-headers-instant " + " --quic-log /srv/aioquic/qlog/CF3 " + "https://lucaspardue.com/wp-content/uploads/2018/12/Anti-Matter-676x956.jpg")
# run_command( basecommand +  " --experiment late-highprio-delayed " + " --quic-log /srv/aioquic/qlog/CF3 " + "https://lucaspardue.com/wp-content/uploads/2018/12/Anti-Matter-676x956.jpg")
# run_command( basecommand +  " --experiment late-highprio-instant " + " --quic-log /srv/aioquic/qlog/CF3 " + "https://lucaspardue.com/wp-content/uploads/2018/12/Anti-Matter-676x956.jpg")

# run_command( basecommand +  " --experiment no-headers-instant " + " --quic-log /srv/aioquic/qlog/CF4 " + "https://www.cloudflare.com/app-fb825b9f46d28bd11d98.js")
# run_command( basecommand +  " --experiment late-highprio-delayed " + " --quic-log /srv/aioquic/qlog/CF4 " + "https://www.cloudflare.com/app-fb825b9f46d28bd11d98.js")
# run_command( basecommand +  " --experiment late-highprio-instant " + " --quic-log /srv/aioquic/qlog/CF4 " + "https://www.cloudflare.com/app-fb825b9f46d28bd11d98.js")




# run_command( basecommand + " --quic-log /srv/aioquic/qlog " + "https://www.fastly.com" )