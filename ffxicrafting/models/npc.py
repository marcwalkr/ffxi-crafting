class Npc:
    def __init__(self, npc_id, name, polutils_name, pos_rot, pos_x, pos_y,
                 pos_z, flag, speed, speed_sub, animation, animation_sub,
                 namevis, status, entity_flags, look, name_prefix, content_tag,
                 widescan) -> None:
        self.npc_id = npc_id
        self.name = name
        self.polutils_name = polutils_name
        self.pos_rot = pos_rot
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.flag = flag
        self.speed = speed
        self.speed_sub = speed_sub
        self.animation = animation
        self.animation_sub = animation_sub
        self.namevis = namevis
        self.status = status
        self.entity_flags = entity_flags
        self.look = look
        self.name_prefix = name_prefix
        self.content_tag = content_tag
        self.widescan = widescan
