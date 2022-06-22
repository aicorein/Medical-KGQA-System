def trimURI(string: str): 
    return string.strip('http://www.blcu.edu.cn/ontology#')


def processData(query_keys, data, state):
    if state == 1:
        if not data:
            return {
                "type": 'string',
                "state": 1,
                "content": "任何药品不具有您所询问的特性或物质。"
            }
        else:
            name_list = []
            number_list = []
            for result in data['results']['bindings']:
                name = trimURI(result['sub']['value'])
                number = trimURI(result['number']['value'])

                if name.isdigit(): continue
                if name not in name_list: name_list.append(name)
                number_list.append(number)
            return {
                "type": 'object',
                "state": 1,
                "content": {
                    "names": name_list,
                    "numbers": number_list
                }
            }
    elif state == 2:
        if not data:
            return {
                "type": 'string',
                "state": 2,
                "content": "该药品不含有您询问的特性或物质。"
            }
        else:
            number_list = []
            for result in data['results']['bindings']:
                number_list.append(trimURI(result['number']['value']))
            return {
                "type": 'object',
                "state": 2,
                "content": {
                    "numbers": number_list
                }
            }
    elif state == 3:
        if not data:
            return {
                "type": 'string',
                "state": 3,
                "content": "不存在与您问题相关的信息。"
            }
        else:
            all_obj_list = []

            number_obj_list = []
            pre_number = trimURI(data['results']['bindings'][0]['number']['value'])
            number_obj_dict = {
                "number": pre_number,
                "obj": '',
            }
            work_list = []

            for result in data['results']['bindings']:
                number = trimURI(result['number']['value'])
                obj = trimURI(result['obj']['value'])
                if obj not in all_obj_list:
                    all_obj_list.append(obj)
                
                if number == pre_number:
                    if obj not in work_list:
                        work_list.append(obj)
                else:
                    number_obj_dict['obj'] = work_list.copy()
                    work_list.clear()
                    number_obj_list.append(number_obj_dict.copy())
                    number_obj_dict = {
                        "number": number,
                        "obj": '',
                    }
                    pre_number = number
            return {
                "type": 'object',
                "state": 3,
                "medical": query_keys[0],
                "content": {
                    "allObj": all_obj_list,
                    "numberObj": number_obj_list
                }
            }



