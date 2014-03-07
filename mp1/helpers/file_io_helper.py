import os

def save_snapshot_state(pid, snapshot_id, state):
    """state is a tuple of (logical, vector, asset) where logical is an int,
    vector is a list, state is [widget, money]"""

    logical = state[0]
    vector = " ".join(str(i) for i in state[1])
    asset = state[2]
    content = "id {} : snapshot {} : logical {} : vector {} : money {} : widgets {}\n".format(
        pid, snapshot_id, logical, vector, asset[1], asset[0]
    )

    filename = os.path.dirname(os.path.realpath(__file__)) + "/../../snapshots/snapshot." + str(pid)
    with open(filename, "a") as f:
        f.write(content)

def save_snapshot_channel(pid, snapshot_id, channel, channel_id):
    for entry in channel['data']:
        type = entry[0]

        asset_type = ''
        if type == 'send_widget':
            asset_type = 'widget'
        else:
            asset_type = 'money'


        amount = entry[1]
        logical_timestamp = entry[2]
        vector_timestamp = entry[3:]

        vector_timestamp_str = " ".join(str(i) for i in entry[3:])

        content = content + "id {} : snapshot {} : logical {} : vector {} : message {} to {} : {} {}\n".format(
            pid, snapshot_id, logical_timestamp, vector_timestamp_str, channel_id, pid, asset_type, amount
        )

    filename = os.path.dirname(os.path.realpath(__file__)) + "/../../snapshots/snapshot." + str(pid)
    with open(filename, "a") as f:
        f.write(content)