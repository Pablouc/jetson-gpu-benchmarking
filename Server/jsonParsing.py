def transform_input_json(input_json):
    apps_to_include = [
        'bfs',
        'lava',
        'filter',
        'srad',
        'cfd',
        'lud'
    ]

    jsonStruct = {
        'apps': [],
        'external_app':[],
        'execType': input_json['execType'],
        'execNum': input_json['execNum'],
        'freq': input_json['freq']
    }

    for app_name in apps_to_include:
        app_key = app_name + '_name'
        if app_key in input_json:
            app_entry = {'name': input_json[app_key]}
            workloads_key = app_name + '_workloads'
            app_entry['workloads'] = input_json.get(workloads_key, 'None')
            # Include 'threads' key only for 'cfd' and 'lud' apps
            if app_name in ['cfd', 'lud']:
                threads_key = app_name + '_threads'
                app_entry['threads'] = input_json.get(threads_key, 'None')
            jsonStruct['apps'].append(app_entry)
    
    external_app = {'appName': input_json['appName']}
    external_app['workload_input'] = input_json.get('workload_input', '')
    external_app['makefile_flag'] = input_json.get('makefile_flag', False)
    external_app['makefile_input'] = input_json.get('makefile_input', '')
    jsonStruct['external_app'].append(external_app)
    
    return jsonStruct
