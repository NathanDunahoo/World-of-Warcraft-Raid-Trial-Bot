valid_classes = ["Paladin", "Monk", "Druid", "Priest", 'Deathknight', 'Demonhunter', 'Rogue', 'Mage', 'Warlock', 'Warrior', 'Shaman', 'Hunter']
valid_specs = {
    'Paladin': ['prot', 'ret', 'holy'],
    'Monk': ['brew', 'mistweaver', 'windwalker'],
    'Druid': ['boomkin', 'bear', 'resto'],
    'Priest': ['shadow', 'disc', 'holy'],
    'Deathknight': ['unholy', 'blood', 'frost'],
    'Demonhunter': ['havoc', 'vengeance'],
    'Rogue': ['sub', 'ass', ''],
    'Mage': ['fire', 'arcane', 'frost'],
    'Warlock': [''],
    'Warrior': ['arms', 'fury', 'prot'],
    'Shaman': ['resto', 'ele', 'enhance'],
    'Hunter': ['marksman', 'beastmastery', 'survival'],
}

class_icons = {
            "Paladin": r'https://static.wikia.nocookie.net/wowpedia/images/f/fa/Charactercreate-class_paladin.png/revision/latest/scale-to-width-down/120?cb=20200517190005',
            "Monk": r'https://static.wikia.nocookie.net/wowpedia/images/4/40/Charactercreate-class_monk.png/revision/latest/scale-to-width-down/120?cb=20200517190000',
            "Druid": r'https://static.wikia.nocookie.net/wowpedia/images/6/66/Charactercreate-class_druid.png/revision/latest/scale-to-width-down/120?cb=20200517185946',
            "Priest": r'https://static.wikia.nocookie.net/wowpedia/images/7/7e/Charactercreate-class_priest.png/revision/latest/scale-to-width-down/120?cb=20200517190009',
            'Deathknight': r'https://static.wikia.nocookie.net/wowpedia/images/d/de/Charactercreate-class_deathknight.png/revision/latest/scale-to-width-down/120?cb=20200517185937',
            'Demonhunter': r'https://static.wikia.nocookie.net/wowpedia/images/9/97/Charactercreate-class_demonhunter.png/revision/latest/scale-to-width-down/120?cb=20200517185942',
            'Rogue': r'https://static.wikia.nocookie.net/wowpedia/images/6/66/Charactercreate-class_rogue.png/revision/latest/scale-to-width-down/120?cb=20200517190014',
            'Mage': r'https://static.wikia.nocookie.net/wowpedia/images/c/cc/Charactercreate-class_mage.png/revision/latest/scale-to-width-down/120?cb=20200517185956',
            'Warlock': r'https://static.wikia.nocookie.net/wowpedia/images/4/4f/Charactercreate-class_warlock.png/revision/latest/scale-to-width-down/120?cb=20200517190024',
            'Warrior': r'https://static.wikia.nocookie.net/wowpedia/images/0/0f/Charactercreate-class_warrior.png/revision/latest/scale-to-width-down/120?cb=20200517190030',
            'Shaman': r'https://static.wikia.nocookie.net/wowpedia/images/1/17/Charactercreate-class_shaman.png/revision/latest/scale-to-width-down/120?cb=20200517190019',
            'Hunter': r'https://static.wikia.nocookie.net/wowpedia/images/e/e8/Charactercreate-class_hunter.png/revision/latest/scale-to-width-down/120?cb=20200517185951'
}

class ClassError(Exception):
    pass

class SpecError(Exception):
    pass

def check_valid_class_spec(_class: str, spec: str):
    if _class not in valid_classes:
        raise ClassError
    else:
        if spec.lower() not in valid_specs[_class]:
            raise SpecError
