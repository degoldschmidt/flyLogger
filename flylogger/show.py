def sheets(client):
    for each in client.list_ssheets():
        print(each['name'])
