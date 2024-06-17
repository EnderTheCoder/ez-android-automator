from ez_android_automator.client import create_usb_client

cli = create_usb_client()

print(cli.dump_xml())
cli.refresh_xml()
lst = cli.find_xml_by_attr({'resource-id': 'idm.internet.download.manager.plus:id/progressView'})
single = lst[0].find(attrs={'text': '完成a'})
pass