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

    return jsonStruct