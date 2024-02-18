def json_value_find(json_data, target_key):
    def iter_node(node_data):
        if isinstance(node_data, dict):
            key_value_iter = (x for x in node_data.items())
        elif isinstance(node_data, list):
            key_value_iter = (x for x in enumerate(node_data))
        else:
            return

        for key, value in key_value_iter:
            if key == target_key:
                yield value
            if isinstance(value, (dict, list)):
                yield from iter_node(value)

    return list(iter_node(json_data))



#  定义一个函数，用于获取每个 "video_info" 中比特率最大的 URL
def get_max_bitrate_url(variants):
    max_bitrate = -1
    max_bitrate_url = None
    for variant in variants:
        bitrate = variant.get("bitrate", 0)
        if bitrate > max_bitrate:
            max_bitrate = bitrate
            max_bitrate_url = variant["url"]
    return max_bitrate_url
