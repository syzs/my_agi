import  json
def show_json(obj):
    print(json.dumps(json.loads(obj.model_dump_json()),
                     indent=4, ensure_ascii=False))
