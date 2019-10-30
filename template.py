# "я повезу жену в гипермаркет"
# "я повезу документы к нотариусу"
# "я поеду в гипермаркет"
# "я планирую поехать в гипермарке"
# "я поеду на работу"
# "я буду на работе"
# "я буду строить дом" "я собираюсь строить дом" 

#http://www.mylanguage.ru/materials/130/3181


def template_1():
    # подлежащее + сказуемое в буд. вр. + дополнение + предлог + обстоятельство
    podlezh = get_podlezh()
    skaz = get_skaz(podlezh, to_be=0)
    dopolnenie = get_noun_add(skaz)
    predlog = ''
    obstoyatelstvo = get_noun_circ(skaz, dopolnenie)
    

    text = f'{podlezh} {skaz} {dopolnenie} {predlog} {obstoyatelstvo}'
    return text
    