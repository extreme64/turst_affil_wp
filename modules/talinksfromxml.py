from xml.dom import minidom
import urllib.request


def readWpData(url: str ="") -> dict:

    response = urllib.request.urlopen(
        'https://forwardcreating.com/wp-content/themes/forwardcreating_v3/ta_added_links.xml'
    )
    results = response.read()

    # print(results)

    xmldoc = minidom.parseString(results) 
    itemlist = xmldoc.getElementsByTagName('root')

    # We read WP links from remote XML file.
    # This data will get compared ,
    # to Google Drive sheet
    wp_links_info = {}

    for root in itemlist:
        links = root.childNodes

        # read all the links and their data
        for link in links:
            dataDict = {}
            # current child tag name
            tagName= link.tagName

            # is a link-[id] tag, that has all the attrs
            if link.hasAttribute('post-id'):
                wpId =  link.attributes['post-id'].value
                dataDict = dict({'post-id': wpId, 'data': {}})

                # add nodes text value
                linkNodes = link.childNodes
                for dataTag in linkNodes:
                    dataDict['data'][dataTag.tagName] = dataTag.firstChild.nodeValue
                    # print("Tag: {name} >> {val} \n".format(name=dataTag.tagName,
                    #                                     val=dataTag.firstChild.nodeValue))

                # append values from attributes
                dataDict['data']['mod']     = link.attributes['mod'].value
                dataDict['data']['mod_gmt'] = link.attributes['mod_gmt'].value

            # use ID as key for each link item dictionary
            wp_links_info[wpId] = dataDict

        # print(wp_links_info)
        return wp_links_info
