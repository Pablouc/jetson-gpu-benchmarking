import json
class App:
    def __init__(self, name, workloads, blocks, threads):
        self.name = name
        self.workloads = workloads
        self.blocks = blocks
        self.threads = threads


def process_input(data):
    # Create App instances while iterating over the input data
    apps_list = [App(app_data['name'], app_data['workloads'], app_data['blocks'], app_data['threads']) for app_data in data['apps']]
    
    # Return the list of App instances and other values
    return apps_list, data['execType'], data['execNum'], data['freq']



jsonStruct = {
    'apps': [
        {
            'name': 'bfs',
            'workloads': '256.dat',
            'blocks': '32',
            'threads': '16'
        },
        {
            'name': 'lud',
            'workloads': 'graph65536.txt',
            'blocks': '32',
            'threads': '16'
        }
    ],
    'execType': 'not-simult',
    'execNum': '10',
    'freq': '242'
}



apps, exec_type, exec_num, freq = process_input(jsonStruct)

# Now, you can work with the list of App instances and the other values as needed
for app in apps:
    print(app.name, app.workloads, app.blocks, app.threads)


