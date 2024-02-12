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

basecommand = "python3 ./examples/http3_client.py --insecure -v "

class Endpoint:
    def __init__(self, name, urls):
        self.urls = urls
        self.name = name

# runname = ""

endpoints = [
    # Endpoint("Cloudflare", ["https://www.cloudflare.com/app-fb825b9f46d28bd11d98.js"]), # 1.3MB JS
    Endpoint("Akamai", ["https://www.internetonmars.org/h3prios/server-tests/test.js"]), # same 1.3MB JS as Cloudflare, to keep results as consistent as possible (I have direct control over this Akamai deployment)
    Endpoint("QUICCloud", ["https://www.quic.cloud/wp-content/litespeed/js/4719a4072c1a2469d85886b6a8e768ad.js?ver=b9fc0"]), # 366 KB, largest I could find
    # Endpoint("Fastly", ["https://www.fastly.com/app-d3379d2cd2b112b78397.js"]), # 526 KB

    Endpoint("AmazonCloudfront", ["https://a.b.cdn.console.awsstatic.com/a/v1/C2LGMTKF7HUIMXMWTJOQPYZ4QQM6U7NBNAZLZEQRWULUVZAZFLVQ/module.js"]), # 1.1 MB
    Endpoint("GoogleCloudCDN", ["https://cdn.hackersandslackers.com/2017/11/_retina/pandasmerge@2x.jpg"]), # 544 KB
    
    Endpoint("Caddy", ["https://nodefalcon.com/img/art-collection-management.jpg", "https://moebuta.org/posts/using-templates-with-caddy-and-hugo/go_integration_with_go_templates.animated_hu0048abfae485ab9ce34f494d8251d3d0_401071_720x0_resize_box_1.gif"]), # 2.1MB gif

    Endpoint("jsdelivr", ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.css"]),
    Endpoint("gstatic", ["https://www.gstatic.com/devrel-devsite/prod/v89c3b644dadab0c1b29fcdfaa83db3f3db74c1887a83ba5a78318ee59aec3871/cloud/js/devsite_app_custom_elements_module.js"]), # 1.1 MB JS 

    Endpoint("Shopify", ["https://cdn.shopify.com/shopifycloud/brochure-iii/production/_assets/brochureV2-DT5SJUFK.css", "https://cdn.shopify.com/b/shopify-brochure2-assets/288aa2d76b4e7aaff082af1eb4279091.avif"])
]

experiments = [
    "no-priority-instant",
    "no-priority-staggered",

    "u3-incremental-headers-instant",
    "u3-incremental-preframes-instant",
    "u3-incremental-preframes-100ms-instant",
    "u3-incremental-preframes-200ms-instant",
    "u3-incremental-postframes-instant",
    "u3-incremental-postframes-100ms-instant",
    "u3-incremental-postframes-200ms-instant",
    "u3-incremental-headers-staggered",
    "u3-incremental-preframes-staggered",
    "u3-incremental-preframes-100ms-staggered",
    "u3-incremental-preframes-200ms-staggered",
    "u3-incremental-postframes-staggered",
    "u3-incremental-postframes-100ms-staggered",
    "u3-incremental-postframes-200ms-staggered",

    "late-highprio-headers-instant",
    "late-highprio-preframes-instant",
    "late-highprio-preframes-100ms-instant",
    "late-highprio-preframes-200ms-instant",
    "late-highprio-postframes-instant",
    "late-highprio-postframes-100ms-instant",
    "late-highprio-postframes-200ms-instant",
    "late-highprio-headers-staggered",
    "late-highprio-preframes-staggered",
    "late-highprio-preframes-100ms-staggered",
    "late-highprio-preframes-200ms-staggered",
    "late-highprio-postframes-staggered",
    "late-highprio-postframes-100ms-staggered",
    "late-highprio-postframes-200ms-staggered",

    "late-highprio-incremental-headers-instant",
    "late-highprio-incremental-preframes-instant",
    "late-highprio-incremental-preframes-100ms-instant",
    "late-highprio-incremental-preframes-200ms-instant",
    "late-highprio-incremental-postframes-instant",
    "late-highprio-incremental-postframes-100ms-instant",
    "late-highprio-incremental-postframes-200ms-instant",
    "late-highprio-incremental-headers-staggered",
    "late-highprio-incremental-preframes-staggered",
    "late-highprio-incremental-preframes-100ms-staggered",
    "late-highprio-incremental-preframes-200ms-staggered",
    "late-highprio-incremental-postframes-staggered",
    "late-highprio-incremental-postframes-100ms-staggered",
    "late-highprio-incremental-postframes-200ms-staggered",

    "mixed-bucket-headers-instant",
    "mixed-bucket-preframes-instant",
    "mixed-bucket-preframes-100ms-instant",
    "mixed-bucket-preframes-200ms-instant",
    "mixed-bucket-postframes-instant",
    "mixed-bucket-postframes-100ms-instant",
    "mixed-bucket-postframes-200ms-instant",
    "mixed-bucket-headers-staggered",
    "mixed-bucket-preframes-staggered",
    "mixed-bucket-preframes-100ms-staggered",
    "mixed-bucket-preframes-200ms-staggered",
    "mixed-bucket-postframes-staggered",
    "mixed-bucket-postframes-100ms-staggered",
    "mixed-bucket-postframes-200ms-staggered",
]

# handshake failure for some reason... seems to work with chrome though
# Endpoint("nginx", ["https://welcome.huddersfield.click/wp-content/themes/twentytwenty/assets/fonts/inter/Inter-upright-var.woff2"]),

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
            cmd = basecommand + " --experiment " + experiment + " --quic-log ./qlog/" + endpoint.name + " " + endpoint.urls[0]
            print( "Running ", cmd )
            run_command( cmd )

run_experiments()

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