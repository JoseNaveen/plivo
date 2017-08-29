from string import Template

class Template(Template):
    delimiter = "%"

def formatter(time_delta, format):
    d = {"D": time_delta.days}
    d["H"], rem = divmod(time_delta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    t = Template(format)
    return t.substitute(**d)