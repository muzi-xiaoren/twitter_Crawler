def json_value_find(json_obj, key):
    # 递归查找JSON对象中的指定键的值，返回一个列表
    results = []
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            if k == key:
                results.append(v)
            results.extend(json_value_find(v, key))
    elif isinstance(json_obj, list):
        for item in json_obj:
            results.extend(json_value_find(item, key))
    return results


def get_max_bitrate_url(variants):
    # 获取比特率最高的视频URL
    max_bitrate = -1
    max_bitrate_url = ""
    for variant in variants:
        # print(variant)
        if "bitrate" in variant and variant["bitrate"] > max_bitrate:
            max_bitrate = variant["bitrate"]
            max_bitrate_url = variant["url"]
    return max_bitrate_url
